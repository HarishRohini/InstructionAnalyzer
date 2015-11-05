__author__ = 'HarishRohini'

import optparse

class Malloctrace(object):
    """Returns a list containing the tuples of address ranges"""
    def __init__(self, filename):
        super(Malloctrace, self).__init__()
        self.filename = filename
        self.address_range_list = []
        self.address_dict = {}
        self.min_heap_address, self.max_heap_address, self.max_heap_address_allocated_bytes = 0, 0, 0

    def process_file(self):
        number_of_bytes, start_address, end_address = None, None, None
        with open(self.filename, 'r') as f:
            temp = f.readline()
            for line in f:
                if line.find('returns') != -1:
                    number_of_bytes, start_address = temp[7:-2], line[10:-1]
                    print (number_of_bytes,start_address)
                    end_address = hex(int(start_address,16) + int(number_of_bytes,16))
                    if self.min_heap_address >= int(start_address,16) or self.min_heap_address == 0:
                        self.min_heap_address = int(start_address,16)
                    if self.max_heap_address <= int(end_address,16) or self.max_heap_address == 0:
                        self.max_heap_address = int(end_address,16)
                        self.max_heap_address_allocated_bytes = int(number_of_bytes,16)
                    self.address_range_list.append((start_address,end_address))
                    self.address_dict[start_address] = number_of_bytes
                elif line.find('free') != -1:
                    self.address_dict.pop(line[5:-2],None)
                    temp = line
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
    #print malloctrace.address_dict
    #print hex(malloctrace.min_heap_address), hex(malloctrace.max_heap_address + malloctrace.max_heap_address_allocated_bytes)
