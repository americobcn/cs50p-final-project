from project import app_args_parser, convert_files, look_up_files
import pytest


def test_app_args_parser_no_args(capsys):
    with pytest.raises(SystemExit):
        app_args_parser([])
    captured = capsys.readouterr()
    assert "usage: " in captured.err


def test_app_args_parser_invalid_args(capsys):
    with pytest.raises(SystemExit):
        app_args_parser(
            ["-p", "./test_files", "-i", "mp3", "-o ", "wav", "-q", "lou"]
        )  # mispelling last arg
    captured = capsys.readouterr()
    assert "usage: " in captured.err


def test_look_up_files():
    assert look_up_files("./files/no_audio_files", "wav") == []
    assert look_up_files("./files", "wav") == ["./files/SFX/0regular.wav"]
    assert len(look_up_files("./files", "mp3")) == 3


def test_convert_files(): ...
