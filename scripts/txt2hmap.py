#! /usr/bin/env python
import aipy as a, numpy as n, sys

for txt in sys.argv[1:]:
    outfile = txt[:-len('.txt')] + '.hmap'
    print txt, '->', outfile
    mdl = n.recfromtxt(txt, skip_header=2, usecols=[0,1,2])
    th = mdl[:,0] * a.const.deg
    ph = mdl[:,1] * a.const.deg
    dBi = mdl[:,2]
    pwr = 10**(dBi/10.)
    bm = a.map.Map(nside=32, interp=True)
    bm.add((th,ph), 1, pwr/n.max(pwr))
    bm.to_fits(outfile, clobber=True)
