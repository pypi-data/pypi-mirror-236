# Architecture of Lark

Originally written for Python 2, which influenced the coding style.

Lark was intended to support the standalone parser from the get-go, which is part of the reason it has no required dependencies. The standalone generator reads the code from Lark itself, using specialized comments to mark the sections that are relevant.

## Module Overview


### User-facing modules

List of modules intended to be used directly by the users:

- lark.py - main interface
- tree.py - provides a tree structure, used to store the parse tree
- visitors.py - provides utilities for processing the tree, namely transformer visitor and interpreter.
- ast_utils.py - provides utilities for transforming the tree into a custom Abstract Syntax Tree (AST)
- reconstruct.py - an experimental tool for reconstructing text from a shaped tree, based on a grammar.
- indenter.py - provides a post-lexer for implementing Python-style indentation.
- tools/standalone.py - generates a standalone version of the lalr parser, by copying the relevant code sections from Lark itself.
- tools/serialize.py - outputs Lark's internal LALR analysis as a JSON file. Can be used to create parsers in other languages.
- tools/nearley.py - imports a grammar from NearleyJS into Lark (legacy code)

### Core internal modules

A list of internal modules used to provide the core functionality of Lark:

- lexer.py - provides the basic and contextual lexer classes
- parser_frontends.py - provides the various configurations of parser+lexer that Lark supports.
- load_grammar.py - parses and compiles Lark grammars into an internal representation.
- parse_tree_builder.py - provides functions for the automatic building and shaping of the parse-tree 
- parsers/grammar_analysis.py - provides superficial grammar analysis.
- parsers/lalr_analysis.py - builds a LALR(1) transition-table.
- parsers/lalr_parser.py - implements the LALR(1) Parser.
- parsers/lalr_interactive_parser.py - implements the LALR interactive parser.
- parsers/earley_forest.py - provides an SPPF implementation for the Earley parsers
- parsers/earley.py - implements the Earley Parser (with a basic lexer).
- parsers/xearley.py - implements the Earley parser with a dynamic lexer.
- parsers/cyk.py - implements a CYK parser (legacy code).

## Overview of the main flow

1) A Lark instance is created with a grammar, either as a string or a file.
    - The grammar is sent to "load_grammar.py" to be parsed and processed, returning an internal representation.
    - The resulting internal representation is used to construct the lexer and parser using "parser_frontends.py", and the parse-tree builder using "parse_tree_builder.py", according to the options given.
    - A caching mechanism will store and load the internal respresentation, if enabled, so the steps above only happen once per change. It does so using Lark's serialization/deserialization mechanism.

2) The "parse" method is called with an input, usually a text string.
    - The lexer consumes the text and produces tokens, while the parser consumes the tokens and produces rule matches.
    - Those rule matches are then used to call to the parse tree builder, to generate the appropriate tree nodes, and apply tree-shaping.
    - If a transformer is provided, it is applied to each newly created tree node.

### Flow details when using LALR

When creating the instance, parser_frontends.py will use lalr_analysis.py (which uses grammar_analysis.py) to generate the parse table. That is a computationally expensive analysis, which may take long on very large grammars. In that case, using the cache option will greatly improve the performance.

Calls to parse() will use lalr_parser.py, while calls to parse_interactive() will use lalr_interactive_parser.py


## Module details

### lexer.py

Lark's lexers use regular expressions to split text into tokens.

The module contains the following classes - 

- Pattern - an abstraction over regular expressions.

- TerminalDef - a definition of a terminal

- Token - a string with meta-information

- LineCounter - a utility class for keeping track of line & column information