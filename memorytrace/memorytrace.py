__author__ = 'HarishRohini'

class MemoryTrace(object):
    """Take the mem trace file and check if the R/W address exists in the allocated range from Malloctrace"""
    def __init__(self, filename):
        super(MemoryTrace, self).__init__()
        self.filename = filename

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
