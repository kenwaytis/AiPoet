#-*- coding : utf-8 -*-
# coding: utf-8

"""
    诗分类模型 ；ff分类
    数据格式 ：'__label__'  + classtage(类型) + '\t'+ line（诗内容） + '\n'
"""
from _import import *

def read_Stopwords():
    stop_word = []
    stop_path = 'corpus/CNstopwords.txt'
    with open (stop_path, 'r', encoding='utf-8') as stop_file:
        for line in stop_file:
            line = str (line.replace('\n', '').replace ('\r', '').split ())
            stop_word.append (line)
        stop_word = set (stop_word)  # 去重列表中重复的词汇
    return stop_word
 

def ff_deal():
    path = r'corpus\poetry_class.txt'
    print('生成模型')
    model = ff.train_supervised(
        input = path,
        epoch=10000, lr=0.025,wordNgrams=2, verbose=2, minCount=1)
    print('保存模型')
    path_save = 'corpus/class_poetry.model'
    model.save_model(path_save)



def file_deal(test):
    answer=''
    stop_word = read_Stopwords()
    # 文本预处理
    sentecnces = []
    rules =u'[\u4e00-\u9fa5]+'
    pattern  =re.compile(rules)
    line =test
    line = line.replace('\r','').replace('\n','').split()
    line = str(line)
    line =' '.join(jieba.cut(line))
    seg_list = pattern.findall(line)
    word_list= []
    for word in seg_list:
        if word not in stop_word:
            word_list.append(word)  # 去除停用词
    if len(word_list)>0:  # 去除空行
        sentecnces.append(word_list)
        answer = ' '.join(word_list) # 以空格来划分各各词
    return answer


 
if __name__ =='__main__':
    print('程序开始')
    save_path = 'corpus/class_poetry.model'
    if os.path.exists(save_path):
        print('加载模型')
        model = ff.load_model(save_path)
        print('模型加载成功')
    else: # 没有训练模型，先训练，再加载
        print('训练模型中')
        ff_deal()
        model = ff.load_model(save_path)
        print('训练完成，加载完成')
    test_path = r'corpus/poetrySong.txt'  # 30w诗歌数据集
    # f_reader =open(test_path , 'r',encoding='utf-8')
    # 分类后数据写入各类文件
    class_path1 = "corpus/biansai_new.txt"
    f_write1 = open (class_path1, 'a+', encoding='utf-8')
    class_path2 = "corpus/huaigu_new.txt"
    f_write2 = open (class_path2, 'a+', encoding='utf-8')
    class_path3 = "corpus/songbie_new.txt"
    f_write3 = open (class_path3, 'a+', encoding='utf-8')
    class_path4 = "corpus/xiejing_new.txt"
    f_write4 = open (class_path4, 'a+', encoding='utf-8')
    print('准备工作完成')
    print(model)
    f_reader = open(test_path , 'r',encoding='utf-8')
    print('开始处理诗库')
    while True:
        line = f_reader.readline()
        if not line:
            break
        tests_str = file_deal(line)
        print(tests_str)
        label = model.predict(tests_str)
        # label[0] 类别 label[1] 概率  label为元组
        print(label[0])
        print(label[1])
        value= str(label[0])
        if value ==  "('__label__边塞',)" :
            print('边塞')
            f_write1.write(line)
            f_write1.flush()
        elif value == "('__label__怀古',)" :
            print('怀古')
            f_write2.write(line)
            f_write2.flush()
        elif value == "('__label__送别',)" :
            print('送别')
            f_write3.write(line)
            f_write3.flush()
        elif value == "('__label__写景',)" :
            print('写景')
            f_write4.write(line)
            f_write4.flush()
