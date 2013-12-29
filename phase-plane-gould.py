import numpy as np
import matplotlib.pyplot as plt

import Graphics as artist

from numpy.random import random_sample

from matplotlib import rcParams

rcParams['text.usetex'] = True

mEE = 1.25#1.25 #mEE mIE
mIE = 1#1    #mEI mII
mII = 0#0
mEI = 1#-1

M = np.array([[mEE, mEI],[mIE, mII]])

gE = -10
gI = 10

g = np.array([gE, gI])

tauE = .01
tauI = .03

timesteps = 10000
dt = 0.001
data = np.zeros((2,timesteps))

#initial conditions
data[:,0] = random_sample(size=data[:,0].shape)

for t in range(1,timesteps):
	#Rectification
	inp = np.dot(M,data[:,t-1]-g)
	inp[inp<0] = 0

	data[:,t] = data[:,t-1] + dt*(-data[:,t-1] + inp)

#Phase planes

x = 1./(1.-mEE)*(data[0,:]-gE) #These are the equations that need to be satisfied for da/dt to be 0
y = 1./(1.-mII)*(data[1,:]-gI)

fig,axs = plt.subplots(nrows=1,ncols=2)

#Plot phase portrait
axs[0].plot(data[0,:], color='k', label=r'\Large \textbf{Group 1}',linewidth=2)
axs[0].plot(data[1,:], color='r', label=r'\Large \textbf{Group 2}',linewidth=2)
artist.adjust_spines(axs[0])
axs[0].set_ylabel(r'\Large \textbf{Rate of Information Transfer} $\frac{\textrm{bits}}{\textrm{sec}}$')
axs[0].set_xlabel(r'\Large \textbf{Timestep}')

axs[1].plot(x,y,'k',linewidth=2)
artist.adjust_spines(axs[1])
axs[1].set_ylabel(r'\Large \textbf{Rate of Information Transfer in Group 1} $\frac{\textrm{bits}}{\textrm{sec}}$')
axs[1].set_xlabel(r'\Large \textbf{In Group 2} $\frac{\textrm{bits}}{\textrm{sec}}$')
plt.legend(frameon=False)
plt.tight_layout()
plt.show()
