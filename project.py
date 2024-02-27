import argparse, re
from os.path import join
from os import walk
from subprocess import Popen, PIPE


class Converter:
    """
    Implemented as Singleton

    """

    # def __new__(cls):
    #     if not hasattr(cls, "instance"):
    #         cls.instance = super(Converter, cls).__new__(cls)
    #         return cls.instance

    def __init__(self, input_format=str, output_format=str) -> None:
        self.input_format = input_format
        self.output_format = output_format

    def convert(self, input_file=str):
        codec = []
        match self.output_format:
            case ("wav", "aif"):
                codec = ["-c:a", "pcm_s24le", "-ar", "48000"]
            case "mp3":
                codec = ["-acodec", "libmp3lame", "-b:a", "320k"]
            case "aac":
                codec = ["-acodec", "aac", "-vbr", "5"]

        output_file = re.sub(
            r"(\.)" + self.input_format + r"($)",
            "." + self.output_format,
            input_file,
        )

        try:
            with Popen(
                [
                    "/usr/local/bin/ffmpeg",
                    "-i",
                    input_file,
                    *codec,
                    output_file,
                ],
                # stdout=PIPE,
                stderr=PIPE,
            ) as proc:
                error, output = proc.communicate()
                print(f"converting: '{input_file}' to '{output_file}'")
                # print(str(output, encoding="utf-8"))
                if error:
                    raise ValueError(error)

        except (OSError, ValueError) as e:
            print(e)


def app_args_parser():
    parser = argparse.ArgumentParser(description="Scan folder.")
    parser.add_argument(
        "-p",
        "--path",
        required=True,
        help="Root folder to search audio files.",
        type=str,
    )
    parser.add_argument(
        "-i",
        "--input",
        choices=["wav", "caf", "mp3", "aif"],
        required=True,
        help="Input format audio files ['wav', 'caf', 'mp3', 'aif', ...].",
        type=str,
    )
    parser.add_argument(
        "-o",
        "--output",
        choices=["wav", "aif", "aac", "mp3"],
        required=True,
        help="Output format audio files ['wav', 'aif', 'aac', 'mp3'].",
        type=str,
    )
    parser.add_argument(
        "-l",
        "--log",
        required=False,
        choices=[True, False],
        help="Log while converting files",
        type=bool,
    )
    return parser.parse_args()


def look_up_files(root_folder=str, input_format=str):
    """
    Scan folder.

    :param root_folder: Root folder to be scanned
    :type root_folder: str
    :param input_format: str 'wav, mp3, aif'
    :type input_format: str
    :return: A list fo paths
    :rtype: list
    """

    files_to_convert = []
    for root, dirs, files in walk(root_folder, onerror=handle_error):
        for f in files:
            if f.endswith(f".{input_format}"):
                files_to_convert.append(join(root, f))
    return files_to_convert


def convert_files(files=list, input_format=str, output_format=str):
    """
    Convert a list of files to output format.

    :param files: List of files to be converted
    :type root_folder: list
    :param imput_format: str 'wav, mp3, aif'
    :param output_format: str 'wav, mp3, aif'
    :type output_format: str
    """

    c = Converter(input_format, output_format)
    try:
        for f in files:
            c.convert(f)
    except ValueError:
        ...


def handle_error(error=OSError, root_folder=str):
    with open(join(root_folder, "log.txt"), "w+") as file:
        file.write(error)


def main():
    args = app_args_parser()
    files = look_up_files(args.path, args.input)
    convert_files(files, args.input, args.output)


if __name__ == "__main__":
    main()


"""
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


"""
