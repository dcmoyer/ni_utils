

import csv

import numpy as np

from ni_utils.vol import make_gif, one_slice_from_list

def make_gif_seq( dim, idx, file_list, output_filename, scale=1.0, percent_max_clip=1.0, reorder=None, flip_axis=[]):

  image_block = one_slice_from_list.one_slice_from_list(dim, idx, file_list=file_list)

  for axis in flip_axis:
    image_block = np.flip(image_block, axis=axis)

  if reorder is not None:
    image_block = np.transpose(image_block, reorder)
  else:
    image_block = np.transpose( image_block, [dim] + [i for i in range(3) if i != dim] )

  image_block /= np.max(image_block) * args.percent_max_clip
  image_block = np.clip( image_block, 0, 1 )
  image_block *= 255

  #image_block = np.concatenate( [image_block, np.flip(image_block, axis=0)] )

  make_gif.gif(output_filename, image_block, fps=8, scale=scale )

if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description=\
    "Output .gif of the same slice of a list of .nii.gz files")

  parser.add_argument("--output")
  parser.add_argument("--dim", default=0, type=int)
  parser.add_argument("--idx", default=40, type=int)
  parser.add_argument('--file-list', nargs='+', default=None)
  parser.add_argument('--file-list-csv', default=None)
  parser.add_argument('--file-list-csv-col', default=0)
  parser.add_argument("--scale",default=1,type=float)
  parser.add_argument("--percent-max-clip",default=1.0,type=float)
  parser.add_argument("--reorder",nargs=3, type=int)
  parser.add_argument("--flip-axis",nargs='+', type=int, default=[])
  parser.add_argument("--every-other", default=None, type=int)

  args = parser.parse_args()

  if args.file_list is not None:
    file_list = args.file_list
  elif args.file_list_csv is not None:
    with open(args.file_list_csv, "r") as f:
      file_list = [ line[args.file_list_csv_col] for line in csv.reader(f) ]

  if args.every_other is not None:
    file_list = [filename for idx,filename in enumerate(file_list) if idx % 2 == args.every_other]

  make_gif_seq(
    args.dim, args.idx, file_list, output_filename=args.output, \
    scale=args.scale, \
    percent_max_clip=args.percent_max_clip, \
    reorder=args.reorder, flip_axis=args.flip_axis \
  )




