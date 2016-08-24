#! /usr/bin/env python
'''Reads in CSV beam files, with format:
Theta [deg], dB(GainTotal) [] - Freq='0.1GHz' Phi='0deg', dB(GainTotal) [] - Freq='0.1GHz' Phi='1deg', ...'''

import numpy as np
import csv, sys, re, os, os.path

pwd = os.getcwd()
sys.path.append('/Users/ddeboer/Documents/ubase/Code/aipy')
inpath = os.path.join(os.path.split(pwd)[0],'GP4Y2H_4900/')
outpath= os.path.join(os.path.split(pwd)[0],'HP4Y2H_4900/')
print inpath
print outpath
import aipy as ap

re_gain = re.compile(r"dB\(Gain[X,Y]\) \[\] - Freq='([\d.]+)GHz' Phi='([\d.]+)deg'")
re_phas = re.compile(r"ang_deg\(rE[X,Y]\) \[deg\] - Freq='([\d.]+)GHz' Phi='([\d.]+)deg'")

def __splitMagPhaseFilesFromString(s):
    """Splits file mag/phase pairs from string as mag0:phase0,mag1:phase1,..."""
    magfile = []
    phafile = []
    data = s.split(',')
    for d in data:
        f = d.split(':')
        magfile.append(f[0])
        phafile.append(f[1])
    return magfile,phafile
def __procfile(s):
    """So you can use mag:phase pairs from a file"""
    fp = open(s,'r')
    magfile = []
    phafile = []
    for line in fp:
        m,p=__splitMagPhaseFilesFromString(line.strip())
        magfile.append(m[0])
        phafile.append(p[0])
    fp.close()
    return magfile,phafile

###Processes command line.  
###   Can be mag0:phase0,mag1:phase1,...  or mag0:phase0 mag1:phase1 ...
###   If first character is '-', it assumes that is a filename containing mag:phase pairs on subsequent lines
for f in sys.argv[1:]:
    if f[0]=='-':
        fn = f[1:]
        mag,phase=__procfile(fn)
    else:
        mag,phase=__splitMagPhaseFilesFromString(f)
    for i,mmfile in enumerate(mag):
        mfile = os.path.join(inpath,mmfile)
        outfile = os.path.join(outpath,mmfile[:-len('.csv')]+'.hmap')
        pfile = os.path.join(inpath,phase[i])
        print 'Converting', mfile, '->', outfile
        with open(mfile) as mcsvfile:
            with open(pfile) as pcsvfile:
                pcsvread = csv.reader(pcsvfile)
                mcsvread = csv.reader(mcsvfile)
                header_m = mcsvread.next()
                header_p = pcsvread.next()
                fqs,phi    =np.array([map(float,re_gain.match(h).groups()) for h in header_m[1:]]).T
                ###Do phase just to make sure they agree
                fqs_p,phi_p=np.array([map(float,re_phas.match(h).groups()) for h in header_p[1:]]).T
                phi.shape = (1,-1)
        dm = np.loadtxt(mfile,delimiter=',',skiprows=1)
        th,dBi = dm[:,:1], dm[:,1:]
        th,phi = th * np.ones_like(phi) * ap.const.deg, phi * np.ones_like(th) * ap.const.deg
        pm = np.loadtxt(pfile,delimiter=',',skiprows=1)
        prad = pm[:,1:]*ap.const.deg
        ggg = 10**(dBi/20.)
        g = ggg*np.cos(prad) + 1j*ggg*np.sin(prad)
        h = ap.map.Map(nside=32,dtype=np.complex128)
        th,phi,g = th.flatten(), phi.flatten(), g.flatten()
        th,phi = np.abs(th), np.where(th < 0, phi + np.pi, phi)
        h.add((th,phi), np.ones_like(g), g)
        h.reset_wgt()
        h = h.map
        h.to_fits(outfile, clobber=True)
