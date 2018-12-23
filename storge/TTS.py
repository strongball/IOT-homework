# coding=UTF-8
from gtts import gTTS
import os

filename = "tmp.mp3"
aud = gTTS(text="你他媽的是智障嗎", lang="zh-tw")
aud.save(filename)
os.system("mpg321 "+filename)