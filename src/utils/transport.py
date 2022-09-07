import pypandoc
from utils import name_split


def main(filename: str, filetype: str):
    pypandoc.convert(source=filename, to=name_split.main(filename)[0][0] + '.' + filetype, format=filetype)
