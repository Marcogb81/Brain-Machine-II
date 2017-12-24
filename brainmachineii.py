#!/usr/bin/env python 2.7

from os.path import dirname, join, realpath
import pygame
from pygame.locals import *
import math
import numpy
from Tkinter import *


license = 'GPLv3'
authors = 'Marco Garcia Baturan, Reset Reboot, remoteObserver '
date = '2017/09/13/Wednesday'
doc_license = '/Brain_machine_II/gpl-3.0.txt'
"""Brain Machine II in Python:Program who emulate a Brain machine, a device who induce alpha waves in the brain.
Based in Dream Machine developed by Brion Gysin and Ian Sommerville who reads the book:'The Living Brain' of Walter Gray.
Use a code (thank you Reset) for sinusoidal sound with binaural beat of 10 Hz of perception and endless
loop of switching the background screen between black and withe color by 10 Hz/s.
Please, read carefully with critical thinking the article: https://en.wikipedia.org/wiki/Mind_machine"""

if __name__ == "__main__":  # Windows compatibilityclass bmii():
    class Application(Frame):

        # binaural and strobo
        def brainmachine(running =True):
            size = (800, 600)  # size screen
            bits = 16
            black = (0, 0, 0)  # define background color
            white = (255, 255, 255)
            # This will keep the sound playing forever, the quit event handling allows the pygame window to close without crashing
            _running = running
            flapper = False  # keep the background do flip flop

            # the number of channels specified here is NOT
            # the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels
            pygame.mixer.pre_init(44100, -bits, 2)
            pygame.init()
            # Added fullscreen so the display works without borders
            _display_surf = pygame.display.set_mode(size,
                                                    pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)  # display the screen
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
            pygame.mixer.music.load(join(realpath(dirname(__file__)),
                                         "Marconi Union - Weightless.mp3"))
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

        # create widget
        def createWidgets(self):
            """"Create widget who manage the core script"""
            # create label
            self.LABEL = Label(self)
            self.LABEL["text"]= """Please, use the program wiht close eyes\nand earphones in a dark room.\nand not test in people with epileptic\nsindrome. For shut out the programm\njust click Escape button"""
            self.LABEL.pack({"side": "top"})
            # button for quit program
            self.QUIT = Button(self)
            self.QUIT["text"] = "QUIT"
            self.QUIT["fg"] = "red"
            self.QUIT["command"] = self.quit
            self.QUIT.pack({"side": "left"})
            # button wihc start core script
            self.hi_there = Button(self)
            self.hi_there["text"] = "Start Brain Machine II",
            self.hi_there["command"] = self.brainmachine

            self.hi_there.pack({"side": "left"})

        # call all
        def __init__(self, master=None):
            Frame.__init__(self, master)
            self.pack()
            self.createWidgets()

# start all
root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
