
import nibabel as nib
import nipy
import joblib

import os

ps = "[one_slice_from_list] "

##
##
##
def main( args ):

  if args.list is not None:
    file_list = args.list
  elif args.csv is not None:
    if not os.path.exists(args.csv):
      print(ps + "csv file not found, aborting.")
      exit(1)
    with open(args.csv, "r") as f:
      try:
        file_list = [ line[args.csv_col] for line in csv.reader(f) ]
      except exc:
        print(ps + "csv file read error, aborting.")
        print(exc)
        exit(1)

  dim = args.slice_dim
  if dim not in [0,1,2]:
    print(ps + "slice dim is not 0, 1, or 2, aborting")
    exit(1)

  idx = args.slice_idx
  list_of_slices = []

  for file_loc in file_list:
    scan = nib.load(file_loc)
    scan_affine = scan.affine
    scan_img = scan.get_fdata()

    if idx < scan_img.shape[ dim ]:
      print( ps + "Requested idx larger than image shape.")
      print( ps + " file: %s")
      print( ps + " Aborting.")
      #TODO:override?
      exit(1)

    if dim == 0:
      list_of_slices.append(scan[idx,:,:])
    elif dim == 1:
      list_of_slices.append(scan[:,idx,:])
    elif dim == 2:
      list_of_slices.append(scan[:,:,idx])
    else:
      print("shouldn't get here")
      exit(1)

  output = np.stack( list_of_slices, axis=idx )

  out_img = nib.Nifti1Image(output.astype(np.float32), np.eye(4))

  nib.save(out_img, args.output_vol)

  return

if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description=\
    "Test Function to Create")

  parser.add_argument("--csv", default=None)
  parser.add_argument("--csv-col", default=0, type=int)
  parser.add_argument("--output-vol",default=None)
  parser.add_argument("--slice-dim", default=0, type=int)
  parser.add_argument("--slice-idx", default=40, type=int)
  parser.add_argument('--list', nargs='+', default=None)

  args = parser.parse_args()

  main( args )  




