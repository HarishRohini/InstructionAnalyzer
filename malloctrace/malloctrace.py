__author__ = 'HarishRohini'

import optparse

class Malloctrace(object):
    """Returns a list containing the tuples of address ranges"""
    def __init__(self, filename):
        super(Malloctrace, self).__init__()
        self.filename = filename
        self.address_range_list = []

    def process_file():
        pass

    def write_to_file():
        pass


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f','--file',help="malloctrace.out file", dest='malloctrace_file', action='store_true')
    (opts, args) = parser.parse_args()

    if opts.malloctrace_file is None:
        parser.print_help()
        exit(-1)
