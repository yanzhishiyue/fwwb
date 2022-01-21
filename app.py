import settings
import os
from moviepy.editor import *
from flask import Flask,jsonify,request,render_template,redirect,url_for,flash
import json
from os import path
from werkzeug.utils import secure_filename
import pathlib
import pyquery
import sqlite3
from flask_cors import *
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from  wtforms import SubmitField,StringField,PasswordField
from wtforms.validators import DataRequired,EqualTo
import pyaudio
import wave
import pydub
import numpy as np
import os
import operator
from pydub import AudioSegment
from flask import Response
from urllib import parse
import shutil
app = Flask(__name__)
app.secret_key="qyy"
app.config.from_object(settings)  # 加载配置文件
CORS(app, supports_credentials=True)
# print(app.config)  # 打印配置文件

# @app.after_request
# def cors(environ):
#     environ.headers['Access-Control-Allow-Origin']='*'
#     environ.headers['Access-Control-Allow-Method']='*'
#     environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
#     return environ

login_id =''
resid=0
videodata=''
times=0
countfile=0
locatetime=[]
csz=[]



app.route('/user/<username>')
def username(username):
    return "username"%username


class LoginForm(FlaskForm):
    username=StringField('登录名:',validators=[DataRequired()])
    password=PasswordField('密码:',validators=[DataRequired()])
    name = StringField('用户姓名:' ,validators=[DataRequired()])
    email=StringField('邮箱:',validators=[DataRequired()])
    phonenumber=StringField('手机号:',validators=[DataRequired()])
    submit =SubmitField('提交')





@app.route('/wave',methods=['GET','POST'])
def wave():
    return  render_template('wavevisual.html')

@app.route('/',methods=['GET','POST'])
def hello_world():
     global login_id
     if request.method == "POST":

        user_info = request.form.to_dict()
        # print(user_info.get("username"))
        # print(user_info.get("password"))
        conn = sqlite3.connect('sqlitesave/videosave.db')
        cursor = conn.execute("SELECT login_name,login_pwd from sys_user ")
        flag=1
        for it in cursor:
            # print(it[0],it[1])
            if user_info.get("username")== it[0] and  user_info.get("password") == it[1]:

                    login_id=it[0]
                    return redirect("/index")
            else:
                flag=0

        conn.close()
        if flag==0:
             flash("不存在该用户或密码错误")
             return redirect("/")
     return render_template("loginin.html")

@app.route('/register',methods=['GET','POST'])
def register():
    login_form=LoginForm()
    if request.method == "POST":
        conn = sqlite3.connect('sqlitesave/videosave.db')
        cursor = conn.execute("SELECT login_name,login_pwd,user_name,email,tel from sys_user ")
        c = conn.cursor()
        if login_form.validate_on_submit():
            username=request.form.get('username')
            password = request.form.get('password')
            name = request.form.get('name')
            email = request.form.get('email')
            phonenumber = request.form.get('phonenumber')
            flag=1
            for it in  cursor:
                if username==it[0]:
                    print(it[0],it[1])
                    flash("该用户名已被注册")
                    return redirect("/register")
                else:
                    flag=0
            if flag==0:
                c.execute("INSERT INTO sys_user(login_name,login_pwd ,user_name ,email ,tel) VALUES (?,?,?,?,?)",
                          (username, password, name, email, phonenumber))
                conn.commit()
                print(username, password, name, email, phonenumber)
                return render_template("index.html")


    return render_template("register.html",form=login_form)

