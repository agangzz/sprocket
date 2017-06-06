#! /usr/local/bin/python
# -*- coding: utf-8 -*-
#
# init_spkr.py
#   First ver.: 2017-06-05
#
#   Copyright 2017
#       Kazuhiro KOBAYASHI <kobayashi.kazuhiro@g.sp.m.is.nagoya-u.ac.jp>
#
#   Distributed under terms of the MIT license.
#

"""
create speaker-dependent configure file (spkr.yml)

"""

import os
import argparse
import numpy as np
import glob
from scipy.io import wavfile
from multiprocessing import Pool
import matplotlib.pyplot as plt

from vctk.backend import WORLD


def world_f0_analysis(flbl):
    # read .wav file
    fs, x = wavfile.read(flbl)
    x = np.array(x, dtype=np.float)

    # feature extraction for min and max f0 range definition
    world = WORLD(period=5.0, fs=fs, f0_floor=40.0, f0_ceil=700.0)
    speechparameter = world.analyze_f0(x)
    return speechparameter.f0


def create_f0_histgram(f0s, histfile):
    # flatten two dimensional list into one dimensional list
    f0 = [f0val for i in f0s for f0val in i]

    # plot histgram
    plt.hist(f0, bins=200, range=(40, 700), normed=True, histtype="stepfilled")
    plt.xlabel("Fundamental frequency")
    plt.ylabel("Probability")
    plt.savefig(histfile)


def main():
    # Options for python
    description = 'create speaker-dependent configure file (spkr.yml)'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-m', '--multicore', type=int, default=1,
                        help='# of cores for multi-processing')
    parser.add_argument('spkr', type=str,
                        help='input speaker label')
    parser.add_argument('wav_dir', type=str,
                        help='wav file directory of the speaker')
    parser.add_argument('conf_dir', type=str,
                        help='configure directory of the speaker')
    args = parser.parse_args()

    # grab .wav files in data directory
    files = glob.glob(args.wav_dir + '/' + args.spkr + '/*.wav')

    # F0 extraction with WORLD.dio on multi processing
    p = Pool(args.multicore)
    f0s = p.map(world_f0_analysis, files)

    # create F0 histgram
    hist_dir = args.conf_dir + '/f0histgram/'
    if not os.path.exists(hist_dir):
        os.makedirs(hist_dir)
    histfile = hist_dir + args.spkr + '.pdf'
    create_f0_histgram(f0s, histfile)

if __name__ == '__main__':
    main()