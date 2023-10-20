
import numpy as np 
import random
import pandas as pd 
import wave, os

from tpf.box.fil import parentdir
from tpf.box.fil import iswin

if iswin():
    img_path1 = "K:\\tpf\\aiwks\\datasets\\images\\001"
    csv_path1 = ""
else:
    img_path1 = "/opt/tpf/aiwks/datasets/images/001"
    csv_path1 = "/opt/tpf/aiwks/datasets/text/a.cvs"



def get_data_path(fil):
    data_dir = "/data"
    fil_path = os.path.join(data_dir,fil)
    return  fil_path
    

class TestEnvPath(object):
    ABS_DIR = "K:\\tpf\\aiwks\\datasets\\images\\001"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data_tmp")

    DATA_PATH = os.path.join(ABS_DIR,"dataset")
    DATA_BREAST_CANCER_PATH = os.path.join(DATA_PATH,"breast_cancer\\data")


class data_file_path:
    pd2 = get_data_path("pd2.csv")
    
    @staticmethod
    def mnist():
        """
        手写数字识别
        """
        return get_data_path("deep/mnist.npz")

    @staticmethod
    def taitan01():
        """
        泰坦原始数据
        """
        return "/opt/aidoc/data/taitan_train.csv"

    def taitan02():
        """
        泰坦独热编码后的数据
        """
        return "/opt/aidoc/data/taitan02.csv"

    def pd2():
        """
        pandas 测试数据存文件
        
        """
        return "/opt/aidoc/data/pd2.csv"
    
    def wordcount1():
        """
        word count 
        单词统计文本
        """
        return [
            "/data/1_PySpark/test-1.txt",
            "/data/1_PySpark/test-2.txt"]

    def ctr_train01():
        """
        点击率训练集01
        """ 
        return "/data/ctr/train_sample_ctr.csv"

    def ctr_test01():
        """
        点击率测试集01
        """ 
        return "/data/ctr/test_sample_ctr.csv"

    def text_news01_small():
        """
        长文本新闻数据，用于代码开发，22行
        tail -n 100 > cnews_row_2.train.txt
        """
        return "/opt/aisty/data/text_news/kaifa.txt"
        
    def text_news01_small2():
        """
        长文本新闻数据，用于代码开发，5718行
        tail -n 60000 cnews.train.txt|grep "体育" > cnews_row_6.train.txt
        """
        return "/opt/aisty/data/text_news/cnews_row_6.train.txt"

    def text_news01_small_save():
        """
        长文本新闻数据，用于代码开发
        """
        return "/opt/aisty/data/text_news/cnews_row_2.train2.pkl"

    def text_news01_small_save2():
        """
        长文本新闻数据，用于代码开发
        """
        return "/opt/aisty/data/text_news/cnews_row_2.train6.pkl"

    def text_news01_small_save2():
        """
        长文本新闻数据，用于代码开发
        """
        return "/opt/aisty/data/text_news/cnews_row_2.train6.pkl"

    def text_news01_train():
        """
        长文本新闻数据，训练集,125M
        """
        return "/opt/aisty/data/text_news/cnews.train.txt"

    def text_news01_train2():
        """
        长文本新闻数据，训练集,125M
        """
        return "/opt/aisty/data/text_news/cnews.train2.pkl"

    def text_news01_train3():
        """
        长文本新闻数据，训练集
        """
        return "/opt/aisty/data/text_news/cnews.train3.pkl"

    def text_news01_test():
        """
        长文本新闻数据，测试集，27M
        """
        return "/opt/aisty/data/text_news/cnews.test.txt"

    def text_news01_val():
        """
        长文本新闻数据，可用于超参调优，12M
        """
        return "//opt/aisty/data/text_news/cnews.val.txt"

    def text_news01_lda_small():
        """
        长文本新闻数据，用于代码开发,
        LDA降维后数据
        """
        return "/opt/aisty/data/text_news/text.npz"

    def text_news01_lda_small_pkl():
        """
        长文本新闻数据，用于代码开发,
        LDA降维后数据
        """
        return "/opt/aisty/data/text_news/cnews_lda_2.train2.pkl"

    def text_news01_lda_small_pkl2():
        """
        长文本新闻数据，用于代码开发,
        LDA降维后数据
        """
        return "/media/xt/source/data/text_news/cnews_lda_2.train6.pkl"

    def text_news01_lda_train():
        """
        长文本新闻数据，用于代码开发,
        LDA降维后数据
        """
        return "/opt/aisty/data/text_news/text_lda_train.pkl"