@app.route('/selfinfo',methods=['GET','POST'])
def selfinfo():
    global login_id #用户 id
    global videodata #视频名称
    global  times # 次数
    global countfile #文件个数
    global locatetime #修改位置
    conn = sqlite3.connect('sqlitesave/videosave.db')
    cursor = conn.execute("SELECT login_name,user_name,email,tel from sys_user ")
    login_name = ''
    login_email = ''
    login_tel = ''
    for it in cursor:
        if login_id==it[0]:
            login_name=it[1]
            login_email=it[2]
            login_tel=it[3]
    imgstream=return_img_stream("word.png")
    imgfengge = return_img_stream("segpivture.png")
    import getnowtime
    datalist=[]

    time=getnowtime.gettime() #时间
    conn.commit()
    conn.close() #搜索用户信息
    print("用户id："+login_id,"视频名字："+videodata,"时间："+time,"次数："+str(times))
    strlocaltime=' '.join(locatetime)
    conn = sqlite3.connect('sqlitesave/videosave.db')
    c = conn.cursor()
    c.execute("INSERT INTO showtable(id,name,date,exchangetime) VALUES (?,?,?,?)",
              ("集合概述",videodata,time,strlocaltime))
    conn.commit()
    conn.close()#插入 视频修改信息到数据库

    conn = sqlite3.connect('sqlitesave/videosave.db')
    cursor=conn.execute("SELECT id,name,date,exchangetime from showtable ")
    for it in cursor:
        datalist.append(it)
    conn.commit()
    conn.close()#从数据库取出

    print(datalist)
    return render_template("个人中心.html",countfile=countfile,id=login_id,name = login_name,email=login_email,tel=login_tel,imgstream=imgstream,imgfengge=imgfengge,listall=datalist)




@app.route('/index',methods=['GET','POST'])
def index():

    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, r'static\uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

    return  render_template('index.html')

@app.route('/selectvideo',methods=['GET','POST'])
def selectvideo():
    return  render_template('selectvideo.html')
@app.route('/weneben',methods=['GET','POST'])
def wenbenye():
    global csz

    # os.system("python iat_ws_python3.py %s" % (".\\save_audio\\"))  # 传输音——>文本位置
    # conn = sqlite3.connect('sqlitesave/videosave.db')
    # conn.execute("drop table videosall   ")
    # conn.commit()
    # c = conn.cursor()
    # c.execute('''CREATE TABLE videosall
    #            (ID INT PRIMARY KEY     NOT NULL,
    #            PATH           TEXT    NOT NULL,
    #            TEXTS           TEXT    NOT NULL,
    #            FATHER            INT,
    #            videoduration    TEXT
    #                     );''')
    # conn.commit()
    # # c.execute('''alter table videosall add column videoduration TEXT;''')
    # print("Table created successfully")
    # import sqlitesave.sqlite3insert as ss
    # ss.save_tovideoallmethod()

    conn = sqlite3.connect('sqlitesave/videosave.db')
    cursor = conn.execute("SELECT ID ,TEXTS from videosall ")
    zidian = dict()
    for it in cursor:
        zidian[it[0]] = it[1]
    conn = sqlite3.connect('sqlitesave/videosave.db')
    cursor = conn.execute("SELECT ID ,TEXTS ,videoduration from videosall ")
    zidian = dict()
    csztime = []

    for it in cursor:
        zidian[it[0]] = it[1]
        csztime.append(it[2])
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, r'static\uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
    import duiyinspt as dui
    csz=dui.dytime(csztime) #视频初始帧



    return render_template("wenben.html",zidian=zidian,csz=csz)
@app.route('/showvideo',methods=['GET','POST'])
def showvideo():
    # pydub.AudioSegment.converter = "D:\\ffmpeg-N-100592-g42ee3898c8-win64-gpl-shared-vulkan\\bin\\ffmpeg.exe"
    # mp3_path = 'save_audio/0.wav'
    # music1 = AudioSegment.from_wav(mp3_path)
    # path = 'save_audio'  # 获取当前路径
    # count = 0
    # for root, dirs, files in os.walk(path):  # 遍历统计
    #     for each in files:
    #         if each.endswith('wav'):
    #             count += 1  # 统计文件夹下文件个数
    # print("文件的总数量为：", count)
    # for i in range(count - 1):
    #
    #     mp3_path = "./save_audio/" + str(i + 1) + ".wav"
    #     music2 = AudioSegment.from_wav(mp3_path)
    #     music1 += music2
    #     _music1_db = music1.dBFS
    #     _music2_db = music2.dBFS
    #     dbplus = _music1_db - _music2_db
    #     if dbplus < 0:
    #         music1 += abs(dbplus)
    #     elif dbplus > 0:
    #         music2 += abs(dbplus)
    # music1.export('./mixfile/mix.wav', format='wav')
    global times
    return render_template("showvideo.html",times=times)



