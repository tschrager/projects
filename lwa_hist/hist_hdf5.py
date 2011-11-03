import h5py
import numpy
import glob
import pylab

f=h5py.File('data/055859_000007075_TBW.hdf5','r')
myhists = dict([ ((stand,pol),numpy.zeros(4096)) for stand in list(f) for pol in list(f[stand])])
numsamples = dict([ ((stand,pol),0) for stand in list(f) for pol in list(f[stand]) ])

for datafile in glob.glob('data/*.hdf5'):
    h5pyfile=h5py.File(datafile,'r')
    for stand in list(h5pyfile):
        for pol in list(f[stand]):
            dset=f[stand][pol]
            bins=numpy.arange(-2048,2049)
            myhists[stand,pol]+=numpy.histogram(dset,bins)[0]
            numsamples[stand,pol] += dset.shape[0]


for currenthist in list(myhists):
    # display a standard plot
    pylab.clf()
    pylab.plot(myhists[currenthist])
    pylab.savefig('plots/'+''.join(currenthist) + '.pdf',format='pdf')

    #display a log plot
    pylab.clf()
    pylab.plot(myhists[currenthist])
    pylab.yscale('log')
    pylab.savefig('plots/'+''.join(currenthist) + '_log.pdf',format='pdf')

    numpy.save('data/'+''.join(currenthist)+'hist.npy',myhists[currenthist])
    
