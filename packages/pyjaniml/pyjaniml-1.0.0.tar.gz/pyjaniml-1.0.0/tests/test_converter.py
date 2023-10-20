from pathlib import Path

import pytest

from pyjaniml.converters import Converter
from pyjaniml.janiml_schema import ExperimentStepSchema

FIXTURE_DIR = Path(__file__).resolve().parent / "test_files"


@pytest.mark.parametrize("file", [FIXTURE_DIR / "ewa_as_opus.0"])
def test_opus_converter(file):
    converter = Converter()
    janiml = converter.from_opus_file(file)
    json = ExperimentStepSchema().dumps(janiml)
    assert json


@pytest.mark.parametrize("file_path", [FIXTURE_DIR])
def test_opus_converter_on_folder(file_path):
    converter = Converter()
    _ = converter.convert_folder_and_zip(file_path)
