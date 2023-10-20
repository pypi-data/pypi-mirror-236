import sys

import pyjaniml.converters

if __name__ == "__main__":
    file_path = sys.argv[1:][0]
    converter = pyjaniml.converters.Converter()
    _ = converter.convert_folder_and_zip(file_path)
