
from dipy.io.streamline import load_trk 
from dipy.io.trackvis import save_trk
import numpy as np
from dipy.tracking.life import transform_streamlines
#from nibabel.orientations import inv_ornt_aff
from nipy.algorithms.registration.affine import Affine
#from xfm.inv_affine import inv_affine
from dipy.tracking import utils


def main( args ):
  streamlines = load_trk( args.input )
  offset = np.array(streamlines[1]["dimensions"])
  vx_size = np.array(streamlines[1]["voxel_sizes"])

  FS_xfm = [
    [1.25, 0.000, 0.000, (-90) / 2],
    [0.000, 1.25, 0.000, (-126) / 2 ],
    [0.000, 0.000, 1.25, (-72) / 2],
    [0.000, 0.000, 0.000,  1.000]
  ]

  vox_to_ras = np.array([[  -1.25,    0.  ,    0.  ,   90.  ],
    [   0.  ,    1.25,    0.  , -126.  ],
    [   0.  ,    0.  ,    1.25,  -72.  ],
    [   0.  ,    0.  ,    0.  ,    1.  ]]
  )
  zooms = np.sqrt((vox_to_ras * vox_to_ras).sum(0))
  vox_to_trk = np.diag(zooms)
  vox_to_trk[3, 3] = 1
  vox_to_trk[:3, 3] = zooms[:3] / 2.

  #FS_xfm = Affine().from_matrix44(FS_xfm).inv().as_affine()
  #FS_xfm = inv_affine(np.array(FS_xfm))

  #new_streamlines = transform_streamlines(streamlines[0],FS_xfm)
  new_streamlines = utils.move_streamlines(
    streamlines[0],
    input_space=vox_to_trk,
    output_space=np.eye(4)
  )
  new_streamlines = utils.move_streamlines(
    new_streamlines,
    input_space=np.eye(4),
    output_space=FS_xfm
  )
  #new_streamlines = utils.move_streamlines(
  #  streamlines[0],
  #  input_space=vox_to_trk,
  #  output_space=vox_to_ras
  #)
  #new_streamlines = utils.move_streamlines(
  #  new_streamlines,
  #  input_space=vox_to_ras,
  #  output_space=np.eye(4)
  #)
  #new_streamlines = []
  #for idx in range(len(streamlines[0])):
  #  s = np.array(streamlines[0][idx]) - offset
  #  new_streamlines.append(s.tolist())
  #save_trk( args.output, new_streamlines, vox_to_ras, shape=offset)
  save_trk( args.output, new_streamlines, np.eye(4), shape=[0,0,0])

if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description=\
    "Test Function to Create")

  parser.add_argument("-i","--input")
  parser.add_argument("-o","--output")

  args = parser.parse_args()

  main( args )  


