# -*- coding: utf-8 -*-
"""Brainlink.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12WB_lpfLgga0yKCoE47n6kaaoe0pfTrr
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install numpy
!pip install pandas

import itertools
import os 
import scipy
import numpy
from scipy import signal 
import pandas as pd
import matplotlib.pyplot as plt

"""A Norch Filter:
  Band-stop filter
  stop frequency: 50Hz
"""

sample_rate=512


def Notch_filter(sig_data):

  fr=50
  fs=sample_rate
  Q=10
  b,a = signal.iirnotch(fr,Q,fs)
  filted_data=scipy.signal.filtfilt(b,a,sig_data)
   
  b, a = signal.butter(8, [0.004,0.86], 'bandpass')   #配置滤波器 8 表示滤波器的阶数
  filtedData = signal.filtfilt(b, a, filted_data)  #data为要过滤的信号

  return filtedData

"""FFT with hamming window"""

def FFT_ham(sig_data):
  sample_rate=512
  N=5*sample_rate
  
  hamming_win=signal.hamming(N)
  sig_win=sig_data*hamming_win

  sig_fft=numpy.fft.fft(sig_win)

  f=numpy.fft.fftfreq(N, 1/sample_rate)

  
  #plt.plot(f, np.abs(sig_fft))
  #plt.xlabel('Freq')
  #plt.ylabel('Magnitude')
  #plt.show()
  return sig_fft, f

"""# Read txt datafiles: 
* cut the data into 5s/peice. The data is totally aroundd 14min long. 
* Consisit of 1min relax, 4min open eyes, 1min relax, 4min close eyes, 1min relax, 4min open eyes.
* use the signal between 2min-4min and 6.5min-8.5min

