import matplotlib.pyplot as plt
import numpy as np

from matplotlib import rcParams
from matplotlib.mlab import psd
from scipy.stats import scoreatpercentile

import utils as tech

rcParams['xtick.direction'] = 'in'
rcParams['ytick.direction'] = 'in'
rcParams['text.usetex'] = True

def angle_plot(one,two=None):
	if not two:
		two=one

	#must take the product of the columns
	angles = np.array([np.inner(first,second)/(np.inner(first,first)*np.inner(second,second)) 
			for first,second in zip(one.transpose(),two.transpose())])
	print angles

def dashboard(data,numpc=3, labels = None):

	coeff,projections,latent = tech.princomp(data,numpc=numpc)
	panels = {'projection':plt.subplot2grid((2,3),(0,0),colspan=2, rowspan=2),
			  'spectrum':plt.subplot2grid((2,3),(0,2)),
			  'silhouette':plt.subplot2grid((2,3),(1,2))}
	panels['projection'].scatter(projections[0],projections[1],s=30)
	adjust_spines(panels['projection'])
	panels['projection'].set_xlabel(r'\Large \textbf{Principal Component 1}')
	panels['projection'].set_ylabel(r'\Large \textbf{Principal Component 2}')

	cutoff=10
	panels['spectrum'].stem(range(1,cutoff+1),latent[:cutoff]/np.sum(latent))
	panels['spectrum'].set_xlim(0,cutoff+1)
	panels['spectrum'].set_ylim((0,1))
	adjust_spines(panels['spectrum'])
	panels['spectrum'].set_xlabel(r'\Large \textbf{Eigenvector}')
	panels['spectrum'].set_ylabel(r'\Large \textbf{Eigenvalue} $\left(\lambda\right)$')

	silhouettes = tech.silhouette(projections, k=8)
	idx = range(2,len(silhouettes)+2)
	panels['silhouette'].stem(idx,[silhouettes[x]['data'] for x in idx])

	#Get confidence intervals
	CIs = np.array([scoreatpercentile(silhouettes[x]['distribution'], 95) for x in idx])
	print CIs
	plt.hold(True)
	panels['silhouette'].plot(idx,CIs,linewidth=2,color='r',linestyle='--')
	adjust_spines(panels['silhouette'])
	panels['silhouette'].set_xlim((0,len(idx)+3))
	panels['silhouette'].set_ylim((0,1))
	panels['silhouette'].set_xlabel(r'\Large \textbf{Number of clusters}')
	panels['silhouette'].set_ylabel(r'\Large \textbf{Silhouette coefficient}')
	plt.tight_layout()

	rot = plt.figure()
	panel = rot.add_subplot(111)
	dt = coeff*(latent[:3]/np.sum(latent))
	dt_args = np.argsort(dt,axis=0)
	cax = panel.imshow(np.sort(coeff*(latent[:3]/np.sum(latent)),axis=0)[::-1], aspect='auto',interpolation='nearest', vmin=-.15,vmax=0.15)
	adjust_spines(panel)
	if labels:
		panel.set_yticks(np.arange(len(labels)))
		panel.set_yticklabels(map(lambda word: word.capitalize(),labels))
	panel.set_xticks(np.arange(3))
	panel.set_xticklabels(np.arange(3)+1)
	panel.set_xlabel(r'\Large \textbf{Principal Component}')
	rot.colorbar(cax)
	plt.tight_layout()
	plt.grid(True)
	plt.show()

def adjust_spines(ax,spines=['bottom','left']):
	''' Taken from http://matplotlib.org/examples/pylab_examples/spine_placement_demo.html '''
	for loc, spine in ax.spines.iteritems():
		if loc in spines:
			spine.set_position(('outward',10))
			#spine.set_smart_bounds(True) #Doesn't work for log log plots
			spine.set_linewidth(1)
		else:
			spine.set_color('none') 
	if 'left' in spines:
		ax.yaxis.set_ticks_position('left')
	else:
		ax.yaxis.set_ticks([])

	if 'bottom' in spines:
		ax.xaxis.set_ticks_position('bottom')
	else:
		ax.xaxis.set_ticks([])

