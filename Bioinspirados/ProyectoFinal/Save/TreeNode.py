class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None 

    def add_child(self, child_node):
        child_node.parent = self  
        self.children.append(child_node)

    def get_child(self, index):
            return self.children[index]

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.data) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret