import psana
import numpy as np
import time
import matplotlib.pyplot as plt
import h5py as h5
import os

experimentName = 'amo86615'
#experimentName = 'cxic0415'
runNumber = '197'#'99'
detInfo = 'pnccdBack' #'DscCsPad'
evtNum = 0

ds = psana.DataSource('exp='+experimentName+':run='+runNumber+':idx')
run = ds.runs().next()
det = psana.Detector(detInfo)

times = run.times()
env = ds.env()
eventTotal = len(times)

number = 1000


pedestal = det.pedestals(run) # get pedestal
pattern_shape = pedestal.shape
f = h5.File('pedestals.h5','w')
dset = f.create_dataset('ped', shape=(number,)+pattern_shape,dtype=np.int32, chunks=(1,)+pattern_shape, compression="gzip", compression_opts=4)

rms = det.rms(run)            # get rms
goodPix = np.where(rms>0)     # pixel rms should be > zero
badPix = np.where(rms==0)     # some pixels have rms < 0
rms[badPix] = np.mean(rms[goodPix]) # bad pixels set to mean rms
for i in range(eventTotal):
    dark = np.random.normal(pedestal,rms) # pedestal generated using Gaussian distribution
    dset[i] = dark 
    #plt.subplot(131)
    #plt.imshow(det.image(run,pedestal),vmin=0,vmax=2000)
    #plt.title('pedestal for run'+str(runNumber))
    #plt.subplot(132)
    #plt.imshow(det.image(run,rms),vmin=3,vmax=4)
    #plt.title('rms for run'+str(runNumber))
    #plt.subplot(133)
    #plt.imshow(det.image(run,dark),vmin=0,vmax=2000)
    #plt.title('Random pedestal for event'+str(i))
    #plt.show()
    #if i == 2: break
