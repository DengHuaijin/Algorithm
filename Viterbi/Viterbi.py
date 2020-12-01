import numpy as np

def viterbi(A, C, B, O):
	"""
	A: State transition prob matrix [I,I]
	C: Initial state distribution of dimension I
	B: Ouptut prob matrix [I,K]
	O: Observation sequence of length N
	"""
	I = A.shape[0]
	N = len(O)
	D = np.zeros(shape = [I, N])
	E = np.zeros(shape = [I, N-1]).astype(np.int32)
	D[:, 0] = np.multiply(C, B[:, O[0]])
	
	for n in range(1, N):
		for i in range(I):
			tmp_product = np.multiply(A[:, i], D[:, n-1])
			D[i, n] = np.max(tmp_product) * B[i, O[n]]
			E[i, n-1] = np.argmax(tmp_product)
			
	S_opt = np.zeros(shape = [N]).astype(np.int32)
	S_opt[-1] = np.argmax(D[:, -1])
	for n in range(N-2, 0, -1):
		S_opt[n] = E[int(S_opt[n+1]), n]
		
	return S_opt, D, E

def viterbi_log(A, C, B, O):
	I = A.shape[0]
	N = len(O)
	A_log = np.log(A + 1e-7)
	C_log = np.log(C + 1e-7)
	B_log = np.log(B + 1e-7)
	
	D_log = np.zeros(shape = [I, N])
	E = np.zeros(shape = [I, N-1]).astype(np.int32)
	D_log[:, 0] = C_log + B_log[:, O[0]]
	
	for n in range(1, N):
		for i in range(I):
			tmp_sum = A_log[:, i] + D_log[:, n-1]
			D_log[i, n] = np.max(tmp_sum) + B_log[i, O[n]]
			E[i, n-1] = np.argmax(tmp_sum)
			
	S_opt = np.zeros(shape = [N]).astype(np.int32)
	S_opt[-1] = np.argmax(D_log[:, -1])
	for n in range(N-2, 0, -1):
		S_opt[n] = E[int(S_opt[n+1]), n]
		
	return S_opt, D_log, E
	
if __name__ == "__main__":

	A = np.array([[0.8, 0.1, 0.1], 
                  [0.2, 0.7, 0.1], 
                  [0.1, 0.3, 0.6]])

	C = np.array([0.6, 0.2, 0.2])
	
	B = np.array([[0.7, 0.0, 0.3], 
                  [0.1, 0.9, 0.0], 
                  [0.0, 0.2, 0.8]])

	O = np.array([0, 2, 0, 2, 2, 1]).astype(np.int32)

	S_opt, D, E = viterbi_log(A, C, B, O)
	
	print(O)
	print(S_opt)
	np.set_printoptions(formatter = {"float": "{:7.4f}".format})
	print(D)
	print(E)
	
	