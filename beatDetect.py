import wave, array, math, time, argparse, sys
import numpy, pywt
from scipy import signal
import pdb
import matplotlib.pyplot as plt

def read_wav(filename):

    #open file, get metadata for audio
    try:
        wf = wave.open(filename,'rb')
    except IOError as e:
        print(e)
        return

    nsamps = wf.getnframes()
    assert(nsamps > 0)

    fs = wf.getframerate()
    assert(fs > 0)

    # read entire file and make into an array
    samps = list(array.array('i',wf.readframes(nsamps)))
    try:
        assert(nsamps == len(samps))
    except AssertionError as e:
        print(nsamps, "not equal to", len(samps))

    return samps, fs

# print an error when no data can be found
def no_audio_data():
    print("No audio data for sample, skipping...")
    return None, None

# simple peak detection
def peak_detect(data):
    max_val = numpy.amax(abs(data))
    peak_ndx = numpy.where(data==max_val)
    if len(peak_ndx[0]) == 0: #if nothing found then the max must be negative
        peak_ndx = numpy.where(data==-max_val)
    return peak_ndx

def bpm_detector(data,fs):
    cA = []
    cD = []
    correl = []
    cD_sum = []
    levels = 4
    max_decimation = 2**(levels-1)
    min_ndx = math.floor(60./ 220 * (fs/max_decimation))
    max_ndx = math.floor(60./ 40 * (fs/max_decimation))

    for loop in range(0,levels):
        cD = []
        # 1) DWT
        if loop == 0:
            [cA,cD] = pywt.dwt(data,'db4')
            cD_minlen = len(cD)/max_decimation+1
            cD_sum = numpy.zeros(math.floor(cD_minlen))
        else:
            [cA,cD] = pywt.dwt(cA,'db4')

        # 2) Filter
        cD = signal.lfilter([0.01],[1 -0.99],cD)

        # 3) Decimate for reconstruction later.
        cD = abs(cD[::(2**(levels-loop-1))])
        cD = cD - numpy.mean(cD)

        # 4) Recombine the signal before ACF
        #    essentially, each level I concatenate
        #    the detail coefs (i.e. the HPF values)
        #    to the beginning of the array
        cD_sum = cD[0:math.floor(cD_minlen)] + cD_sum

    if [b for b in cA if b != 0.0] == []:
        return no_audio_data()
    # adding in the approximate data as well...
    cA = signal.lfilter([0.01],[1 -0.99],cA)
    cA = abs(cA)
    cA = cA - numpy.mean(cA)
    cD_sum = cA[0:math.floor(cD_minlen)] + cD_sum

    # ACF
    correl = numpy.correlate(cD_sum,cD_sum,'full')

    midpoint = math.floor(len(correl) / 2)
    correl_midpoint_tmp = correl[midpoint:]
    peak_ndx = peak_detect(correl_midpoint_tmp[min_ndx:max_ndx])
    if len(peak_ndx) > 1:
        return no_audio_data()

    peak_ndx_adjusted = peak_ndx[0]+min_ndx
    bpm = 60./ peak_ndx_adjusted * (fs/max_decimation)
    print(bpm)
    return bpm,correl

def detect(file_name, window_size=3):
    samps,fs = read_wav(file_name)
    data = []
    correl=[]
    bpm = 0
    n=0
    nsamps = len(samps)
    window_samps = (window_size*fs)
    samps_ndx = 0  #first sample in window_ndx
    max_window_ndx = math.floor(nsamps / window_samps)
    bpms = numpy.zeros(max_window_ndx)

    #iterate through all windows
    for window_ndx in range(0,max_window_ndx):

        #get a new set of samples
        data = samps[samps_ndx:samps_ndx+window_samps]
        if not ((len(data) % window_samps) == 0):
            raise AssertionError( str(len(data) ) )

        bpm, correl_temp = bpm_detector(data,fs)
        if bpm == None:
            continue
        bpms[window_ndx] = bpm
        correl = correl_temp

        #iterate at the end of the loop
        samps_ndx = samps_ndx+window_samps
        n=n+1

    return numpy.median(bpms)
