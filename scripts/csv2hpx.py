#! /usr/bin/env python
'''Reads in CSV beam files, with format:
Theta [deg], dB(GainTotal) [] - Freq='0.1GHz' Phi='0deg', dB(GainTotal) [] - Freq='0.1GHz' Phi='1deg', ...'''

import numpy as np, aipy as ap
import csv, sys, re

re_gain = re.compile(r"dB\(GainTotal\) \[\] - Freq='([\d.]+)GHz' Phi='([\d.]+)deg'")

for f in sys.argv[1:]:
    outfile = f[:-len('.csv')]+'.hmap'
    print 'Converting', f, '->', outfile
    with open(f) as csvfile:
        csvread = csv.reader(csvfile)
        header = csvread.next()
        fqs,phi = np.array([map(float,re_gain.match(h).groups()) for h in header[1:]]).T
        phi.shape = (1,-1)
    d = np.loadtxt(f,delimiter=',',skiprows=1)
    th,dBi = d[:,:1], d[:,1:]
    th,phi = th * np.ones_like(phi) * ap.const.deg, phi * np.ones_like(th) * ap.const.deg
    g = 10**(dBi/10.)
    h = ap.map.Map(nside=32)
    th,phi,g = th.flatten(), phi.flatten(), g.flatten()
    th,phi = np.abs(th), np.where(th < 0, phi + np.pi, phi)
    h.add((th,phi), np.ones_like(g), g)
    h.reset_wgt()
    h = h.map
    h.to_fits(outfile, clobber=True)
