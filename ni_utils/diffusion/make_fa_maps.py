

import numpy as np
import nibabel as nib
import dipy
from dipy.io import read_bvals_bvecs
import dipy.reconst.dti as dti
from dipy.core.gradients import gradient_table

def fa_maps( target_file, bval_file, bvec_file, mask_file, out_file ):

  ##
  ## LOAD IN DATA
  ##

  scan_img = nib.load( target_file )
  scan_data = scan_img.get_data()
  img_affine = scan_img.affine

  bvals,bvecs = read_bvals_bvecs(\
    bval_file, bvec_file\
  )

  while bvecs.shape[0] < scan_data.shape[3]:
    bvecs = np.concatenate([bvecs,[[0,0,0]]],axis=0)
    bvals = np.concatenate([bvals,[0]],axis=0)
  while bvecs.shape[0] > scan_data.shape[3]:
    bvecs = bvecs[:-1,:]
    bvals = bvals[:-1]

  gtab = gradient_table(bvals, bvecs, b0_threshold=10)

  from dipy.segment.mask import median_otsu

  mask = nib.load( mask_file ).get_data()
  #maskdata, mask = median_otsu(scan_data, 3, 1, True)

  for idx in range(scan_data.shape[3]):
    scan_data[:,:,:,idx] = scan_data[:,:,:,idx] * mask

  tenmodel = dti.TensorModel(gtab)
  tenfit = tenmodel.fit(scan_data)

  from dipy.reconst.dti import fractional_anisotropy, color_fa

  FA = fractional_anisotropy(tenfit.evals)

  output_img = np.zeros(scan_data.shape[0:3])
  FA[np.isnan(FA)] = 0
  output_img[np.where(FA > 0)] = FA[np.where(FA > 0)]
  fa_img = nib.Nifti1Image(output_img.astype(np.float32), img_affine)

  nib.save(fa_img, out_file)

if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description=\
    "Generate FA measurements from DWI scan")

  parser.add_argument("--target")
  parser.add_argument("--bvals")
  parser.add_argument("--bvecs")
  parser.add_argument("--mask")
  parser.add_argument("--output")

  args = parser.parse_args()

  fa_maps( args.target, args.bvals, args.bvecs, args.mask, args.output )






