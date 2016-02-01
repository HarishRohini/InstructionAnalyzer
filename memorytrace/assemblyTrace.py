__author__ = 'HarishRohini'

import optparse
import pickle

class AssemblyTrace(object):
    """docstring for AssemblyTrace"""
    def __init__(self, filename):
        super(AssemblyTrace, self).__init__()
        self.filename = filename
        self.register_128bit = ['xmm'+str(i) for i in range(8)]
        self.register_64bit = ['RAX', 'RBX', 'RCX', 'RDX', 'RSI', 'RDI', 'RBP', 'RSP']
        self.register_32bit = ['EAX', 'EBX', 'ECX', 'ESI', 'ESI', 'EDI', 'EBP', 'ESP']
        self.memreference_dict = {'byte': 8, 'word': 16, 'dword': 32, 'qword': 64, 'xmmword': 128}
        self.memory_access = {}
        self.unique_program_counter = 0

    def process_file(self):
        with open(self.filename, 'r') as f:
            for line in f:
                split_assembly_trace = line.split(' : ')
                if len(split_assembly_trace) < 2:
                    continue
                else:
                    if split_assembly_trace[2][:-1] == '0':
                        continue
                    split_inst = split_assembly_trace[1].split()
                    if 'byte' in split_inst:
                        self.memory_access[split_assembly_trace[0]] = 1
                    elif 'word' in split_inst:
                        self.memory_access[split_assembly_trace[0]] = 2
                    elif 'dword' in split_inst:
                        self.memory_access[split_assembly_trace[0]] = 4
                    elif 'qword' in split_inst:
                        self.memory_access[split_assembly_trace[0]] = 8
                    elif 'xmmword' in split_inst:
                        self.memory_access[split_assembly_trace[0]] = 16
                    elif 'zmmword' in split_inst:
                        self.memory_access[split_assembly_trace[0]] = 32
                    elif 'pop' in split_inst or 'push' in split_inst or 'call' in split_inst or 'ret' in split_inst or 'leave' in split_inst:
                        #ignore stack operations
                        pass
                    else:
                        print ("Unkown instruction : ", split_assembly_trace)

                    self.unique_program_counter += 1

        f.close()


    def write_to_file(self):
        f = open('memreference_dict.in','wb')
        temp_list = []
        temp_list.append(self.memory_access)
        pickle.dump(temp_list,f)
        f.close()


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f','--file',help="assembly_trace.out file", dest='assemblytrace_file', action='store', type='string')
    (opts, args) = parser.parse_args()

    if opts.assemblytrace_file is None:
        parser.print_help()
        exit(-1)

    assemblytrace = AssemblyTrace(opts.assemblytrace_file)
    assemblytrace.process_file()
    assemblytrace.write_to_file()
    print ("Unique program counter : ", assemblytrace.unique_program_counter)
