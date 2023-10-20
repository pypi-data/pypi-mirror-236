import colorama
from colorama import Back

from PrettyPrint import PrettyPrintLinkedList
from PrettyPrint import PrettyPrintTree

# n1 = NodeFormatter.from_string("wow\nlook\na\ntraiiiinnnnn")
# n2 = NodeFormatter.from_string("so\nHello!!!\nWorld")
# n3 = NodeFormatter.from_string("AMEN")
# n4 = NodeFormatter.from_string("1\n2\n3\n4\n5\n6\n7\n8")
# n1.add_border()
# n2.add_border()
# n2.color_bg(colorama.Back.LIGHTBLACK_EX, False)
# n12 = join_horizontally([n1, n2, n3, n4])
# x = add_parent_horizontal_join(n1, n12)
# # n34 = join_horizontally([n4, n3])
# # joined = join_horizontally([n12, n34])
# # joined.add_border()
# print(n12.to_str())
# print(x.to_str())
# exit()

class Tree:
    def __init__(self, value, label=None):
        self.val = value
        self.children = []
        self.label = label

    def add_child(self, child):
        self.children.append(child)
        return child


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"""Person {{
    age: {self.age},
    name: {self.name}
}}"""


tree = Tree(1)
child1 = tree.add_child(Tree("""10\\n000
01001
11011
01110"""))
child2 = tree.add_child(Tree(10001))
child1_1 = child1.add_child(Tree("""10010
00010
11011"""))
child1_2 = child1.add_child(Tree(10011))
child1_2_1 = child2.add_child(Tree(10100))
child1_2_1 = child2.add_child(Tree("""10101
11111
00000"""))
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val, show_newline_literal=True)(tree)
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val, border=True, show_newline_literal=True)(tree)
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val, trim=5)(tree)
print()
PrettyPrintTree(
    lambda x: x.children, lambda x: x.val, trim=5,
    trim_symbol=' ' + colorama.Back.GREEN
)(tree)
print()
mx1 = PrettyPrintTree(lambda x: x.children, lambda x: x.val, max_depth=2, return_instead_of_print=True)(tree)
print(mx1)
print()
PrettyPrintTree(
    lambda x: x.children, lambda x: x.val,
    show_newline_literal=True,
    newline_literal=colorama.Fore.LIGHTGREEN_EX + '\\n' + colorama.Fore.RESET
)(tree)
print()

PrettyPrintTree(
    lambda x: x.children, lambda x: x.val, start_message=lambda node: f'printing tree of type BINARY:'
)(tree)
print()
# exit()
PrettyPrintTree(lambda x: x.children, lambda x: x.val, lambda x: x.label)(tree)
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val, lambda x: x.label, label_color=Back.BLACK)(tree)
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val, orientation=PrettyPrintTree.Horizontal)(tree)
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val, lambda x: x.label, orientation=PrettyPrintTree.Horizontal)(tree)
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val, lambda x: x.label, label_color=Back.BLACK, orientation=PrettyPrintTree.Horizontal)(tree)
print()

PrettyPrintTree(lambda x: x.children, lambda x: x.val, orientation=PrettyPrintTree.Horizontal)(tree)
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val,
                orientation=PrettyPrintTree.Horizontal,
                show_newline_literal=True)(tree)
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val,
                orientation=PrettyPrintTree.Horizontal, border=True, max_depth=3)(tree)
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val, trim=5, color=Back.BLACK,
                orientation=PrettyPrintTree.Horizontal)(tree)
print()

some_json = {'foo': 1, 'bar': (('a', 'a2'), 'b'), 'qux': {'foo': 1, 'arr': [{1: 2, 2: 1}], 'bar': ['a', 'b']}}
PrettyPrintTree(color=Back.WHITE).print_json(some_json)
print()
PrettyPrintTree().print_json(some_json, name="DICT", max_depth=3)
print()


def nodes_below(node: tuple[int, int], level: int) -> list[tuple[int, int]]:
    node_lvl, node_idx = node
    levels_below = level - node_lvl
    start_idx = node_idx * (2 ** levels_below)  # Binary tree
    nodes = [(level, idx) for idx in range(start_idx, start_idx + (2 ** levels_below))]
    return nodes


pt = PrettyPrintTree(
    lambda lvl_index: nodes_below((lvl_index[0], lvl_index[1]), lvl_index[0] + 1) if lvl_index[0] < 3 else [],
    lambda x: x
)

pt((0, 0))
print()

PrettyPrintTree(
    lambda x: [] if x is None or x.prev_node is x.next_node is None else [x.prev_node, x.next_node],
    lambda x: x.val if x else (colorama.Back.BLACK + '   ' + colorama.Back.LIGHTBLACK_EX)
)

some_json = {'foo': 1, 'bar': ('a', 'b'), 'qux': {'foo': 1, 'bar': ['a', 'b']}}
pt = PrettyPrintTree()
print()
pt.print_json(some_json, name="DICT")
print()

class Node:
    def __init__(self, val):
        self.val = val
        self.next_node = None
        self.prev_node = None


n1, n2, n3, n4 = Node("Node1"), Node("Node2"), Node("Node\nJs"), Node("Node4")
n1.next_node = n2
n2.next_node = n3
n3.next_node = n4
n3.prev_node = n2
pt = PrettyPrintLinkedList(
    lambda x: x.val,
    lambda x: x.next_node,
    lambda x: x.prev_node,
    orientation=PrettyPrintLinkedList.Horizontal,
)
pt(n1)