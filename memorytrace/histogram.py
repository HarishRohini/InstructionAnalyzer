__author__ = 'HarishRohini'

import optparse
import pickle
import matplotlib.pyplot as plt
import numpy as np

class MemoryHistogram(object):
    """Draw Histograms with the Read and write references in the allocated address space"""
    def __init__(self, pickle_file):
        super(MemoryHistogram, self).__init__()
        self.pickle_file = pickle_file
        self.heap_ref_dict = {}
        self.read_write_reference = ()

    def process_pickle_file(self):
        f = open(self.pickle_file,'rb')
        pickle_list = pickle.load(f)
        f.close()
        self.read_write_reference = pickle_list[0]
        self.heap_ref_dict = pickle_list[1]
        #find the Avg of values in the dictionary and delete the keys < Avg Value
        temp_list = self.heap_ref_dict.values()
        avg = reduce(lambda x, y : x + y, temp_list) / len(temp_list)
        for i in self.heap_ref_dict.keys():
            if self.heap_ref_dict[i] < avg:
                self.heap_ref_dict.pop(i, None)
        #print "Heap Dictionary Length : ", len(self.heap_ref_dict)
        #print "Avg value : ", avg

    def draw_histogram(self):
        x_plots = []
        y_plots = []
        for k, v in sorted(self.heap_ref_dict.items()):
            x_plots.append(k)
            y_plots.append(v)
        x_range = np.arange(len(x_plots))
        plt.bar(x_range, y_plots, align = 'center')
        plt.xticks(x_range, x_plots)
        plt.savefig('histogram.png')
        #plt.show()
        # Find % of memory addresss referenced ?..


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-p','--pickle_file', help="Pickle file", dest = 'pickle_file', action='store', type='string')
    (opts, args) = parser.parse_args()

    if opts.pickle_file is None:
        parser.print_help()
        exit(-1)

    memoryhistogram = MemoryHistogram(opts.pickle_file)
    memoryhistogram.process_pickle_file()
    memoryhistogram.draw_histogram()
    #print memoryhistogram.heap_ref_dict
