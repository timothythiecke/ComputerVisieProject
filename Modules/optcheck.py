import os
import argparse


def getArguments():
    """
    Returns a list of the arguments that are passed with the script.
    """
    parser = argparse.ArgumentParser(description='This program analyses paintings from the Museum of Fine Arts, Ghent and decides in which room the painting resides. The input of this program is a photograph of a painting in the museum.')
    parser.add_argument('imagePath', type=str, nargs='+', help='The path to the image')
    args = parser.parse_args()

    for arg in args.imagePath:
        if(not os.path.isfile(arg)):
            print(f"'{arg}' not an existing file.")
            exit(1)
    return args.imagePath
