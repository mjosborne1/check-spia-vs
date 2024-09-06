import numpy as np
import pandas as pd
import requests
from urllib.parse import quote

import urllib 
import re
import os, io, csv
import json
from fhirpathpy import evaluate

baseurl="https://r4.ontoserver.csiro.au/fhir"
system="http://snomed.info/sct"

def path_exists(path):
    if os.path.exists(path):
        return True
    else:
        print("Warning: "+path+" does not exist, creating path.")
        os.makedirs(path, exist_ok=True)
        if os.path.exists(path):
           return True
        else:
           return False

## get_concept_all_props
## Perform a CodeSystem lookup and get all properties 
## return a json resposne from the curl call
def get_concept_all_props(code):
  cslookup='/CodeSystem/$lookup'  
  query=baseurl+cslookup+'?system='+urllib.parse.quote(system,safe='')+"&code="+code+"&property=*"
  headers = {'Accept': 'application/fhir+json'}  
  response = requests.get(query, headers=headers)
  data = response.json()
  return data


## get_snomed_props
## Expand the defining relationships (properties) of the SNOMED CT Concept
##   return a pandas data frame with the expanded properties 
def get_snomed_descriptions(code):
  # Expand the properties for the SNOMED CT concept (code)
  data=get_concept_all_props(code)
  # Evaluate a fhirpath expression to get the Concept subproperties
  expr="Parameters.parameter.where(name=\'designation\').part.valueString"
  desc_list = evaluate(data,expr)

  return desc_list


def get_spia_valueset():
    url='https://www.rcpa.edu.au/fhir/ValueSet/spia-requesting-refset-3'
    query=baseurl+'/ValueSet/$expand?url='+urllib.parse.quote(url)
    headers = {'Accept': 'application/fhir+json'}
    response = requests.get(query, headers=headers)
    data = response.json()
    codes = evaluate(data,"expansion.contains")
    return codes

def process_refset_file(infile,outfile):
    lines = []
    cnt=0
    max_displays=1
    codes = get_spia_valueset()
    for concept in codes:
        line=""
        vscode = concept["code"]
        vsdisplay = concept["display"]
        cs_concepts = get_snomed_descriptions(vscode)
        has_match="False" 
        for cs_disp in cs_concepts:
            if cs_disp.strip() == vsdisplay.strip():
                has_match = "True"
                break
        line += f'{vscode}\t{vsdisplay}\t{has_match}'
        display_count = 0
        for cs_display in cs_concepts:
           line += f'\t{cs_display}'
           display_count += 1
           if display_count > max_displays:
               max_displays = display_count
        print(line)
        lines.append(line)
    
    with open(outfile, 'w') as file:
        heading = 'VSCode\tVSDisplay\tHas Match in CS'
        for i in range(1,max_displays+1):
            heading += f'\tCS Display {i}'
        file.write(f'{heading}\n')
        for line in lines:
            file.write(line + '\n')
            cnt+=1
    
    # End 
    print(f'...{cnt} rows written to {outfile}')

def run_main(infile,outfile):
    process_refset_file(infile,outfile)