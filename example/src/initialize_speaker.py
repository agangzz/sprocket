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
Generate F0 histgram

"""

import argparse
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import os
from os.path import exists, dirname
from sprocket.feature import FeatureExtractor


def create_f0_histgram(f0s, histgramf):
    # plot histgram
    plt.hist(f0s, bins=200, range=(40, 700), normed=True, histtype="stepfilled")
    plt.xlabel("Fundamental frequency")
    plt.ylabel("Probability")

    dst_dir = dirname(histgramf)
    if not exists(dst_dir):
        os.makedirs(dst_dir)

    plt.savefig(histgramf)


def main():
    # Options for python
    dcp = 'create speaker-dependent configure file (speaker.yml)'
    parser = argparse.ArgumentParser(description=dcp)
    parser.add_argument('speaker', type=str,
                        help='Input speaker label')
    parser.add_argument('list_file', type=str,
                        help='List file of the input speaker')
    parser.add_argument('wav_dir', type=str,
                        help='Wav file directory of the speaker')
    parser.add_argument('histgramf', type=str,
                        help='Output histgram file')
    args = parser.parse_args()

    # open list file
    with open(args.list_file, 'r') as fp:
        files = fp.readlines()

    f0s = []
    for f in files:
        # open waveform
        f = f.rstrip()
        wavf = args.wav_dir + '/' + f + '.wav'
        fs, x = wavfile.read(wavf)
        x = np.array(x, dtype=np.float)
        print("Processing: " + wavf)

        # constract AcousticFeature clas
        feat = FeatureExtractor(
            x,
            analyzer='world',
            fs=fs,
        )
        feat.analyze()

        # f0 extraction
        f0s.append(feat.f0())

    # create figure to visualize F0 range of the speaker
    create_f0_histgram(np.hstack(f0s).flatten(), args.histgramf)


if __name__ == '__main__':
    main()