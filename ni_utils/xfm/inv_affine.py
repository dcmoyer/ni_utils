

import numpy as np

def inv_affine( mat ):
  A = mat[0:3,0:3]
  b = mat[0:3,3:4]
  A_inv = np.linalg.inv(A)
  return np.concatenate(
    ((np.concatenate((A_inv,-np.dot(A_inv,b)), axis=1)),
    mat[3:,:]),
    axis=0
  )





