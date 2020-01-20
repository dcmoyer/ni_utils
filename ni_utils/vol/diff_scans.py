
import nibabel as nib
import nipy
import joblib
import numpy as np
import sklearn.preprocessing as skpp

from scipy.linalg import block_diag

##
##
##
def main( args, verbose=1 ):

  scan_affine = nib.load( args.input1 ).affine
  scan1 = nib.load( args.input1 ).get_fdata() / args.norm_const
  scan2 = nib.load( args.input2 ).get_fdata() / args.norm_const

  if len(scan2.shape) > 3:
    #b0 correction
    if scan2.shape[3] < scan1.shape[3]:
      scan1 = scan1[:,:,:,:scan2.shape[3]]
    #b0 correction
    if scan1.shape[3] < scan2.shape[3]:
      scan2 = scan2[:,:,:,:scan1.shape[3]]
  #TODO:more general exception handling here

  diff = scan1 - scan2

  if args.output_diff is not None:
    diff_img = nib.Nifti1Image(diff.astype(np.float32), scan_affine)
    nib.save(diff_img, args.output_diff)

  diff = diff*diff

  if args.mask_4d is not None:
    diff = diff[:,:,:,args.mask_4d]

  if(len(diff.shape) > 3):
    diff = np.sum(diff,axis=3)

  if args.mask is not None:
    mask = nib.load( args.mask ).get_data()
    diff = diff * mask
    N = np.sum(mask)
  else:
    N = np.prod(scan1.shape)

  if args.output_err is not None:
    diff_img = nib.Nifti1Image(diff.astype(np.float32), scan_affine)
    nib.save(diff_img, args.output_err)

  if len(scan2.shape) > 3:
    N = N*scan2.shape[3]
  #TODO: outputs?

  if verbose > 0:
    print(np.sum(diff)/(N))

  if args.output_list is not None:
    x,y,z = np.where(mask > 0)
    if len(scan2.shape) > 3:
      output = diff[x,y,z].flatten() / scan2.shape[3]
    else:
      output = diff[x,y,z].flatten()
    np.savetxt(args.output_list,output,fmt="%0.6f")

  return diff

if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description=\
    "Outputs MSE between [input1] and [input2] to console. Expects 3d or 4d .nii.gz files.")

  parser.add_argument("--input1")
  parser.add_argument("--input2")
  parser.add_argument("--output-list",default=None)
  parser.add_argument("--output-diff",default=None)
  parser.add_argument("--output-err",default=None)
  parser.add_argument("--mask")
  parser.add_argument("--mask-4d", default=None, nargs="+")
  parser.add_argument("--norm-const",default=1,type=float)
  parser.add_argument("--verbose",default=1,type=int)

  args = parser.parse_args()

  main( args, verbose=args.verbose )



