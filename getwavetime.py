import  os
import re

# def get_file_duration(path):
#     """
#     获取单个wav文件时长
#     :param path: 文件路径
#     :return:
#     """
#     popen = os.popen('sox {file_path} -n stat 2>&1'.format(file_path=path))
#     content = popen.read()
#     li = re.findall('Length \(seconds\):(.*?)Scaled by:', content, re.DOTALL)
#     try:
#         wav_len_str = li[0].strip()
#     except Exception:
#         wav_len_str = popen.readlines()[1].split()[-1]
#     wav_len = float(wav_len_str)
#     popen.close()
#     return wav_len
import contextlib
import wave
import sqlite3
def gettime(WAVE_OUTPUT_FILENAME):
    with contextlib.closing(wave.open(WAVE_OUTPUT_FILENAME, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        wav_length = frames / float(rate)
        wavetime=str(wav_length)+"秒"

        return wavetime
def find():
    import os
    res=[]
    base_path = 'save_audio'
    files = os.listdir(base_path)
    files.sort(key=lambda x: int(x.split('.')[0]))
    for path in files:
        full_path = os.path.join(base_path, path)
        res.append(gettime(full_path))
    return res
res=find()
# print(gettime("save_audio/13.wav"))








