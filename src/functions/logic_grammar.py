# logic_grammar.py
from src.functions.logic_lexer import LogicLexer
import ply.yacc as pyacc


class LogicGrammar:

    def __init__(self):
        self.yacc = None
        self.lexer = None
        self.tokens = None

    def build(self, **kwargs):
        self.lexer = LogicLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.yacc = pyacc.yacc(module=self, **kwargs)

    def parse(self, string):
        self.lexer.input(string)
        return self.yacc.parse(lexer=self.lexer.lexer)

    def p_CODE(self, p):
        """code : S"""
        p[0] = [p[1]]

    def p_Code1(self, p):
        """code : code S"""
        p[0] = p[1]
        p[0].append(p[2])

    def p_s0(self, p):
        """S : Variable
             | Commands
             | Function"""
        p[0] = p[1]

    def p_Commands0(self, p):
        """Commands : LOAD T
                    | DISCARD T
                    | SAVE T
                    | SHOW T
                    | SELECT J
                    | CREATE T"""
        p[0] = {'Command': p[1], "args": p[2]}

    def p_Commands1(self, p):
        """T : TABLE var ';'
             | TABLE var F """
        p[0] = {p[1]: p[2], 'args': p[3]}

    def p_Commands2(self, p):
        """F : FROM string ';'
            | FROM var W
            | FROM var O
            | FROM var ';'
            | FROM Commands
            | AS string ';'
            | FROM var LIMIT nr ';'"""

        if len(p) == 3:
            p[0] = {'FROM': p[1], 'nCommands': p[2]}
        elif len(p) == 4:
            p[0] = {p[1]: p[2], 'args':p[3]}
        elif len(p) == 5:
            p[0] = {'args': [p[1], p[3]], 'from': p[2], 'b': p[4]}
        elif len(p) == 6:
            p[0] = {p[1]: p[2], p[3]: p[4], 'end': p[5]}

    def p_Commands3(self, p):
        """W : WHERE C"""
        p[0] = {'WHERE': p[2]}

    def p_Commands4(self, p):
        """C : Variable '=' nr L
             | Variable '=' string L
             | Variable '<' N L
             | Variable '>' N L
             | Variable '>' '=' N L
             | Variable '<' '=' N L
             | Variable '<' '>' N L
             | Variable '<' '>' string L"""

        if len(p) == 5:
            p[0] = {'column': p[1], 'rule': p[2], 'value': p[3], 'args': p[4]}
        if len(p) == 6:
            p[0] = {'column': p[1], 'rule': [p[2], p[3]], 'value': p[4], 'args': p[5]}

    def p_Commands6(self, p):
        """L : AND C
            | LIMIT N ';'
            | ';' """
        if len(p) == 4:
            p[0] = {p[1]: p[2], 'end': p[3]}
        elif len(p) == 3:
            p[0] = {p[1]: p[1], 'Condictions': p[2]}
        else:
            p[0] = p[1]

    def p_Commands7(self, p):
        """J : '*' F
             | a_list F"""
        p[0] = {'list': p[1], 'args': p[2]}

    def p_Commands8(self, p):
        """O : JOIN var U"""
        p[0] = {'JOIN': p[2], 'args': p[3]}

    def p_Commands9(self, p):
        """U : USING '(' Variable '=' N ')' ';'
              | USING '(' Variable '=' string ')' ';'
              | USING '(' Variable '=' N ')' W
              | USING '(' Variable '=' string ')' W"""
        p[0] = {'USING': p[1], 'column': p[3], 'rule': p[4], 'value': p[5], 'args': p[7]}

    def p_CFunction(self, p):
        """Function : CALL var ';'"""
        p[0] = {'Command': p[1], 'FunctionName': p[2], 'end': p[3]}

    def p_argsList0(self, p):
        """a_list : var"""
        p[0] = [p[1]]

    def p_argsList1(self, p):
        """a_list : a_list ',' var"""
        p[0] = p[1]
        p[0].append(p[3])

    def p_number(self, p):
        """N : nr"""
        p[0] = p[1]

    def p_variable(self, p):
        """Variable : var"""
        p[0] = p[1]

    def p_Functions0(self, p):
        """Function : PROCEDURE var DO c_list END"""
        p[0] = {'Function': p[1], 'FunctionName': p[2], 'ListofComands': p[4], 'end': p[5]}

    def p_CommandList0(self, p):
        """c_list : Commands"""
        p[0] = [p[1]]

    def p_CommandList1(self, p):
        """c_list : c_list Commands"""
        p[0] = p[1]
        p[0].append(p[2])

    def p_error(self, p):
        if p:
            raise Exception(f"Syntax error: unexpected '{p.type}'")
        else:
            raise Exception("Syntax error: unexpected end of file")
