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
        vaild_lens = vaild_lens.repeat_interleave(shape[1])
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
        queries, keys, values = self.dense_query(queries).reshape(-1, queries.shape[1],
                                                                  self.num_hiddens // self.num_heads), \
                                self.dense_key(keys).reshape(-1, keys.shape[1], self.num_hiddens // self.num_heads), \
                                self.dense_value(values).reshape(-1, values.shape[1],
                                                                 self.num_hiddens // self.num_heads)
        if valid_lens is not None:
            valid_lens = valid_lens.repeat_interleave(self.num_heads)
        # output_concat，形状：(num_heads * batch_size, num_queries, num_hiddens // num_heads)
        output_concat = self.attention(queries, keys, values, valid_lens)
        # 恢复形状: (batch_size, num_queries, num_hiddens)
        output = self.dense_out(output_concat.reshape(queries.shape[0], queries.shape[1], -1))
        return output


class AddNorm(nn.Module):
    """残差连接后层规范化"""

    def __init__(self, normalized_shape, dropout: float):
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        self.lay_norm = nn.LayerNorm(normalized_shape)

    def forward(self, X: Tensor, Y: Tensor) -> Tensor:
        return self.lay_norm(self.dropout(Y) + X)


class PositionWiseFFN(nn.Module):
    """基于位置的前馈神经网络"""

    def __init__(self, ffn_in_features, ffn_num_hiddens, ffn_out_features):
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


if __name__ == '__main__':
    q = torch.randn(2, 3, 5)
    k = torch.randn(2, 4, 3)
    # k = torch.randn(2, 4, 5)
    v = torch.randn(2, 4, 6)
    vaild_lens = torch.tensor([2, 4])
    # at = AddtiveAttention(5, 3, 6, 10)
    # at = DotProductAttention()
    at = MultiHeadAttention(5, 3, 6, 12, 4)
    print(at(q, k, v, vaild_lens).shape)
    # print(at.attention.attentiion_weights)
    print(at.attention.attentiion_weights.shape)

    # import d2l.torch as d2l
    #
    # at1 = d2l.MultiHeadAttention(3, 5, 6, 12, 4, 0.1, bias=True)
    # print(at1(q, k, v, vaild_lens).shape)
    # # print(at1.attention.attention_weights)
    # print(at1.attention.attention_weights.shape)
