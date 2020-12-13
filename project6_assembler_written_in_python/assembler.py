from sys import argv, exit
from parser import Parser


if len(argv) < 2:
    print("Missing input file")
    exit()
elif len(argv) > 2:
    print("Incorrect number of arguments. Only 1 source file accepted")
    exit()

file_source = argv[1]
filename = file_source.split(".")[0]

hack = Parser(filename, file_source)
hack.parse()
