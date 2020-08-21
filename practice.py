from _import import *
 
class Word2vec_similar():
    # 处理数据（若分类已处理过，则不用再次处理）
    def file_deal(self,path_before,path_after):
        # 处理停用词
        stop_word = []
        with open("corpus/CNstopwords.txt",'r',encoding='utf-8') as f_reader:
            for line in f_reader:
                line = str(line.replace('\n','').replace('\r','').split())
                stop_word.append(line)
        stop_word = set(stop_word)
 
        rules = u'[\u4e00-\u9fa5]+'
        pattern = re.compile(rules)
        f_write = open(path_after, 'a',encoding='utf-8')
        with open(path_before, 'r', encoding='utf-8') as f_reader2:
            for line in f_reader2:
                title,author,poem = line.strip().split("::")
                poem = poem.replace('\n','').replace('\r','').split()
                poem = str(poem)
                poem = ' '.join(jieba.cut(poem))
                seg_list = pattern.findall(poem)
 
                word_list = []
                for word in seg_list:
                    if word not in stop_word:
                        word_list.append(word)
                line = " ".join(word_list)
                f_write.write(line + '\n')
                f_write.flush()
            f_write.close()
 
    """"
    Word2vec 训练模型参数
    sentences 分析的预料，可以是一个列表，或从文件中遍历读出
    size ：词向量的维度， 默认值 100 ， 语料> 100M, size值应增大
    window: 词向量上下文最大距离，默认 5，小语料值取小
    sg: 0--> CBOW模型    1--> Skip-Gram模型
    hs: 0 负采样 ， 1 Hierarchical Softmax
    negative ： 使用负采样 的个数， 默认 5
    cbow_mean:  CBOW中做投影，默认 1，按词向量平均值来描述
    min_count: 计算词向量的最小词频 ，可以去掉一些生僻词（低频），默认 5
    iter:随机梯度下降法中迭代的最大次数，默认 5，大语料可增大
    alpha: 迭代的初始步长，默认 0.025
    min_alpha:最小迭代步长，随机梯度下降法，迭代中步长逐步减小
    """
    def practice_model (self ,poetry, path_save_key):
        # path 全唐诗路径(处理后的) ，path_save_key 生成模型后保存的路径
        path = poetry
        sentences = word2vec.Text8Corpus (path)  # 加载文件
 
        # 调参 iter 训练轮次    size 大小
        # 全部诗个模型性 iter = 20 ，size = 300
        # 其余5类是模型  iter = 20 ， size = 200
        model = word2vec.Word2Vec(sentences,
                                  iter=20, alpha=0.01, min_alpha=0.005, min_count=8,size=150)
        # 保存模型   path_save模型路径
        path_save = path_save_key
        model.save (path_save)
 
    # 返回 6 个相似词
    def similar_6words(key_word, label):
        if label == '边塞':
            path_save = "corpus\class_model/Keyword_biansai.model"
        elif label == '怀古':
            path_save = "corpus\class_model/Keyword_huaigu.model"
        elif label == '送别':
            path_save = "corpus\class_model/Keyword_songbie.model"
        elif label == '写景':
            path_save = 'corpus\class_model/Keyword_xiejing.model'
        # 维基百科 2 词 相似度计算
        model = word2vec.Word2Vec.load(path_save)
        re_word = []
        re_key_word = key_word
        # 异常处理，当语料中无此关键词时，先取词前2个字，若还没有，取第一个字
        try:
            similary_words = model.wv.most_similar(positive=[key_word], topn=6)
        except:
            key_word = key_word[0:2]
            try:
                similary_words = model.wv.most_similar(positive=[key_word], topn = 6)
            except:
                key_word = key_word[0]
                try:
                    similary_words = model.wv.most_similar(positive=[key_word], topn=6)
                except:
                    key_word=re_key_word[1]
                    try:
                        similary_words = model.wv.most_similar(positive=[key_word], topn=6)
                    except:
                        key_word=re_key_word[2]
                        similary_words = model.wv.most_similar(positive=[key_word], topn=6)
        print(similary_words)
        for e in similary_words:
            print(e[0],e[1])
            re_word.append(e[0])
        return re_word
 
    # 计算 2 词之间的相似度
    def class_tags(str1):

        # 5类诗的主题词，用于与用户输入的关键词进行相似度计算，判断类别--》5*15 二维矩阵
        Themeword = [['' for i in range (4)] for i in range (15)]
        Themeword[0] = ['万里', '不见', '将军', '长征', '战士', '黄沙', '征战', '大漠', '漫漫', '红旗', '功名', '男儿', '黄河', '单于', '大刀']
        Themeword[1] = ['不知', '平生', '人间', '何人', '乾坤', '可怜', '无人', '千里', '天下', '四海', '人生', '不须', '千载', '尘埃', '太平']
        Themeword[2] = ['古', '青山', '送别', '离别', '无人', '相思', '平生', '天涯', '理想', '秋风', '相逢', '相识', '明月', '故人', '夕阳']
        Themeword[3] = ['梅花', '桃花', '山中', '今日', '白云', '西湖', '昨夜', '寂寞', '风雨', '日月', '星辰', '徘徊', '大地', '无心', '老去']
 
        # 维基百科计算2个词的相似度
        wiki_path_model = "corpus/class_model\wiki_corpus.model" # 加载训练好的模型wiki_corpus.model
        model2 = word2vec.Word2Vec.load (wiki_path_model)
        sum_similar = [0 for i in range(4)]
        for i in range(4):
            for j in range(15):
                # 异常处理，解决 wiki_model中没用此关键词的情况
                # 异常处理，当语料中无此关键词时，先取词前2个字，若还没有，取第一个字
                flag = False
                try:
                    sim_value = model2.similarity (str1, Themeword[i][j])
                    flag = True
                except:
                    print ("少女似乎在词库中找不到这个词呢...")
                    print('但是问题不大！')
                    print('替换词生成中...')
                    str1 = str1[0:2]
                    try:
                        sim_value = model2.similarity (str1, Themeword[i][j])
                        flag = True
                    except:
                        str1 = str1[0]
 
                if flag == False:
                    sim_value = model2.wv.similarity('相思', Themeword[i][j])
                sum_similar[i] += sim_value
 
        max_value = max(sum_similar) #  选出最相似的那类
        similar_index = sum_similar.index(max_value) # 确定是哪类的标签
        print('诗词类型确定...')
        label_tags = ["边塞", "怀古", "送别", "写景"]
        print(similar_index)
        return label_tags[similar_index]
 
    # 选择《诗学含英》中的6个与主题词最相似的标题词
    def label_offen_words(character):
        before_key = 6
        title =[]
        word_list = []
        shi_xue_han_ying_path = 'corpus/sxhy.txt'
        with open(shi_xue_han_ying_path,'r',encoding='utf-8') as f_reader:
            for line in f_reader:
                t,w = line.split("::")
                title.append(t)
                word_list.append(w)
        # 维基百科的模型
        path_save = 'corpus/class_model\wiki_corpus.model'
        # 加载训练好的模型 wiki_corpus.model
        model = word2vec.Word2Vec.load(path_save)
        similary_6value = [0 for i in range(len(title))]
        for i in range(len(title)):
            try:
                similary_6value[i] = model.wv.similarity(character)
            except Exception as e:
                character  =character[0:2]
                try:
                    similary_6value[i] = model.wv.similarity(character)
                except :
                    character = character[0]
 
        similary_6value = np.array(similary_6value)
        # 返回一个排序后的数组的索引, 倒序-截取数组下标值
        max_6value_id = similary_6value.argsort()[::-1][0:before_key]
        word_6list = ""
        for i in range(before_key):
            word_6list += "".join(word_list[max_6value_id[i]])
 
        word_6list = word_6list.replace("\n", "")
        word_6list = set(word_6list)
        return word_6list
    # 训练生成 5 类诗歌的word2vec模型
    def train_6poems_word2vec_model(self):
        print('准备开始训练模型')
        ws = Word2vec_similar ()
        # path1..,path1_save_model ,生成各类诗的word2vec的模型
        path1 = 'corpus/biansai_new.txt'
        path11 = "corpus/biansai_after.txt"
        path2 = 'corpus/huaigu_new.txt'
        path22= "corpus/huaigu_after.txt"
        path3 = 'corpus/songbie_new.txt'
        path33 = "corpus/songbie_after.txt"
        path4 = 'corpus/xiejing_new.txt'
        path44 = "corpus/xiejing_after.txt"
        path1_save_model = 'corpus\class_model/Keyword_biansai.model'
        path2_save_model = 'corpus\class_model/Keyword_huaigu.model'
        path3_save_model = 'corpus\class_model/Keyword_songbie.model'
        path4_save_model = 'corpus\class_model/Keyword_xiejingu.model'
        if os.path.exists('corpus/biansai_after.txt'):#格式化后的文本存在就直接训练
            print("直接开始训练")
            ws.practice_model(path11, path1_save_model)
            print('立志豪放模型训练完成')
            ws.practice_model(path22, path2_save_model)
            print('家国情怀模型训练完成')
            ws.practice_model(path33, path3_save_model)
            print('离别送别模型训练完成')
            ws.practice_model(path44, path4_save_model)
            print('咏物抒情模型训练完成')
        else: #否则就先格式化
            ws.file_deal(path1,path11)
            print('立志豪放类型格式化完成')
            ws.file_deal (path2, path22)
            print('家国情怀类型格式化完成')                         
            ws.file_deal (path3,path33)
            print('离别送别类型格式化完成')          
            ws.file_deal (path4, path44)
            print('咏物抒情类型格式化完成')           
        # 训练每类的模型
            ws.practice_model(path11, path1_save_model)
            print('立志豪放模型训练完成')
            ws.practice_model(path22, path2_save_model)
            print('家国情怀模型训练完成')
            ws.practice_model(path33, path3_save_model)
            print('离别送别模型训练完成')
            ws.practice_model(path44, path4_save_model)
            print('咏物抒情模型训练完成')

 
   
if __name__ == '__main__':
    print('程序开始')
    ws = Word2vec_similar()
    # 若5 类诗歌的word2vec模型不存在，则训练生成
    #if os.path.exists('corpus/class_model/Keyword_biansai.model')== False:
    #    ws.train_6poems_word2vec_model()
 
    # # 测试：根据输入词，来判别哪一类, eg: 边塞--->边塞征战类
    key_word = '大刀'
    result = ws.class_tags(key_word)
    print(result)
 
    # 测试：判断类别后返回6个相似词,eg: 秋思-->['秋意', '寒砧', '竹声', '空阶', '窗且', '灯昏']
    new_result = ws.similar_6words(key_word,result)
    print(new_result)
 
    # 测试：绘制一类诗歌的云图
