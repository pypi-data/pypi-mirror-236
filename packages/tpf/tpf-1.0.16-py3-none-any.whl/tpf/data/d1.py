"""
所有方法
输入:各种各样的原始数据(绝对路径),cvs,pkl,...
处理:空值,字符串编码,特征过滤, ...
输出:numpy 数组 
"""
import torch 
import re 
import numpy as np
from numpy.core.fromnumeric import reshape
import pandas as pd 
from sklearn.preprocessing import MinMaxScaler

from tpf.box.fil import fil_suffix 


class Stat():
    print_level = 2
    
    def __init__(self, print_level=1) -> None:
        """
        日志输出级别:
        0-什么都不输出,1-输出少量信息,2-详细的输出,3-超级详细的代码调试信息 
        """
        self.print_level = print_level
        self.score_list = []
        

    def update_print_level(self,print_level):
        self.print_level = print_level


    def log(self,msg, print_level=1):
        if self.print_level >= print_level:
            print(msg)
    def stat():
        pass 

import joblib 
import pickle as pkl 
import pandas as pd
import numpy as np 
import os, json,zipfile
from ai.box.dtype import NumpyEncoder 


def pkl_save(data, file_path, use_joblib=True, compress=0):
    """
    data:保存一个列表时直接写列表,多个列表为tuple形式
    """
    if use_joblib:
        joblib.dump(data, filename=file_path, compress=compress)
    else:
        data_dict = {}
        if type(data).__name__ == 'tuple':
            index = 0
            for v in data:
                index = index+1
                key = "k"+str(index)
                data_dict[key]= v 
        else:
            data_dict["k1"] = data 

        # 在新文件完成写入之前，不要损坏旧文件
        tmp_path = file_path+".tmp"
        bak_path = file_path+".bak"

        with open(tmp_path, 'wb') as f:
            # 如果这一步失败，原文件还没有被修改，重新写入即可
            pkl.dump(data_dict, f)

            # 如果这一步失败，.tmp文件已经被成功写入，直接将.tmp去掉就是最新写入的文件
            # 这里并没有测试rename是否被修改文件的内容，从命名上看，rename是不会的，
            if os.path.exists(file_path):
                os.rename(src=file_path,dst=bak_path)
        if os.path.exists(tmp_path):
            # 如果是下面这一步被强制中止，直接将.tmp去掉就是最新写入的文件
            # 也可以通过.bak文件恢复到修改之前的文件
            # 重命后，不会删除备份文件，最坏的结果是丢失当前的写入，但也会保留一份之前的备份
            os.rename(src=tmp_path,dst=file_path)
        

def pkl_load(file_path, use_joblib=True):
    """ 
    与pkl_load配对使用
    """
    if use_joblib:
        data = joblib.load(file_path)
        return data

    try:
        with open(file_path, 'rb') as f:
            data_dict = pkl.load(f)
        data = tuple(list(data_dict.values()))
        if len(data) == 1:
            return data[0]
        return data 
    except Exception as e:
    #     print(repr(e))
        model = joblib.load(file_path)
        return model 

def write(obj,file_path):
    """
    直接将对象转字符串写入文件,这样可以在文件打开时,看到原内容,还可以进行搜索
    """
    ss = str(obj)
    with open(file_path,"w",encoding="utf-8") as f:
        f.write(ss)

def read(file_path):
    with open(file_path,'r',encoding="utf-8") as f:
        c = eval(f.read())
        return c 

def write_json(obj,file_path):
    fout=open(file_path, "w", encoding='utf-8')
    fout.write(json.dumps(obj, ensure_ascii=False,cls=NumpyEncoder))               
    fout.close() 

def read_zip1(filename):
    """
    读取zip压缩文件中的第一个文件内容

    return
    ---------------------------
    二进制数据
    """
    with zipfile.ZipFile(filename) as f:
        # namelist是解压后的文件列表
        # read返回的是二进制数据
        data = f.read(f.namelist()[0])
    return data


def np_save(x,file_path):
    """
    代码内容实际与np_save_x一样，但这里的参数，特定使用元组，
    在使用np_load方法时，直接以元组的方式取，就可以直接拿到对应的变量
    """
    np.savez(file_path,x=x)

def np_load(file_path): 
    sfx = fil_suffix(file_path)
    if sfx != ".npz":
        file_path = file_path+".npz"
    if os.path.exists(file_path) and os.path.getsize(file_path)>0: 
        fil = np.load(file_path)
        x = fil["x"]
        return x 

def np_save_x(x,file_path):
    np.savez(file_path,x=x)

def np_load_x(file_path): 
    sfx = fil_suffix(file_path)
    if sfx != ".npz":
        file_path = file_path+".npz"
    if os.path.exists(file_path) and os.path.getsize(file_path)>0: 
        fil = np.load(file_path)
        x = fil["x"]
        return x 


