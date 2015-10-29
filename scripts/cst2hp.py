import numpy as np
import healpy as hp
import pylab as pl


def cst2hp(cstfile,filetype='eloy',column=2):
# It's annoying that the file types are difficul enough to parse that
# I really need completely different sets of parameters

    if filetype == 'eloy':
        #print 'Eloy'
        skiprows = 3

    if filetype == 'rich':
        #print 'Rich'
        skiprows = 2
        
    # Read in the text file
    data = np.loadtxt(cstfile,skiprows=skiprows)
    # Pretty much theta and phi in physics spherical coordinates
    thetad = data[:,0]
    phid = data[:,1]

    if filetype=='eloy':
        
        # Eloy's coordinates are really hard to parse in the language of
        # spherical coordinates.  Basically, the first column IS theta, but it
        # wraps to both sides of the pole.  The second column is phi, but you
        # can only figure out what phi is by knowing the signs of both theta
        # and phi.  Here goes.
        tp_pp = np.array(np.where((thetad >= 0) * (phid >=0))[0])
        tp_pm = np.array(np.where((thetad >= 0) * (phid < 0))[0])
        tm_pp = np.array(np.where((thetad < 0) * (phid >= 0))[0])
        tm_pm = np.array(np.where((thetad < 0) * (phid < 0))[0])

        phid_shift = np.zeros(len(phid))
        
        phid_shift[tp_pp] = phid[tp_pp]
        phid_shift[tp_pm] = phid[tp_pm]+360.
        phid_shift[tm_pp] = phid[tm_pp]+180
        phid_shift[tm_pm] = phid[tm_pm]+180

        phid = phid_shift
        thetad = np.abs(thetad)

    # Healpix likes everything in radians
    theta = np.radians(thetad)
    phi = np.radians(phid)

    # Third column is E field magnitude, so square and divide by max
    # to get power response
    if filetype=='eloy':
        val = np.power(data[:,column],2)
        val = val/val.max()

    # Third column is dBi    
    if filetype=='rich':
        val = np.power(10.,data[:,column]/10.)
        #val = val/val.max()

    # Original Healpix gridding
    nside=32
    npix = hp.nside2npix(nside)

    map = np.zeros(npix)
    hits = np.zeros(npix)

    # just straight-up HEALpix-ellize that bitch
    pix = hp.ang2pix(nside,theta,phi)
    #print 'Pix values'
    #print pix.min()
    #print pix.max()
    
    # Simplest gridding is
    #map[pix] = val
    # This tries to do some averaging
    for i,v in enumerate(val):
        map[pix[i]] += v
        hits[pix[i]] +=1
    map = map/hits

    # Let's decompose this into a_lm and recompose at higher resolution
    if True:
        nside_synth = 128
        lmax = 3*nside-1
        l,m = hp.Alm.getlm(lmax)

        # Do the alm decomposition on dBi map
        alm = hp.map2alm(10.*np.log10(map),lmax=lmax)
        # Reconstitute at high resolution
        bm = hp.alm2map(alm,nside_synth,lmax=lmax,verbose=False)
        bm = np.power(10.,bm/10.)
        
    return {'data':data,'bm32':map,'bm128':bm}#,'thetad':thetad,'phid':phid,'val':val,'alm':alm,'l':l,'m':m,'hits':hits}

def theta_cut_at_phi(nside,phi_d_cut,npts=3600):
    """For a HEALpix map of side nside, give the pixel values for a cut that runs -90 < theta < 90 at some phi.  npts should be determinable from nside, but right now I'm lazy"""
    # Ugh.  Usual physics spherical coordinates do not make nice cuts
    # through the beam.  Easiest way to make cuts
    theta = np.linspace(-180,180,npts)
    phi = np.ones_like(theta)
    phi[np.where(theta < 0)] = phi_d_cut+180
    phi[np.where(theta >= 0)] = phi_d_cut

    p = np.radians(phi)
    t = np.radians(np.abs(theta))
    pix = np.array(hp.ang2pix(nside,t,p))
    return {'pix':pix,'theta':theta}
