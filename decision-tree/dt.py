
from collections import Counter
import operator
import math



class DecisionTreeClassifier(object):

    def __init__(self, attributes, target, root):
        self.attributes = attributes
        self.target = target
        self.root = root
    
    def predict(self, inputs):
        return self._predict(inputs, self.root)
    
    def _predict(self, inputs, node):
        if type(node) is LeafNode:
            return node.value
        else :
            value = inputs[node.attribute]
            return self._predict(inputs, node.children[value])    


def create_tree(rows, target):
    attributes = [i for i in range(len(rows[0])) if i != target]
    tree = _create_tree(rows, target, attributes)
    return DecisionTreeClassifier(attributes, target, tree)


def _create_tree(rows, target, attributes):

    splits = {i: split_by_attribute(rows, i) for i in attributes}

    current_entropy = entropy(rows, target)

    gains = ((attribute, current_entropy - entropy_of_split(split, target))
             for attribute, split in splits.iteritems())

    splitting_attribute = max(gains, key=operator.itemgetter(1))[0]

    remaining_attributes = [
        attribute for attribute in attributes if attribute != splitting_attribute]

    children = {value: (_create_tree(split_rows, target, remaining_attributes) if entropy(split_rows, target) > 0 else LeafNode(split_rows[0][target])) 
                for (value, split_rows) in splits[splitting_attribute].iteritems()}

    return DecisionNode(splitting_attribute, children)


def entropy(rows, target):
    values = [row[target] for row in rows]
    counts = Counter(values)
    total = float(len(values))
    e = -sum((count / total) * math.log((count / total), 2)
             for count in counts.values())
    return e


def entropy_of_split(parts, target):
    total = float(sum(len(rows) for rows in parts.values()))
    e = sum(entropy(rows, target) * len(rows)
            / total for rows in parts.values())

    return e


def split_by_attribute(rows, attribute):
    unique_values = set([row[attribute] for row in rows])
    parts = {value: [row for row in rows if row[attribute] == value]
             for value in unique_values}
    return parts
