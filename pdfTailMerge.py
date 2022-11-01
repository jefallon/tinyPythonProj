from PyPDF2 import PdfFileMerger, PdfFileReader
import argparse
import glob
from os import mkdir


def main():
    try:
        mkdir("merged")
    except:
        pass
    if args.file:
        # Specify a single file
        filenames = [args.file]
    else:
        # Append to each file in the working directory
        filenames = list(glob.iglob("*.pdf"))
        try:
            filenames.remove(args.tail)
        except:
            pass
    for filename in filenames:
        merger = PdfFileMerger()
        merger.append(PdfFileReader(open(filename, "rb")))
        merger.append(PdfFileReader(open(args.tail, "rb")))
        merger.write(f"merged/{filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tail", type=str)
    parser.add_argument("-f", "--file", type=str, required=False)
    args = parser.parse_args()
    main()
