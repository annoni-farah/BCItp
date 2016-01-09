'''
	def compute_calibration(self):
		X=self.importa(self.globalpath+'/users/%s/samples.txt' %self.user)
		Y=self.importa(self.globalpath+'/users/%s/marcas.txt' %self.user)
	
		ind_T = np.argsort(Y[1].A1)
		Y[1] = Y[1].A1[ind_T]
		Y[0] = Y[0].A1[ind_T]
		X_bp=np.matrix(sig.convolve(X,self.fir))
		X_T=[X_bp.T[y+3*250:y+6*250].T for y in Y.tolist()[0]]
		Xclass=[X_T[self.number_trials*element:self.number_trials*(element+1)] for element in range(len(self.classes))]
		Cclass_ = [[cov_(X) for X in element] for element in Xclass]
		Cclass = [sum(element)/len(element) for element in Cclass_]	
		Csum = [Cclass[element[0]]+Cclass[element[1]] for element in list(combinations(range(len(Cclass)),2))]
		Eighenval = [np.linalg.eigh(element) for element in Csum]
		for ind in range(len(Eighenval)):
			V1 = Eighenval[ind][1][:,np.argsort(Eighenval[ind][0])]
			V0 = np.matrix(np.diag(Eighenval[ind][0][np.argsort(Eighenval[ind][0])]))
			Eighenval[ind]=[V0,V1]
		Q = [np.sqrt(element[0].I)*element[1].T for element in Eighenval]
		Eighenval2 = [np.linalg.eigh(element2*Cclass[element[0]]*element2.T) for element,element2 in zip(list(combinations(range(len(Cclass)),2)),Q)]
		for ind in range(len(Eighenval2)):
			V1 = Eighenval2[ind][1][:,np.argsort(Eighenval2[ind][0])]
			V0 = np.matrix(np.diag(Eighenval2[ind][0][np.argsort(Eighenval2[ind][0])]))
			Eighenval2[ind]=[V0,V1]
		W = [element[1].T*element2 for element,element2 in zip(Eighenval2,Q)]
		W_n=3
		W_ = [element[np.arange(W_n).tolist() + sorted((-1-np.arange(W_n)).tolist())] for element in W]
		[Cclass[element[0]]+Cclass[element[1]] for element in list(combinations(range(len(Cclass)),2))]
		[Za,Zb] for element,element2 in zip(list(combinations(range(len(Cclass)),2)),W_) 
		Za = np.matrix((np.log10([np.diag(x) for x in [W_*X*W_.T for X in Ca_]])).T)
		Zb = np.matrix((np.log10([np.diag(x) for x in [W_*X*W_.T for X in Cb_]])).T)
		Ma, Mb = (sum(Za.T).T/len(Za.T)), (sum(Zb.T).T/len(Zb.T))
		Sa, Sb = (Za*Za.T - Ma*Ma.T), (Zb*Zb.T - Mb*Mb.T)
		W2 = (Sa + Sb).I * (Ma - Mb)
		self.W_lda=W2
		L = W2.T * (Ma + Mb) * 0.5
		self.L=L
'''
