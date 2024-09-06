import argparse
import os
import checker

homedir=os.environ['HOME']
parser = argparse.ArgumentParser()
infiledefault=os.path.join(homedir,"data","check-spia-vs","RCPA---SPIA-Requesting-Pathology-Terminology-Reference-Set-3.0.1-definition.json")
outfiledefault=os.path.join(homedir,"data","check-spia-vs","spia-check-results.txt")
parser.add_argument("-i", "--infile", help="RCPA SPIA Requesting ValueSet Filename", default=infiledefault)
parser.add_argument("-o", "--outfile", help="outfile for results of the check", default=outfiledefault)
args = parser.parse_args()
print("Started")
checker.run_main(args.infile,args.outfile)
print("Finished")