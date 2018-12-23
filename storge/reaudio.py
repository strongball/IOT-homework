import audioop
import pyaudio
import numpy as np
chunk = 1024

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=chunk)

while True:
    data = stream.read(chunk)
    # # check level against threshold, you'll have to write getLevel()
    # if getLevel(data) > THRESHOLD:
    #     break
    rms = audioop.rms(data, 2)
    decibel = 20 * np.log10(rms)
    print(decibel)
    # print(max(data))
if __name__