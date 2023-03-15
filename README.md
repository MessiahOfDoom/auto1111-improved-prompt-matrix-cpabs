# auto1111-improved-prompt-matrix

This script is [ArrowM/auto1111-improved-prompt-matrix](https://github.com/ArrowM/auto1111-improved-prompt-matrix) modified to support both `batch size` and `custom group symbols`.

## Usage

The script contains three new textboxes. With these you can set custom symbols for the opening brackets, closing brackets and separator. By default these are still bound to `<`, `>` and `|` respectively; leaving the textboxes blank behaves like the original script. Do note that while it is possible to use arbitrarily long group symbols, this was never the intended use case and may thus lead to unintended/undefined behavior.

The following instructions assume you left the symbols as their default values.

Use `<` `>` to create a group of alternate texts. Separate text options with `|`. Multiple groups and multiple options can be used. For example:

An input of `a <corgi|cat> wearing <goggles|a hat>`  
will output 4 prompts: `a corgi wearing goggles`, `a corgi wearing a hat`, `a cat wearing goggles`, `a cat wearing a hat`

Each output prompt will be generated for each seed when using a `batch count * batch size` > 1.  
Note that the batch with the lowest seed is generated for each prompt before moving on to the next set of seeds; this may mean the output is sorted a little unintuitively in both the grid and on disk. 
