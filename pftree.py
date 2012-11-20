#! /usr/bin/env python
#
# Wrapper for Apache Preflight (PDFBox) that processes all PDF files
# in a directory tree and then reports results as nicely formatted XML file.
#
# For demonstrational purposes only; for a stable production solution it would
# be better to add an XML output handler directly to Apache Preflight, and
# this is just a quick & dirty solution to streamline my Preflight tests without
# having to go into any Java code!
#
# Requires Python v. 2.7 OR Python 3.2 or better 
# Apache Preflight requires Java
#
# Apache Preflight / Apache PDFBox are published under the Apache License v2.0
#
#
# Copyright 2012 Johan van der Knijff / The SCAPE Project Consortium
#
# This software is copyrighted by the SCAPE Project Consortium.
# The SCAPE project is co-funded by the European Union under
# FP7 ICT-2009.4.1 (Grant Agreement number 270137).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
import imp
import argparse
import subprocess as sub
import etpatch as ET
from glob import glob

scriptPath, scriptName = os.path.split(sys.argv[0])

__version__= "0.1.0"

def main_is_frozen():
    return (hasattr(sys, "frozen") or # new py2exe
            hasattr(sys, "importers") # old py2exe
            or imp.is_frozen("__main__")) # tools/freeze

def errorExit(msg):
    msgString=("Error: " + msg + "\n")
    sys.stderr.write(msgString)
    sys.exit()

def get_main_dir():
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(sys.argv[0])

def getFilesFromTree(rootDir):
    # Recurse into directory tree and return list of all files
    # NOTE: directory names are disabled here!!

    filesList=[]
    for dirname, dirnames, filenames in os.walk(rootDir):
        #Suppress directory names
        for subdirname in dirnames:
            thisDirectory=os.path.join(dirname, subdirname)

        for filename in filenames:
            thisFile=os.path.join(dirname, filename)
            filesList.append(thisFile)
    return filesList

def parseFile(fileObject):
    parser = xml.parsers.expat.ParserCreate()
    parser.ParseFile(fileObject)
                      
def parseCommandLine():
    # Create parser
    parser = argparse.ArgumentParser(description="Analyse PDF files in directory tree with Apache Preflight (PDFBox)",version=__version__)

    # Add arguments
    parser.add_argument('dirIn', action="store", help="input directory tree")
    # Parse arguments
    args=parser.parse_args()
    
    return(args)
    
def getErrors(output):
    # Parse preflight output and return error codes and descriptions as element object
    
    errorsElt=ET.Element("errors")
    outputLines=output.split('\n')
    noLines=len(outputLines)
    
    # Loop through output, skip 1st line which doesn't contain any useful info
    for i in range(1,noLines):
        thisLine=outputLines[i]
        thisLineItems=thisLine.split(":")
        
        noItems=len(thisLineItems)
        
        if noItems>=2:
            thisErrorCode=thisLineItems[0]
            
            thisErrorDescription=thisLineItems[1]
            
            # Some silly looking code but error descriptions may contain colons
            if noItems>2:
                for j in range (2,noItems):
                    thisErrorDescription = thisErrorDescription + ":" + thisLineItems[j]
                       
            thisErrorCode.strip()
            thisErrorDescription.strip()
            
            errorElt=ET.Element("error")
            errorElt.appendChildTagWithText("code", thisErrorCode)
            errorElt.appendChildTagWithText("description", thisErrorDescription)            
            errorsElt.append(errorElt)
 
    return(errorsElt)
    
def main():
    
    # From where is this script executed?)
    applicationPath=os.path.abspath(get_main_dir())

    # Path to Preflight app
    preflightApp=os.path.normpath(applicationPath+ "/preflight/preflight-1.8.0-20121114.230701-58-jar-with-dependencies.jar")
    
    # Command to launch preflight (may not work on all platforms, ideally move
    # this all to separate config file instead of hard-coding it)
    preflightCommand="java -jar " + preflightApp

    # Get input from command line
    args=parseCommandLine()
    dirIn=args.dirIn

    # Check if dirIn is directory (and exit if not)
    if os.path.isdir(dirIn)==False:
        msg=dirIn + " is not a directory!"
        errorExit(msg)
               
    # Create output elementtree object
    root=ET.Element('preflight')
                        
    # Generate list of files to process
    myFilesIn=getFilesFromTree(dirIn)
    numberOfFiles=len(myFilesIn)

    for i in range(0,numberOfFiles):

        myFileIn=myFilesIn[i]
        
        fileElt=ET.Element("file")
        
        fileElt.appendChildTagWithText("fileName", myFileIn)
        
        if myFileIn.lower().endswith(".pdf"):
            
            systemString= preflightCommand + ' "' + myFileIn + '"'
            
            p = sub.Popen(systemString,stdout=sub.PIPE,stderr=sub.PIPE)
            output, errors = p.communicate()
                    
            # Extract error codes and descriptions from output
            errorCodesDescs=getErrors(output)
            
            if len(errorCodesDescs)!=0:
                # Errors were found, so not valid
                isValidPDFA1b="False"
                
                # Add errors codes + descriptions to output
                fileElt.append(errorCodesDescs)           
            
            else:
                # No errors found, so valid
                isValidPDFA1b="True"
            
            # Append validation outcome to output
            fileElt.appendChildTagWithText("isValidPDFA1b", isValidPDFA1b)
            
            # Add output to root element 
            root.append(fileElt)              
    
    # Write xml-formatted log to stdout
    sys.stdout.write(root.toxml().decode('UTF-8'))

if __name__ == "__main__":
    main()








