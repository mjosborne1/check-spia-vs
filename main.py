import argparse
import os
import checker

homedir=os.environ['HOME']
parser = argparse.ArgumentParser()

outfiledefault=os.path.join(homedir,"data","check-spia-vs","spia-check-results.txt")
parser.add_argument("-o", "--outfile", help="outfile for results of the check", default=outfiledefault)
args = parser.parse_args()

print("Started")
checker.run_main(args.outfile)
print("Finished")