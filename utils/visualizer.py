from fractions import Fraction
from dataclasses import dataclass
from typing import Optional, NewType
from utils.errors import EndOfStream, EndOfTokens, TokenError
from utils.datatypes import Num, Bool, Keyword, Identifier, Operator, NumLiteral, BinOp, Variable, Let, Assign, If, BoolLiteral, UnOp, ASTSequence, AST, Buffer, ForLoop, Range, Declare, While, DoWhile, Print
from core import RuntimeEnvironment
import graphviz as gv

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

        if type(node) == Declare:
            dot.node(id, "Declare")
            dot.edge(id, self.treebuilder(node.var, self.depth))
            print(node.value, self.depth, "pass as edge from Declare")
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