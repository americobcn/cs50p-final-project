# Audio Converter Utility

## Video Demo: `Link to url`

### Description: Audio Converter Utility is a solution for audio file conversion that uses [FFMPEG](https://www.ffmpeg.org/) in the background. Search files recursively in a `root_folder`, raise an `FFMPEGError` exception if the conversion failed saving a log file called `Error_log.txt` in the root folder with information about the error and the path of the file that caused the exception and prints info for `succes` or `error` status while converting files. Any OSError produced while scanning root folder and subfolders will be printed and logged into a file called `OSError_log.txt` in the current scanned folder

- `Converter`class implement conversion funcionality, it is initialized with the parameters needed to perform the batch conversion.

  - **input_format:** the format of the files to look for.
  - **output_format**: the destinaton format that audio files will be converted to.
  - **root_folder**: the path to start looking for audio files.
  - **quality**: defines the preset that will be used to convert files.
  - **options**: an empty list to add the options that will be passed to `subprocess.run` call, it depends on `output_format` and `quality`parameters.
  - **counter**: a property to track the number audio files succesfully converted
  - **convert()**: a function that accepts one argument, the path of the audio file to convert. Set the options needed to perform the call to `ffmpeg` command line application via `subprocess.run` function. Create the output file name using de `re` module. Raise an `FFMPEGError` passing the `stderr` to `FFMPEGError`class. Print succes info to the terminal and update `counter` property.

- `FFMPEGError`class sublcass `Exception` class to catch `fffmpeg` errors.
- `bcolors` class is used to customize strings colors in the `stdout`.

Functions:

- `app_args_parser`: Handle the arguments needed and provide help to users. Returns a `parser` object.
- `look_up_files`: Search audio files recursively in the `root_folder` returning a list of path files.
- `convert_files`: Create a `Converter` object used to perform the audio conversion. Return an `Int` with the number of files succesfully converted. Raise an `FFMPEGError` when the conversion failed, print a message of the error and log into an `Error_log.txt` file.
- `handle_walk_error`: Print and log `OSError` into a file while scanning folders and subfolders.

Example:

```python
python project.py -p audio_files_folder -i wav -o mp3 -q high

```

| Options      | Description                                                |
| ------------ | ---------------------------------------------------------- |
| -p --path    | Path to the root folder where audio files are stored       |
| -i --input   | The original format to look for (wav,aif,aac,mp3)          |
| -o --output  | The output format to convert audio files (wav,aif,aac,mp3) |
| -q --quality | The quality of the output format audio file (low , high )  |

Audio Converter Utility simplifies the process of transforming audio files into the format you need. With support for a wide range of formats, including MP3, WAV, and AIF, Audio Converter Utility ensures compatibility and flexibility for all your audio projects.

### Key Features

1. **Effortless Conversion:** With a simple CLI command, Audio Converter Utility swiftly converts audio files from one format to another.

2. **Wide Format Support:** Flexibility of converting to and from popular audio formats such as MP3, WAV, and AIF, ensuring compatibility with various devices and software.

3. **High-Quality Output:** Choose the quality of the output format between high and low.

4. **Batch Processing:** Convert multiple audio files on one call.

5. **Cross-Platform Compatibility:** Whether you're using Windows, macOS, or Linux, Audio Converter Utility is compatible with all major operating systems, ensuring seamless integration into your workflow.

#### Requirements: In order to run the script you must install [FFMPEG](https://www.ffmpeg.org/download.html) in your system
