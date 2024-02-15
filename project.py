import sys, os, argparse


def main():
    args = app_args_parser()




def app_args_parser():
    parser = argparse.ArgumentParser(description="Scan folder ")
    parser.add_argument("-p", "--path", required=True, help="folder to lookup for audio files to be converted", type=str)
    parser.add_argument("-d", "--dest", required=True, help="Destination folder to save converted audio files", type=str)
    parser.add_argument("-l", "--log", required=True, choices=[True, False] ,help="Log while converting files", type=bool)
    return parser.parse_args()


def function_2():
    ...


def function_n():
    ...


if __name__ == "__main__":
    main()