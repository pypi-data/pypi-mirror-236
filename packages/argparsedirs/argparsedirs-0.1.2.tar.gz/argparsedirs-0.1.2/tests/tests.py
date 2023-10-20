import argparse
import argparsedirs


def test_valid():
    parser = argparse.ArgumentParser()
    parser.add_argument('indir', action=argparsedirs.ReadableDir)
    parser.add_argument('outdir', action=argparsedirs.WriteableDir)
    parser.parse_args()


test_valid()
