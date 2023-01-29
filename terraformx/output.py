# importing required modules
import argparse
 
# create a parser object
parser = argparse.ArgumentParser(description = "An addition program")
 
# arguments
parser.add_argument("-var-file", type = str, help = "Location of variable definitions file.")
parser.add_argument("-auto-approve", action="store_true", help = "Auto approve command.")
 
# parse the arguments from standard input
args = parser.parse_args()
 
# check if add argument has any input data.
print("Printing all args: %s" % args)