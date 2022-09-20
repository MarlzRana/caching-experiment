import hashlib
import argparse


def mangle(n):
    string = str(n ^ 3).encode()
    return hashlib.md5(string).hexdigest()[:8]


def sample_data(size=100):
    return [mangle(n) for n in range(0, size)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size',
                        help='size of memory',
                        type=int,
                        default=100)
    parser.add_argument('-o', '--output',
                        help='output file',
                        default="data.txt")

    args = parser.parse_args()
    with open(args.output, 'w') as output_file:
        for datum in sample_data(size=args.size):
            output_file.write("{}\n".format(datum))
