from _import import *
import LSTM_data
import LSTM_main
import practice
import tkinter


class Main():
    def trainmod(keyworld):
        class_tag = keyworld
        checkpointsPath = "corpus/class_model/" + class_tag  
        trainPoems = "corpus/" + class_tag+ "_new.txt" 
        trainData = LSTM_data.POEMS(trainPoems)
        trainstart = LSTM_main.MODEL(trainData) 
        print('开始训练模型')
        trainstart.train(checkpointsPath)
        
    def Finalsummary(Num,JueLv,Keyword,write_continue):
        # characters = input("Please input characters：")
        characters = Keyword
        # # 根据关键词返回类别标签
        label = practice.Word2vec_similar.class_tags(characters)
        print(label)
        Imbalance_words = practice.Word2vec_similar.similar_6words(characters, label)
        if  '边塞'== label:
            class_tag = 'biansai'
        elif '怀古'== label:
            class_tag = 'huaigu'
        elif '送别'== label:
            class_tag = 'songbie'
        elif '写景'== label:
            class_tag = 'xiejing'

        checkpointsPath = "corpus/class_model/" + class_tag   
        trainPoems = "corpus/" + class_tag+ "_new.txt" 
        trainData = LSTM_data.POEMS(trainPoems)
        MCPangHu = LSTM_main.MODEL(trainData) 
        poems = MCPangHu.testHead(characters,Imbalance_words,checkpointsPath,Num,JueLv,write_continue)
        print('少女祈祷完成...')
        return poems




if __name__ == "__main__":
    print('程序开始')
    #Main.trainmod('test')
    var=1
    write_continue=1
    txt_new=input('输入一个写诗关键词叭：')
    Num=input('一句几个字呢：')
    JueLv=input('一共几句呢：')
    res  = Main.Finalsummary(Num , JueLv, txt_new,write_continue)
    print(res)
