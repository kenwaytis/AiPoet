import os
import jieba 
from wordcloud import WordCloud
import numpy as np
from PIL import Image

file_dir=r"corpus"
file_name="xiejing_after.txt"
pic_dir=r"corpus"
pic_name="ditu.png"
path=os.path.join(file_dir,file_name)
in_path=os.path.join(pic_dir,os.path.basename(pic_name).split(".")[0]+".png")
to_path=os.path.join(pic_dir,os.path.basename(file_name).split(".")[0]+".png")
  
with open(path,"r",encoding="utf-8") as f:
    t=f.read()
ls=jieba.lcut(t)
txt=" ".join(ls)
mask=np.array(Image.open(in_path))
w=WordCloud(
    font_path="msyh.ttc",
    mask=mask,
    width=800,
    height=600)
w.generate(txt)
w.to_file(to_path)