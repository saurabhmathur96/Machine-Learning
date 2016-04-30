from lxml import etree, objectify

class Node(object):

    def __init__(self):
        pass


class DecisionNode(Node):

    def __init__(self, attribute, majority_target_value, children):
        super(DecisionNode, self).__init__()
        self.attribute = attribute
        self.majority_target_value = majority_target_value

        # dict of value -> Node
        self.children = children
    
    def toxml(self):
        root = etree.Element('DecisionNode')
        root.set('attribute', unicode(self.attribute))
        root.set('majority_target_value', unicode(self.majority_target_value))
        for value, child in self.children.iteritems():
            childNode = child.toxml()
            childNode.set('value', unicode(value))
            root.append(childNode)
        return root


class LeafNode(Node):

    def __init__(self, value, targetValue):
        super(LeafNode, self).__init__()
        self.value = value
        self.targetValue = targetValue

    def toxml(self):
        root = etree.Element('LeafNode')
        root.set('value', self.value)
        root.set('targetValue', self.targetValue)
        return root
