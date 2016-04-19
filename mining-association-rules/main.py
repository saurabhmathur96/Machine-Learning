#!/usr/bin/env python
import apriori
import csv
import pprint
import sys


def main(file_name, minimum_support_count, minimum_confidence) :
    with open(file_name) as f:
        rows = [tuple(filter(bool, row)) for row in csv.reader(f, delimiter=' ')]
    
    frequent_itemsets = apriori.find_association_rules(rows, minimum_support_count, minimum_confidence)
    pprint.pprint(frequent_itemsets)
    
    
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'usage: main.py [file-name] [minimum-support-count] [minimum-confidence]'
    else :
        main(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))