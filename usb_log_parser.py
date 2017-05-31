from extractor import Extractor
import argparse
import logging


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('images', nargs='+',
                        help='Files that contain the disk image')
    return parser.parse_args()


logging.basicConfig(filename='debug.log', level=logging.DEBUG)
args = parse_arguments()
extractor = Extractor(args.images)

for usb_info in extractor.get_usb_info():
    print(usb_info)
