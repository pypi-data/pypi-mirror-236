
from tpf.att import Attn 
from tpf.att import MultiHead 
import torch 



"""
求B相对A的注意力 
"""
A = torch.linspace(0,31,32).reshape(2,16)
# print(A)
"""
tensor([[ 0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10., 11., 12., 13.,
         14., 15.],
        [16., 17., 18., 19., 20., 21., 22., 23., 24., 25., 26., 27., 28., 29.,
         30., 31.]])
"""

B = torch.ones(2,16)
mask = B # 全计算 

# 添加批次维度
A = A.unsqueeze(dim=0)
# print(A.shape)  # torch.Size([1, 2, 16])

B = B.unsqueeze(dim=0)
mask = mask.unsqueeze(dim=0)

# att = attention(B,A,A, mask)
# print(att)

attn = Attn('dot',16)

context = attn(B,A)
print(context)

#模拟单词计算，转换批次维度 

mh = MultiHead(in_features=16,out_features=16)
c = mh(B,A,A,mask)
print(c)