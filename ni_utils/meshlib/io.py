
import numpy as np

def read_meshlib( filename ):
  V = []
  F = []
  with open(filename, "r") as f:
    for line in f:
      line = line.split()
      if len(line) == 0:
        continue
      if line[0] == "Vertex":
        V.append(list(map(float,line[2:5])))
      elif line[0] == "Face":
        F.append(list(map(int,line[2:5])))
  return np.array(V),np.array(F)-1

def write_meshlib( filename, V, F ):
  F = F + 1
  with open( filename, "w") as f:
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




