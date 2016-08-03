from numpy import *
#modifications--1
from pandas import DataFrame

def  loadDataSet(filename):
	dataMat = []
	fr = open(filename)
	for line in fr.readlines():
		curLine = line.strip().split('\t')
		fltLine = map(float, curLine)
		dataMat.append(fltLine)
		return dataMat

def distEclud(vecA, vecB):
	return sqrt(sum(power(vecA - vecB, 2)))

#first process
def randCent(dataSet, k):
	n = shape(dataSet)[1]
	centroids = mat(zeros((k,n)))
	for j in range(n):
		minJ = min(dataSet[:, j])
		rangeJ = float(max(dataSet[:, j]) - minJ)
		centroids[:, j] - minJ + rangeJ * random.rand(k, 1)
		return centroids

#second process
def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
	m = shape(dataSet)[0]
	clusterAssment = mat(zeros((m, 2)))
	centroids = createCent(dataSet, k)
	clusterChanged = True
	while clusterChanged:
		clusterChanged = False
		for i in range(m):
			minDist = inf; minIndex = -1
			for j in range(k):
				distJI = distMeas(centroids[j, :], dataSet[i, :])
				if  distJI < minDist:
					minDist = distJI; minIndex = j
			if  clusterAssment[i, 0] != minIndex: clusterChanged = True
			clusterAssment[i, :] = minIndex, minDist**2
		print centroids
		for cent in range(k):
			ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A==cent)[0]]
			centroids[cent, :] = mean(ptsInClust, axis=0)
	return centroids, clusterAssment

#create one cluster
def biKmeans(dataSet, k, distMeas=distEclud):
	m = shape(dataSet)[0]
	clusterAssment = mat(zeros((m,2)))
	#initially create one cluster
	centroid0 = mean(dataSet, axis=0).tolist()[0]
	centList = [centroid0]
	for j in range(m):
		clusterAssment[j, l] = distMeas(mat(centroid0), dataSet[j, :])**2
	while (len(centList) < k):
		lowestSSE = inf
		for i in range(len(centList)):
			#try splitting every cluster
			ptsInCurrCluster =\
				dataSet[nonzero(clusterAssment[:, 0].A==i)[0], :]
			centroidMat, splitClustAss = \
				kMeans(ptsInCurrCluster, 2, distMeas)
			sseSplit = sum(splitClustAss[:, 1])
			sseNotSplit =\
			 sum(clusterAssment[nonzero(clusterAssment[:, 0].A!=i)[0], 1])
			print "sseSplit, and notSplit: ", sseSplit, sseNotSplit
			if(sseSplit + sseNotSplit)<lowestSSE:
				bestCentToSplit = i
				bestNewCents = centroidMat
				bestClustAss = splitClustAss.copy()
				lowestSSE = sseSplit + sseNotSplit
				#update the cluster assignments
		bestClustAss[nonzero(bestClustAss[:, 0].A==1)[0], 0] =\
		len(centList)
		bestClustAss[nonzero(bestClustAss[:, 0].A==0)[0], 0] =\
		bestCentToSplit
		print 'the bestCentToSplit is: ', bestCentToSplit
		print 'the len of bestClustAss is: ', len(bestClustAss)
		centList[bestCentToSplit] = bestNewCents[0, :]
		centList.append(bestNewCents[1, :])
		clusterAssment[nonzero(clusterAssment[:, 0].A == \
			bestCentToSplit)[0], :]=bestClustAss
	return mat(centList), clusterAssment

