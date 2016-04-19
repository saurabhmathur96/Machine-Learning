import itertools
import operator
import pprint 

def compute_support_count(itemset, records):
    return float(sum(set(itemset).issubset(set(record)) for record in records))

def itemset_filter(minimum_support_count, number_of_records):
    def filter_function(itemset_with_frequency):
        return itemset_with_frequency[1]/float(number_of_records) > minimum_support_count
    return filter_function

def is_frequent(itemset, current_itemsets):
    return all(tuple(subset) in current_itemsets for subset in itertools.combinations(itemset, len(itemset)-1) )

def compute_confidence(rule, records):
    return compute_support_count(rule[0], records)/compute_support_count(rule[1], records)

def rule_filter(minimum_confidence, records):
    def filter_function(candidate_rule):
        return compute_confidence(candidate_rule, records) > minimum_confidence
    return filter_function

def powerset(iterable):
    '''
        return non empty strict subsets of iterable
    '''
    s = list(iterable)
    return list(itertools.chain.from_iterable(tuple(itertools.combinations(s, r)) for r in range(1, len(s))))

def tuple_without(t, values):
    return tuple(i for i in t if i not in values)

def find_association_rules(records, minimum_support_count, minimum_confidence):
    # find set of unique items in all records
    unique_items = set([item for record in records for item in record])
    
    # create initial itemsets
    itemsets = [tuple([item]) for item in unique_items]
    
    k = 2
    frequent_itemsets = find_frequent_itemsets(records, minimum_support_count, itemsets, k)
    
    candidate_rules = [(itemset, subset) for itemset in frequent_itemsets for subset in powerset(itemset)]
    
    return filter(rule_filter(minimum_confidence, records), candidate_rules)
    
    
def find_frequent_itemsets(records, minimum_support_count, itemsets, k):
    itemsets_with_frequency = [(itemset, compute_support_count(itemset, records)) for itemset in itemsets]

    # filter out the itemsets with frequency/number_of_records < minimum_support_count
    itemsets_with_support_count = filter(
        itemset_filter(minimum_support_count, len(records)), itemsets_with_frequency) 
        
    filtered_itemsets = map(operator.itemgetter(0), itemsets_with_support_count)
    
    # find remaining unique items
    unique_items = set([item for itemset, count in itemsets_with_support_count for item in itemset])
    
    # find itemsets for next iteration
    next_itemsets = [tuple(combination) for combination in itertools.combinations(unique_items, k)]
    
    # prune next_itemsets
    pruned_next_itemsets = [next_itemset for next_itemset in next_itemsets if is_frequent(next_itemset, filtered_itemsets)]
    
    print 'next: ',
    print pruned_next_itemsets
    if len(pruned_next_itemsets) > 0:
        return find_frequent_itemsets(records, minimum_support_count, pruned_next_itemsets, k+1)
    else:
        return itemsets