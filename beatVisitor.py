
# Imports
if __name__ is not None and "." in __name__:
    from .llullParser import llullParser
    from .llullVisitor import llullVisitor
else:
    from llullParser import llullParser
    from llullVisitor import llullVisitor
from colored import fg, bg, attr

# This class defines a complete generic visitor for a parse tree produced by llullParser.


class beatVisitor(llullVisitor):

    def __init__(self):
        self.nivell = 0
        self.b = True

    # Visit a parse tree produced by llullParser#root.
    def visitRoot(self, ctx: llullParser.RootContext):

        return self.visitChildren(ctx)

    # Visit a parse tree produced by llullParser#program.
    def visitProgram(self, ctx: llullParser.ProgramContext):

        return self.visitChildren(ctx)

    # Visit a parse tree produced by llullParser#void.
    def visitVoid(self, ctx: llullParser.VoidContext):

        clist = list(ctx.getChildren())
        print(("%s"+clist[0].getText()+"%s") % (fg(5), attr(0)), end=" ")
        print(("%s"+clist[1].getText()+"%s") % (fg(4), attr(0)), end="")
        parameters = self.visit(clist[2])
        print("(", end="")
        print(parameters[0], end=", ")
        for p in parameters[1:-1]:
            print(p, ", ", sep="", end="")
        print(parameters[-1], end="")
        print(") ", end=" ")
        self.visit(clist[4])

    # Visit a parse tree produced by llullParser#voidmain.
    def visitVoidmain(self, ctx: llullParser.VoidmainContext):

        clist = list(ctx.getChildren())
        print(("%s"+clist[0].getText()+"%s") % (fg(5), attr(0)), end=" ")
        print(("%s"+clist[1].getText()+"%s") % (fg(4), attr(0)), end="")
        print("()", end=" ")
        self.visit(clist[4])

    # Visit a parse tree produced by llullParser#v_id.
    def visitV_id(self, ctx: llullParser.V_idContext):

        clist = list(ctx.getChildren())

        parameters = []
        for i in range(1, len(clist), 2):

            par = clist[i].getText()
            parameters.append(par)

        return parameters

    # Visit a parse tree produced by llullParser#bloc.
    def visitBloc(self, ctx: llullParser.BlocContext):

        print("{")
        self.nivell += 1
        self.visitChildren(ctx)
        self.nivell -= 1
        print("    "*self.nivell+"}")

    # Visit a parse tree produced by llullParser#sentence.
    def visitSentence(self, ctx: llullParser.SentenceContext):

        return self.visitChildren(ctx)

    # Visit a parse tree produced by llullParser#expr.
    def visitExpr(self, ctx: llullParser.ExprContext):

        clist = list(ctx.getChildren())
        if len(clist) == 1:
            try:
                if llullParser.symbolicNames[clist[0].getSymbol().type] == 'INT':
                    return (("%s"+clist[0].getText()+"%s") % (fg(19), attr(0)))
                # Mirem si es un float
                if llullParser.symbolicNames[clist[0].getSymbol().type] == 'FLOAT':
                    return (("%s"+clist[0].getText()+"%s") % (fg(29), attr(0)))

                if llullParser.symbolicNames[clist[0].getSymbol().type] == 'TEXT':
                    return (("%s"+clist[0].getText()+"%s") % (fg(202), attr(0)))

                if llullParser.symbolicNames[clist[0].getSymbol().type] == 'ID':
                    return (("%s"+clist[0].getText()+"%s") % (fg(27), attr(0)))
                else:
                    return self.visit(clist[0])
            except Exception:
                return self.visit(clist[0])

        else:
            if clist[0].getText() == '(':
                return "(" + self.visit(clist[1]) + ")"
            else:
                op1 = self.visit(clist[0])
                operation = clist[1].getText()
                op2 = self.visit(clist[2])
                return op1 + " " + operation + " " + op2

    # Visit a parse tree produced by llullParser#arrayop.
    def visitArrayop(self, ctx: llullParser.ArrayopContext):

        clist = list(ctx.getChildren())
        print("    "*self.nivell, end="")
        print(("%s"+clist[0].getText()+"%s") % (fg(104), attr(0)), end="")
        print("(", end="")
        print(("%s"+clist[2].getText()+"%s") % (fg(27), attr(0)), end="")
        print(", ", end="")
        print(self.visit(clist[4]), end="")
        print(")")

    # Visit a parse tree produced by llullParser#getarray.
    def visitGetarray(self, ctx: llullParser.GetarrayContext):

        clist = list(ctx.getChildren())
        output = (("%s"+clist[0].getText()+"%s") % (fg(104), attr(0)))
        output += ("(")
        output += (("%s"+clist[2].getText()+"%s") % (fg(27), attr(0)))
        output += (", ")
        output += self.visit(clist[4])
        output += (")")
        return output

    # Visit a parse tree produced by llullParser#setarray.
    def visitSetarray(self, ctx: llullParser.SetarrayContext):

        clist = list(ctx.getChildren())
        print("    "*self.nivell, end="")
        print(("%s"+clist[0].getText()+"%s") % (fg(104), attr(0)), end="")
        print("(", end="")
        print(("%s"+clist[2].getText()+"%s") % (fg(27), attr(0)), end="")
        print(", ", end="")
        print(self.visit(clist[4]), end="")
        print(", ", end="")
        print(self.visit(clist[6]), end="")
        print(")")

    # Visit a parse tree produced by llullParser#f_sent.
    def visitF_sent(self, ctx: llullParser.F_sentContext):

        clist = list(ctx.getChildren())
        print("    "*self.nivell, end="")
        print(("%s"+clist[0].getText()+"%s") % (fg(4), attr(0)), end="")
        print(self.visit(clist[2]))

    # Visit a parse tree produced by llullParser#p_exec.
    def visitP_exec(self, ctx: llullParser.P_execContext):

        clist = list(ctx.getChildren())
        parameters = "("
        if (len(clist) == 1):
            parameters = self.visit(clist[0]) + ")"
            return parameters
        else:
            for i in range(0, len(clist)-1, 2):
                parameters += self.visit(clist[i])
                parameters += ", "
            parameters += self.visit(clist[-1])
            return parameters + ")"

    # Visit a parse tree produced by llullParser#assig_sent.
    def visitAssig_sent(self, ctx: llullParser.Assig_sentContext):

        clist = list(ctx.getChildren())
        output = (("%s"+clist[0].getText()+"%s") % (fg(27), attr(0)))
        output += (" = ")
        if self.b:
            print("    "*self.nivell, end="")
            print(output + self.visit(clist[2]))
        else:
            return (output + self.visit(clist[2]))

    # Visit a parse tree produced by llullParser#read_sent.
    def visitRead_sent(self, ctx: llullParser.Read_sentContext):

        clist = list(ctx.getChildren())
        print("    "*self.nivell, end="")
        print(("%s"+clist[0].getText()+"%s") % (fg(104), attr(0)), end="")
        print("(", end="")
        print(("%s "+clist[2].getText()+" %s") % (fg(27), attr(0)), end="")
        print(")")

    # Visit a parse tree produced by llullParser#write_sent.
    def visitWrite_sent(self, ctx: llullParser.Write_sentContext):

        clist = list(ctx.getChildren())
        print("    "*self.nivell, end="")
        print(("%s"+clist[0].getText()+"%s") % (fg(104), attr(0)), end="")
        print(self.visit(clist[2]))

    # Visit a parse tree produced by llullParser#w_expr.
    def visitW_expr(self, ctx: llullParser.W_exprContext):

        clist = list(ctx.getChildren())
        if len(clist) == 1:
            return "("+self.visit(clist[0])+")"
        else:
            par = ""
            for lprint in range(0, len(clist)-1, 2):
                par = par + (self.visit(clist[lprint]))
                par = par + ", "
            par = par + (self.visit(clist[-1]))
        return "(" + par + ")"

    # Visit a parse tree produced by llullParser#if_sent.
    def visitIf_sent(self, ctx: llullParser.If_sentContext):

        clist = list(ctx.getChildren())
        print("    "*self.nivell, end="")
        print(("%s"+clist[0].getText()+"%s") % (fg(12), attr(0)), end="")
        print(" (", end="")
        print(self.visit(clist[2]), end="")
        print(")", end=" ")
        self.visit(clist[5])
        if len(clist) == 11:
            print("    "*self.nivell, end="")
            print(("%s"+clist[7].getText()+"%s") % (fg(12), attr(0)), end="")
            self.visit(clist[9])

    # Visit a parse tree produced by llullParser#while_sent.
    def visitWhile_sent(self, ctx: llullParser.While_sentContext):

        clist = list(ctx.getChildren())
        print("    "*self.nivell, end="")
        print(("%s"+clist[0].getText()+"%s") % (fg(12), attr(0)), end="")
        print(" (", end="")
        print(self.visit(clist[2]), end="")
        print(") ", end="")
        self.visit(clist[5])

    # Visit a parse tree produced by llullParser#for_sent.
    def visitFor_sent(self, ctx: llullParser.For_sentContext):

        clist = list(ctx.getChildren())
        print("    "*self.nivell, end="")
        print(("%s"+clist[0].getText()+"%s") % (fg(12), attr(0)), end="")
        print(" (", end="")
        self.b = False
        print(self.visit(clist[2]), end="")
        self.b = True
        print("; ", end="")
        print(self.visit(clist[4]), end="")
        print(";", end=" ")
        self.b = False
        print(self.visit(clist[6]), end="")
        self.b = True
        print(") ", end="")
        self.visit(clist[9])

# del llullParser
