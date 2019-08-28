



def main( args ):
  args.target = list(map(lambda x: int(x),args.target))

  with open(args.output,"w") as output_file:
    with open(args.input,"r") as input_file:
      first_line = True

      for line in input_file:
        label = int(line[:-1])

        if first_line:
          first_line = False
        else:
          output_file.write("\n")

        if (args.reverse and label not in args.target) or \
          (label in args.target):
          output_file.write("1")
        else:
          output_file.write("0")



if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description=\
    "Takes label .txt files to binary masks through listed targets.")

  parser.add_argument("-i","--input")
  parser.add_argument("-o","--output")
  parser.add_argument("-t","--target",nargs="+")
  parser.add_argument("-r","--reverse",action="store_true",default=False)

  args = parser.parse_args()

  main( args )  







