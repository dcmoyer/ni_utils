
from dipy.io.streamline import load_trk

def main( args ):
  streamlines = load_trk( args.input )
  for key, value in streamlines[1].items():
    print(key,value)

if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description=\
    "Test Function to Create")

  parser.add_argument("-i","--input")

  args = parser.parse_args()

  main( args )  





