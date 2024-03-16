# Audio Converter Utility

## Video Demo: Link to url

### Description: Audio Converter Utility is a solution for audio file conversion that uses [FFMPEG](https://www.ffmpeg.org/) in the background. Search files recursively in the `root_folder`, raise an `FFMPEGError` exception if the conversion failed saving a log file called `Error_log.txt` in the root folder whith information about the error and the path of the file that caused the exception and prints info for `succes` or `error` status while converting files

- `Converter`class implement conversion funcionality.
- The `Converter` class uses the `subprocess` module to call `ffmpeg` applcation passing the arguments needed to perform the batch processing.
- `FFMPEGError`class sublcass `Exception` class to catch `fffmpeg` errors.
- `bcolors` class is used to customize strings colors in the `stdout`.

Functions:

- `app_args_parser`: Handle the arguments needed and provide help to users. Return a `parser` object.
- `look_up_files`: Search audio files recursively in the `root_folder` returning a list of path files.
- `convert_files`: Create a `Converter` object used to perform the audio conversion. Return an `Int` with the number of files succesfully converted. Raise an `FFMPEGError` when the conversion failed.

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

Audio Converter Utility simplifies the process of transforming your audio files into the format you need. With support for a wide range of formats, including MP3, WAV, and AIF, Audio Converter Utility ensures compatibility and flexibility for all your audio projects.

### Key Features

1. **Effortless Conversion:** With a simple CLI command, Audio Converter Utility swiftly converts audio files from one format to another.

2. **Wide Format Support:** Enjoy the flexibility of converting to and from popular audio formats such as MP3, WAV, and AIF, ensuring compatibility with various devices and software.

3. **High-Quality Output:** Choose the quality of the output format.

4. **Batch Processing:** Convert multiple audio files simultaneously, streamlining your workflow and boosting productivity.

5. **Cross-Platform Compatibility:** Whether you're using Windows, macOS, or Linux, Audio Converter Utility is compatible with all major operating systems, ensuring seamless integration into your workflow.

With Audio Converter Utility, transforming your audio files has never been easier. Say goodbye to compatibility issues and hello to seamless conversion.

#### Requirements: In order to run the script you must install [FFMPEG](https://www.ffmpeg.org/download.html) in your system
