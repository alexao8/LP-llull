from antlr4 import *
from llullLexer import llullLexer
from llullParser import llullParser
from beatVisitor import beatVisitor
import sys

# Llegim de la entrada de consola
input_stream = FileStream(sys.argv[1])

# Lexer
lexer = llullLexer(input_stream)
token_stream = CommonTokenStream(lexer)

# Parser
parser = llullParser(token_stream)
tree = parser.root()

# Visitor
visitor = beatVisitor()
visitor.visitRoot(tree)
