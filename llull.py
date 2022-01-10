from antlr4 import *
from llullLexer import llullLexer
from llullParser import llullParser
from visitor import Visitor
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
visitor = Visitor()
visitor.visitRoot(tree)

if len(sys.argv) > 2:
    nomf = sys.argv[2]
    paramval = [int(x) for x in sys.argv[3:]]
    paramname = visitor.f_dict[nomf]['parameters']
    codi = visitor.f_dict[nomf]['code']
    visitor.context = dict(zip(paramname, paramval))
    visitor.visit(codi)

else:
    visitor.visit(visitor.main)
