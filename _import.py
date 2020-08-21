import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import io
import fastText as ff
import re
import jieba
import numpy as np
import random


# word2vec 工具包
from gensim.models import word2vec
from matplotlib.font_manager import FontProperties
from sklearn.decomposition import PCA
from matplotlib import pyplot
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections#用于LSTM_data

#tf.disable_v2_behavior()#2.0 tf 使用 1.0 tf 时关闭紧急执行

# 设置全局变量参数 + LSTM 模型参数
batchSize = 32
learningRateBase = 0.001     # 学习率
learningRateDecayStep = 1000 # 每隔 1000 步学习率下降
learningRateDecayRate = 0.95
epochNum = 30                    # train epoch
generateNum = 1                  # number of generated poems per time


Yayun = ""   # 第二句最后一个字， （押韵字）
Yayunlist=[]
saveStep = 1000                  # save model every savestep
type = "poetryTang"                   # dataset to use, shijing, songci, etc

'''
import argparse
import time
import operator

# TF-IDF所需工具包
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


'''
