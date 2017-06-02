from extractor import Extractor
import argparse
import logging


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('images', nargs='+',
                        help='Files that contain the disk image')
    return parser.parse_args()


def main():
    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    args = parse_arguments()
    extractor = Extractor(args.images)

    print('-' * 116)
    print('| {:20} | {:20} | {:20} | {:20} | {:20} |'.format(
            'Manufacturer', 'Product', 'Serial Number',
            'Insertion time', 'Removal time'))
    print('-' * 116)

    for usb_info in extractor.get_usb_info():
        print(usb_info)

    print('-' * 116)

if __name__ == '__main__':
    main()
