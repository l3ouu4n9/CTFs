import requests
from base64 import b64encode, b64decode
import json
import uuid
import re
import math
import wave
import struct
import math
import time


#slightly modified version of https://github.com/hfeeki/dtmf/blob/master/dtmf-decoder.py
class pygoertzel_dtmf:
    def __init__(self, samplerate):
        self.samplerate = samplerate
        self.goertzel_freq = [1209.0,1336.0,1477.0,1633.0,697.0,770.0,852.0,941.0]
        self.s_prev = {}
        self.s_prev2 = {}
        self.totalpower = {}
        self.N = {}
        self.coeff = {}
        # create goertzel parameters for each frequency so that
        # all the frequencies are analyzed in parallel
        for k in self.goertzel_freq:
            self.s_prev[k] = 0.0
            self.s_prev2[k] = 0.0
            self.totalpower[k] = 0.0
            self.N[k] = 0.0
            normalizedfreq = k / self.samplerate
            self.coeff[k] = 2.0*math.cos(2.0 * math.pi * normalizedfreq)
    def __get_number(self, freqs):
        hi = [1209.0,1336.0,1477.0,1633.0]
        lo = [697.0,770.0,852.0,941.0]
        # get hi freq
        hifreq = 0.0
        hifreq_v = 0.0
        for f in hi:
            if freqs[f]>hifreq_v:
                hifreq_v = freqs[f]
                hifreq = f
        # get lo freq
        lofreq = 0.0
        lofreq_v = 0.0
        for f in lo:
            if freqs[f]>lofreq_v:
                lofreq_v = freqs[f]
                lofreq = f
        if lofreq==697.0:
            if hifreq==1209.0:
                return "1"
            elif hifreq==1336.0:
                return "2"
            elif hifreq==1477.0:
                return "3"
            elif hifreq==1633.0:
                return "A"
        elif lofreq==770.0:
            if hifreq==1209.0:
                return "4"
            elif hifreq==1336.0:
                return "5"
            elif hifreq==1477.0:
                return "6"
            elif hifreq==1633.0:
                return "B"
        elif lofreq==852.0:
            if hifreq==1209.0:
                return "7"
            elif hifreq==1336.0:
                return "8"
            elif hifreq==1477.0:
                return "9"
            elif hifreq==1633.0:
                return "C"
        elif lofreq==941.0:
            if hifreq==1209.0:
                return "*"
            elif hifreq==1336.0:
                return "0"
            elif hifreq==1477.0:
                return "#"
            elif hifreq==1633.0:
                return "D"
    def run(self, sample):
        freqs = {}
        for freq in self.goertzel_freq:
            s = sample + (self.coeff[freq] * self.s_prev[freq]) - self.s_prev2[freq]
            self.s_prev2[freq] = self.s_prev[freq]
            self.s_prev[freq] = s
            self.N[freq]+=1
            power = (self.s_prev2[freq]*self.s_prev2[freq]) + (self.s_prev[freq]*self.s_prev[freq]) - (self.coeff[freq]*self.s_prev[freq]*self.s_prev2[freq])
            self.totalpower[freq]+=sample*sample
            if (self.totalpower[freq] == 0):
                self.totalpower[freq] = 1
            freqs[freq] = power / self.totalpower[freq] / self.N[freq]
        return self.__get_number(freqs)



def goertzelify(args):
    (i, framerate, left, binsize) = args
    goertzel = pygoertzel_dtmf(framerate)
    for j in left[i:i+binsize]:
        value = goertzel.run(j)
    return value
