
from dipy.io.streamline import load_trk
from dipy.io.trackvis import save_trk
import numpy as np

def reshape_to_xyz( trk_tensor ):
  #abuses Fortran ordering
  return trk_tensor.reshape(
    (trk_tensor.shape[0], trk_tensor.shape[1] * 3),\
    order="F"\
  )

def reshape_to_Nx3( trk_tensor ):
  return trk_tensor.reshape(\
    (trk_tensor.shape[0], trk_tensor.shape[1]//3, 3 ),\
    order="F"
  )

def load_trk_tensor( filename ):
  streamlines = load_trk( filename )

  #just the coordinates
  streamlines = streamlines[0]
  the_one_true_shape = streamlines[0].shape

  #check lengths 
  for s in streamlines:
    if s.shape != the_one_true_shape:
      raise Exception(\
        "Streamlines have not been resampled to same length, aborting."
      )
      exit(1)
  return np.stack( streamlines )

##testing
if __name__ == "__main__":
  load_trk_tensor( "data/test_resamp_1000.trk" )


