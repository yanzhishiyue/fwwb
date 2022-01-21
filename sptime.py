data=["63.868秒","1.424秒","2.221秒","4.141秒","1.245秒","3.333秒"]

def spcstime(data):
    cstime=0.000
    for i  in data:
       cstime+= float(i[:-1])
    # print(cstime)
    yushu= int(cstime)%60
    # print(yushu)
    xiaoshu=round(cstime,3)-int(cstime)
    xiaoshu= "{:.3f}".format(xiaoshu)
    print(xiaoshu)
    fenzhong=int(cstime)//60
    res=str(fenzhong) + "分" + str(yushu)+xiaoshu[1:]+ "秒"
    return  res
print(spcstime(data))
# ['0.000秒/63.868秒']
