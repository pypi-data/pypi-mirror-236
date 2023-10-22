import math

import torch
import torch.nn as nn
from torch import Tensor
from torch.nn import functional as F


def mask_seq(seqs: Tensor, vaild_lens: Tensor, mask_value=0.0) -> Tensor:
    """
    对序列的无效的元素用mask_value替换
    :param seqs: (n, m)
    :param vaild_lens: (n*m, )
    :param mask_value: 数值
    :return: (n, m)
    """
    # seqs: (batch_size, num_steps)
    # valid_lens: (batch_size, )
    # mask: seqs.shape, 每一行对应的是不要屏蔽的元素就是1, 要屏蔽的就是0
    mask = torch.tensor([[1] * vaild_len + [0] * (seqs.shape[-1] - vaild_len)
                         for vaild_len in vaild_lens])
    # 把零元素都换成屏蔽元素的值
    seqs[mask == 0] = mask_value
    return seqs


class MaskSoftmask(nn.Module):
    """
    掩蔽softmax
    """

    def __init__(self, dim: int):
        """
        :param dim: 进行softmax的维度
        """
        super(MaskSoftmask, self).__init__()
        self.dim = dim

    def forward(self, X: Tensor, vaild_lens=None) -> Tensor:
        """
        :param X: (batch_size, num_queries, num_keys/num_values)
        :param vaild_lens: (batch_size, ), 每个value的有效长度
        :return: (batch_size, num_queries, num_keys/num_values)
        """
        # X: (batch_size, num_query, num_keys)
        # valid_lens: (batch_size, )
        if vaild_lens is None:
            return F.softmax(X, dim=self.dim)
        shape = X.shape
        if vaild_lens.dim() == 1:
            vaild_lens = vaild_lens.repeat_interleave(shape[1])
        else:
            vaild_lens = vaild_lens.reshape(-1)  # 变成一维
        mask_X = mask_seq(X.reshape(-1, shape[-1]), vaild_lens, -1e6).reshape(shape)
        return F.softmax(mask_X, dim=self.dim)


class AddtiveAttention(nn.Module):
    """加性注意力"""

    def __init__(self, query_features: int, key_features: int, num_hiddens: int, dropout=0.1):
        """
        :param query_features: query的特征维度
        :param key_features: key的特征维度
        :param num_hiddens: 隐层特征维度
        :param dropout: 丢弃百分之dropout的数据，防止过拟合
        """
        super().__init__()
        self.attention_weights = None
        # 将queries和keys的特征维度统一
        self.dense_query = nn.Linear(query_features, num_hiddens)
        self.dense_key = nn.Linear(key_features, num_hiddens)
        # 相加后将num_hiddens映射到1个特征，因为每个query对每个value只有一个权重
        self.dense_query_add_key = nn.Linear(num_hiddens, 1)
        self.mask_softmax = MaskSoftmask(dim=-1)
        self.dropout = nn.Dropout(dropout)

    def forward(self, queries: Tensor, keys: Tensor, values: Tensor, valid_lens: Tensor) -> Tensor:
        """
        前向传播
        :param queries: (batch_size, num_queries, query_features)
        :param keys: (batch_size, num_keys, key_features)
        :param values: (batch_size, num_values, value_features)
        :param valid_lens: (batch_size, )
        :return: 所有value的加权和: (batch_size, num_queries, value_features)
        """
        queries, keys = self.dense_query(queries), self.dense_key(keys)
        q_k = queries.unsqueeze(2) + keys.unsqueeze(1)  # 广播机制，使得可以相加
        scores = torch.tanh(self.dense_query_add_key(q_k).squeeze(-1))
        self.attention_weights = self.mask_softmax(scores, valid_lens)
        return torch.bmm(self.dropout(self.attention_weights), values)


class DotProductAttention(nn.Module):
    """缩放点积注意力，要求query和key有同样的特征维度"""

    def __init__(self, dropout=0.1):
        """
        :param dropout: 丢弃百分之dropout的数据，防止过拟合
        """
        super(DotProductAttention, self).__init__()
        self.attention_weights = None
        self.mask_softmax = MaskSoftmask(dim=-1)
        self.dropout = nn.Dropout(dropout)

    def forward(self, queries: Tensor, keys: Tensor, values: Tensor, valid_lens: Tensor) -> Tensor:
        """
        要求query和key有同样的特征维度, 即query_features=key_features
        :param queries: (batch_size, num_queries, query_features)
        :param keys: (batch_size, num_keys, key_features)
        :param values: (batch_size, num_values, value_features)
        :param valid_lens: (batch_size, )
        :return: 所有value的加权和: (batch_size, num_queries, value_features)
        """
        d = queries.shape[-1]
        scores = torch.bmm(queries, keys.transpose(1, 2)) / math.sqrt(d)  # keys.permute(0, 2, 1)
        self.attention_weights = self.mask_softmax(scores, valid_lens)
        return torch.bmm(self.dropout(self.attention_weights), values)


