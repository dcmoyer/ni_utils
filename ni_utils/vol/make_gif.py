

import os
from moviepy.editor import ImageSequenceClip
import nibabel as nib
import numpy as np

def gif(filename, array, fps=10, scale=1.0):
    """Creates a gif given a stack of images using moviepy
    Notes
    -----
    works with current Github version of moviepy (not the pip version)
    https://github.com/Zulko/moviepy/commit/d4c9c37bc88261d8ed8b5d9b7c317d13b2cdf62e
    Usage
    -----
    >>> X = randn(100, 64, 64)
    >>> gif('test.gif', X)
    Parameters
    ----------
    filename : string
        The filename of the gif to write to
    array : array_like
        A numpy array that contains a sequence of images
    fps : int
        frames per second (default: 10)
    scale : float
        how much to rescale each image by (default: 1.0)
    """

    # ensure that the file has the .gif extension
    fname, _ = os.path.splitext(filename)
    filename = fname + '.gif'

    # copy into the color dimension if the images are black and white
    if array.ndim == 3:
        array = array[..., np.newaxis] * np.ones(3)

    # make the moviepy clip
    clip = ImageSequenceClip(list(array), fps=fps).resize(scale)
    clip.write_gif(filename, fps=fps)
    return clip

def main(args, verbose=0):
    scan = nib.load( args.input )
    scan_block = scan.get_fdata()

    if args.four_d_frame is not None:
      scan_block = scan_block[:,:,:,int(args.four_d_frame)]

    scan_block /= np.max(scan_block) * args.percent_max_clip
    scan_block = np.clip( scan_block, 0, 1 )
    scan_block *= 255

    if args.reorder is not None:
      scan_block = np.transpose(scan_block, args.reorder)

    if args.doubled:
      scan_block = np.concatenate( [scan_block, np.flip(scan_block, axis=0)] )

    gif( args.output, scan_block, fps=10, scale=args.scale)

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description=\
      "Outputs .gif of .nii.gz file, with reverse scroll")

    parser.add_argument("--input")
    parser.add_argument("--output")
    parser.add_argument("--reorder",nargs=3, type=int)
    parser.add_argument("--four-d-frame",default=None, type=int)
    parser.add_argument("--doubled",default=False,action="store_true")
    parser.add_argument("--verbose",default=1,type=int)
    parser.add_argument("--scale",default=1,type=float)
    parser.add_argument("--percent-max-clip",default=1,type=float)
  
    args = parser.parse_args()
  
    main( args, verbose=args.verbose )

    


