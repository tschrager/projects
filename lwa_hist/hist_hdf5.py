import h5py
import numpy

f=h5py.File('data/055859_002700166_TBW.hdf5','r')

myhist=numpy.zeros(4095)
for stand in list(f):
    dset=f[stand]['X']
    bins=numpy.arange(-2048,2048)
    myhist+=numpy.histogram(dset,bins)
