from neopixel import *
from threading import Thread 
import numpy as np
import config 
import color
import pyaudio
import time

# Visual effect flag
visual_flag = 1 

# Audio data updates per second
refresh_rate = 1.0 / 15.0

# NeoPixel Strip and PyAudio object and stream
strip = config.get_strip()
p_s = config.get_pyaudio_and_stream()
p = p_s[0]
stream = p_s[1]

def clear_strip():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def volume_unit_meter(*colors):
    clear_strip()
    color_map = color.get_color_map(strip.numPixels(), list(colors))

    prev_num_bars = 0
    while visual_flag == 1: 
        cur_data = np.fromstring(config.data, np.int16)
        peak = np.average(np.abs(cur_data) / 2)
        num_bars = int(300 * peak / 2**16)
        if num_bars <= prev_num_bars:
            for i in range(prev_num_bars - 1, num_bars - 1, -1):
                strip.setPixelColor(i, Color(0, 0, 0))
                strip.show()
                time.sleep(refresh_rate / (prev_num_bars - num_bars))
        else:
            for i in range(prev_num_bars, num_bars):
                strip.setPixelColor(i, color_map[i])
                strip.show()
                time.sleep(refresh_rate / (num_bars - prev_num_bars))
        prev_num_bars = num_bars

def volume_unit_scroll(*colors):
    clear_strip()
    color_map = ([Color(0, 0, 0)] * len(colors)) + color.get_color_map(len(colors) * 10, list(colors))
    strip_pixels = np.zeros((strip.numPixels(),), dtype=int)

    while visual_flag == 2: 
        cur_data = np.fromstring(config.data, np.int16)
        peak = np.average(np.abs(cur_data) / 2)
        for i in range(strip.numPixels() - 1, 0, -1):
            strip_pixels[i] = strip_pixels[i - 1]
            strip.setPixelColor(i, strip_pixels[i])
        strip_pixels[0] = color_map[int(np.interp(peak, [0, 13000], [0, len(color_map)]))]
        strip.setPixelColor(0, strip_pixels[0])
        strip.show()
        time.sleep(refresh_rate / 10)

def volume_unit_spectrum(*colors):
    clear_strip()
    color_map = color.get_color_map(len(colors) * 10, list(colors))

    while visual_flag == 3:
        cur_data = np.fromstring(config.data, np.int16)
        peak = np.average(np.abs(cur_data) / 2)
        cur_color = color_map[int(np.interp(peak, [0, 13000], [0, len(color_map)]))]
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, cur_color)
        strip.show()
        time.sleep(refresh_rate)

def visual_handler():
    time.sleep(0.1)
    while visual_flag != 0:
        if visual_flag == 1:
            volume_unit_meter(Color(255, 0, 0), Color(255, 255, 0))
        elif visual_flag == 2:
            volume_unit_scroll(Color(255, 0, 0), Color(255, 255, 0))
        elif visual_flag == 3:
            volume_unit_spectrum(Color(255, 0, 0), Color(255, 255, 0))
    clear_strip()

if __name__ == '__main__':
    strip.begin()
    stream.start_stream()

    visual_thread = Thread(target=visual_handler)
    visual_thread.start()
    try:
        while True:
            x = raw_input("Change visual: ")
            if x == "meter":
                visual_flag = 1 
            elif x == "scroll":
                visual_flag = 2
            elif x == "spectrum":
                visual_flag = 3
            else:
                print("No visual " + x)

    except KeyboardInterrupt:
        visual_flag = 0
        visual_thread.join()

        stream.stop_stream()
        stream.close()
        p.terminate()
        clear_strip()