@app.route('/shijianxian',methods=['GET'])
def shijianxian():
    return render_template("shijianxian.html")


@app.route('/fengge',methods=["POST","GET"])
def fengge():
    import uuid
    import datetime
    def mkdir(path):
        # 引入模块
        import os
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            return False



    def getsavefilename():
        dy = str(datetime.datetime.now().year)
        dm = str(datetime.datetime.now().month)
        dd = str(datetime.datetime.now().day)
        if len(dm) == 1:
            dm = '0' + dm
        if len(dd) == 1:
            dd = '0' + dd
        dall = dy + dm + dd
        print(dall)
        uid = str(uuid.uuid4())
        suid = ''.join(uid.split('-'))
        suid = suid[:20]
        print(suid)
        res = "/" + dall + '/' + suid
        return res[:9], res[9:]

    dictfile, filename = getsavefilename()
    f = request.data
    s1 = str(f, encoding='utf-8')
    rdata = s1[-9:]
    rdata = rdata[1:]
    print(rdata)
    audiolocal = "static/uploads/courseKpoint/video"+dictfile
    for root, dirs, files in os.walk(audiolocal):  # 遍历统计
        for each in files:
            if each.endswith('wav'):
                 rdata=each
                 break

    audiolocal = "static/uploads/courseKpoint/video" +dictfile+"/"+ rdata
    import  multi_detect_BIC as bic
    bic.seg(audiolocal)
    path = 'save_audio'    #获取当前路径
    count = 0
    for root,dirs,files in os.walk(path):    #遍历统计
          for each in files:
              if each.endswith('wav'):
                 count += 1   #统计文件夹下文件个数
    returncount="切分成功，切分成"+str(count)+"条"
    return jsonify({"tips":returncount})

@app.route('/extrator',methods=['POST','GET'])
def extrator():
            global countfile
            global videodata
            import uuid
            import datetime
            def mkdir(path):
                # 引入模块
                import os
                # 去除首位空格
                path = path.strip()
                # 去除尾部 \ 符号
                path = path.rstrip("\\")
                # 判断路径是否存在
                # 存在     True
                # 不存在   False
                isExists = os.path.exists(path)
                # 判断结果
                if not isExists:
                    # 如果不存在则创建目录
                    # 创建目录操作函数
                    os.makedirs(path)
                    return True
                else:
                    # 如果目录存在则不创建，并提示目录已存在
                    return False

            f = request.data
            s1 = str(f, encoding='utf-8')
            rdata = s1[-9:]
            rdata = rdata[1:]
            print(rdata)

            def getsavefilename():
                dy = str(datetime.datetime.now().year)
                dm = str(datetime.datetime.now().month)
                dd = str(datetime.datetime.now().day)
                if len(dm) == 1:
                    dm = '0' + dm
                if len(dd) == 1:
                    dd = '0' + dd
                dall = dy + dm + dd
                print(dall)
                uid = str(uuid.uuid4())
                suid = ''.join(uid.split('-'))
                suid = suid[:20]
                print(suid)
                res = "/" + dall + '/' + suid
                return res[:9], res[9:]

            dictfile, filename = getsavefilename()
            rawaudio = "static/uploads/courseKpoint/video/" + dictfile
            mkdir(rawaudio)

            print(request)
            f=request.data
            s1 = str(f, encoding='utf-8')
            rdata=s1[-9:]
            rdata=rdata[1:]
            fname= "static/uploads/temp/"+rdata
            videodata=rdata
            video = VideoFileClip(fname)
            audio = video.audio
            audiolocal = rawaudio + filename+".wav"
            audio.write_audiofile(audiolocal)
            audiolocal = "static/uploads/courseKpoint/video" + dictfile

            for root, dirs, files in os.walk(audiolocal):  # 遍历统计
                for each in files:
                    if each.endswith('wav'):
                        rdata = each
                        break
            print(rdata)
            audiolocal = "static/uploads/courseKpoint/video" + dictfile + "/" + rdata
            import multi_detect_BIC as bic
            bic.seg(audiolocal)
            path = 'save_audio'  # 获取当前路径
            countfile = 0
            for root, dirs, files in os.walk(path):  # 遍历统计
                for each in files:
                    if each.endswith('wav'):
                        countfile += 1  # 统计文件夹下文件个数

            return jsonify({"tips":fname})

