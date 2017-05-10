#!/usr/bin/env python
# Turn csv dataset into images dir and label set
import os
import argparse
import csv
import urllib

class Dataset:
    def __init__(self):
        self.raw_data = []
        self.data = {}

    def read_csv(self, fname, index_key, attributes):
        with open(fname, 'rb') as f:
            reader = csv.reader(f)
            self.raw_data = list(reader)
        cols = self.raw_data[0]
        id_ind = [x for x in range(len(cols)) if cols[x] == index_key][0]
        attr_inds = [x for x in range(len(cols)) for y in attributes if cols[x] == y]

        for item in self.raw_data[1:]:
            
            try:
                self.data[item[id_ind]]
            except KeyError, e:
                self.data[item[id_ind]] = {}
            for aid, attr in enumerate(attr_inds):
                try:
                    self.data[item[id_ind]][attributes[aid]]
                except KeyError, e:
                    self.data[item[id_ind]][attributes[aid]] = []
                self.data[item[id_ind]][attributes[aid]].append(item[attr])

    def consensus(self, attributes):
        for key in self.data.keys():
            for attr in attributes:
                if type(self.data[key][attr]) is not list:
                    continue
                else:
                    lst = self.data[key][attr]
                    # majority vote consensus
                    self.data[key][attr] = max(set(lst), key=lst.count)

    def dl_save_images(self,url_key, attr_key, root_dir):
        for key in self.data.keys():
            print key
            attr = self.data[key][attr_key]
            path = os.path.join(root_dir, attr)
            try: 
                os.makedirs(path)
            except OSError:
                if not os.path.isdir(path):
                    raise

                # assumes that the key is an image's base filename
                urllib.urlretrieve(self.data[key][url_key], os.path.join(path,key))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-csv", help="csv file", type=str)
    parser.add_argument("-index_key", help="", type=str)
    parser.add_argument("-attributes",  nargs = '*', help="")
    parser.add_argument("-root_dir", help="", type=str)
    parser.add_argument("-folder_attr", help="", type=str)
    parser.add_argument("-url_key", help="", type=str)
    args = parser.parse_args()
    
    dset = Dataset()
    dset.read_csv(args.csv, args.index_key, args.attributes)
    dset.consensus(args.attributes)
    dset.dl_save_images(args.url_key, args.folder_attr, args.root_dir)