class MultiHeadAttention(nn.Module):
    """多头注意力"""

    def __init__(self, query_features: int, key_features: int, value_features: int, num_hiddens: int, num_heads: int,
                 dropout=0.1):
        """
        :param query_features: query的特征维度
        :param key_features: key的特征维度
        :param num_hiddens: 隐层特征维度
        :param dropout: 丢弃百分之dropout的数据，防止过拟合
        """
        super().__init__()
        self.attentiion_weights = None
        self.num_heads = num_heads
        self.num_hiddens = num_hiddens
        # 将queries、keys和values的特征维度统一
        self.dense_query = nn.Linear(query_features, num_hiddens)
        self.dense_key = nn.Linear(key_features, num_hiddens)
        self.dense_value = nn.Linear(value_features, num_hiddens)
        # 注意力
        self.attention = DotProductAttention(dropout)
        self.mask_softmax = MaskSoftmask(dim=-1)
        self.dense_out = nn.Linear(num_hiddens, num_hiddens)

    def forward(self, queries: Tensor, keys: Tensor, values: Tensor, valid_lens=None) -> Tensor:
        """
        前向传播
        :param queries: (batch_size, num_queries, query_features)
        :param keys: (batch_size, num_keys, key_features)
        :param values: (batch_size, num_values, value_features)
        :param valid_lens: (batch_size, )
        :return: 所有value的加权和: (batch_size, num_queries, value_features)
        """
        # 下面的操作就是把多头做并行计算，并且改变形状，方便后续恢复
        # quries: (batch_size * num_heads, num_queries, num_hiddens // num_heads)
        # keys: (batch_size * num_heads, num_keys, num_hiddens // num_heads)
        # values: (batch_size * num_heads, num_values, num_hiddens // num_heads)
        # 相当于有batch_size * num_heads个样本，且每batch_size个样本都属于同一个头
        shape = queries.shape[:2] + (self.num_hiddens,)
        queries, keys, values = self.dense_query(queries).reshape(-1, queries.shape[1],
                                                                  self.num_hiddens // self.num_heads), \
                                self.dense_key(keys).reshape(-1, keys.shape[1], self.num_hiddens // self.num_heads), \
                                self.dense_value(values).reshape(-1, values.shape[1],
                                                                 self.num_hiddens // self.num_heads)
        if valid_lens is not None:
            valid_lens = valid_lens.repeat_interleave(self.num_heads, dim=0)
        # output_concat，形状：(num_heads * batch_size, num_queries, num_hiddens // num_heads)
        output_concat = self.attention(queries, keys, values, valid_lens)
        # 恢复形状: (batch_size, num_queries, num_hiddens)
        output = self.dense_out(output_concat.reshape(shape))
        return output


class PositionEncoder(nn.Module):
    """位置编码"""

    def __init__(self, num_hiddens: int, dropout: float, max_len=1000):
        """
        位置编码
        :param num_hiddens: X的特征维度
        :param dropout: 丢弃百分之dropout，防止过拟合
        :param max_len: 序列最大长度
        """
        super(PositionEncoder, self).__init__()
        self.dropout = nn.Dropout(dropout)
        self.P = torch.zeros((max_len, num_hiddens))
        # pv: (max_len, num_hiddens / 2 向上取整)
        pv = torch.arange(max_len).reshape(-1, 1) / torch.pow(10000,
                                                              torch.arange(0, num_hiddens, 2) / num_hiddens)  # 广播机制
        self.P[:, 0::2] = torch.sin(pv)  # 偶数列使用sin
        # num_hiddens为奇数时，pv多了最后一列
        i = 0 if pv.shape[1] % 2 == 0 else 1
        self.P[:, 1::2] = torch.cos(pv[:, :pv.shape[1] - i])  # 奇数列使用cos

    def forward(self, X: Tensor) -> Tensor:
        """
        :param X: (batch_size, num_steps, num_hiddens)
        :return: (batch_size, num_steps, num_hiddens)
        """
        X = X + self.P[:X.shape[1], :].to(X.device)  # 广播机制
        return self.dropout(X)


class AddNorm(nn.Module):
    """残差连接后层规范化"""

    def __init__(self, normalized_shape, dropout: float):
        """
        :param normalized_shape: 层规范化后的形状
        :param dropout: 丢弃百分之dropout的数据，防止过拟合
        """
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        self.lay_norm = nn.LayerNorm(normalized_shape)

    def forward(self, X: Tensor, Y: Tensor) -> Tensor:
        """
        残差连接后层规范化
        :param X:
        :param Y:
        :return: 残差连接和层规范化后的结果
        """
        return self.lay_norm(self.dropout(Y) + X)


class PositionWiseFFN(nn.Module):
    """基于位置的前馈神经网络"""

    def __init__(self, ffn_in_features, ffn_num_hiddens, ffn_out_features):
        """
        基于位置的前馈神经网络
        :param ffn_in_features: 输入的特征数
        :param ffn_num_hiddens: 隐层特征数
        :param ffn_out_features: 输出特征数
        """
        super().__init__()
        self.dense1 = nn.Linear(ffn_in_features, ffn_num_hiddens)
        self.relu = nn.ReLU()
        self.dense2 = nn.Linear(ffn_num_hiddens, ffn_out_features)

    def forward(self, X: Tensor) -> Tensor:
        return self.dense2(self.relu(self.dense1(X)))


class TransformerEncoderBlock(nn.Module):
    """Transformer编码块"""

    def __init__(self, query_features: int, key_features: int, value_features: int, num_hiddens: int, num_heads: int,
                 normalized_shape, ffn_num_hiddens, dropout=0.1):
        """
        Transformer编码块
        :param query_features: query的特征维度
        :param key_features: key的特征维度
        :param value_features: value的特征维度
        :param num_hiddens: 隐层特征维度
        :param num_heads: 头的数量
        :param normalized_shape: 层规范化后的形状
        :param ffn_num_hiddens: 基于位置的前馈神经网络的隐层特征维度
        :param dropout: 丢弃百分之dropout的数据，防止过拟合
        """
        super().__init__()
        self.attention = MultiHeadAttention(query_features, key_features, value_features, num_hiddens, num_heads,
                                            dropout)
        self.add_norm1 = AddNorm(normalized_shape, dropout)
        self.ffn = PositionWiseFFN(num_hiddens, ffn_num_hiddens, num_hiddens)  # 保持形状不变
        self.add_norm2 = AddNorm(normalized_shape, dropout)

    def forward(self, X: Tensor, valid_lens: Tensor) -> Tensor:
        Y = self.attention(X, X, X, valid_lens)  # 多头自注意力
        Y2 = self.ffn(self.add_norm1(X, Y))
        Y3 = self.add_norm2(Y, Y2)
        return Y3


class TransformerDecoderBlock(nn.Module):
    """Transformer解码块"""

    def __init__(self, query_features: int, key_features: int, value_features: int, num_hiddens: int, num_heads: int,
                 normalized_shape, ffn_num_hiddens: int, i: int, dropout=0.1):
        """
        Transformer解码块
        :param query_features: query的特征维度
        :param key_features: key的特征维度
        :param value_features: value的特征维度
        :param num_hiddens: 隐层特征维度
        :param num_heads: 头的数量
        :param normalized_shape: 层规范化后的形状
        :param ffn_num_hiddens: 基于位置的前馈神经网络的隐层特征维度
        :param i: Transformer解码器中的第i个块
        :param dropout: 丢弃百分之dropout的数据，防止过拟合
        """
        super().__init__()
        self.i = i
        self.attention1 = MultiHeadAttention(query_features, key_features, value_features, num_hiddens, num_heads,
                                             dropout)
        self.add_norm1 = AddNorm(normalized_shape, dropout)
        self.attention2 = MultiHeadAttention(query_features, key_features, value_features, num_hiddens, num_heads,
                                             dropout)
        self.add_norm2 = AddNorm(normalized_shape, dropout)
        self.ffn = PositionWiseFFN(num_hiddens, ffn_num_hiddens, num_hiddens)  # 保持形状不变
        self.add_norm3 = AddNorm(normalized_shape, dropout)

    def forward(self, X: Tensor, state: Tensor) -> tuple:
        """
        训练时是并行计算的，预测时是根据前一个预测结果预测下一个结果（第一次是编码器的输入和初始state作为输入，后续都是前面的预测结果和state作为输入）
        :param X: (batch_size, num_steps, num_hiddens)
        :param state: 元组，其中三个元素分别是编码器的输出、编码的有效长度和Transformer解码器中每个解码块的state
        :return: 解码结果和state
        """
        # 训练时，encoder_output，encoder_valid_lens是编码器的输出
        # 预测时，encoder_output，encoder_valid_lens第一次是编码器的输入和初始state作为输入，后续都是前面的预测结果和输出state作为输入
        # 注意，预测时，state[0]和state[1]是不变的，变化的只有state[2]
        encoder_output, encoder_valid_lens = state[0], state[1]
        # 训练时：state[2][self.i]都是None，因为是并行计算
        # 测试时，state[2][self.i]除一开始都是None，后面存的都是Transformer解码器的第i解码块直到当前时间步前的所有预测结果的拼接
        if state[2][self.i] is None:
            keys = X
            values = X
        else:
            keys = torch.cat([state[2][self.i], X], dim=1)
            values = torch.cat([state[2][self.i], X], dim=1)

        if self.training:
            batch_size, num_steps = X.shape[0], X.shape[1]
            # 因为是并行的，所有让其只能看到从开始到自己位置的序列
            # decoder_valid_lens: (batch_size, num_steps)，每行都是1, 2, 3, ..., num_steps
            decoder_valid_lens = torch.arange(1, num_steps + 1).repeat(batch_size, 1)
        else:
            decoder_valid_lens = None
        Y = self.attention1(X, keys, values, decoder_valid_lens)  # 掩蔽多头自注意力，关注解码器的输入
        Y2 = self.add_norm1(X, Y)

        Y3 = self.attention2(Y2, encoder_output, encoder_output, encoder_valid_lens)  # 关注编码器的输出
        Y4 = self.add_norm2(Y2, Y3)

        Y5 = self.ffn(Y4)
        Y6 = self.add_norm3(Y4, Y5)
        return Y6, state


class TransformerEncoder(nn.Module):
    """Transformer编码器"""

    def __init__(self, vocab_size, num_hiddens, num_lays, num_heads, normalized_shape, ffn_num_hiddens, dropout):
        super(TransformerEncoder, self).__init__()
        self.num_hiddens = num_hiddens
        self.embedding = nn.Embedding(vocab_size, num_hiddens)
        self.position_encoder = PositionEncoder(num_hiddens, dropout)
        # 编码块
        self.blocks = nn.Sequential()
        for i in range(num_lays):
            self.blocks.add_module(f'block{i}', TransformerEncoderBlock(num_hiddens, num_hiddens, num_hiddens,
                                                                        num_hiddens, num_heads, normalized_shape,
                                                                        ffn_num_hiddens, dropout))

    def forward(self, X, valid_lens):
        # self.embedding(X)的输出结果相较于位置编码（值是-1~1）较小，所有先将其进行缩放再与位置编码相加
        X2 = self.position_encoder(self.embedding(X) * math.sqrt(self.num_hiddens))
        for block in self.blocks:
            X2 = block(X2, valid_lens)
        return X2


class TransformerDecoder(nn.Module):
    def __init__(self, vocab_size, num_hiddens, num_lays, num_heads, normalized_shape, ffn_num_hiddens, dropout):
        super(TransformerDecoder, self).__init__()
        self.num_hiddens = num_hiddens
        self.embedding = nn.Embedding(vocab_size, num_hiddens)
        self.position_encoder = PositionEncoder(num_hiddens, dropout)
        # 解码器块
        self.blocks = nn.Sequential()
        for i in range(num_lays):
            self.blocks.add_module(f"block{i}",
                                   TransformerDecoderBlock(num_hiddens, num_hiddens, num_hiddens, num_hiddens,
                                                           num_heads, normalized_shape, ffn_num_hiddens, i, dropout))
        self.out = nn.Linear(num_hiddens, vocab_size)

    def forward(self, X, state):
        X2 = self.position_encoder(self.embedding(X) * math.sqrt(self.num_hiddens))
        for block in self.blocks:
            X2, state = block(X2, state)
        return self.out(X2), state


if __name__ == '__main__':
    x = torch.ones(2, 4, dtype=torch.long)
    vl = torch.tensor([3, 4])
    te = TransformerEncoder(2, 120, 4, 2, [120], 200, 0.1)
    y = te(x, vl)
    print(y.shape)
    # x2 = torch.ones(2, 4, dtype=torch.long)
    # td = TransformerDecoder(10, 120, 4, 2, [120], 200, 0.1)
    # state = [y, vl, [None]*4]
    # print(td(x2, state)[0].shape)