@app.route('/allword',methods=['POST','GET'])
def allword():
    conn = sqlite3.connect('sqlitesave/videosave.db')
    cursor = conn.execute("SELECT ID ,TEXTS from videosall ")
    zidian = dict()
    for it in cursor:
        zidian[it[0]] = it[1]

    return jsonify(zidian)

@app.route('/voicetoword',methods=['POST','GET'])
def voicetoword():

    os.system("python iat_ws_python3.py %s" % (".\\save_audio\\"))#传输音——>文本位置
    conn = sqlite3.connect('sqlitesave/videosave.db')
    conn.execute("drop table videosall   ")
    conn.commit()
    c = conn.cursor()
    c.execute('''CREATE TABLE videosall
           (ID INT PRIMARY KEY     NOT NULL,
           PATH           TEXT    NOT NULL,
           TEXTS           TEXT    NOT NULL,
           FATHER            INT,
           videoduration    TEXT
                    );''')
    conn.commit()
    # c.execute('''alter table videosall add column videoduration TEXT;''')
    print("Table created successfully")
    import sqlitesave.sqlite3insert as ss
    ss.save_tovideoallmethod()
    conn = sqlite3.connect('sqlitesave/videosave.db')
    cursor = conn.execute("SELECT ID ,TEXTS from videosall ")
    zidian=dict()
    for it in cursor:
        zidian[it[0]]=it[1]

    return jsonify(zidian)

@app.route('/textsearch',methods=['POST','GET'])
def textsearch():
    global csz
    from urllib import parse
    conn = sqlite3.connect('sqlitesave/videosave.db')
    cursor = conn.execute("SELECT ID ,TEXTS from videosall ")
    zidian = dict()
    for it in cursor:
        zidian[it[0]] = it[1]

    searchdata=request.data
    s1 = str(searchdata,encoding="utf-8")
    ressearch=parse.unquote(s1[5:])

    print(ressearch)
    sedic=dict()
    for key,value in zidian.items():
        if ressearch in value:
            sedic[key]=(value,csz[key])
    return jsonify(sedic)

@app.route('/exchangetxt',methods=['POST','GET'])
def exchangetxt():
    global resid
    global times
    import os
    import demo_cli as dc

    res = dict()
    if request.method == "POST":
       rawdict = request.data
       s1 = str(rawdict, encoding="utf-8")
       resdic = parse.unquote(s1)
       id,data = resdic.split("&")

       resid=int(id[3:])
       resdata=data[5:]
       res[resid]=resdata
       voicepath=".\save_audio"+"\\"+str(resid+1)+".wav"
       vvoicepath=".\save_audio"+"\\"+str(resid)+".wav "
       print(resdata,voicepath)
       # dc.tts(resdata,voicepath)
       os.system("python zhrtvc-master\\zhrtvc\\demo_cli.py %s %s"%(resdata,voicepath))

       conn = sqlite3.connect('sqlitesave/videosave.db')
       sql='''UPDATE videosall SET TEXTS=?,father=father+1 
       where ID=?'''
       t=(vvoicepath,)
       cursor=conn.execute("SELECT videoduration  from videosall where PATH=?",t)
       restime=''
       for it in cursor:
           restime=it[0]
           print(restime)
       from ffmpeg import audio
       import getwavetime as gt
       after = gt.gettime(voicepath)
       front = str(restime[:-1])
       after = float(after[:-1])
       front = float(front)
       rat= after/front
       audio.a_speed(voicepath, rat, voicepath)

       cur=conn.cursor()
       cur.execute(sql,(resdata,resid))
       conn.commit()
       times=times+1
    return jsonify(res)

