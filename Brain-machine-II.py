#!/usr/bin/env python

import pygame
from pygame.locals import *
import math
import numpy
license = 'GPLv3'
authors ='Marco Garcia Baturan, Reset Reboot'
date = '2017/09/13/Wednesday'
doc_license ='/Brain_machine_II/gpl-3.0.txt'
"""Brain Machine II in Python:Program who emulate a Brain machine, a device who induce alpha waves in the brain.
Based in Dream Machine developed by Brion Gysin and Ian Sommerville who reads the book:'The Living Brain' of Walter Gray.
Use a code (thank you Reset) for sinusoidal sound with binaural beat of 10 Hz of perception and endless
loop of switching the background screen between black and withe color by 10 Hz/s.
Please, read carefully with critical thinking the article: https://en.wikipedia.org/wiki/Mind_machine"""

if __name__ == "__main__":     # Windows compatibility
    size = (800, 600)  # size screen
    bits = 16
    black = (0, 0, 0)  # define background color
    white = (255, 255, 255)
    # This will keep the sound playing forever, the quit event handling allows the pygame window to close without crashing
    _running = True
    flapper = False  # keep the background do flip flop

    # the number of channels specified here is NOT
    # the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels
    pygame.mixer.pre_init(44100, -bits, 2)
    pygame.init()
    # Added fullscreen so the display works without borders
    _display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)  # display the screen
    pygame.display.set_caption("Brain Machine II in Python")  # Title of window and program

    duration = 1.0  # in seconds
    # frequency for the left speaker
    frequency_l = 440
    # frequency for the right speaker
    frequency_r = 450  # 550

    # this sounds totally different coming out of a laptop versus coming out of headphones
    sample_rate = 44100

    n_samples = int(round(duration * sample_rate))

    # setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
    buf = numpy.zeros((n_samples, 2), dtype=numpy.int16)
    max_sample = 2 ** (bits - 1) - 1

    for s in range(n_samples):
        t = float(s) / sample_rate  # time in seconds
        # grab the x-coordinate of the sine wave at a given time, while constraining the sample to what our mixer is set to with "bits"
        buf[s][0] = int(round(max_sample * math.sin(2 * math.pi * frequency_l * t)))  # left
        buf[s][1] = int(round(max_sample * 0.5 * math.sin(2 * math.pi * frequency_r * t)))  # right

    sound = pygame.sndarray.make_sound(buf)
    # play once, then loop forever
    sound.play(loops=-1)
    # play relaxing scientific meditation music
    pygame.mixer.music.load("Marconi Union - Weightless.mp3")
    pygame.mixer.music.play(-1)
    # refresh control of screen
    reloj = pygame.time.Clock()

    while _running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _running = False

            elif event.type == pygame.KEYUP:
                # If the user presses ESC key, the program ends
                if event.key == pygame.K_ESCAPE:
                    _running = False

        if not flapper:
            _display_surf.fill(black)
        else:
            _display_surf.fill(white)
        flapper = not flapper
        pygame.display.flip()
        reloj.tick(10)

    pygame.quit()
