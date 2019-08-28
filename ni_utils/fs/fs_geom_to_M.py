
from nibabel import freesurfer as fs


def main( args ):
  V,F = fs.io.read_geometry( args.input )

  F = F + 1

  with open(args.output, "w") as f:
    f.write("#ni_utils")

    n_verts = V.shape[0]
    n_faces = F.shape[0]

    for row in range(n_verts):
      f.write("\nVertex %i %0.6f %0.6f %0.6f {normal=(0,0,0)}" % \
        (row+1,V[row,0],V[row,1],V[row,2])
      )

    for row in range(n_faces):
      f.write(
        "\nFace %i %i %i %i " % (row+1, F[row,0], F[row,1], F[row,2])
      )


if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description=\
    "Test Function to Create")

  parser.add_argument("-i","--input")
  parser.add_argument("-o","--output")

  args = parser.parse_args()

  main( args )  




