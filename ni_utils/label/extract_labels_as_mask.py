


import nibabel as nib
import numpy as np

def main( args ):

  scan = nib.load( args.input )
  scan_block = scan.get_fdata()
  output = np.zeros(scan.shape)

  for label in args.labels:
    output[np.where(scan_block == label)] = 1

  if args.labels_gt is not None:
    output[np.where(scan_block > args.labels_gt)] = 1

  nib.save( nib.Nifti1Image( output, scan.affine ), args.output )

if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description=\
    "Function that takes label volumes with elements in {0,1,...,K} to masks ({0,1}), given specific labels.")

  parser.add_argument("--input")
  parser.add_argument("--output", default=None)
  parser.add_argument("--labels", default=[], nargs="+")
  parser.add_argument("--labels-gt", default=None, type=int)

  args = parser.parse_args()

  args.labels = list(map(lambda x : int(x), args.labels))

  main( args )














