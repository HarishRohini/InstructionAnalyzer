__author__ = 'HarishRohini'

import optparse
import pickle

class MemoryTrace(object):
    """Take the mem trace file and check if the R/W address exists in the allocated range from Malloctrace"""
    def __init__(self, filename, pickle_file, memreference_file):
        super(MemoryTrace, self).__init__()
        self.filename = filename
        self.pickle_file = pickle_file
        self.memreference_file = memreference_file
        self.heap_read_reference = 0
        self.heap_write_reference = 0
        self.heap_ref_read_dict = {}
        self.heap_ref_write_dict = {}
        self.number_of_bytes_allocated = 0
        self.program_counter_addresses = set()
        self.memreference_dict = {}


    def process_file(self):
        with open(self.filename, 'r') as f:
            for line in f:
                split_mem_trace = line.split()
                if len(split_mem_trace) <= 2:
                    continue
                self.program_counter_addresses.add(split_mem_trace[0])
                if split_mem_trace[1] == 'R':
                    if int(self.address_range[0],16) <= int(split_mem_trace[2],16) <= int(self.address_range[1],16):
                        if int(split_mem_trace[2],16) in self.heap_ref_read_dict:
                            self.heap_ref_read_dict[int(split_mem_trace[2],16)] += self.memreference_dict[split_mem_trace[0][:-1]]
                        else:
                            self.heap_ref_read_dict[int(split_mem_trace[2],16)] = self.memreference_dict[split_mem_trace[0][:-1]]
                        self.heap_read_reference += 1
                    else:
                        pass
                else:
                    if int(self.address_range[0],16) <= int(split_mem_trace[2],16) <= int(self.address_range[1],16):
                        if int(split_mem_trace[2],16) in self.heap_ref_write_dict:
                            self.heap_ref_write_dict[int(split_mem_trace[2],16)] += self.memreference_dict[split_mem_trace[0][:-1]]
                        else:
                            self.heap_ref_write_dict[int(split_mem_trace[2],16)] = self.memreference_dict[split_mem_trace[0][:-1]]
                        self.heap_write_reference += 1
                    else:
                        pass
        f.close()
        #print "Read reference : ", self.heap_read_reference
        #print "Write reference : ", self.heap_write_reference


    def write_to_file(self):
        f = open('heap_trace_read.in','wb')
        temp_list = [] #first element tuple, second dictionary
        temp_list.append((self.heap_read_reference, self.heap_write_reference))
        temp_list.append(self.heap_ref_read_dict)
        #print temp_list
        pickle.dump(temp_list,f)
        f.close()

        f = open('heap_trace_write.in','wb')
        temp_list = [] #first element tuple, second dictionary
        temp_list.append((self.heap_read_reference, self.heap_write_reference))
        temp_list.append(self.heap_ref_write_dict)
        #print temp_list
        pickle.dump(temp_list,f)
        f.close()


    def process_pickle_file(self):
        f = open(self.pickle_file,'rb')
        pickle_list = pickle.load(f)
        self.address_range = pickle_list[0]
        self.address_dict = pickle_list[1]
        self.number_of_bytes_allocated = pickle_list[2]
        f.close()
        #print self.address_range, self.address_dict

        f = open(self.memreference_file,'rb')
        pickle_list = pickle.load(f)
        self.memreference_dict = pickle_list[0]
        f.close()

    def percentage_reference(self):
        #number_of_bytes_refereced_read = len(self.heap_ref_read_dict) * 1.0 # *4.0
        #number_of_bytes_refereced_write = len(self.heap_ref_write_dict) * 1.0 # *4.0
        number_of_bytes_refereced_read = reduce(lambda x, y: x + y, self.heap_ref_read_dict.values()) * 1.0
        number_of_bytes_refereced_write = reduce(lambda x, y: x + y, self.heap_ref_write_dict.values()) * 1.0
        print ("Num of Bytes allocated : ", self.number_of_bytes_allocated)
        print ("Percentage_read_reference : ", number_of_bytes_refereced_read / self.number_of_bytes_allocated)
        print ("Percentage_write_reference : " , number_of_bytes_refereced_write / self.number_of_bytes_allocated)


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f','--file',help="pinatrace.out file", dest='pinatrace_file', action='store', type='string')
    parser.add_option('-p','--pickle_file', help="Pickle file", dest = 'pickle_file', action='store', type='string')
    parser.add_option('-m','--memreference_pickle_file', help="memreference file", dest='memreference_file', action='store', type='string')
    (opts, args) = parser.parse_args()

    if opts.pinatrace_file is None or opts.pickle_file is None or opts.memreference_file is None:
        parser.print_help()
        exit(-1)

    memoryrtrace = MemoryTrace(opts.pinatrace_file, opts.pickle_file, opts.memreference_file)
    memoryrtrace.process_pickle_file()
    memoryrtrace.process_file()
    memoryrtrace.percentage_reference()
    memoryrtrace.write_to_file()
    #print memoryrtrace.heap_ref_read_dict
    #print memoryrtrace.heap_ref_write_dict
    print "Unique program counter : ", len(memoryrtrace.program_counter_addresses)
