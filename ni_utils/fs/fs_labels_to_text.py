
from nibabel import freesurfer as fs
import numpy as np

from optparse import OptionParser as OP

parser = OP()
parser.add_option("-i","--input",dest="input",help="file path")
parser.add_option("-o","--output",dest="output",help="out path")
parser.add_option("-t","--roi-table",dest="roi_table",help="roi table")

##
## Parse
##

(options,args) = parser.parse_args()

##
##
##

A = fs.io.read_annot(options.input)

np.savetxt(options.output,A[0],"%d")
if options.roi_table is not None:
  f = open(options.roi_table,"w")
  for line in A[2]:
    f.write(line + "\n")
  f.close()

