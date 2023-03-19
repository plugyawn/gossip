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

```pip
pip install graphviz
```
```conda
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

```bash
python main.py -i -v
```

This will open the Gossip interpreter. We can then copy and paste the code into the interpreter and press enter. This will generate the AST for the code and display it.

Or it will also be saved as `AST.png` in the current directory.