
import nibabel as nib
import nipy
from dipy.io import read_bvals_bvecs
from dipy.core.gradients import gradient_table
import joblib
import numpy as np
import sklearn.preprocessing as skpp

import shmpy
import ipmi_featurizers as ife

from scipy.linalg import block_diag

##
##
##
def main( args ):

  scan_affine = nib.load( args.input1 ).affine
  scan1 = nib.load( args.input1 ).get_fdata() / args.norm_const
  scan2 = nib.load( args.input2 ).get_fdata() / args.norm_const

  if args.mask is not None:
    mask = nib.load( args.mask ).get_data()
    scan1[np.where(mask)] = np.nan
    scan2[np.where(mask)] = np.nan

  mean1 = np.nanmean(scan1)
  mean2 = np.nanmean(scan2)

  scan1 = scan1 - mean1
  scan2 = scan2 - mean2

  corr = np.nansum(scan1*scan2)
  corr /= np.sqrt(np.nansum(scan1*scan1))
  corr /= np.sqrt(np.nansum(scan2*scan2))

  #TODO: outputs?
  print(corr)

  return

if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description=\
    "Test Function to Create")

  parser.add_argument("--input1")
  parser.add_argument("--input2")
  parser.add_argument("--mask")
  parser.add_argument("--norm-const",default=1,type=float)

  args = parser.parse_args()

  main( args )  