def json_dump(obj,file_path):
    ss = json.dumps(obj)
    with open(file_path,'w') as file_obj:
        json.dump(ss,file_obj)

def json_load(file_path):
    with open(file_path,'r') as file_obj:
        names = json.load(file_obj)
    names = json.loads(names)
    return names


def list_diff(a,b):
    """a减b
    Args:
        a (_type_): python list
        b (_type_): python list

    示例:
        a = [1,2,3,3]

        b = [2,3,4,4]

        c = set(a).difference(set(b))

        print(c)

        {1}
    """
    ll = list(set(a).difference(set(b)))
    return ll 

def list_jiaoji(a,b):
    ll = list(set(a).intersection(set(b)))
    return ll 


def numpy2pd(mat):
    """
    numpy 转 pandas,列的名称默认为0,1,2,...
    """
    mat = pd.DataFrame(mat)
    return mat 

def pd2numpy(mat):
    mat = np.array(mat)
    return mat 


def csv_slice(csv_path, target_file, start_end_index=(0,1)):
    """
    大文件截取一个切片，便于开发测试使用
    """
    fil = pd.read_csv(csv_path)
    fil = fil.iloc[start_end_index[0]:start_end_index[1]]
    fil.to_csv(target_file,index=False)

def csv_slice_small(csv_path, target_dir, max_row_one_csv=100000):
    """
    将一个大的CSV文件拆分成一个个小的CSV文件
    """
    fil = pd.read_csv(csv_path)
    # print(fil.shape[0])
    (filepath, tempfilename) = os.path.split(csv_path)
    (filesname, extension) = os.path.splitext(tempfilename)
        
    
    all_row_counts = fil.shape[0]

    single_file_rows = max_row_one_csv 
    if all_row_counts > single_file_rows*3:  # 是批次的3倍才值得拆一下，1个多批次的数据合在一起计算就可以了
        start_index = 0
        while start_index < all_row_counts:
            end_index = start_index + single_file_rows

            if end_index > all_row_counts:
                end_index = all_row_counts

            one_batch_data = fil.iloc[start_index:end_index]
            one_csv_path = os.path.join(target_dir,"{}_{}_{}".format(filesname,start_index, end_index)+".csv")
            one_batch_data.to_csv(one_csv_path, index=False)
            start_index = end_index 
    else:
        start_index = 0
        end_index = all_row_counts
        one_csv_path = os.path.join(target_dir,"{}_{}_{}".format(filesname,start_index, end_index)+".csv")
        one_batch_data.to_csv(one_csv_path, index=False)
         
         
class OneHot(object):
    def __init__(self):
        pass 
     
    @staticmethod
    def get_one_hot(idx, n_classes=10):
        """one hot 编码
        """
        matrix = torch.eye(n_classes)
        return matrix[idx]

    @staticmethod
    def get_one_hot_test():
        oh = OneHot.get_one_hot(3,n_classes=5)
        print(oh)
        
    
