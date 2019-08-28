
import nibabel as nib
import nipy
import joblib
import numpy as np
import sklearn.preprocessing as skpp

from scipy.linalg import block_diag

##
##
##
def main( args ):

  scan_affine = nib.load( args.input ).affine
  scan = nib.load( args.input ).get_fdata()

  if args.x_max is None:
    args.x_max = scan.shape[0]

  if args.y_max is None:
    args.y_max = scan.shape[1]

  if args.z_max is None:
    args.z_max = scan.shape[2]

  scan = scan[
    args.x_min:args.x_max,
    args.y_min:args.y_max,
    args.z_min:args.z_max
  ]

  diff_img = nib.Nifti1Image(scan.astype(np.float32), scan_affine)
  nib.save(diff_img, args.output)

  return

if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description=\
    "Test Function to Create")

  parser.add_argument("--input")
  parser.add_argument("--output",default=None)

  parser.add_argument("--x-min",default=0,type=int)
  parser.add_argument("--x-max",default=None,type=int)

  parser.add_argument("--y-min",default=0,type=int)
  parser.add_argument("--y-max",default=None,type=int)

  parser.add_argument("--z-min",default=0,type=int)
  parser.add_argument("--z-max",default=None,type=int)

  args = parser.parse_args()

  main( args )  




