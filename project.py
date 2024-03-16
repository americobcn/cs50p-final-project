import argparse, re, sys
from os.path import join, isfile
from os import walk
from subprocess import run


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class FFMPEGError(Exception):
    """Raise an error if call to ffmpeg return code is not 0"""

    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        error = "".join(self.args[0].split("\n")[-2:-1])
        return error


class Converter:
    """Convert an audio file to another supported format"""

    def __init__(
        self, input_format=str, output_format=str, root_folder=str, quality=str
    ) -> None:
        self.input_format = input_format
        self.output_format = output_format
        self.root_folder = root_folder
        self.quality = quality
        self.options = list()
        self.counter = 0

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, counter):
        self._counter = counter

    def __str__(self) -> str:
        return f"Initializing converter:\nin: {self.input_format}\nout: {self.output_format}\nq: {self.quality}"

    def convert(self, input_file=str):
        if self.quality == "high":
            match self.output_format:
                case "wav" | "aif":
                    self.options = ["-acodec", "pcm_s24le", "-ar", "48000"]
                case "mp3":
                    self.options = [
                        "-acodec",
                        "libmp3lame",
                        "-b:a",
                        "320k",
                        "-ar",
                        "48000",
                    ]
                case "aac":
                    self.options = ["-acodec", "aac", "-vbr", "5"]
        else:
            match self.output_format:
                case "wav" | "aif":
                    self.options = ["-acodec", "pcm_s16le", "-ar", "44100"]
                case "mp3":
                    self.options = [
                        "-acodec",
                        "libmp3lame",
                        "-b:a",
                        "160k",
                        "-ar",
                        "44100",
                    ]
                case "aac":
                    self.options = ["-acodec", "aac", "-vbr", "2"]

        output_file = re.sub(
            r"(\.)" + self.input_format + r"($)",
            "." + self.output_format,
            input_file,
        )

        if not isfile(output_file):
            completed = run(
                [
                    "ffmpeg",
                    "-i",
                    input_file,
                    *self.options,
                    output_file,
                ],
                # check=True,
                text=True,
                capture_output=True,
            )
            if completed.returncode != 0:
                raise FFMPEGError(completed.stderr)
            else:
                self.counter += 1
                print(
                    f"{bcolors.OKGREEN}Succes converting '{input_file}' to '{output_file}', quality: {self.quality}{bcolors.ENDC}"
                )


def app_args_parser(args):
    parser = argparse.ArgumentParser(
        description="Convert audio files starting in the 'root_folder' recursively. Save an error log file in the 'root_folder'."
    )
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
        "-q",
        "--quality",
        required=True,
        choices=["low", "high"],
        help="Set quality of converted files (default='high')",
        type=str,
    )
    return parser.parse_args(args)


def look_up_files(root_folder=str, search_format=str):
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
    for root, dirs, files in walk(root_folder, onerror=handle_walk_error):
        for f in files:
            if f.endswith(f".{search_format}"):
                files_to_convert.append(join(root, f))
    return files_to_convert


def convert_files(
    files=list, input_format=str, output_format=str, root_folder=str, quality=str
):
    """
    Convert a list of files to output format.

    :param files: List of files to be converted
    :type root_folder: list
    :param imput_format: str 'wav, mp3, aif'
    :param output_format: str 'wav, mp3, aif'
    :type output_format: str
    :type quality: str 'low, high'
    """

    c = Converter(input_format, output_format, root_folder, str(quality))
    for f in files:
        try:
            c.convert(f)

        except FFMPEGError as e:
            print(f"{bcolors.FAIL}{e}: {f}{bcolors.ENDC}")
            with open(join(root_folder, "Error_log.txt"), "a") as log_file:
                log_file.write(f"{e}: {f}\n")

    return c.counter


def handle_walk_error(error=OSError):
    print(
        f"{bcolors.FAIL}Error walking: [{error.errno}] : {error.filename}{bcolors.ENDC}"
    )
    with open(join(error.filename, "looking_log.txt"), "a") as file:
        file.write(error)


def main():
    args = app_args_parser(sys.argv[1:])
    files = look_up_files(args.path, args.input)
    converted_num = convert_files(
        files, args.input, args.output, args.path, args.quality
    )
    print(f"Succesfully converted {converted_num} files.")


if __name__ == "__main__":
    main()
