import os
import argparse


def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_paths', type=str, nargs='+')
    args = parser.parse_args()

    for arg in args.image_paths:
        if(not os.path.isfile(arg)):
            print(f"'{arg}' not an existing file.")
            exit(1)
            
    return args.image_paths



