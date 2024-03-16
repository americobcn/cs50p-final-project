from project import (
    app_args_parser,
    convert_files,
    look_up_files,
)
import pytest, os, time


def test_app_args_parser(capsys):
    """Test no arguments calling parser"""
    with pytest.raises(SystemExit):
        app_args_parser([])
    captured = capsys.readouterr()
    assert "usage: " in captured.err

    """Test invalid arguments"""
    with pytest.raises(SystemExit):
        app_args_parser(["-p", "./test_files", "-i", "mp3", "-o ", "wav", "-q", "LOU"])
    captured = capsys.readouterr()
    assert "usage: " in captured.err


def test_look_up_files():
    assert look_up_files("./files/no_audio_files", "wav") == []
    assert set(look_up_files("./files", "wav")) == set(
        [
            "./files/SFX/sfx01.wav",
            "./files/SFX/damaged_file.wav",
        ]
    )
    assert len(look_up_files("./files", "mp3")) == 3
    assert len(look_up_files("./files", "wav")) == 2


def test_convert_files(capsys):
    """Test 'Error' converting a file"""
    convert_files(
        [
            "./files/SFX/damaged_file.wav",
        ],
        "wav",
        "mp3",
        "./files",
        "low",
    )
    captured = capsys.readouterr()
    assert "Error" in captured.out

    """Test 'Succes' converting a MP3 file"""
    convert_files(
        [
            "./files/file01.mp3",
        ],
        "mp3",
        "wav",
        "./files",
        "low",
    )
    captured = capsys.readouterr()
    assert "Succes" in captured.out

    """Test 'Succes' converting a WAV file"""
    convert_files(
        [
            "./files/SFX/sfx01.wav",
        ],
        "wav",
        "aac",
        "./files",
        "low",
    )
    captured = capsys.readouterr()
    assert "Succes" in captured.out

    """Clean files created while runnig pytest"""
    os.remove("./files/SFX/sfx01.aac")
    os.remove("./files/file01.wav")


@pytest.mark.parametrize(
    "a, b, c, d, e, expected",
    [
        (
            ["./files/SFX/sfx01.wav"],
            "wav",
            "aac",
            "./files",
            "high",
            "\x1b[92mSucces converting './files/SFX/sfx01.wav' to './files/SFX/sfx01.aac', quality: high\x1b[0m",
        ),
        (
            ["./files/SFX/damaged_file.wav"],
            "wav",
            "aac",
            "./files",
            "high",
            "\x1b[91mError opening input files: Invalid data found when processing input: ./files/SFX/damaged_file.wav\x1b[0m",
        ),
    ],
)
def test_convert_files_parametrization(capsys, a, b, c, d, e, expected):
    convert_files(a, b, c, d, e)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected


def test_clean():
    """Clean files created while runnig pytest"""
    os.remove("./files/SFX/sfx01.aac")
