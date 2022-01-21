import matplotlib.pyplot as plt
data1 =['jhgs.mp4','jhsl.mp4','d15k.mp4',"d14k.mp4",'d1k.mp4',"d3k.mp4"] #视频的文件名
exchangetime=[6,7,3,8,1,9] #修改的次数
def echartsj(data1,exchangetime):

    bar = Bar("用户视频编辑次数情况")
    bar.add("修改次数",data1,exchangetime,mark_line=['average'],mark_point=["max","min"])
    bar.render()


echartsj(data1,exchangetime)
