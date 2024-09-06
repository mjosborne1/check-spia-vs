## Installation

### Installation Requirements
- Python and the ability to install modules using pip. This will be automatic through the requirements file.

### How to install this script
   * `pip install -r requirements.txt`
   * `virtualenv env`
   * `source env/bin/activate`

### Run the script
    `python main.py -o OUTFILE`
    
    `usage: main.py [-h] [-o OUTFILE]

    options:
    -h, --help            show this help message and exit
    -o OUTFILE, --outfile OUTFILE
                            outfile for results of the check
    `

### Regenerating the requirements.txt file
If you change this code and want to regenerate the requirements use this:
   `pip freeze >| requirements.txt`