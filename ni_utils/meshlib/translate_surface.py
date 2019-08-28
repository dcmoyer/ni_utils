
import numpy as np
from ni_utils.meshlib.io import read_meshlib, write_meshlib

def main( args ):
  V,F = read_meshlib( args.input )

  if not args.flip_after:
    if args.x_flip:
      V[:,0] = -V[:,0]
      F = F[:,[0,2,1]]
    if args.y_flip:
      V[:,1] = -V[:,1]
      F = F[:,[0,2,1]]
    if args.z_flip:
      V[:,2] = -V[:,2]
      F = F[:,[0,2,1]]

  V = V + np.array( [args.x_offset, args.y_offset, args.z_offset] )

  if args.flip_after:
    if args.x_flip:
      V[:,0] = -V[:,0]
      F = F[:,[0,2,1]]
    if args.y_flip:
      V[:,1] = -V[:,1]
      F = F[:,[0,2,1]]
    if args.z_flip:
      V[:,2] = -V[:,2]
      F = F[:,[0,2,1]]

  write_meshlib( args.output, V, F )

if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description=\
    "Test Function to Create")

  parser.add_argument("-i","--input")
  parser.add_argument("-x", "--x-offset", default=0.0, type=float)
  parser.add_argument("-y", "--y-offset", default=0.0, type=float)
  parser.add_argument("-z", "--z-offset", default=0.0, type=float)

  parser.add_argument("--x-flip", default=False, action="store_true")
  parser.add_argument("--y-flip", default=False, action="store_true")
  parser.add_argument("--z-flip", default=False, action="store_true")
  parser.add_argument("--flip-after", default=False, action="store_true")

  parser.add_argument("-o","--output")

  args = parser.parse_args()

  main( args )  

  