class DataStat(Stat):
    def __init__(self, print_level=2) -> None:
        """
        数据处理常用方法 
        """
        super().__init__(print_level=print_level)

    def value_counts(self, data, print_level=2):
        """统计不重复值的个数,用于样本标签均衡判断,

        参数
        ----------------------------
        data: 2维numpy数组


        return 
        --------------------------------
        字典{"值":个数}


        示例
        ----------------------------------
        import ai.box.d1 as d1 

        import numpy as np 

        a = np.array([
            [1,1,3,3,4,5,5,7],
            [1,1,3,3,4,5,5,7]])

        dss = d1.DataStat()

        dss.value_counts(a)


        {
            1:4
            3:4
            4:2
            5:4
            7:2
        }


        """
        data = np.reshape(data,(1,-1))
        data = data[0]
        count = {}
        key_list = []
        for v in data:
            if v in count.keys():
                count[v] = count[v] + 1
            else:
                count[v] = 1
                key_list.append(v)

        
        key_list = np.sort(key_list)
        ss = "{\n"
        if self.print_level >= print_level:
            for k in key_list:
                ss = ss + "  {}:{}\n".format(k,count[k])
        ss = ss + "}"
        self.log(ss,print_level)
        return count 

    def resample_count(self, x, y, count_dict, print_level=2):
        """
        按指定数量对样本进行重采样,用于样本均衡


        参数
        -----------------------------------
        count_dict:类别个数字典,{"0":10,"1":20}
        """
        # 按标签对数据集分类,每类标签一个数据集列表
        x_count_lable = self.sort_by_lable(x,y,print_level) 

        index = 0
        for key in x_count_lable.keys():
            x_tmp = np.array(x_count_lable[key])
            
            # 数据扩展
            x_tmp = self.__resample_1(x_tmp, n_samples=count_dict["{}".format(key)])

            # 标签扩展,由于数据已按标签分类,所有一类数据对应的标签是相同的
            # 只要个数对应上即可 
            if index ==0:
                x_new = x_tmp
                y_new = np.array([key for i in range(len(x_new))])
            else:
                x_new = np.concatenate((x_new,x_tmp),axis=0)
                y_tmp = np.array([key for i in range(len(x_tmp))])
                y_new = np.concatenate((y_new,y_tmp),axis=0)
            index = index + 1
        return x_new,y_new


    def __resample_1(self,data,n_samples):
        """
        重采样,对数据集进行扩展/收缩,使数据集的数量增加/减少

        固定replace=True,如此,样本数据不仅可以减少,而且还可以增加 
        """
        from sklearn.utils import resample
        data = resample(data, n_samples=n_samples, replace=True)
        return data 

    def sort_by_lable(self,x,y,print_level=2):
        """
        按标签对数据集分类,每类标签一个数据集列表,

        return 
        --------------------------------
        不重复字典,标签字典,每个标签对应该标签所有的数据集
        """
        y_lable = np.reshape(y,(1,-1)) 
        lable = y_lable[0] 

        index = 0 
        # 分类列表,每类标签对应一个列表
        sort_dict = {}
        for ss in set(y):
            sort_dict[ss] = []

        for v in lable:
            sort_dict[v].append(x[index])
            index = index + 1

        return sort_dict

    def get_data_by_lable(self, x, y, data_size_every_lable):
        """"

        data_size_every_lable:每个类别的数据量,如果有10个类别,总数据量为10*data_size


        从原数据集中，抽取一部分数据出来,
        接每个标签类别获取指定行数的数据,
        防止出现数据集中只有一个类别的情况，
        单类别场景,模型无法处理，也没有处理的必要
        """
        x_new = []
        y_new = []

        data_count = {}
        max_len = data_size_every_lable 
        index = 0
        for v in y:
            
            if v in data_count:
                data_count[v] += 1
            else:
                data_count[v] = 1
            if data_count[v] < max_len:
                y_new.append(v)
                x_new.append(x[index])
            index += 1
        return x_new,y_new
    
    def lable_encoding(self, lable_y, print_level=2):
        """
        文本分类打标签
        1. 取不重复分类数据集set
        2. 建立元组(标签名称，该标签在set中的索引下标)
        3. 转换为字典{标签名称：索引下标}
        4. 获取原分类名称对应的索引下标列表

        return
        ----------------------------------
        lable encoding后的列表和对应的字典,
        
        其中的类别转换为0,1,2,3,...等索引下标 

        """
        st = set(lable_y)
        dt = dict(zip(st,range(len(st))))
   
        lable_dict = dt
        self.log(lable_dict, print_level=print_level)
        lable_index = np.array([dt[k] for k in lable_y])

        return lable_index,lable_dict

    def onehot_keras(self,y):
        """
        使用keras to_categorical方法独热编码,类别数为不重复标签个数 

        目前的独热编码,如果句子有重复的字或词,则不考虑这种场景 
        """
        from keras.utils import to_categorical
        num_classes = len(set(y))
        y = to_categorical(y, num_classes=num_classes)
        return y 

    
    def onehot_pd(self, dataset, to_numpy=True):
        """
        对整个数据集进行独热编码,不准备进行独热编码的列提前过滤掉不要包含进来

        目前的独热编码,如果句子有重复的字或词,则不考虑这种场景 
        """

        data = np.array(dataset)
        df = numpy2pd(data)
        print("columns:",df.columns)

        dataset = pd.get_dummies(data = df, columns=df.columns)
        if to_numpy:
            data = pd2numpy(dataset)
            return data 
        return dataset

    def onehot_text(self, text, split_flag="\n"):
        """
        一个段落 或 一句话 的独热编码 

        目前的独热编码,如果句子有重复的字或词,则按一个字或词计算 

        示例
        ---------------------------------------
        ss = "啊哈舍不得璀璨俗世,啊哈躲不开痴恋的欣慰,啊哈找不到色相代替,啊哈参一生参不透这条难题"
            
        onehot_text(ss,split_flag=",")


        return
        -------------------------------
        段落的向量表示,分词列表,去重排序后的词条

        """
        import jieba 
        # 原始词列表 
        ss = text 
        word_all = ""
        if split_flag == "":  # 按空白切词
            token_segments = ss.split()
        else:
            token_segments = ss.split(split_flag)  # 划分句子或段落
        # print(token_segments)
        for seg in token_segments:
            word_all = word_all + seg 
        words = jieba.lcut(word_all)           # 词汇列表 

        vocab = sorted(set(words))      # 去重后的词条 

        row_size = len(words)           # 某个词在整个段落或句子中的位置 
        col_size = len(vocab)           # 多少个不重复的词或特征 ,某个词条在向量中的位置 

        #初始化0矩阵
        import numpy as np 
        onehot_vector = np.zeros((row_size,col_size),dtype=int)

        for i,word in enumerate(words):
            onehot_vector[i,vocab.index(word)] = 1 

        return onehot_vector,words,vocab


