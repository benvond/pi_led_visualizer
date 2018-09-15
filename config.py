from neopixel import *
import pyaudio

# LED strip configuration:
LED_COUNT   = 60                     # Number of LED pixels.
LED_PIN     = 18                     # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000                 # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 10                     # DMA channel to use for generating signal (try 10)
LED_BRIGHT  = 15                     # Set to 0 for darkest and 255 for brightest
LED_INVERT  = False                  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0                      # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_TYPE    = ws.WS2811_STRIP_GRB    # LED strip type (rgb, grb, gbr, rgbw)

# Audio configuration:
WIDTH = 2
FORMAT = 8 
CHANNELS = 1
RATE = 44100

# Global variable of current audio data
data = ' ' * 4096

def pyaudio_callback(in_data, frame_count, time_info, status):
    """
    Callback function for the PyAudio stream. Used to grab the current
    audio data from the input device and simultaneously play it back
    to the output device.

    Args:
        in_data:      Recorded data if input=True; else None
        frame_count:  Number of frames
        time_info:    Dictionary
        status_flags: PaCallbackFlags

    Returns:
        out_data
        flag
    """
    global data
    data = str(in_data)
    return (in_data, pyaudio.paContinue)

def get_pyaudio_and_stream():
    """
    Creates both a PyAudio object as well as the audio stream
    using the audio configuration above.

    Returns:
        p:      The PyAudio object
        stream: The PyAudio stream
    """
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=True,
        stream_callback=pyaudio_callback
    )
    return (p, stream)


def get_strip():
    """
    Creates an Adafruit Neopixel LED strip object using the
    strip configuration provided above.

    Returns:
        strip: The LED strip object
    """
    strip = Adafruit_NeoPixel(
        LED_COUNT, 
        LED_PIN, 
        LED_FREQ_HZ, 
        LED_DMA, 
        LED_INVERT, 
        LED_BRIGHT, 
        LED_CHANNEL,
        LED_TYPE
    )
    return strip
