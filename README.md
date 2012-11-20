#Pftree

## About
_Pftree_ is simple wrapper for the Apache Preflight _PDF/A-1b_ validator (which is part of the _PDFBox_ library). The wrapper processes all files in a directory tree that have a _.pdf_ extension, and then reports the results as nicely formatted XML file.

Note that this software was written for demonstrational purposes only; for a stable production solution it would
be better to add an XML output handler directly to Apache Preflight, and this is really just a quick & dirty solution to streamline my Preflight tests without having to go into any Java code!

Development partially supported by the [SCAPE][4] Project. The SCAPE project is co-funded by the European Union under FP7 ICT-2009.4.1 (Grant Agreement number 270137).


## Command line use

#### Usage
`pftree.py [-h] [-v] p2In`

#### Positional arguments

`dirIn` : input directory tree

#### Optional arguments

`-h, --help` : show help message and exit

`-v, --version` : show program's version number and exit

## Output 
Output is directed to the standard output device (_stdout_).

#### Example

`pftree.py d:\data\Isartor_testsuite >isartor_Preflight.xml`

In the above example, output is redirected to the file 'isartor_Preflight.xml'.


[4]: http://www.scape-project.eu/