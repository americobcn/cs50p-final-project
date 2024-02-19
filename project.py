import argparse, time
from os.path import join
from os import walk


class Converter:
    def __init__(self) -> None:
        pass

    @classmethod
    def convert(cls, input_file=str, output_format=str):
        # ffmpeg -i sound.caf sound.wav
        ...
        

def main():
    args = app_args_parser()
    files = look_up_files(args.path)
    convert_files(files, args.output)



def app_args_parser():
    parser = argparse.ArgumentParser(description="Scan folder ")
    parser.add_argument("-p", "--path", required=True, help="folder to lookup for audio files to be converted", type=str)
    parser.add_argument("-d", "--dest", required=True, help="Destination folder to save converted audio files", type=str)
    parser.add_argument("-i", "--input", required=True, help="Input format audio files [wav, aiff , mp3, ...]", type=str)
    parser.add_argument("-o", "--output", required=True, help="Output format audio files [wav, aiff , mp3, ...]", type=str)
    parser.add_argument("-l", "--log", required=True, choices=[True, False] ,help="Log while converting files", type=bool)
    return parser.parse_args()


def look_up_files(root_folder=str, output_format=str):
    files_to_convert = []
    for root, dirs, files in walk(root_folder):
        for f in files:
            if f.endswith(f".{output_format}"):
                files_to_convert.append(join(root, f))
    return files_to_convert


def convert_files(files=list, output_format=str):
    for f in files:
        Converter.convert(f, output_format)


if __name__ == "__main__":
    main()
    



'''
import os
from os.path import join
import time

files_to_convert = []
tic = time.perf_counter()

for root, dirs, files in os.walk("/Volumes/Library/FX"):
    for f in files:
        if f.endswith(".caf"):
            files_to_convert.append(join(root, f))


with open("files.txt", "w") as file:
    file.write("\n".join(str(path) for path in files_to_convert))


toc = time.perf_counter()

print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")

print("FIN")


'''