def search_for_node(node, token, k=10, visited=None, print_node=False):
    if print_node:
        print(str(node))

    # found the token
    if node.get_token() == token:
        return node

    if k == 0 or (visited is not None and token in visited):
        return False

    # leaf node
    if not node.has_children():
        return False

    # search the nodes children
    for child in node.get_children():
        n = search_for_node(child, token, k - 1,
                            [node] if visited is None else (visited + [node]), print_node=print_node)
        if n:
            return n

    return False


class Node:

    def __init__(self, token_str):
        self.token_str = str(token_str)
        self.children = []
        self.parents = []

    def get_token(self):
        return self.token_str

    def has_children(self):
        return len(self.children) > 0

    def has_parents(self):
        return len(self.parents) > 0

    def __add_parent(self, parent):
        self.parents.append(parent)

    def get_children(self):
        return self.children

    def add_child(self, child_node):
        if self != child_node and child_node not in self.children:
            child_node.__add_parent(self)
            self.children.append(child_node)

    def paths(self, k=10):
        """Get all possibles paths in the graph starting in this node"""

        if not self.children or k == 0:  # leaf or max depth
            return [[self.token_str]]

        paths = []
        for child in self.children:
            for path in child.paths(k-1):
                paths.append([self.token_str] + path)
        return paths

    def __str__(self):
        child_names = [str(child.token_str) for child in self.children]
        return self.get_token() + str(child_names)