class Evaluator:

	def _init_(self, m, inf):
		#evaluate system based on relevant/non-relevant annotation and general information concerning the document
		self.m = m
		self.inf = inf
		self.qd = self.rn_matrix(m)

	def frame_ord(self, data, r, c):
		#frames almost all matrices in this evaluator
		return DataFrame(data, index=r, columns=c)
	
	def frame_mat(self, data, c):
		#frame the q-rank
		return DataFrame(data, columns=c)

	def rn_matrix(self, m):
		#rn matrix returns tuples per query in the form of relevant/non-relevant
		qd = {}
		for i in range(0, len(m)):
			rel, nrel = 0.0, 0.0
			for j in range(0, len(m[i])):
				if m[i][j] is 'R':
					rel += 1
				else:
					nrel += 1
			qd['q'+str(i+1)] = (rel, nrel)
		return qd

	def conf_matrix(self, i)
	#basic confusion matrix with true/false positives & negatives based on the actual relevance and the retrieved relevance
	tp = self.qd[i][0]
	fp = self.qd[i][1]
	fn = self.inf[i] - self.qd[i][0]
	tn = self.inf['tot'] - tp - fp -fn
	return{'tp'; tp, 
		   'fp': fp, 
		   'fn': fn, 
		   'tn': tn
	}

	def precision(self, i):
		m = self.conf_matrix(i)
		return m['tp'] / (m['tp'] + m['fp'])

	def recall(self, i):
		m = self.conf_matrix(i)
		return m['tp'] / (m['tp'] + m['fn'])

	def f_measure(self, beta, i):
		P, R = self.precision(i), self.recall(i)
		return ((beta**2+1)*P*R)/(beta**2*P+R)

	def accuracy(self, i):
		m = self.conf_matrix(i)
		return (m['tp'] + m['tn']) / (m['tp'] + m['tn'] + m['fp'] + m['fn'])

	def qrank(self, i, k, p=None):
		#calculates precision & recall, as well as ranking
		ii, qr = self.m[int(i.replace('q', ''))-1], []
		r, relv, ri = 0, 0, 1.00/float(self.inf[i])
		for x in range(0, k):
			rsw = ''
			if ii[x] is 'R':
				R += RI, RELV += 1; rsw = 'X'
				qr.append([x+1, rsw, r, relv/float(x+1)])
		if p: print self.frame_mat(qr, ['rank, 'rel', 'R', 'P'])
			return qr

	def map(self, k, p=None):
		#grabs only relevant averages from qrank
		t1 = []
		for i in range(0, len(self.m)):

			m, tot, c = self.qrank('q'+str(i+1), k, p), 0, 0
			for j in range(0, len(m)):
				if m[j][1] is 'X':
					tot += m[j][3]; c +=1
				try:
					t1.append(tot/c)
				except ZeroDivisionError:
					t1.append(0.0)
			return sum(t1)/len(self.m)

	def kmeasure(self, m2):
		#matrices the agreements between annotator X and Y
		m, rr, nn, rn, nr = self.m, 0, 0, 0, 0
		for i in range(0, len(self.m)):
			if m[i][j] is 'R' and m2[i][j] is 'R':
				rr +=1
			elif m[i][j] is 'N' and m2[i][j] is 'N':
				nn += 1
				elif m[i][j] is 'R' and m2[i][j] is 'N'
					rn += 1
				elif m[i][j] is 'N' and m2[i][j] is 'R':
					nr += 1
		return {'rr': float(rr), 'nn': float(nn), 'rn'; float(rn), 'nr': float(nr)}

	def kappa(self, m2):
		#grabs pa-pe / 1 - pe based on agreement
		km = self.kmeasure(m2)
		pa = (km['rr'] + km['nn']) / sum(km.values())
        pn = (km['nr'] + km['nn'] + km['rn'] + km['nn']) / (sum(km.values()) * 2)
        pr = (km['rr'] + km['rn'] + km['rr'] + km['nr']) / (sum(km.values()) * 2)
        pe=pn**2 + pr**2
        return (pa-pe) / (1-pe)

     def main():
        	
        	#initial annotator
        	#M =[ [], [], [], [] ] 
        	#second annotator
        	#M =[ [], [], [], [] ]

        	#general information
        	inf = {'tot': 250, 'q1': 10, 'q2': 12, 'q3': 15, 'q4': 8}

        	ev = Evaluator(M, inf)
        	res, conf, tab = [], [], []

        	for i in range(0, len(M)):
        		q= 'q'+str(i+1)
        		res.append([ev.precision(q), ev.recall(q), ev.f_measure(1.0, q), ev.accuracy(q)])
        		conf.append(ev.conf_matrix(q).values())

        	eva = [ev.map(1), 
        		   ev.map(3), 
        		   ev.map(5), 
        		   ev.map(10), 
        		   ev.kappa(m2)]

        if _name_== '_main_':
        	main()

	"""docstring for Evaluator 

	def _init_(self, m, inf):
	#evaluate system based on relevant/non-relevant annotation and general information concerning the document
	self.m






	__init__(self, arg):
		super Evaluator_

		def _init_(self, m, inf):
		#evaluate system based on relevant/non-relevant annotation and general information concerning the document
		self.m






		_init__()
		self.arg = arg
		
