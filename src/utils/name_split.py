import re


def main(filename: str):
    return re.compile(r"(.+)\.(.+)").findall(filename)
