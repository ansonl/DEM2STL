import argparse, sys

from enum import Enum


class ProcessingMode(Enum):
    UNKNOWN = 0
    MANUAL = 1
    AUTO_TEMPLATE_DIR = 2
    
    @staticmethod
    def mode(input:str):
        if input == 'manual':
            return ProcessingMode.MANUAL
        if input == 'autoTemplateDir':
            return ProcessingMode.AUTO_TEMPLATE_DIR
        return ProcessingMode.UNKNOWN

def readArguments():
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # get all args after "--"
    
    def list_of_strings(a:str):
        return a.split(',')
    
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help')
    
    parser.add_argument('-mode', type=str, required=True, help='Processing mode')
    parser.add_argument('-inputFiles', type=str, nargs='*') # input files
    parser.add_argument('-outputFile', type=str) # output file
    parser.add_argument('-inputDirectory', type=str) # input directory, regions top dir
    parser.add_argument('-regex', type=str) # regex match files to import in reigon folder
    parser.add_argument('-eScaleLabel', type=str)
    parser.add_argument('-version', type=str)
    parser.add_argument('-newVersion', type=str)
    parser.add_argument('-colors', type=list_of_strings, nargs='*')
    
    parser.add_argument('-ops', required=False, nargs='*') #list of operations
    
    parsedArgs = parser.parse_args(argv)
    
    return parsedArgs