from decisiontree import id3
from lxml import etree
import csv
import sys
import random

def main(rows, target_attribute):
    random.seed(0)
    
    # split dataset into test and train
    test_indexes = random.sample(range(len(rows)), int(len(rows)*.2))
    train_rows = [row for i, row in enumerate(rows) if i not in test_indexes ]
    test_rows = [row for i, row in enumerate(rows) if i in test_indexes ]
    
    # create decision tree
    dtree = id3.create_tree(train_rows, target_attribute)
    
    # print xml representation of tree
    print etree.tostring(dtree.root.toxml(), pretty_print=True)
    
    # test
    tests = test_rows
    count = 0
    for test in tests:
        inputs = [each for i, each in enumerate(test) if i != target_attribute ]
        output = test[target_attribute]
        if dtree.predict(inputs) == output:
            count += 1
        # print 'predicted : ', dtree.predict(inputs)
        # print 'expected : ', output
    # print count/float(len(tests))
    
    
if __name__ == '__main__':
    with open(sys.argv[1]) as inputfile:
        rows = [row for row in csv.reader(inputfile)]
        main (rows, int(sys.argv[2]))