class CsvStat(Stat):
    """
    csv文件数据处理
    """

    def stat(self, csv_path=""):
        """
        使用pandas统计数据信息
        """
        if csv_path=="":
            print(type(self.data))
            print(self.data.info())
            print(self.data.describe())
        else:
            fil = pd.read_csv(csv_path)
            self.data = fil 
            info = fil.info()
            self.log(info)
            desc = fil.describe()
            self.log(desc)
    def update_data(self,data):
        self.data = data 

    def columns(self,print_level=3):
        cols = self.data.columns.tolist()
        self.log(cols,print_level)
        # cols = self.data.columns
        # for c in cols:
        #     print(c)
        #     print(self.data[c].isnull())
        #     print("---------------")
        return cols

    
    def head(self,num):
        return self.data.head(num)


    def col_filter(self,regex):
        """
        选择指定的列,不同的列以|分隔,"name|age",
        "一元.*" 匹配 "一元一次","一元二次"等所有以"一元"开头的字符串 
        """
        self.data = self.data.filter(regex=regex)
        self.log("数据过滤之后的列-------------------------:",2)
        self.log(self.data.info(),2)

    def empty_num(self,col_name):
        self.data.loc[(self.data[col_name].isnull()), col_name] = np.mean(self.data[col_name])

    def empty_str(self,col_name,char_null="N"):
        self.data.loc[(self.data[col_name].isnull()), col_name] = char_null

    def error_max_7mean(self,col_name):
        """
        超过均值7倍的数据转为均值7倍
        """
        col_mean = np.mean(self.data[col_name])
        self.data[col_name][self.data[col_name]>7*col_mean] = 7*col_mean

    def word2id(self,c_names):
        for cname in c_names:

            words_set = set(self.data[cname]) 
            word2id = dict(zip(words_set, range(len(words_set))))

            idlist = []

            for val in self.data[cname]:
                idlist.append(word2id[val])

            self.data[cname] = idlist 



    def onehot_encoding(self,c_new_names):
        for cname in c_new_names:
            c_new_1 = pd.get_dummies(self.data[cname], prefix=cname)
            self.data = pd.concat([self.data,c_new_1],axis=1)
            self.data.drop([cname],axis=1,inplace=True)

    def col_drop(self,c_names):
        self.data.drop(c_names,axis=1,inplace=True)

    def replace_blank(self,to_float=True):
        """
        去除空格，并将NIL置0
        """
        for col in self.columns():
            index = 0
            for val in self.data[col]:
                # print("data type :",type(val))
                if isinstance(val,str):
                    matchObj = re.search( r'\s+', val)

                    if to_float:
                        # print("---col:{},val--{}==".format(col,val))
                        if val == "NIL":
                            val = "0"
                        if matchObj:
                            self.data[col].iloc[index] = float(val.replace('\s+','',regex=True,inplace=True))
                        else:
                            self.data[col].iloc[index] = float(val)
                    else:
                        if matchObj:
                            self.data[col].iloc[index] = val.replace('\s+','',regex=True,inplace=True)
                else:
                    continue
                index +=1





    def min_max_scaler(self,feature_range=(0, 1)):
        """
        return
        ---------------------
        <class 'numpy.ndarray'>,MinMaxScaler自动将pandas.core.frame.DataFrame转为了numpy.ndarray
        
        """
        self.scaler = MinMaxScaler(feature_range=feature_range)
        self.replace_blank()
        data = self.scaler.fit_transform(self.data)
        return data 

    def min_max_scaler_inverse(self, data):
        data = self.scaler.inverse_transform(data)
        return data 


def min_max(data,index_col=[]):
    """
    2维数据归一化处理
    """
    if not isinstance(data,np.ndarray):
        data = np.array(data)
    row_num,col_num = data.shape
    # print("len(index_list):",len(index_col))
    if len(index_col)==0:
        for i in range(col_num):
            _max,_min = data[:,i].max(),data[:,i].min()
            aa = _max 
            if _max>_min:
                aa = _max - _min 
            data[:,i] = (data[:,i]-_min )/aa 
    else:
        for i in index_col:
            _max,_min = data[:,i].max(),data[:,i].min()
            aa = _max 
            if _max>_min:
                aa = _max - _min 
            data[:,i] = (data[:,i]-_min )/aa  
    return data 



if __name__ == "__main__":
    OneHot.get_one_hot_test()  # tensor([0., 0., 0., 1., 0.])
    pass 