@app.route('/voicehebing',methods=['POST','GET'])
def voicehebing():
    pydub.AudioSegment.converter = "D:\\ffmpeg-N-100592-g42ee3898c8-win64-gpl-shared-vulkan\\bin\\ffmpeg.exe"
    mp3_path = 'save_audio/0.wav'
    music1 = AudioSegment.from_wav(mp3_path)
    path = 'save_audio'  # 获取当前路径
    count = 0
    for root, dirs, files in os.walk(path):  # 遍历统计
        for each in files:
            if each.endswith('wav'):
                count += 1  # 统计文件夹下文件个数
    print("文件的总数量为：", count)
    for i in range(count - 1):

        mp3_path = "./save_audio/" + str(i + 1) + ".wav"
        music2 = AudioSegment.from_wav(mp3_path)
        music1 += music2
        _music1_db = music1.dBFS
        _music2_db = music2.dBFS
        dbplus = _music1_db - _music2_db
        if dbplus < 0:
            music1 += abs(dbplus)
        elif dbplus > 0:
            music2 += abs(dbplus)
    music1.export('./mixfile/mix.wav', format='wav')
    return jsonify({"data":"音频合并成功"})

@app.route('/videovoicehe',methods=['POST','GET'])
def videovoicehe():
            global videodata
            rdata=videodata
            print(rdata+"fdfdf")
            # f=request.data
            # s1 = str(f, encoding='utf-8')
            # rdata=s1[-9:]
            # rdata=rdata[1:]
            # print(rdata,s1)
            old_video= "static/uploads/temp/"+rdata
            new_video = 'static/uploads/temp/new'+rdata
            video = VideoFileClip(old_video)
            video = video.without_audio()  # 删除声音，返回新的视频对象，原有对象不更改
            video.write_videofile(new_video)

            wawvpath = 'mixfile/mix.wav'
            final_video = "static/uploads/temp/final"+rdata

            video2 = VideoFileClip(new_video)
            audio_clip = AudioFileClip(wawvpath)
            video2 = video2.set_audio(audio_clip)
            video2.write_videofile(final_video)
            os.remove(new_video)
            return jsonify({"tips":final_video})

def return_img_stream(img_local_path):
  """
  工具函数:
  获取本地图片流
  :param img_local_path:文件单张图片的本地绝对路径
  :return: 图片流
  """
  import base64
  img_stream = ''
  with open(img_local_path, 'rb') as img_f:
    img_stream = img_f.read()
    img_stream = base64.b64encode(img_stream).decode()
  return img_stream

@app.route('/echarts',methods=['GET','POST'])
def echarts():

    conn = sqlite3.connect('sqlitesave/videosave.db')
    cursor = conn.execute("SELECT videoduration from videosall ")
    res=[]
    for it in cursor:
        res.append(it[0])
    print(res)
    img_path = 'word.png'
    img_stream = return_img_stream(img_path)
    return render_template("test_echarts.html",res=res,img_stream=img_stream)

