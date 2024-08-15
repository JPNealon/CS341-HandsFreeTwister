import random
from gtts import gTTS
from time import sleep
from pygame import mixer
import pvporcupine
from pvrecorder import PvRecorder
from sense_hat import SenseHat

sns = SenseHat()

def audio_detection():
    porcupine = pvporcupine.create(
        access_key='K9TMWltm8F/ePLVUN+m83XmxBPSPWGLSUWbVxG+Bih1ETIm8mRM17A==',
        keyword_paths=[
            './Next-Spin_en_raspberry-pi_v2_1_0/Next-Spin_en_raspberry-pi_v2_1_0.ppn',
            './Two-Players_en_raspberry-pi_v2_1_0/Two-Players_en_raspberry-pi_v2_1_0.ppn']
    )
    # -1 is the default input audio device.
    recorder = PvRecorder(device_index=-1, frame_length=512)
    try:
        recorder.start()
        while True:
            pcm = recorder.read()
            keyword_index = porcupine.process(pcm)
            if keyword_index == 0: # detects "next spin"
                return True # next command
            if keyword_index == 1: # detects "two players"
                return False # two players
    except KeyboardInterrupt:
        recorder.stop()
    finally:
        recorder.delete()
        porcupine.delete()

def twister_command(command, color): # SenseHat Display Commands
    if(color == 'red'):
        x = (255,0,0)
    elif(color == 'green'):
        x = (0,255,0)
    elif(color == 'blue'):
        x = (0,0,255)
    elif(color == 'yellow'):
        x = (255,255,0)

    b = (1, 1, 1) #Black

    left_hand = [
        x, x, x, x, x, x, x, x,
        x, b, x, x, x, b, x, b,
        x, b, x, x, x, b, x, b,
        x, b, x, x, x, b, b, b,
        x, b, x, x, x, b, x, b,
        x, b, x, x, x, b, x, b,
        x, b, b, b, x, b, x, b,
        x, x, x, x, x, x, x, x,
    ]

    left_foot = [
        x, x, x, x, x, x, x, x,
        x, b, x, x, x, b, b, b,
        x, b, x, x, x, b, x, x,
        x, b, x, x, x, b, b, x,
        x, b, x, x, x, b, x, x,
        x, b, x, x, x, b, x, x,
        x, b, b, b, x, b, x, x,
        x, x, x, x, x, x, x, x,
    ]

    right_hand = [
        x, x, x, x, x, x, x, x,
        x, b, b, b, x, b, x, b,
        x, b, x, b, x, b, x, b,
        x, b, b, x, x, b, b, b,
        x, b, x, b, x, b, x, b,
        x, b, x, b, x, b, x, b,
        x, b, x, b, x, b, x, b,
        x, x, x, x, x, x, x, x,
    ]

    right_foot = [
        x, x, x, x, x, x, x, x,
        x, b, b, b, x, b, b, b,
        x, b, x, b, x, b, x, x,
        x, b, b, x, x, b, b, x,
        x, b, x, b, x, b, x, x,
        x, b, x, b, x, b, x, x,
        x, b, x, b, x, b, x, x,
        x, x, x, x, x, x, x, x,
    ]

    if(command == 'left_foot'):
        sns.set_pixels(left_foot)
    elif(command == 'right_foot'):
        sns.set_pixels(right_foot)
    elif(command == 'right_hand'):
        sns.set_pixels(right_hand)
    elif(command == 'left_hand'):
        sns.set_pixels(left_hand)
           
def AudioOutput(output):
    #gTTS Creation of Output
    tts = gTTS(output)
    tts.save('./hello.mp3')
    #pygame Audio Output (using mixer)
    mixer.init()
    mixer.music.load("./hello.mp3")
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        sleep(1)
    mixer.quit()

def run(): # main/driver
    color_count = {'Red': 0, 'Blue': 0, 'Green': 0, 'Yellow': 0} # number of body parts on each color
    body_on = {'Left Hand': '', 'Right Hand': '',
                'Left Foot': '', 'Right Foot': ''} # what color each body part is on
    x = True # loops while true
    y = 2 # number of body parts allowed on each color

    while x:
        part = random.choice(list(body_on.keys()))
        color = random.choice(list(color_count.keys()))

        if body_on[part] == color: # if body part already on color, respin
            continue
        if color_count[color] == y: # if color is full, respin
            continue

        output = part + ' ' + color
        twister_command(part.replace(' ', '_').lower(), color.lower()) # update SenseHat display
        print(output) # console out
        AudioOutput(output) # audio out

        # update dicts
        if body_on[part] in color_count.keys():
            color_count[body_on[part]] -= 1
        body_on[part] = color
        color_count[body_on[part]] += 1

        x = audio_detection() # listen for next command

        if (not x) and (y == 2): # update players if "two players" detected
            y = 3
            sns.show_message("TWO PLAYERS")
        x = True

if __name__ == '__main__':
    run()
