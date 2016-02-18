__author__ = 'HarishRohini'

import optparse
import pickle
import matplotlib.pyplot as plt
import numpy as np
from bitarray import bitarray

class MemoryGraph(object):
    """Histograms on Memory Usage for different benchmarks"""
    def __init__(self, pickle_list):
        super(MemoryGraph, self).__init__()
        self.pickle_list = pickle_list.split(',')
        self.memblock_list = []
        self.hot_mem_regions = {}
        self.hot_mem_usage = {}
        self.total_mem_usage = {}

    def get_hot_memory_regions(self, memreference_file):
        f = open(memreference_file,'rb')
        pickle_list = pickle.load(f)
        f.close()
        list_length = len(pickle_list)
        total_references = reduce(lambda x, y: x+y[1], pickle_list, 0)
        ref_count_hot, ref_count_all = 0, 0
        mem_ref_count_all = 0
        actual_mem_block_usage_hot, actual_mem_block_usage_all = 0, 0
        total_mem_block_hot, total_mem_block_all = 0, 0
        flag = True #for maintaining the reference counts for hot vs all the memory regions
        for i in pickle_list:
            ref_count_all += 1
            mem_ref_count_all += i[1]
            total_mem_block_all += len(i[0])
            actual_mem_block_usage_all += i[0].count(True)
            if flag:
                if mem_ref_count_all >= 0.9 * total_references:
                    ref_count_hot = ref_count_all
                    actual_mem_block_usage_hot = actual_mem_block_usage_all
                    total_mem_block_hot = total_mem_block_all
                    flag = False
        return (ref_count_hot*100.0)/(list_length), (actual_mem_block_usage_hot*1.0/ total_mem_block_hot), (actual_mem_block_usage_all*1.0/total_mem_block_all)

    def process_pickle_file(self):
        print self.pickle_list
        for i in self.pickle_list:
            self.hot_mem_regions[i], self.hot_mem_usage[i], self.total_mem_usage[i] = self.get_hot_memory_regions(i)

    def draw_histograms(self):
        x_plots = []
        y_plots = []
        #hot_mem_region graph
        x = np.arange(len(self.hot_mem_regions))
        plt.bar(x, self.hot_mem_regions.values(), align='center', width = 0.5)
        plt.xticks(x, self.hot_mem_regions.keys())
        ymax = max(self.hot_mem_regions.values()) + 5
        plt.ylim(0, ymax)
        plt.xlabel("Benchmarks")
        plt.ylabel("% fraction that account for 90% of references")
        plt.savefig('hot_mem_regions_90p.png')

        #percentage usage of memory in hot regions
        plt.clf()
        x = np.arange(len(self.hot_mem_usage))
        plt.bar(x, map(lambda x: x*100, self.hot_mem_usage.values()), align='center', width = 0.5)
        plt.xticks(x, self.hot_mem_usage.keys())
        ymax = max(map(lambda x: x*100, self.hot_mem_usage.values())) + 5
        plt.ylim(0, ymax)
        #plt.show()
        plt.xlabel("Benchmarks")
        plt.ylabel("% of used memory in hot regions")
        plt.savefig('hot_mem_usage_90p.png')

        # % of the total memory usage in all the regions
        plt.clf()
        x = np.arange(len(self.total_mem_usage))
        plt.bar(x, map(lambda x: x*100, self.total_mem_usage.values()), align='center', width = 0.5)
        plt.xticks(x, self.total_mem_usage.keys())
        ymax = max(map(lambda x: x*100, self.total_mem_usage.values())) + 5
        plt.ylim(0, ymax)
        #plt.show()
        plt.xlabel("Benchmarks")
        plt.ylabel("% of used memory in all the regions")
        plt.savefig('total_mem_usage_90p.png')



if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-p','--pickle_file_list', help="Pickle file", dest = 'pickle_file_list', action='store', type='string')
    (opts, args) = parser.parse_args()

    if opts.pickle_file_list is None:
        parser.print_help()
        exit(-1)

    memhistorgram = MemoryGraph(opts.pickle_file_list)
    memhistorgram.process_pickle_file()
    print memhistorgram.hot_mem_regions, memhistorgram.hot_mem_usage, memhistorgram.total_mem_usage
    memhistorgram.draw_histograms()
