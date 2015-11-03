__author__ = 'HarishRohini'

import optparse

class Malloctrace(object):
    """Returns a list containing the tuples of address ranges"""
    def __init__(self, filename):
        super(Malloctrace, self).__init__()
        self.filename = filename
        self.address_range_list = []

    def process_file(self):
        number_of_bytes, start_address = None, None
        with open(self.filename, 'r') as f:
            temp = f.readline()
            for line in f:
                if line.find('returns') != -1:
                    number_of_bytes, start_address = temp[7:-2], line[10:-1]
                    print (number_of_bytes,start_address)
                else:
                    temp = line

    def write_to_file():
        pass


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f','--file',help="malloctrace.out file", dest='malloctrace_file', action='store', type='string')
    (opts, args) = parser.parse_args()

    if opts.malloctrace_file is None:
        parser.print_help()
        exit(-1)

    malloctrace = Malloctrace(opts.malloctrace_file)
    malloctrace.process_file()