def power_spectrum(data,Fs=20000, savename=None,show=True, cutoff=50):
	p = Periodogram(data,sampling=Fs)
	p.run()
	p.plot()
	'''
	#stop = np.where(freqs>cutoff)[0][0]
	#print stop
	fig = plt.figure()
	ax = fig.add_subplot(111)
	spec, = ax.plot(freqs,db,'o-')
	adjust_spines(ax,['bottom','left'])
	ax.set_xlabel(r'frequency $\left(Hz\right)$')
	ax.set_ylabel(r'Power $\left(dB\right)$')
	'''
	if show:
		plt.show()
	if savename:
		plt.savefig(savename,dpi=72)

def scree_plot(eigVals,cutoff=0.95,savename=None, show=False,save=True,savebase=None):
	#Assume the list is all of the eigenvalues
	rel = np.cumsum(eigVals)/eigVals.sum()
	x = np.arange(len(rel))+1
	print eigVals.shape
	fig = plt.figure()
	ax = fig.add_subplot(111)
	line, = ax.plot(x,rel)
	line.set_clip_on(False)
	adjust_spines(ax,['bottom','left'])
	ax.set_xlabel(r'$\LARGE \lambda$')
	ax.set_ylabel('Fraction of variance')
	ax.set_xlim(0,len(eigVals))
	
	cutoff_idx = np.where(rel>cutoff)[0][0]
	
	ax.axvline(x=cutoff_idx, color='r',linestyle='--', linewidth=2)
	ax.axhline(y=rel[cutoff_idx],color='r',linestyle='--',linewidth=2)
	ax.tick_params(direction='in')
	ax.annotate(r" {\Large $\mathbf{\lambda=%d}$}" % cutoff_idx,xy=(.25, .9), xycoords='axes fraction', 
											horizontalalignment='center', verticalalignment='center')
	plt.tight_layout()
	if save:
		print savebase
		plt.savefig(savebase+'_scree.png',dpi=100)
			
	if show:
		plt.show()
	plt.close()

