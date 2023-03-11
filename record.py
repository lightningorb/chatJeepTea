import time
import os
import pyaudio
import wave
import math
import struct
import logging


def record():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    WAVE_OUTPUT_FILENAME = "output.wav"
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    frames, min_vol, max_vol, started_talking = [], 1e6, 0, 0
    while True:
        data = stream.read(CHUNK)
        signal = struct.unpack(f"<{CHUNK}h", data)
        rms = math.sqrt(sum([(s**2) for s in signal]) / CHUNK)
        min_vol, max_vol = min(rms, min_vol), max(rms, max_vol)
        diff = rms - min_vol
        delta = 3_000
        if diff > delta:
            started_talking = time.time()
            print(f"STARTED TALKING AT: {started_talking}")
        if started_talking:
            frames.append(data)
            print(diff < delta, time.time() - started_talking > 3)
            if diff < delta and time.time() - started_talking > 3:
                print("SILENCE")
                break
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()
    os.system("rm -f output.mp3")
    os.system(f"ffmpeg -i output.wav -vn -ar 44100 -ac 2 -ab 192k -f mp3 output.mp3")
    return "output.mp3"
