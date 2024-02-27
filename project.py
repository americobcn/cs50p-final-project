import argparse, re
from os.path import join
from os import walk
from subprocess import run, CalledProcessError


class Converter:
    """ """

    def __init__(self, input_format=str, output_format=str, root_folder=str) -> None:
        self.input_format = input_format
        self.output_format = output_format
        self.root_folder = root_folder

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
            run(
                [
                    "/usr/local/bin/ffmpeg",
                    "-i",
                    input_file,
                    *codec,
                    output_file,
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            print(f"Succes converting '{input_file}' to '{output_file}'")

        except CalledProcessError as e:
            error = str(e.stderr).split("\n")[-2]
            print(f"Error: {error}")
            with open(join(self.root_folder, "Error_logs.txt"), "w+") as log_file:
                log_file.write(error)


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


def convert_files(files=list, input_format=str, output_format=str, root_folder=str):
    """
    Convert a list of files to output format.

    :param files: List of files to be converted
    :type root_folder: list
    :param imput_format: str 'wav, mp3, aif'
    :param output_format: str 'wav, mp3, aif'
    :type output_format: str
    """

    c = Converter(input_format, output_format, root_folder)

    for f in files:
        c.convert(f)


def handle_walk_error(error=OSError):
    print(f"Error walking: [{error.errno}] : {error.filename}")
    with open(join(error.filename, "looking_log.txt"), "w+") as file:
        file.write(error)


def main():
    args = app_args_parser()
    files = look_up_files(args.path, args.input)
    convert_files(files, args.input, args.output, args.path)


if __name__ == "__main__":
    main()
