
# Imports
if __name__ is not None and "." in __name__:
    from .llullParser import llullParser
    from .llullVisitor import llullVisitor
else:
    from llullParser import llullParser
    from llullVisitor import llullVisitor

from queue import LifoQueue


class Visitor(llullVisitor):
    context = {}
    context_stack = LifoQueue()

    # Atributs per les funcions
    main = None
    f_dict = {}
    f_inicial = 'main'
    pars_inicials = None

    # Visit a parse tree produced by llullParser#root.
    def visitRoot(self, ctx: llullParser.RootContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by llullParser#program.
    def visitProgram(self, ctx: llullParser.ProgramContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by llullParser#void.
    def visitVoid(self, ctx: llullParser.VoidContext):

        clist = list(ctx.getChildren())

        # Nom de la funcio
        f_id = clist[1].getText()

        if f_id in self.f_dict.keys():
            print(ProcAlreadyDefined())
            exit()

        # Atributs de la funcio
        parameters = self.visit(clist[2])
        code = clist[4]

        # Guardem la nova funcio al diccionari
        self.f_dict[f_id] = {}
        self.f_dict[f_id]['parameters'] = parameters
        self.f_dict[f_id]['code'] = code

    # Visit a parse tree produced by llullParser#voidmain.
    def visitVoidmain(self, ctx: llullParser.VoidmainContext):

        clist = list(ctx.getChildren())
        f_id = clist[1].getText()

        parameters = []
        code = clist[4]
        self.main = code

    # Visit a parse tree produced by llullParser#v_id.
    def visitV_id(self, ctx: llullParser.V_idContext):

        clist = list(ctx.getChildren())

        parameters = []
        for i in range(1, len(clist), 2):

            par = clist[i].getText()

            if par in parameters:
                print(RepeatedFormalParameter())
                exit()

            parameters.append(par)

        return parameters

    # Visit a parse tree produced by llullParser#bloc.
    def visitBloc(self, ctx: llullParser.BlocContext):

        c1 = self.context.copy()
        self.visitChildren(ctx)
        c2 = self.context.copy()
        self.context = {x: c2[x] for x in c2 if x in c1}

    # Visit a parse tree produced by llullParser#sentence.
    def visitSentence(self, ctx: llullParser.SentenceContext):

        return self.visitChildren(ctx)

    # Visit a parse tree produced by llullParser#expr.
    def visitExpr(self, ctx: llullParser.ExprContext):

        clist = list(ctx.getChildren())

        # Si es una fulla retorna el seu valor
        if len(clist) == 1:

            try:
                # Mirem si es un enter
                if llullParser.symbolicNames[clist[0].getSymbol().type] == 'INT':
                    return int(clist[0].getText())

                # Mirem si es un float
                if llullParser.symbolicNames[clist[0].getSymbol().type] == 'FLOAT':
                    return float(clist[0].getText())

                if llullParser.symbolicNames[clist[0].getSymbol().type] == 'TEXT':
                    return clist[0].getText()[1:-1]

                if llullParser.symbolicNames[clist[0].getSymbol().type] == 'ID':
                    if clist[0].getText() not in self.context.keys():
                        print("variable no inicialitzada")
                        raise ValueError("ValueError exception thrown")
                    else:
                        return self.context[clist[0].getText()]

            except ValueError:
                exit()
            except Exception:
                return self.visit(clist[0])

        else:  # len(l) == 3

            # Expresio dins de parentesis
            if clist[0].getText() == '(':
                return self.visit(clist[1])

            # Expresio sense parentesis
            op1 = self.visit(clist[0])
            op2 = self.visit(clist[2])
            operation = clist[1].getText()

            if operation == '*':
                return op1 * op2

            elif operation == '/':
                if op2 == 0:
                    print("No es pot fer una divisió entre 0")
                    exit()

                return op1 / op2

            elif operation == '%':
                return op1 % op2

            elif operation == '+':
                return op1 + op2

            elif operation == '-':
                return op1 - op2

            elif operation == '>':
                if op1 > op2:
                    return 1
                else:
                    return 0

            elif operation == '<':
                if op1 < op2:
                    return 1
                else:
                    return 0

            elif operation == '>=':
                if op1 >= op2:
                    return 1
                else:
                    return 0

            elif operation == '<=':
                if op1 <= op2:
                    return 1
                else:
                    return 0

            elif operation == '==':
                if op1 == op2:
                    return 1
                else:
                    return 0

            else:
                if op1 != op2:
                    return 1
                else:
                    return 0

    def visitArrayop(self, ctx: llullParser.ArrayopContext):

        clist = list(ctx.getChildren())
        var = clist[2].getText()
        val = []
        llarg = self.visit(clist[4])
        for i in range(0, llarg):
            val.append(0)
        self.context[var] = val

    # Visit a parse tree produced by llullParser#getarray.
    def visitGetarray(self, ctx: llullParser.GetarrayContext):

        clist = list(ctx.getChildren())
        var = (clist[2]).getText()
        if var not in self.context:
            print("Taula no definida")
            exit()
        vec = self.context[(clist[2]).getText()]
        pos = self.visit(clist[4])
        if pos >= len(vec) or pos < 0:
            print(outOfBounds())
            exit()

        return vec[pos]

    # Visit a parse tree produced by llullParser#setarray.
    def visitSetarray(self, ctx: llullParser.SetarrayContext):

        clist = list(ctx.getChildren())
        var = clist[2].getText()
        if var not in self.context:
            print("Taula no definida")
            exit()
        vec = self.context[(clist[2]).getText()]
        pos = self.visit(clist[4])
        val = self.visit(clist[6])
        if pos >= len(vec) or pos < 0:
            print(outOfBounds())
            exit()

        vec[pos] = val
        self.context[var] = vec

    # Visit a parse tree produced by llullParser#f_sent.
    def visitF_sent(self, ctx: llullParser.F_sentContext):

        clist = list(ctx.getChildren())

        # Nom de la funcio
        f_id = clist[0].getText()

        if f_id not in self.f_dict.keys():
            print(ProcNotDefined())
            exit()

        # Parametres que requereix la funcio
        f_pars = self.f_dict[f_id]['parameters']

        # Parametres que arriben en la crida
        c_pars = self.visit(clist[2])

        if len(f_pars) != len(c_pars):
            print(IncorrectNumberOfParameters())
            exit()

        # Guardar l'estat actual en la pila i resetejarla
        self.context_stack.put(self.context)
        self.context = {}

        # Guardar els parametres com variables locals
        for var, val in zip(f_pars, c_pars):
            self.context[var] = val

        # Cridem a la funcio
        self.visit(self.f_dict[f_id]['code'])

        # Restaurem el contexte anterior a la crida
        self.context = self.context_stack.get()

    # Visit a parse tree produced by llullParser#p_exec.
    def visitP_exec(self, ctx: llullParser.P_execContext):

        clist = list(ctx.getChildren())

        parameters = []
        for i in range(0, len(clist), 2):
            parameters.append(self.visit(clist[i]))

        return parameters

    # Visit a parse tree produced by llullParser#assig_sent.
    def visitAssig_sent(self, ctx: llullParser.Assig_sentContext):

        # Agafa els fills
        clist = list(ctx.getChildren())

        # Nom de la var i valor que se li assigna
        var = clist[0].getText()
        val = self.visit(clist[2])

        # Assignem el valor en el diccionari
        self.context[var] = val
        return var

    # Visit a parse tree produced by llullParser#read_sent.
    def visitRead_sent(self, ctx: llullParser.Read_sentContext):

        clist = list(ctx.getChildren())

        var = clist[2].getText()
        val = int(input())

        self.context[var] = val

    # Visit a parse tree produced by llullParser#write_sent.
    def visitWrite_sent(self, ctx: llullParser.Write_sentContext):

        clist = list(ctx.getChildren())
        lprint = self.visit(clist[2])
        for i in lprint:
            print(i, end=" ")
        print("", end="\n")

    # Visit a parse tree produced by llullParser#w_expr.
    def visitW_expr(self, ctx: llullParser.W_exprContext):

        clist = list(ctx.getChildren())
        res = []
        for lprint in range(0, len(clist), 2):
            res.append(self.visit(clist[lprint]))
        return res

    # Visit a parse tree produced by llullParser#if_sent.
    def visitIf_sent(self, ctx: llullParser.If_sentContext):

        clist = list(ctx.getChildren())
        # Valor de la expressio de la condicio
        cond_val = self.visit(clist[2])
        if cond_val:
            self.visit(clist[5])
        elif len(clist) == 11:
            self.visit(clist[9])

    # Visit a parse tree produced by llullParser#while_sent.
    def visitWhile_sent(self, ctx: llullParser.While_sentContext):

        clist = list(ctx.getChildren())

        while self.visit(clist[2]):
            self.visit(clist[5])

    # Visit a parse tree produced by llullParser#for_sent.
    def visitFor_sent(self, ctx: llullParser.For_sentContext):

        clist = list(ctx.getChildren())

        # Inicialitzacio del contador
        var = self.visit(clist[2])

        while self.visit(clist[4]) == 1:
            self.visit(clist[9])
            self.visit(clist[6])
        self.context.pop(var)

    # Visit a parse tree produced by llullParser#coment.
    def visitComent(self, ctx: llullParser.ComentContext):
        return self.visitChildren(ctx)


class ProcAlreadyDefined(Exception):
    def __str__(self):
        return 'Ja existeix un procediment amb aquest nom'


class outOfBounds(Exception):
    def __str__(self):
        return 'La posició de la taula no existeix'


class ProcNotDefined(Exception):
    def __str__(self):
        return 'El procediment cridat no existeix'


class IncorrectNumberOfParameters(Exception):
    def __str__(self):
        return 'El numero de parametres no és correcte'


class RepeatedFormalParameter(Exception):
    def __str__(self):
        return 'No es poden repetir els noms dels paràmetres formals'

# del llullParser