# def data_file_path():
#     fp = {
#         "pd2": "/opt/aidoc/data/pd2.csv",
#         "taitan02": "/opt/aidoc/data/taitan02.csv",
#     }
#     return fp

def data_sample_small(x, y, batch_size=1):
    '''
    从原样本中随机取出部分数据

    batch_size为取出的行数
    0表示全部数据


    from data_sample import data_sample_small

    X_train = [[1,2],[1,2],[1,2]]

    y_train = [1,2,3]

    X_train = np.array(aa)

    y_train = np.array(b)


    X_train, y_train = data_sample_small(X_train, y_train, batch_size=16)

    print(X_train)
    
    print(y_train)
    '''
    
    x_row_count = len(x)
    if batch_size > x_row_count or batch_size == 0:
        return x, y

    #  随机取batch_size个不重复索引下标
    index_list =  random.sample(range(x_row_count), batch_size) 
    x_samll = [0 for x in range(len(index_list))]
    y_samll = [0 for x in range(len(index_list))]
    
    for i,elem in enumerate(index_list):
        x_samll[i] = x[elem]
        y_samll[i] = y[elem]
        
    return np.array(x_samll), np.array(y_samll)


def pd1(row_num):
    x = np.random.normal(0,1,[row_num,1])
    y = 0.3*x + 0.7

    x1 = pd.DataFrame(x,columns=list("A"))
    y1 = pd.DataFrame(y,columns=list("B"))

    data1 = pd.concat([x1,y1],axis=1)
    return data1

def pd2(row_num):
    x = np.random.normal(0,1,[row_num,1])
    y1 = 0.3*x + 0.7
    y2 = 1.2 * x**2 - 0.3*x + 0.7

    x1 = pd.DataFrame(x,columns=list("A"))
    y1 = pd.DataFrame(y1,columns=list("B"))
    y2 = pd.DataFrame(y2,columns=list("C"))

    data1 = pd.concat([x1,y1,y2],axis=1)
    return data1



def data_numpy2(row_num):
    """
    返回指定行数的两组数据
    y = x**2 + 2x + 1 , 多特征时sum求和
    x 为两列, 表示数据，符合标准正态分布 
    y 为一行，表示标签
    """
    np.random.seed(111)
    x = np.random.randn(row_num, 2)
    # print(len(x))
    # print(x[:1])  # [[-1.13383833  0.38431919]]
    y = []
    for i in range(len(x)):
        d = x[i]**2 + 2*x[i] + 1
        y.append(np.sum(d))
    # print(y[:3])  # [1.9342523289452673, 6.648312741121465, 0.3373482907093769]
    return x, y


# 梯度下降多项式模型数据生成
def sgd111(row_num=1000000, col_num=3):
    """
    梯度下降多项式模型数据生成
    随机系数与随机样本相乘再求和，得到一批训练集与测试集
    生成几行几列的训练集测试集数据
    默认100万行数据，每行3个特征
    """
    np.random.seed(111)

    X_train = np.random.normal(0, 1, [row_num, col_num])

    theta0 = 0.01
    theta = np.random.rand(col_num)
    # theta_real.append(theta0)
    # for i in range(col_num):
    #     theta_real.append(theta[i])
    # print("theta:", theta0, theta)
    y_train = theta * X_train + theta0 + np.random.normal(0, 0.1, [row_num, col_num])

    X_test = np.random.normal(1, 1, [row_num, col_num])
    y_test = theta * X_test + theta0

    ll = len(X_train)
    y_train_new = []
    y_test_new = []

    # y定为sum的一半，也可以定为别的
    for i in range(ll):
        y_train_new.append(np.sum(y_train[i]))
        y_test_new.append(np.sum(y_test[i]))

    y_train_new = np.array(y_train_new)
    y_test_new = np.array(y_test_new)

    return X_train, X_test, y_train_new, y_test_new



if __name__ == '__main__':
    aa = [[1,2],[1,2],[1,2]]
    b = [1,2,3]
    aa = np.array(aa)
    b = np.array(b)

    x,y = data_sample_small(aa, b)
    print(x)
    print(y)




# if __name__ == "__main__":
#     ep = TestEnvPath()
    # print(ep.DATA_TMP)
    # print(ep.DATA_BREAST_CANCER_PATH)

