
import pydicom as pdc
import argparse

parser = argparse.ArgumentParser(description=\
  "Dumps Dicom headers into stdout")

parser.add_argument("input",default=None)

args = parser.parse_args()

if not args.input:
  print("requires dcm as input")

dcm = pdc.dcmread(args.input)

print(dcm)

