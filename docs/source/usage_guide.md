# Usage Guide


1. To run Gossip with an input file containing Gossip code, use the -f or --from-file option followed by the path to the input file:

    ```bash
    python main.py -f ./path/to/input.gos
    ```

    For example, to run the `hello_world.gos` file, use the following command:

    ```bash
    python main.py -f ./examples/test.gos
    ```


2. To update Gossip to the latest version, use the -u or --update option:
    
    ```bash
    python main.py -u
    ```

3. To start an interactive prompt where you can enter Gossip code directly, use the -i or --interpret option:

    ```bash
    python main.py -i
    ```

4. To show feedback whenever a command is entered, use the -s or --show-feedback option:

    ```bash
    python main.py -s
    ```

5. To show a visualization of the Gossip code, line by line, use the -v or --visualize option:

    ```bash
    python main.py -v
    ```

Once you have finished using Gossip, you can exit the program by pressing `CTRL-C` or typing `exit()` at the prompt.

Head on over to the [syntax](syntax.md) page to learn more about the Gossip syntax.