"""

FATIGUE = [
    "/content/drive/MyDrive/BrainLink/BrainLink2/BrainLinkRaw_01_FAT.txt",
   # "/content/drive/MyDrive/BrainLink/BrainLink2/BrainLinkRaw_02_FAT.txt",
    "/content/drive/MyDrive/BrainLink/BrainLink2/BrainLinkRaw_03_FAT2.txt",
    "/content/drive/MyDrive/BrainLink/BrainLink2/BrainLinkRaw_04_FAT.txt",
    "/content/drive/MyDrive/BrainLink/BrainLink2/BrainLinkRaw_05_FAT.txt"
  
]

WAKE = [
    "/content/drive/MyDrive/BrainLink/BrainLink2/BrainLinkRaw_01_WAK.txt",
    "/content/drive/MyDrive/BrainLink/BrainLink2/BrainLinkRaw_02_WAK.txt",
    "/content/drive/MyDrive/BrainLink/BrainLink2/BrainLinkRaw_03_WAK.txt",
    "/content/drive/MyDrive/BrainLink/BrainLink2/BrainLinkRaw_04_WAK.txt",
   # "/content/drive/MyDrive/BrainLink/BrainLink2/BrainLinkRaw_05_WAK.txt"
]

KSS=[]
index = 0
delta, theta, alpha, beta, gamma, fi, KSS = [], [], [], [], [], [], []
filtered_data=numpy.zeros(sample_rate*5)
for file in FATIGUE:
    filtered_data=numpy.zeros(sample_rate*5)
    EEG = numpy.loadtxt(file)
    for i in range(24,48):
      filtered_data=filtered_data+Notch_filter((EEG[i*sample_rate*5:(i+1)*sample_rate*5]))
      sig_fft,freq_fft=FFT_ham(filtered_data)
      eeg_power=numpy.abs(sig_fft)**2
      eeg=eeg_power[:int(sample_rate*5/2)]
      delta.append(numpy.mean(eeg[int(0.5/128*(sample_rate*5/2)):int(4/128*(sample_rate*5/2))]))
      theta.append(numpy.mean(eeg[int(4/128*(sample_rate*5/2)):int(8/128*(sample_rate*5/2))]))
      alpha.append(numpy.mean(eeg[int(7.5/128*(sample_rate*5/2)):int(13/128*(sample_rate*5/2))]))
      beta.append(numpy.mean(eeg[int(13/128*(sample_rate*5/2)):int(30/128*(sample_rate*5/2))]))
      gamma.append(numpy.mean(eeg[int(30/128*(sample_rate*5/2)):int(44/128*(sample_rate*5/2))]))
      fi.append(numpy.mean(eeg[int(0.85/128*(sample_rate*5/2)):int(110/128*(sample_rate*5/2))]))
      
      # KSS.append(KSS_val)
      KSS.append(0)
fkaverageopen=filtered_data/4/24


filtered_data=numpy.zeros(sample_rate*5)
for file in WAKE:
    filtered_data=numpy.zeros(sample_rate*5)
    EEG = numpy.loadtxt(file)
    for i in range(24,48):
      filtered_data=filtered_data+Notch_filter((EEG[i*sample_rate*5:(i+1)*sample_rate*5])) 
      sig_fft,freq_fft=FFT_ham(filtered_data)
      eeg_power=numpy.abs(sig_fft)**2
      eeg=eeg_power[:int(sample_rate*5/2)]
      delta.append(numpy.mean(eeg[int(0.5/128*(sample_rate*5/2)):int(4/128*(sample_rate*5/2))]))
      theta.append(numpy.mean(eeg[int(4/128*(sample_rate*5/2)):int(8/128*(sample_rate*5/2))]))
      alpha.append(numpy.mean(eeg[int(7.5/128*(sample_rate*5/2)):int(13/128*(sample_rate*5/2))]))
      beta.append(numpy.mean(eeg[int(13/128*(sample_rate*5/2)):int(30/128*(sample_rate*5/2))]))
      gamma.append(numpy.mean(eeg[int(30/128*(sample_rate*5/2)):int(44/128*(sample_rate*5/2))]))
      fi.append(numpy.mean(eeg[int(0.85/128*(sample_rate*5/2)):int(110/128*(sample_rate*5/2))]))
      KSS.append(1)
   # for i in range(132,157):
  #    filtered_data=filtered_data+Notch_filter((EEG[i*512*5:(i+1)*512*5]))
wkaverageopen=filtered_data/4/24



filtered_data=numpy.zeros(sample_rate*5)
for file in FATIGUE:
    filtered_data=numpy.zeros(sample_rate*5)
    EEG = numpy.loadtxt(file)
    for i in range(84,108):
      filtered_data=filtered_data+Notch_filter((EEG[i*sample_rate*5:(i+1)*sample_rate*5]))  
      sig_fft,freq_fft=FFT_ham(filtered_data)
      eeg_power=numpy.abs(sig_fft)**2
      eeg=eeg_power[:int(sample_rate*5/2)]
      delta.append(numpy.mean(eeg[int(0.5/128*(sample_rate*5/2)):int(4/128*(sample_rate*5/2))]))
      theta.append(numpy.mean(eeg[int(4/128*(sample_rate*5/2)):int(8/128*(sample_rate*5/2))]))
      alpha.append(numpy.mean(eeg[int(7.5/128*(sample_rate*5/2)):int(13/128*(sample_rate*5/2))]))
      beta.append(numpy.mean(eeg[int(13/128*(sample_rate*5/2)):int(30/128*(sample_rate*5/2))]))
      gamma.append(numpy.mean(eeg[int(30/128*(sample_rate*5/2)):int(44/128*(sample_rate*5/2))]))
      fi.append(numpy.mean(eeg[int(0.85/128*(sample_rate*5/2)):int(110/128*(sample_rate*5/2))]))
      KSS.append(0)
fkaverageclose=filtered_data/4/24



filtered_data=numpy.zeros(sample_rate*5)
for file in WAKE:
    filtered_data=numpy.zeros(sample_rate*5)
    EEG = numpy.loadtxt(file)
    for i in range(84,108):
      filtered_data=filtered_data+Notch_filter((EEG[i*sample_rate*5:(i+1)*sample_rate*5]))  
      sig_fft,freq_fft=FFT_ham(filtered_data)
      eeg_power=numpy.abs(sig_fft)**2
      eeg=eeg_power[:int(sample_rate*5/2)]
      delta.append(numpy.mean(eeg[int(0.5/128*(sample_rate*5/2)):int(4/128*(sample_rate*5/2))]))
      theta.append(numpy.mean(eeg[int(4/128*(sample_rate*5/2)):int(8/128*(sample_rate*5/2))]))
      alpha.append(numpy.mean(eeg[int(7.5/128*(sample_rate*5/2)):int(13/128*(sample_rate*5/2))]))
      beta.append(numpy.mean(eeg[int(13/128*(sample_rate*5/2)):int(30/128*(sample_rate*5/2))]))
      gamma.append(numpy.mean(eeg[int(30/128*(sample_rate*5/2)):int(44/128*(sample_rate*5/2))]))
      fi.append(numpy.mean(eeg[int(0.85/128*(sample_rate*5/2)):int(110/128*(sample_rate*5/2))]))
      KSS.append(1)
wkaverageclose=filtered_data/4/24

"""# Calculate Sp Features
* 15 features are calculated
* $\delta, \theta, \alpha, \frac{\theta}{\beta}, \frac{\theta}{\alpha}, \frac{\theta}{\phi}, \frac{\theta}{\alpha+\beta+\gamma}, \frac{\delta}{\alpha+\beta+\gamma}, \frac{\delta}{\alpha}, \frac{\delta}{\phi}, \frac{\delta}{\beta}, \frac{\delta}{\theta}, \frac{\theta}{\alpha+\beta+\theta}, \frac{\alpha}{\theta+\alpha+\beta}, \frac{\beta}{\theta+\alpha+\beta}$
"""

delta = numpy.array(delta)  
theta = numpy.array(theta)    
alpha = numpy.array(alpha)    
beta = numpy.array(beta)    
gamma = numpy.array(gamma)    
fi = numpy.array(fi)    
 

Sp = [delta, theta, alpha, theta/beta, theta/alpha, theta/fi, theta/alpha+beta+gamma, delta/alpha+beta+gamma, delta/alpha, delta/fi, \
      delta/beta, delta/theta, theta/alpha+beta+theta, alpha/theta+alpha+beta, beta/theta+alpha+beta]

"""# SVM Classify
* classify to fatigue and wake
* shape of KSS and Sp is (384,15), the former 192 points are open eyes data, the later 192 points are close eyes data
"""

# Open eyes classify 
x = numpy.transpose(numpy.array(Sp))
y = numpy.transpose(numpy.array(KSS))

x_open=x[:192]
y_open=y[:192]
x_close=x[192:384]
y_close=y[192:384]

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import RepeatedKFold

average_acc = 0.0
kf = RepeatedKFold(n_splits=10, n_repeats=2)
acc = numpy.zeros(20)
index = 0
for train_index, test_index in kf.split(x_open):
 train_X= x_open[train_index]
 train_y =y_open[train_index]
 test_X, test_y = x_open[test_index], y_open[test_index]
 regr = make_pipeline(StandardScaler(), SVC())
 regr.fit(train_X, train_y)
 y_pred = regr.predict(test_X)
 #print(accuracy_score(test_y, y_pred))
 acc[index] = accuracy_score(test_y, y_pred)
 index = index + 1
print("BrainLink Open Eyes average_acc:", numpy.mean(acc), "std_acc:", 
numpy.std(acc))

average_acc = 0.0
kf = RepeatedKFold(n_splits=10, n_repeats=2)
acc = numpy.zeros(20)
index = 0
for train_index, test_index in kf.split(x_close):
 train_X= x_close[train_index]
 train_y =y_close[train_index]
 test_X, test_y = x_close[test_index], y_close[test_index]
 regr = make_pipeline(StandardScaler(), SVC())
 regr.fit(train_X, train_y)
 y_pred = regr.predict(test_X)
 #print(accuracy_score(test_y, y_pred))
 acc[index] = accuracy_score(test_y, y_pred)
 index = index + 1
print("BrainLink Close Eyes average_acc:", numpy.mean(acc), "std_acc:", 
numpy.std(acc))

average_acc = 0.0
kf = RepeatedKFold(n_splits=10, n_repeats=2)
acc = numpy.zeros(20)
index = 0
for train_index, test_index in kf.split(x):
 train_X= x[train_index]
 train_y =y[train_index]
 test_X, test_y = x[test_index], y[test_index]
 regr = make_pipeline(StandardScaler(), SVC())
 regr.fit(train_X, train_y)
 y_pred = regr.predict(test_X)
 #print(accuracy_score(test_y, y_pred))
 acc[index] = accuracy_score(test_y, y_pred)
 index = index + 1
print("BrainLink MIX average_acc:", numpy.mean(acc), "std_acc:", 
numpy.std(acc))

"""# Plot result
* 5s waveform with normalized amplitude
* 15 Sp features distribution
"""

def normalize(x):
  arange=x.max()-x.min()
  y=(x-x.min())/arange-(x.mean()-x.min())/arange
  return y

plt.rcParams.update({'font.size': 20}) 
x=numpy.arange(0,5,(5/2560))

fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(20, 10))
ax1.set_title("BrainLink OPEN")
ax1.plot(x,normalize(wkaverageopen),label='WAKE-OPEN')
ax1.plot(x,normalize(fkaverageopen),label='FAT-OPEN')
ax1.set_xlabel("Time(s)")
ax1.set_ylabel("EEG")
ax1.set_ylim(-1,1)
ax1.legend()
ax2.set_title("BrainLink CLOSE")

ax2.plot(x,normalize(wkaverageclose),label='WAKE-CLOSE')
ax2.plot(x,normalize(fkaverageclose),label='FAT-CLOSE')
ax2.set_xlabel("Time(s)")
ax2.set_ylabel("EEG")
ax2.legend()
ax2.set_ylim(-1,1)
plt.subplots_adjust(hspace=0.6)
print()
print()
plt.show()

xlabel=['delta','theta','alpha','theta/beta','theta/alpha','theta/fi','theta/alpha+beta+gamma',
        'delta/alpha+beta+gamma','delta/alpha','delta/fi','delta/beta','delta/theta','theta/alpha+beta+theta',
        'alpha/theta+alpha+beta','beta/theta+alpha+beta']
for i in range(0,15):
  fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(20,10))
  
 
 # plt.subplot(121)
  #plt.hist(SPWK[i], 432)
  #plt.subplot(122)
  #plt.hist(SPSL[i], 432)
  ax1.set_title("BrainLink Sp"+str(i+1)+" FAT&WAKE-OPEN")
  ax1.hist([Sp[i][0:96],Sp[i][96:192]],100,histtype='bar',label=['FAT-OPEN','WAKE-OPEN'])
  ax1.set_ylabel("Probability")
  ax1.set_xlabel(xlabel[i])
  #ax1.set_ylim(0,1)
  #print(Sp[i][0:96])
 # ax1.hist(WKO[i],100,label='WAKE-OPEN')
  ax1.legend()
  ax2.set_title("BrainLink Sp"+str(i+1)+" FAT&WAKE-CLOSE")
  ax2.hist([Sp[i][192:288],Sp[i][288:384]],100,histtype='bar',label=['FAT-CLOSE','WAKE-CLOSE'])
  ax2.set_ylabel("Probability")
  #ax2.set_ylim(0,1)
  ax2.set_xlabel(xlabel[i])
  #ax2.hist(WKC[i],100,label='WAKE-CLOSE')
  #print(SP_trans[i])
  ax2.legend()
  plt.subplots_adjust(hspace=0.6)
  print()
  print()
  plt.show()