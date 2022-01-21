def dytime(data):
    from copy import deepcopy
    time = []
    # data=["63.868秒","1.424秒","2.221秒","4.141秒","1.245秒"]
    splitlist=[]
    for i in range(len(data)):
        splitlist.append(data[i][:-1])
    num = 0
    new_list=[]
    new_list1=[]
    list3=[]
    new_list = list(map(eval, splitlist))
    for i in range(len(new_list)):
        num+=new_list[i]
        new_list1.append(num)
    print(new_list1)
    for i in range(len(new_list1)):
        # print(str(timelist[i])+'秒'+'-'+str(new_list1[i])+'秒')
        yushu = int(new_list1[i]) % 60
        xiaoshu = round(new_list1[i], 3) - int(new_list1[i])
        xiaoshu = "{:.3f}".format(xiaoshu)
        fenzhong = int(new_list1[i]) // 60
        res = str(fenzhong) + ":" + str(yushu) + xiaoshu[1:]
        list3.append(res)
    print(list3)
    timelist = deepcopy(list3)
    timelist.insert(0,'0:0')
    print(timelist)

    for i in range(len(list3)):
        # print(str(timelist[i])+'-'+str(list3[i]))

        time.append(str(timelist[i])+' - '+str(list3[i]))
    return time