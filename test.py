# # from moviepy.video.io.VideoFileClip import VideoFileClip
# #
# # receive = "mp4/jhgs.mp4"
# # video = VideoFileClip(receive)
# # audio = video.audio
# #
# # audio.write_audiofile("saveaudio/集合概述.wav")
# # audiolocal = "saveaudio/" + receive[-8:-4] + ".mp4"
# # print(audiolocal)
# # import os
# # os.system("python zhrtvc-master\\zhrtvc\\demo_cli.py")
#
# # from moviepy.editor import *
# #
# # old_video = 'static/uploads/temp/jhgs.mp4'
# # new_video = 'static/uploads/temp/jhgsnew.mp4'
# #
# # video = VideoFileClip(old_video)
# # video = video.without_audio()  # 删除声音，返回新的视频对象，原有对象不更改
# # video.write_videofile(new_video)
# #
# # wawvpath = 'mixfile/mix.wav'
# # final_video="static/uploads/temp/jhgsnew.mp4"
# #
# # video = VideoFileClip(new_video)
# # audio_clip = AudioFileClip(wawvpath)
# # video = video.set_audio(audio_clip)
# # video.write_videofile(final_video)
# # import sqlite3
# #
# # voicepath=r".\save_audio"+"\\"+str(12)+".wav"
# # vvoicepath=".\save_audio"+"\\"+str(11)+".wav "
# # t=(vvoicepath,)
# # conn = sqlite3.connect('sqlitesave/videosave.db')
# # cursor=conn.execute("SELECT videoduration  from videosall where PATH=?",t)
# # restime=''
# # for it  in cursor:
# #     restime=it[0]
# #     print(restime)
# #
# # from ffmpeg import audio
# # import getwavetime as gt
# # after = gt.gettime(voicepath)
# #
# # front =str(restime[:-1])
# # after=float(after[:-1])
# # front=float(front)
# #
# # rat= after/front
# # audio.a_speed(voicepath, rat, "save_audio/2x.wav")
# import pyaudio
# from pydub import AudioSegment
# voicepath = "./static/uploads/temp/video/e0339bc7-8f95-409a-a26f-9db70ac0d1e6.mp3"
# dest="./static/uploads/temp/video/audio.wav"
# # sound = AudioSegment.from_mp3(voicepath)
# # sound.export(dest, format='wav')
# import os
# os.system("ffmpeg -i ./static/uploads/temp/video/e0339bc7-8f95-409a-a26f-9db70ac0d1e6.mp3 -acodec pcm_s16le -ac 2 -ar 44100 ./static/uploads/temp/video/audio.wav")
import cv2

video = cv2.VideoCapture("./static/uploads/temp/jhgs.mp4")

# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

if int(major_ver) < 3:
    fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
else:
    fps = video.get(cv2.CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

video.release()