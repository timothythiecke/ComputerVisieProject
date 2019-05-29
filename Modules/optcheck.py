import os
import argparse


def getVideoPath():
    """
    Returns a list of the arguments that are passed with the script.
    """
    parser = argparse.ArgumentParser(description='This program analyses paintings from the Museum of Fine Arts, Ghent and decides in which room the painting resides. The input of this program is a video.')
    parser.add_argument('videoPath', type=str, nargs=1, help='The path to the video')
    args = parser.parse_args()

    for arg in args.videoPath:
        if(not os.path.isfile(arg)):
            print(f"'{arg}' not an existing file.")
            exit(1)

    return os.path.abspath(args.videoPath[0])
