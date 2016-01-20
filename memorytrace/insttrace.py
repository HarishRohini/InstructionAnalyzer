__author__ = 'HarishRohini'

import optparse
import pickle
import os
import address_range

class InstructionTrace(object):
    """docstring for InstructionTrace"""
    def __init__(self, filename, memreference_file):
        super(InstructionTrace, self).__init__()
        self.filename = filename
        self.memreference_file = memreference_file
        self.address_range_list = []
        self.address_dict = {}
        self.memreference_dict = {}
        self.heap_ref_read_dict = {}
        self.heap_ref_write_dict = {}
        self.malloc_block_dict = {}
        self.min_heap_address, self.max_heap_address, self.max_heap_address_allocated_bytes = 0, 0, 0
        self.number_of_bytes_allocated = 0
        self.heap_read_reference, self.heap_write_reference = 0, 0
        self.count = 0

    def update_min_max_heap_address(self, min_address, max_address):
        if self.min_heap_address >= min_address or self.min_heap_address == 0:
            self.min_heap_address = min_address
        if self.max_heap_address <= max_address or self.max_heap_address == 0:
            self.max_heap_address = max_address


    def get_malloc_block(self, addr_range, search_addr):
        result = None
        if len(addr_range) == 1:
            result = (hex(addr_range[0]), hex(self.address_dict[addr_range[0]]))
            #return (hex(addr_range[0]), hex(self.address_dict[addr_range[0]]))
        else:
            for i in addr_range:
                #print self.count
                if i <= search_addr <= self.address_dict[i]:
                    result =  (hex(i), hex(self.address_dict[i]))
        return result


    def process_rws(self, rw_list):
        pc_address = rw_list[0]
        mem_address = int(rw_list[2], 16)
        if rw_list[1] == 'R':
            if self.min_heap_address <= mem_address <= self.max_heap_address:
                #get the malloc block it belongs to
                #get the bytes referenced using assembly_trace.out
                #Update the Malloc Block bytes counter
                bytes_referenced = self.memreference_dict[pc_address]
                result = address_range.binarySearchRange(self.address_range_list, mem_address)
                malloc_block = self.get_malloc_block(result, mem_address)
                if malloc_block in self.malloc_block_dict:
                    self.malloc_block_dict[malloc_block] += 1 #bytes_referenced
                else:
                    self.malloc_block_dict[malloc_block] = 1 #bytes_referenced
                if mem_address in self.heap_ref_read_dict:
                    self.heap_ref_read_dict[mem_address] += bytes_referenced
                else:
                    self.heap_ref_read_dict[mem_address] = bytes_referenced
                self.heap_read_reference += 1
            else:
                pass
        else:
            if self.min_heap_address <= mem_address <= self.max_heap_address:
                #get the malloc block it belongs to
                #get the bytes referenced using assembly_trace.out
                #Update the Malloc Block bytes counter
                bytes_referenced = self.memreference_dict[pc_address]
                result = address_range.binarySearchRange(self.address_range_list, mem_address)
                malloc_block = self.get_malloc_block(result, mem_address)
                if malloc_block in self.malloc_block_dict:
                    self.malloc_block_dict[malloc_block] += 1 #bytes_referenced
                else:
                    self.malloc_block_dict[malloc_block] = 1 #bytes_referenced
                if mem_address in self.heap_ref_write_dict:
                    self.heap_ref_write_dict[mem_address] += bytes_referenced
                else:
                    self.heap_ref_write_dict[mem_address] = bytes_referenced
                self.heap_write_reference += 1
            else:
                pass


    def process_file(self):
        allocated_size, start_address, end_address,realloc_ptr = None, None, None, None
        with open(self.filename, 'r') as f:
            for line in f:
                self.count += 1
                if line.find("malloc") != -1:
                    malloc_list = line.split(" : ")
                    allocated_size = int(malloc_list[0][7:-1], 16)
                    start_address = int(malloc_list[1], 16)
                    end_address = start_address + allocated_size
                    self.number_of_bytes_allocated += allocated_size
                    self.update_min_max_heap_address(start_address, end_address)
                    if start_address not in self.address_range_list:
                        self.address_range_list.append(start_address)
                    self.address_range_list.sort()
                    self.address_dict[start_address] = end_address
                elif line.find("calloc") != -1:
                    calloc_list = line.split(" : ")
                    num_elements = int(calloc_list[0].split(',')[0][7:], 16)
                    element_size = int(calloc_list[0].split(',')[1][:-1], 16)
                    start_address = int(calloc_list[1], 16)
                    end_address = start_address + num_elements * element_size
                    self.update_min_max_heap_address(start_address, end_address)
                    self.address_range_list.append(start_address)
                    self.address_range_list.sort()
                    self.address_dict[start_address] = end_address
                elif line.find("realloc") != -1:
                    realloc_list = line.split(" : ")
                    realloc_ptr = int(realloc_list[0].split(',')[0][8:], 16)
                    realloc_size = int(realloc_list[0].split(',')[1][:-1], 16)
                    start_address = int(realloc_list[1], 16)
                    end_address = start_address + realloc_size
                    # if start address in dictionary update it else treat it as a malloc
                    self.update_min_max_heap_address(start_address, end_address)
                    if realloc_ptr != start_address:
                        self.address_dict.pop(realloc_ptr, None)
                        self.address_range_list.remove(realloc_ptr)
                        if start_address not in self.address_range_list:
                            self.address_range_list.append(start_address)
                    self.address_range_list.sort()
                    self.address_dict[start_address] = end_address
                elif line.find("free") != -1:
                    free_ptr = int(line[5:-2], 16)
                    free_ptr_hex = line[5:-2]
                    # delete the start_address in the dictionary
                    #print "free_ptr", free_ptr
                    #free Malloc Block dictionary
                    end_address_hex = hex(self.address_dict[free_ptr])
                    if (free_ptr_hex, end_address_hex) in self.malloc_block_dict:
                        print "Malloc Block : ", (free_ptr_hex, end_address_hex), self.malloc_block_dict[(free_ptr_hex, end_address_hex)]
                        self.malloc_block_dict.pop((free_ptr_hex, end_address_hex), None)
                    self.address_dict.pop(free_ptr, None)
                    self.address_range_list.remove(free_ptr)
                    self.address_range_list.sort()

                elif len(line.split()) == 3:
                    self.process_rws(line.split())
                else:
                    print "Unknown text : ", line
                if len(self.address_dict) != len(self.address_range_list):
                    print "lenght : ", self.count

        f.close()

    def process_pickle_file(self):
        f = open(self.memreference_file,'rb')
        pickle_list = pickle.load(f)
        self.memreference_dict = pickle_list[0]
        f.close()


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f','--file',help="insttrace.out file", dest='inst_file', action='store', type='string')
    parser.add_option('-m','--memreference_pickle_file', help="memreference file", dest='memreference_file', action='store', type='string')
    (opts, args) = parser.parse_args()

    if opts.inst_file is None or opts.memreference_file is None:
        parser.print_help()
        exit(-1)

    insttrace = InstructionTrace(opts.inst_file, opts.memreference_file)
    insttrace.process_pickle_file()
    insttrace.process_file()
    print len(insttrace.address_dict)
    print len(insttrace.address_range_list)
    print insttrace.min_heap_address, insttrace.max_heap_address
    print self.malloc_block_dict
