__author__ = 'HarishRohini'

import optparse
import pickle

class MemoryTrace(object):
    """Take the mem trace file and check if the R/W address exists in the allocated range from Malloctrace"""
    def __init__(self, filename, pickle_file):
        super(MemoryTrace, self).__init__()
        self.filename = filename
        self.pickle_file = pickle_file
        self.heap_read_reference = 0
        self.heap_write_reference = 0


    def process_file(self):
        with open(self.filename, 'r') as f:
            for line in f:
                split_mem_trace = line.split()
                if split_mem_trace[1] == 'R':
                    if int(self.address_range[0],16) <= int(split_mem_trace[2],16) <= int(self.address_range[1],16):
                        self.heap_read_reference += 1
                    else:
                        pass
                else:
                    if int(self.address_range[0],16) <= int(split_mem_trace[2],16) <= int(self.address_range[1],16):
                        self.heap_write_reference += 1
                    else:
                        pass
        f.close()
        #print "Read reference : ", self.heap_read_reference
        #print "Write reference : ", self.heap_write_reference


    def write_to_file():
        pass

    def process_pickle_file(self):
        f = open(self.pickle_file,'r')
        pickle_list = pickle.load(f)
        self.address_range = pickle_list[0]
        self.address_dict = pickle_list[1]
        f.close()
        #print self.address_range, self.address_dict


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f','--file',help="pinatrace.out file", dest='pinatrace_file', action='store', type='string')
    parser.add_option('-p','--pickle_file', help="Pickle file", dest = 'pickle_file', action='store', type='string')
    (opts, args) = parser.parse_args()

    if opts.pinatrace_file is None or opts.pickle_file is None:
        parser.print_help()
        exit(-1)

    memoryrtrace = MemoryTrace(opts.pinatrace_file, opts.pickle_file)
    memoryrtrace.process_pickle_file()
    memoryrtrace.process_file()
