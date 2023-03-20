# Visualizing ASTs

Abstract Syntax Trees (ASTs) are a way of representing the structure of code. They are useful in understanding how code works, especially when you need to analyse, transform or manipulate it.

To visualise the AST for a given code, we can use the Graphviz library. Graphviz is an open-source graph visualization software that allows you to visualise data structures like trees and graphs. 

## Installing Graphviz
Before we can visualise the AST using Graphviz, we need to install it on our system. The steps to install Graphviz on your system are as follows:

### Windows
1. Download Graphviz from [http://www.graphviz.org/download/](http://www.graphviz.org/download/)
2. Add the following to your PATH environment variable:
```
C:\Program Files\Graphviz\bin
C:\Program Files\Graphviz\bin\dot.exe
```
3. Close any opened Jupyter notebook and the command prompt. 

### Linux
Run the following commands:
```
sudo apt-get update
sudo apt-get install graphviz
```

Alternatively, you can build it manually from http://www.graphviz.org/download/.

### Installing the Graphviz module for Python
Once Graphviz is installed on your system, you need to install the Graphviz module for Python. You can install the module using pip or conda:

```
pip install graphviz
```
```
conda install graphviz
```

## Visualising the AST
Now that we have installed Graphviz and the Graphviz module for Python, we can use it to visualise the AST for a Gossip code. Let's take the following Gossip code as an example:
```
if a > 5:
    b = 3
else:
    b = 1
``` 

To visualise the AST for this code, we need to first generate the AST using the [`main.py`](https://github.com/plugyawn/gossip/blob/main/main.py) file provided in the Gossip repository. We can do this by running the following command:

```
python main.py -i -v
```

This will open the Gossip interpreter. We can then copy and paste the code into the interpreter and press enter. This will generate the AST for the code and display it.

Or it will also be saved as `AST.png` in the current directory.

## Explanantion

The [`visualizer.py`](https://github.com/plugyawn/gossip/blob/main/utils/visualizer.py) file in the `gossip/utils` directory contains the code for visualizing the AST.

This code defines a class `ASTViz` that visualizes an abstract syntax tree (AST) using the graphviz library. The `treebuilder` method recursively traverses the AST and creates nodes and edges in the graphviz representation according to the type of each node in the AST. For example, if the node is an `If` statement, a diamond-shaped node is created in the graphviz representation with edges to the condition expression and the two possible execution paths. If the node is a `While` loop, an inverted triangle-shaped node is created with edges to the loop condition expression and the loop body. If the node is a `BinOp`, a node with the operator symbol is created with edges to the left and right operands.

The `depth` parameter is used to generate unique IDs for each node in the graphviz representation, and the `code` parameter is used as the label for the graph. When the `treebuilder` method is called with a depth of 0, the graphviz representation is rendered as a PNG image and displayed using the default viewer.