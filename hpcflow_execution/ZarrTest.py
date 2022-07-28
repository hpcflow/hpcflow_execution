import sys

import zarr
import numpy as np

def CreatePersistantEmptyZarr(filename):

    z1 = zarr.open(filename, mode='w', shape = (1000,1000), 
        chunks=(1000,1000), dtype='i4')

def CreatePersistantRandomZarr(filename):

    RandArray = np.random.rand(1000,1000)

    z1 = zarr.save(filename, RandArray)

def LoadZarr(filename):

    z1 = zarr.load(filename)

    return z1

def SaveZarr(filename, z):

    zarr.save(filename, z)

def ManipZarr(z1):

    z1[z1 >= 0.5] = 1.0
    z1[z1 < 0.5] = 0.0

    return z1

if __name__ == '__main__':

    filename = sys.argv[1]

    CreatePersistantRandomZarr(filename)
    z1 = LoadZarr(filename)
    z1 = ManipZarr(z1)
    SaveZarr(filename, z1)