def spike_validation(data,clusters,spiketimes=None,eiglist=None,nclus=None,savebase='res',waveforms=None,multi=False, show=False
					,save=True, adj=False):
	best = clusters['models'][np.argmax(clusters['silhouettes'])]
	nclus = best.n_clusters if not nclus else nclus
	fig = plt.figure()
	plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=.97)
	#Clusters of waveforms projected onto the first two principal components
	ax = fig.add_subplot(2,2,1)
	ax.set_axis_bgcolor('white')
	colors = ['#4EACC5', '#FF9C34', '#4E9A06']
	labels_ = best.labels_
	centers = best.cluster_centers_
	unique_labels = np.unique(labels_)
	for n,col in zip(range(nclus),colors):
		my_members = labels_ == n 
		cluster_center = centers[n]
		ax.plot(data[0,my_members],data[1,my_members],'w',markerfacecolor=col,marker='.', markersize=6)
		plt.hold(True)
		ax.plot(cluster_center[0],cluster_center[1],'o',markerfacecolor=col,markeredgecolor='k',markersize=8)
	adjust_spines(ax,['bottom','left'])
	ax.set_ylabel('PC2')
	ax.set_xlabel('PC1')
	ax.tick_params(direction='in')
	
	if waveforms is not None:
		print 'drawing wfs'
		wfs = fig.add_subplot(2,2,3)#axes([0.37, 0.65, 0.1, 0.15])
		wfs.set_axis_bgcolor('none')
		artists = []
		for n,col in zip(range(nclus),colors):
			#my_members = labels_[:-300]== n
			my_members = labels_ == n
			print len(my_members)
			print waveforms.shape
			line, = wfs.plot(np.average(waveforms[my_members,:],axis=0),col,linewidth=2)
			line.set_clip_on(False)	
		adjust_spines(wfs,['bottom','left'])
		
		if not adj:
			wfs.set_yticks([0,100])
			wfs.set_yticklabels([r'$0$', r'$100 \; \mu V$'],rotation='vertical')
			wfs.set_xticks([0,100])
			wfs.set_xticklabels([r'$0$',r'$800 \; \mu s$'])
			wfs.spines['bottom'].set_bounds(0,100)
		else:
			wfs.set_yticks([-1000,0,1000])
			wfs.set_yticklabels([r'$-100 \; \mu V$',r'$0$', r'$100 \; \mu V$'],rotation='vertical')
			wfs.set_xticks([0,16,32])
			wfs.set_xticklabels([r'$0$',r'$400 \; \mu s$',r'$800 \; \mu s$'])
			wfs.spines['bottom'].set_bounds(0,32)
		
	sils = fig.add_subplot(2,2,2)
	sils.set_axis_bgcolor('none')
	markerline, stemlines,baseline =sils.stem(np.arange(len(clusters['silhouettes'])),clusters['silhouettes'])
	sils.tick_params(direction='in')
	sils.axhline(y=0.5,color='r',linestyle='--',linewidth=2)
	adjust_spines(sils,['bottom','left'])
	sils.set_xticks(np.arange(len(clusters['silhouettes']))+1)
	sils.set_yticks([-1,0,1])
	sils.set_ylabel('Silhouette coefficient')
	sils.set_xlabel('Number of clusters')
	sils.set_xlim((0.5,len(clusters['silhouettes'])))
	
	xmx=100
	if spiketimes is not None:
		#break of up the spiketime vector based on clustering
		short_isi = fig.add_axes([0.8, 0.26, 0.15, 0.20])
		isi = fig.add_subplot(2,2,4)
		for n,col in zip(range(nclus),colors):
			#my_members = labels_[:-300]== n #Always add 3000 noise spikes
			my_members = labels_ == n
			these_isis = 0.1*np.diff(spiketimes[my_members])
			these_isis = these_isis[these_isis>1]
			if these_isis.size:
				
				_,_,patches=isi.hist(these_isis, histtype='stepfilled', range=(0,100),
					alpha=0.5, bins=50)
				adjust_spines(isi,['bottom','left'])
				plt.setp(patches,'facecolor',col)

				_,_,spatches=short_isi.hist(these_isis,range=(0,10), histtype='stepfilled')
				plt.setp(spatches,'facecolor',col)
		isi.tick_params(direction='in')
		isi.set_axis_bgcolor('none')
		isi.set_ylabel(r'\# of spikes')
		isi.set_xlabel(r'Interspike interval $(ms)$')
		isi.set_xlim(xmax=xmx)
		
		
		short_isi.set_axis_bgcolor('none')
		adjust_spines(short_isi,['bottom','left'])
		short_isi.tick_params(direction='in')
		short_isi.set_ylabel(r'\# of Spikes')
		#short_isi.set_yticks(np.arange(8))
		short_isi.axvline(x=2,c='r',linewidth=2)
		short_isi.set_xlabel(r'ISI $(ms)$')
		short_isi.set_xticklabels(np.arange(0,12)[::2])

		
	if eiglist is not None and eiglist.size:
		eigfxns = fig.add_subplot(2,2,3)
		eigfxns.set_axis_bgcolor('none')
		eigfxns.tick_params(direction='in')
		#Assume 6 eigenfunctions
		nfxns =6
		span = len(eiglist[0,:])/2
		print span
		x = arange(2*span) if multi else np.arange(-span,span)
		for i in range(nfxns):
			eigfxns.plot(x,i+eiglist[i,:],'b',linewidth=2)
			plt.hold(True)
		adjust_spines(eigfxns,['bottom','left'])
		if multi:
			eigfxns.set_xlabel(r' $\left(\mu sec\right)$')
		else:
			eigfxns.set_xlabel(r'Time from spike peak $\left(\mu sec\right)$')
			eigfxns.set_xticklabels([r'\textbf{%d}'%(32*(i-5)) for i in range(10)])
			eigfxns.set_yticklabels([' '] + [r' $e_{%d}$' %i for i in range(1,nfxns+1) ])
		eigfxns.set_ylabel(r'Eigenfunctions')
		#draw_sizebar(eigfxns)

	plt.tight_layout()
	plt.savefig(savebase+'_validation.png', bbox_inches='tight')
	if show:
		plt.show()

