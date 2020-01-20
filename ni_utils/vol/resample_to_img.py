
import nibabel as nib
import numpy as np
import nilearn

##
##
##
def main( args, verbose=1 ):

  input_img = nib.load(args.input)
  input_ref = nib.load(args.ref)

  output = nilearn.image.resample_to_img( \
    input_img, \
    input_ref, \
    interpolation=args.interp_method \
  )

  nib.save(output, args.output)

if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description=\
    "Outputs MSE between [input1] and [input2] to console. Expects 3d or 4d .nii.gz files.")

  parser.add_argument("--input")
  parser.add_argument("--ref")
  parser.add_argument("--output")
  parser.add_argument("--interp-method",default="continuous")
  parser.add_argument("--verbose",default=1,type=int)

  args = parser.parse_args()

  if args.verbose < 1:
    print("...why do this with [verbose] < 1? Function would print nothing, and is main. Aborting.")
    exit(1)

  if args.interp_method not in ["continuous","linear","nearest"]:
    print("--interp-method must be one of ['continuous','linear','nearest'], aborting")
    exit(1)

  main( args, verbose=args.verbose )




