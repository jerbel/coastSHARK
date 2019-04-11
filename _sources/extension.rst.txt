How to Extend
=============

*coastSHARK* is currently more a proof of concept like tool than a fully thought through extensible tool.
Therefore, the extendability is not as good as it could be.

Nevertheless, there are 2 ways in which coastSHARK can be extended.


The first would be adding new languages that can be parsed. 
This would require in its simplest form a pure python parser for the language and the AST node types that can be extracted with the parser. The AST node types are required as currently we are building a bag-of-words with AST nodes.

To add a new language parser would require adding it to :any:`util.extract_ast` and including a call to it in :any:`smartshark_plugin`.


The second second method by which *coastSHARK* could be extended is by extracting more complex AST information than a bag-of-words of the nodes, e.g., a tree representation of just additional information like class names.

This would also require changes in :any:`util.extract_ast` for the implementation, in :any:`smartshark_plugin` for the call and possibly in :any:`util.write_mongo` to write this information to the database.
