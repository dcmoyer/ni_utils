
import nibabel as nib
from nibabel import freesurfer as fs
import numpy as np
import inspect

def main( args ):
  surface_obj = nib.load( args.input )

  V = surface_obj.get_arrays_from_intent(1008)[0].data
  F = surface_obj.get_arrays_from_intent(1009)[0].data

  fs.write_geometry( args.output, V, F)


if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description=\
    "Test Function to Create")

  parser.add_argument("-i","--input")
  parser.add_argument("-o","--output")

  args = parser.parse_args()

  main( args )  