def voltage_trace(unfiltered=None,filtered=None,threshold = 0, roi=30000,spread=10000,save=None, 
					show=False, fs = 20000, downsampling= 10,savebase=None):
					
	fig = plt.figure()
	trace_panel = fig.add_subplot(211,axisbg='none')
	start = roi-spread
	stop = roi+spread

	traces, = trace_panel.plot(unfiltered[start:stop][::downsampling],'b') #Downsample just for display
		
	spike_panel = fig.add_subplot(212,axisbg='none',sharex=trace_panel)
	spikes, = spike_panel.plot(filtered[start:stop][::downsampling],'b')
		
	panels = [trace_panel,spike_panel]
	
	for panel in panels:
		adjust_spines(panel,['bottom','left'])
	
	trace_panel.set_xlabel(r'time $\left(s\right)$')
	trace_panel.set_ylabel(r'voltage $ \left(\mu V \right)$')
	trace_panel.set_xticklabels(np.arange(start/fs,1.5+stop/fs,0.5).astype(str))

	spike_panel.set_xlabel(r'time $\left(s\right)$')
	spike_panel.set_xticklabels(np.arange(start/fs,1.5+stop/fs,0.5).astype(str))
	spike_panel.set_ylabel(r'voltage $\left(\mu V \right)$')
	#Draw threshold
	spike_panel.axhline(y=threshold,linewidth=1,color='r',linestyle='--')
	spike_panel.axhline(y=-threshold,linewidth=1,color='r',linestyle='--')
	
	plt.tight_layout()
	if save:
		print savebase
		plt.savefig(savebase+'_voltage.png',dpi=100)
			
	if show:
		plt.show()

def fvt(traces,time):
	left,right = zip(*traces)
	panel_labels = ['Left','Right']
	fig, axs = plt.subplots(nrows=1,ncols=2, sharex=True, sharey=True)
	colors  = ['k','r','b','g']
	for j,(ax,data) in enumerate(zip(axs,[left,right])):
		for i,record in enumerate(data):
			ax.plot(time[::10],record[::10], colors[i],label=r'\Large \textbf{%d}'%(i+1))
			plt.hold(True)

		plt.legend(frameon=False, loc='upper left')
		ax.set_xlim(xmax=600)
		
		ax.annotate(r'\Large \textbf{%s}'%panel_labels[j], xy=(.1, .5),  xycoords='axes fraction',
                horizontalalignment='center', verticalalignment='center')
		adjust_spines(ax)
		ax.set_xlabel(r'\Large \textbf{Time (mins)}')
		ax.set_ylabel(r'\Large \textbf{Force (Arb. Units)}')
	plt.tight_layout()
	plt.show()

def ccf():	
	print 'Calculated'
	rowL=len(filenames)
	colL=rowL
	
	acf_panel,ax=subplots(rowL,colL, sharex=True, sharey=True) 
	#Should use absolute not relative normalization
	#Currently use absolute motivation
	for j in range(rowL):
		for i in range(colL):
			line, = ax[i,j].plot(arange(-w,w),ccfs[i+j], linewidth=2)
			line.set_clip_on(False)
			ax[i,j].axvline(x=0,color='r',linestyle='--', linewidth=2)
			postdoc.adjust_spines(ax[i,j],['bottom','left'])
			ax[i,j].spines['left'].set_smart_bounds(True)
			ax[i,j].spines['bottom'].set_smart_bounds(True)
			ax[i,j].set_ylabel('Covariance')
			ax[i,j].set_xlabel(r'Time $\left(ms\right)$')
			ax[i,j].set_axis_bgcolor('none')
			ax[i,j].tick_params(direction='in')
			ax[i,j].locator_params(nbins=(60/w))
			ax[i,j].annotate(r" {\Large $\mathbf{%s,%s}$}" %(tech.get_channel_id(filenames[i]),tech.get_channel_id(filenames[j])), 
							 xy=(.2, .8), xycoords='axes fraction',horizontalalignment='center', verticalalignment='center')
	tight_layout()
	savefig('test_ccf.png')