from fractions import Fraction
from dataclasses import dataclass
from typing import Optional, NewType
from utils.errors import EndOfStream, EndOfTokens, TokenError
from utils.datatypes import Num, Bool, Keyword, Identifier, Operator, NumLiteral, BinOp, Variable, Let, Assign, If, BoolLiteral, UnOp, ASTSequence, AST, Buffer, ForLoop, Range, Declare, While, DoWhile, Print
from core import RuntimeEnvironment
import graphviz as gv
from math import floor

dot  = gv.Digraph()
dot.node_attr.update(shape='box', style='rounded')
node_id = "node_{}"
depth = 0
class ASTViz:
    """
    An visualizer for Abstract Syntax Trees. Uses graphviz to create a visual representation of the AST.
    Recursively traverses the AST with the treebuilder method.

    Parameters
    ----------
    depth: int
        The depth of the AST. Used to generate unique node ids for graphviz.

    code: str
        The code that the AST represents. Used as the label for the graph.
    """

    def __init__(self, depth: int = 0, code = None):
        self.depth = depth
        dot.clear(keep_attrs=False)
        dot.attr(label = code)

    def treebuilder(self, node: AST, depth: int = 0):
        """
        Takes an AST and returns a treebuilder for that AST.
        """
        id = node_id.format(self.depth)
        self.depth+=1

        if type(node) == If:
            dot.node(id, "If", shape="diamond")
            dot.edge(id, self.treebuilder(node.cond, self.depth))
            dot.edge(id, self.treebuilder(node.e1, self.depth))
            dot.edge(id, self.treebuilder(node.e2, self.depth))

        if type(node) == While:
            dot.node(id, "While", shape = "invtriangle")
            dot.edge(id, self.treebuilder(node.cond, self.depth))
            dot.edge(id, self.treebuilder(node.seq, self.depth))

        if type(node) == ForLoop:
            dot.node(id, "For", shape = "invtriangle")
            dot.edge(id, self.treebuilder(node.var, self.depth))
            dot.edge(id, self.treebuilder(node.val_list, self.depth))
            dot.edge(id, self.treebuilder(node.stat, self.depth))

        if type(node) == Print:
            dot.node(id, "Print")
            dot.edge(id, self.treebuilder(node.value, self.depth))
        
        if type(node) == ASTSequence:
            dot.node(id, "Sequence", shape = "square")
            AST_id = "AST_{}_{}"
            past_node = id
            for _ in range(0, len(node.seq)):
                current_node = AST_id.format(_, self.depth)
                dot.node(current_node, f"{_}", shape = "square", color = "grey")
                dot.edge(current_node, self.treebuilder(node.seq[_], current_node))
                dot.edge(past_node, current_node)
                past_node = current_node

        if type(node) == Range:
            dot.node(id, f"{floor(node.start.value)}")
            range_id = "range_{}_{}"
            past_node = id
            for _ in range(floor(node.start.value) + 1, floor(node.end.value)):
                current_node = range_id.format(_, self.depth)
                dot.node(current_node, f"{_}")
                dot.edge(past_node, current_node)
                past_node = current_node

        if type(node) == Declare:
            dot.node(id, "Declare")
            dot.edge(id, self.treebuilder(node.var, self.depth))
            dot.edge(id, self.treebuilder(node.value, self.depth))
            
        if type(node) == Variable:
            dot.node(id, node.name)

        if type(node) == NumLiteral:
            dot.node(id, str(node.value))
        
        if type(node) == BinOp:
            dot.node(id, node.operator)
            dot.edge(id, self.treebuilder(node.left, self.depth))
            dot.edge(id, self.treebuilder(node.right, self.depth))

        if depth == 0:
            dot.format = 'png'
            dot.render('AST', view=True)
        
        return id
