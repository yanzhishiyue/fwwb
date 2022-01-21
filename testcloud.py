import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy  as np
from PIL import Image
import sqlite3
con= sqlite3.connect("sqlitesave/videosave.db")
cur=con.cursor()
sql = 'select TEXTS from videosall '
data =cur.execute(sql)
text=''
for item in  data:
    text=text+item[0]
cur.close()
con.close()

cut =jieba.cut(text)
string = ''.join(cut)
print(len(string))
img =Image.open("tree.jpg")
img_array=np.array(img)
wc=WordCloud(
    background_color="white",
    mask=img_array,
    font_path="msyh.ttc"

)
wc.generate_from_text(string)
fig=plt.figure(1)
plt.imshow(wc)
plt.axis('off')  #不显示坐标轴
plt.savefig("word.png",dpi=500)
plt.show()

