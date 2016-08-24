# hera-cst
CST files containing beam patterns of HERA dish (swept parabola, modified PAPER feed)

FITS files are HEALpix, nside=128, ring ordering.  
The beam is pointed at (theta=0,phi=0) in the usual HEALpix spherical coordinate system (corresponding to the north pole).
The freuqency and orientation of the dipole are given in the file name.

The png files are orthographic projections of just the response in the forward hemisphere (theta < 90 degrees).


2016 August 23:
This folder is mis-named in that the data are mostly (only?) from HFSS.  4Y2H_4900 refers to the feed used (172/36/36cm with gap) rigged at 4900mm.  GX contains co-linear-polar gain in dBi and PX the phase in deg for rE.  GY/PY are the cross-pol
Directory GP4Y2H_4900 has the csv files and HP4Y2H_4900 has the hmap files.

