import numpy as np
import Clusters as pc
def princomp(A,numpc=0, scale=True):

	# computing eigenvalues and eigenvectors of covariance matrix
	M = (A-np.mean(A.T,axis=1)).T # subtract the mean (along columns)
	M = M / M.std(axis=1)[:,np.newaxis]

	[latent,coeff] = np.linalg.eig(np.cov(M))
	p = np.size(coeff,axis=1)
	idx = np.argsort(latent) # sorting the eigenvalues
	idx = idx[::-1]       # in ascending order
	# sorting eigenvectors according to the sorted eigenvalues
	coeff = coeff[:,idx]
	latent = latent[idx] # sorting eigenvalues
	if numpc < p or numpc >= 0:
		coeff = coeff[:,range(numpc)] # cutting some PCs
		score = np.dot(coeff.T,M) # projection of the data in the new space
	return coeff,score,latent

def silhouette_coefficient(distance_matrix,clustermap,nclus, datashape):
	mass = np.zeros(nclus)
	for c in clustermap:
		mass[c] += 1

	sil = np.zeros(nclus*max(datashape))
	sil.shape = (max(datashape),nclus)

	for i in range(0,max(datashape)):
		for j in range(i+1,max(datashape)):
			d = distance_matrix[j][i]

			sil[i,clustermap[j]] += d
			sil[j,clustermap[i]] += d

	for i in range(0,max(datashape)):
		sil[i,:] /= mass

	s = 0
	for i in range(0,max(datashape)):
		c = clustermap[i]
		a = sil[i,c]
		b = min (sil[i,range(0,c)+range(c+1,nclus)])
		si = (b-a)/float(max(b,a)) #Silhouette coefficient of the ith point
		s += si

	return s/float(max(datashape))

def silhouette(data, k=5, shuffle = True, shufflecount = 100):
	#assume that data is a matrix with variables in rows and dimensions in columns
	coefficients = {}
	data = data.transpose()
	for nclus in range(2,k):
		
		clustermap = pc.kcluster(data,nclusters=nclus,npass=50)[0]
		centroids = pc.clustercentroids(data,clusterid=clustermap)[0]
		m = pc.distancematrix(data)
		res = [silhouette_coefficient(m,clustermap,nclus,data.shape)]

		for _ in range(shufflecount):

			dat = data
			map(np.random.shuffle,dat)
			clustermap = pc.kcluster(dat,nclusters=nclus,npass=50)[0]
			centroids = pc.clustercentroids(dat,clusterid=clustermap)[0]

			#distance matrix-- well it's a list actually
			m = pc.distancematrix(dat)

			res.append([silhouette_coefficient(m,clustermap,nclus,dat.shape)])
		coefficients[nclus]={'data':res[0],'distribution':res[1:]}
	return coefficients
