


import nibabel as nib
import joblib
import numpy as np
import sklearn.preprocessing as skpp

from scipy.linalg import block_diag

from dipy.io import read_bvals_bvecs

def save_bvals_bvecs( bvals, bvecs, filename_bvals, filename_bvecs ):
  with open(filename_bvals,"w") as f:
    f.write("%0.6f" % bvals[0])
    for val in bvals[1:]:
      f.write(" %0.6f" % val)

  for dim in range(3): 
    with open(filename_bvecs,"w") as f:
      f.write("%0.6f" % bvecs[0][dim])
      for val in bvecs[1:][dim]:
        f.write(" %0.6f" % val)

def main( args ):

  #collect bvals/bvecs into lists
  bvals, bvecs = read_bvals_bvecs(\
    args.bvals, args.bvecs\
  )

  mask_4d = []
  new_bvals = []
  new_bvecs = []
  for s in args.shells:
    mask_4d += [ i for i in range(len(bvals)) if np.abs(bvals[i] - s) < args.bval_thold ]
    new_bvals += [ bvals[i] for i in range(len(bvals)) if np.abs(bvals[i] - s) < args.bval_thold ]
    new_bvecs += [ bvecs[i] for i in range(len(bvals)) if np.abs(bvals[i] - s) < args.bval_thold ]

  if len(mask_4d) == 0:
    print("No bvals in [bvals] found matching selected [shells], aborting.")
    exit(1)

  scan = nib.load( args.input )
  scan_block = scan.get_fdata()

  scan_block = scan_block[:,:,:,mask_4d]

  nib.save( nib.Nifti1Image( scan_block, scan.affine ), args.output )

  if args.output_bvals is None:
    args.output_bvals = args.output + "bvals"
  if args.output_bvecs is None:
    args.output_bvecs = args.output + "bvals"

  save_bvals_bvecs( new_bvals, new_bvecs, args.output_bvals, args.output_bvecs )

if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description=\
    "Test Function to Create")

  parser.add_argument("--input")
  parser.add_argument("--output", default=None)
  parser.add_argument("--output-bvals", default=None)
  parser.add_argument("--output-bvecs", default=None)

  parser.add_argument("--bvecs", default=None)
  parser.add_argument("--bvals", default=None)
  parser.add_argument("--bval-thold", default=25.0, type=float)
  parser.add_argument("--shells", default=None, nargs="+")

  args = parser.parse_args()

  args.shells = list(map(lambda x : float(x), args.shells))

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

  main( args )







