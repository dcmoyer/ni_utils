
import nibabel as nib
import nipy
import joblib
import numpy as np
import sklearn.preprocessing as skpp

from scipy.linalg import block_diag

from dipy.io import read_bvals_bvecs

from ni_utils.vol import diff_scans

if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description=\
    "Test Function to Create")

  parser.add_argument("--input1")
  parser.add_argument("--input2")
  parser.add_argument("--output-list", default=None)
  parser.add_argument("--output-diff", default=None)
  parser.add_argument("--output-err", default=None)
  parser.add_argument("--mask")
  parser.add_argument("--norm-const",default=1,type=float)

  parser.add_argument("--bvecs", default=None)
  parser.add_argument("--bvals", default=None)
  parser.add_argument("--bval-thold", default=25.0, type=float)
  parser.add_argument("--shells", default=None, nargs="+")

  args = parser.parse_args()

  args.shells = list(map(lambda x : float(x), args.shells))

  args.mask_4d = None

  if args.bvecs is None and args.bvals is None:
    print("No [bvecs]/[bvals] given, using default diff_scans behavior.")
    diff_scans.main( args, verbose=1 )
    exit(0)
  elif args.bvecs is None or args.bvals is None:
    print("Both [bvals] and [bvecs] files required, aborting.")
    exit(1)
  elif args.shells is None:
    print("[shells] required for selection, aborting.")
    exit(1)

  #collect bvals/bvecs into lists
  bvals,bvecs = read_bvals_bvecs(\
    args.bvals, args.bvecs\
  )

  args.mask_4d = []
  for s in args.shells:
    args.mask_4d += [ i for i in range(len(bvals)) if np.abs(bvals[i] - s) < args.bval_thold ]

  if len(args.mask_4d) == 0:
    print("No bvals in [bvals] found matching selected [shells], aborting.")
    exit(1)

  diff_scans.main( args, verbose=1 )
  
  


