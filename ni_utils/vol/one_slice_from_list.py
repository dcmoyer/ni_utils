
import nibabel as nib
import joblib
import csv
import numpy as np

import os

ps = "[one_slice_from_list] "

##
##
##
def one_slice_from_list( dim, idx, file_list=None, csv_file=None, csv_col=None):

  if file_list is not None:
    pass
    #file_list = file_list
  elif csv_file is not None:
    if not os.path.exists(csv_file):
      print(ps + "csv file not found, aborting.")
      exit(1)
    with open(csv_file, "r") as f:
      try:
        file_list = [ line[csv_col] for line in csv.reader(f) ]
      except exc:
        print(ps + "csv file read error, aborting.")
        print(exc)
        exit(1)
  else:
    print("no list or csv provided, aborting")
    exit(1)

  if dim not in [0,1,2]:
    print(ps + "dim is not 0, 1, or 2, aborting")
    exit(1)

  list_of_slices = []

  for file_loc in file_list:
    scan = nib.load(file_loc)
    scan_affine = scan.affine
    scan_img = scan.get_fdata()

    if idx > scan_img.shape[ dim ]:
      print( ps + "Requested idx larger than image shape.")
      print( ps + " file: %s" % file_loc)
      print( ps + " Aborting.")
      #TODO:override?
      exit(1)

    if dim == 0:
      list_of_slices.append(scan_img[idx,:,:])
    elif dim == 1:
      list_of_slices.append(scan_img[:,idx,:])
    elif dim == 2:
      list_of_slices.append(scan_img[:,:,idx])
    else:
      print("shouldn't get here")
      exit(1)

  output = np.stack( list_of_slices, axis=dim )

  return output

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

  output = one_slice_from_list( dim=args.slice_dim, idx=args.slice_idx, file_list=args.list, csv_file=args.csv, csv_col=args.csv_col, )  

  out_img = nib.Nifti1Image(output.astype(np.float32), np.eye(4))

  nib.save(out_img, args.output_vol)


