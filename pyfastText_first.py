from _import import *
print('读取停用词')
def read_Stopwords():
    print('加载停用词')
    stop_word = []
    stop_path = 'corpus/CNstopwords.txt'
    with open (stop_path, 'r', encoding='utf-8') as stop_file:
        for line in stop_file:
            line = str (line.replace('\n', '').replace ('\r', '').split ())
            stop_word.append (line)
        stop_word = set (stop_word)  # 去重列表中重复的词汇
    return stop_word
 
# 训练数据统一格式
def fileopems_file_deal(path, classtage):
    stop_word = read_Stopwords()
    path_name = path
    rules = u'[\u4e00-\u9fa5]+' # 只是汉字的正则表达式，可以去除，。！（）等特殊符号
    pattern = re.compile(rules)
    sentences = []
 
    with open(path_name, 'r', encoding = 'utf-8') as f_reader:
        for line in f_reader:
            line = line.replace('\n','').replace('\r',"").split()
            line = str(line)
            line = ' '.join(jieba.cut(line)) # 以空格来分词
            seg_list = pattern.findall(line)
            word_list = []
            for word in seg_list:
                if word not in stop_word:  # 去除停用词
                    word_list.append(word)
            if len(word_list)> 0:
                sentences.append(word_list)
                line = ' '.join(word_list)
                f_write =open('corpus/poetry_class.txt','a+')
                line2 = '__label__' + classtage + '\t' + line + '\n'  # 统一ff文本分类的格式
                f_write.write(line2)
                f_write.flush()  #强行把缓冲区中的内容放到磁盘中
 
# 对数据进行训练产生模型   **.model文件
def ff_deal():
    path = r'corpus\poetrySong.txt'
    print('生成模型')
    model = ff.train_supervised(
        input = path,
        epoch=25,lr=1.0,dim=100,wordNgrams = 2, verbose=2, minCount=1
    )
    print('保存模型')
    path_save = 'corpus/class_poetry.model'
    model.save_model(path_save)

# # 对各类训练数据进行统一格式处理---> 汇总写入shi.txt文件
if __name__ =='__main__':
    print('程序开始')
    path1 = 'corpus/biansai.txt'
    classtage1 = '边塞'
    fileopems_file_deal(path1, classtage1)
    print('边塞类型写入成功')
    path2 = 'corpus/huaigu.txt'
    classtage2 = '怀古'
    fileopems_file_deal(path2, classtage2)
    print('怀古类型写入成功')
    path3 = 'corpus/songbie.txt'
    classtage3 = '送别'
    fileopems_file_deal(path3, classtage3)
    print('送别类型写入成功')
    path4 = 'corpus/xiejing.txt'
    classtage4 = '写景'
    fileopems_file_deal(path4, classtage4)
    print('写景类型写入成功')
