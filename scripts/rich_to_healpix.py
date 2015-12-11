From glob import glob
import cst2hp
import healpy as hp
import pylab as pl

path = '/Users/jaguirre/PyModules/MyModules/herapy/beam/hera-cst/'
files = glob(path+'*.txt')

#files = files[0:1]

for file in files:
    print file
    root = file.split('/')[-1].split('.')[0]
    d = cst2hp.cst2hp(file,filetype='rich')
    print d['bm32'].min(), d['bm128'].min()
    hp.write_map(path+root+'_healpix.fits',d['bm128'])
    #hp.orthview(d['bm32'],rot=[0,90],half_sky=True,title=root)
    hp.orthview(d['bm128'],rot=[0,90],half_sky=True,title=root)
    hp.graticule(dpar=15)
    pl.savefig(path+root+'.png')
    #hp.orthview(d['hits'],rot=[0,90])

#pl.show()