@app.route('/correction',methods=['POST','GET'])
def correction():

    # import  correction_seq2seq as  cs
    import text as tt
    conn = sqlite3.connect('sqlitesave/videosave.db')
    cursor = conn.execute("SELECT ID, TEXTS from videosall ")

    listnum=[]
    # dict1=dict()
    for it in cursor:
        find1=str(tt.txt_correction(it[1]))
        print(find1+",")
        find2=[_   for _  in find1 if _ not in ['，','。','!','(',')','.','?']  ]
        find3=[_    for _  in it[1] if _ not in ['，','。','!','(',')','.','?']]
        if not operator.eq(find2,find3):
           num=int(it[0])
           listnum.append(num)
           # dict1[num]=''.join(find2)
    conn.close()
    conn = sqlite3.connect('sqlitesave/videosave.db')
    cursor = conn.execute("SELECT ID ,TEXTS from videosall ")
    zidian = dict()
    for it in cursor:
        zidian[it[0]] = it[1]
    for i in zidian:
        if i in listnum:
            zidian[i]=zidian[i]+'*'

    return jsonify(zidian)

@app.route('/bofang',methods=['POST','GET'])
def bofang():
    conn = sqlite3.connect('sqlitesave/videosave.db')
    cursor = conn.execute("SELECT ID, videoduration,PATH from videosall")
    f = request.data
    s1 = str(f, encoding='utf-8')
    num=int(s1[5:])
    num=str(num+1)
    gettime='音频时长为：'
    path=''
    for it in cursor:
        if num==str(it[0]):
            gettime+=it[1]
            path=it[2]
            print(path)

            print(gettime)

    return jsonify({0:gettime,1:path})

@app.route('/record',methods=['POST','GET'])
def record():
    return render_template("record.html")

@app.route('/luyintihuan',methods=['POST','GET'])
def luyintihuan():
    global times
    global locatetime
    res=dict()
    if request.method == "POST":
       rawdict = request.data
       s1 = str(rawdict, encoding="utf-8")
       print(s1)
       resdic = parse.unquote(s1)
       print(resdic)
       id, data = resdic.split("&")


       resid = int(id[3:])
       print(resid)
       conn=sqlite3.connect('sqlitesave/videosave.db')
       cursor= conn.execute("SELECT ID, videoduration  from videosall")
       duration=[]
       import sptime
       cst=''
       jst=''
       for it in cursor:
           if it[0]==resid:
               cst=sptime.spcstime(duration)
               duration.append(it[1])
               jst=sptime.spcstime(duration)
           duration.append(it[1])
       expart=cst+'/'+jst
       locatetime.append(expart)
       conn.close()   #初始帧算法

       resdata = data[17:]
       res[resid] = resdata
       voicepath = "./static/uploads/"+resdata#录音的mp3g格式
       voicepath2= "./static/uploads/temp/video/"+resdata[:-4]+".wav"#录音的wav格式
       dest=  ".\static\save_audio\\"+str(resid+1)+".wav"

       destsq=".\save_audio\\"+str(resid)+".wav "
       print(destsq)
       os.system("ffmpeg -i %s -acodec pcm_s16le -ac 2 -ar 44100 %s"%(voicepath,voicepath2))
       conn = sqlite3.connect('sqlitesave/videosave.db')
       t=(destsq,)
       cursor = conn.execute("SELECT videoduration  from videosall where PATH=?", t)
       restime = ''
       for it in cursor:
           restime = it[0]
           print(restime)
       from ffmpeg import audio
       import getwavetime as gt
       after = gt.gettime(voicepath)
       front = str(restime[:-1])
       after = float(after[:-1])
       front = float(front)
       print(front)
       rat = after / front
       resup = voicepath2[:-4] + str(rat) + voicepath2[-4:] #倍速以后的录音音频
       audio.a_speed(voicepath2, rat, resup)
       os.remove(destsq)
       print(resid)
       shutil.move(resup, ".\save_audio\\" + str(resid) + ".wav")
       print(res)
       times=times+1
       return jsonify({"录音替换":"ok"})






if __name__ == '__main__':
     # app.run(debug=True,port=8080)
     app.run(host = '0.0.0.0',debug=True)