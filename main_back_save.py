""""
    主函数
    1.根据用户输入的根据词，判断所属类别
    2.在指定类别中，根据关键词生成备选词（字）
    3.LSTM模型进行预测
"""
from _import import *
import LSTM_data
import LSTM_main
import practice
import tkinter


class Main():
    def trainmod(keyworld):
        class_tag = keyworld
        checkpointsPath = "corpus/class_model/" + class_tag    # checkpoints location
        trainPoems = "corpus/" + class_tag+ "_new.txt"  # training file location
        print('开始处理输入诗歌')
        trainData = LSTM_data.POEMS(trainPoems)
        trainstart = LSTM_main.MODEL(trainData) 
        print('开始训练模型')
        trainstart.train(checkpointsPath)
        
    def Finalsummary(Num,JueLv,Keyword):
        # characters = input("Please input characters：")
        characters = Keyword
        # # 根据关键词返回类别标签
        label = practice.Word2vec_similar.class_tags(characters)
        print(label)
        Imbalance_words = practice.Word2vec_similar.similar_6words(characters, label)#返回6个关键词
        if  '边塞'== label:
            class_tag = 'biansai'
        elif '怀古'== label:
            class_tag = 'huaigu'
        elif '送别'== label:
            class_tag = 'songbie'
        elif '写景'== label:
            class_tag = 'xiejing'

        checkpointsPath = "corpus/class_model/" + class_tag    # checkpoints location
        trainPoems = "corpus/" + class_tag+ "_new.txt"  # training file location
        # 训练数据时用，依次更改诗的种类，路径
        # trainPoems = "E:\Desk\MyProjects\Python/NLP_Demo1\File_jar\generate_poem\Poetry_class/yongshi.txt"
        # checkpointsPath = "E:\Desk\MyProjects\Python/NLP_Demo1\File_jar\generate_poem/yongshi"
        trainData = LSTM_data.POEMS(trainPoems)
        MCPangHu = LSTM_main.MODEL(trainData)  # 带参初始化
        #***** 分别训练5类模型
        # MCPangHu.train(checkpointsPath)
        poems = MCPangHu.testHead(characters,Imbalance_words,checkpointsPath,Num,JueLv)
        return poems

def mClick_beign():
    label_var=tkinter.Label(win,text='少女祈祷中\n',font=('宋体','20'))
    label_var.grid(row=2,column=1,rowspan=9)
    txt_new=txt_var.get()
    Num = 5
    JueLv = 8
    res  = Main.Finalsummary(Num , JueLv, txt_new)
    label_var.config(text=res)


if __name__ == "__main__":
    print('程序开始')
    #Main.trainmod('test')
    
    win=tkinter.Tk()
    win.title('你的AI少女 By cst17053 086 061')
    win.geometry('425x200+600+300')
    label_introduce=tkinter.Label(win,text="欢迎来到你的AI写诗软件：敲一个你喜欢的词语叭")
    label_introduce.grid(row=0,column=0)
    txt_var=tkinter.StringVar()
    txt_characters=tkinter.Entry(win,width=20,textvariable=txt_var)
    txt_characters.grid(row=1,column=0)
    btn=tkinter.Button(win,text='ai冲呀',command=mClick_beign)
    btn.grid(row=3,column=0)
    win.mainloop()
