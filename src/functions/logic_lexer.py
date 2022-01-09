#logic_lexer.py
import ply.lex as plex

class LogicLexer:
    tokens = ["LOAD", "DISCARD", "SAVE", "SHOW", "TABLE", "FROM", "WHERE", "AND", "JOIN", "USING", "SELECT", "CREATE", "AS", "var",  "nr", "string", "LIMIT", "PROCEDURE", "DO", "END", "CALL"]
    literals = ['*', '=', '<', '>', ';', '(', ')', ',']
    t_ignore = " \n"

    def t_string(self, t):
        r'"[^"]*"'
        t.value = {"str": t.value[1:-1]}
        return t

    def t_str(self, t):
        r"LOAD|DISCARD|SAVE|SHOW|TABLE|FROM|WHERE|AND|JOIN|USING|SELECT|CREATE|var|nr|string|AS|LIMIT|PROCEDURE|DO|END|CALL"
        t.type = t.value
        return t

    def t_var(self, t):
        r"[A-z_]+"
        return t

    def t_nr(self, t):
        r"[0-9]+(\.[0-9]+)?"
        t.value = float(t.value)
        return t

    def t_error(self, t):
        raise Exception(f"Unexpected token: [{t.value[:10]}]")

    def __init__(self):
        self.lexer = None

    def build(self, **kwargs):
        self.lexer = plex.lex(module=self, **kwargs)

    def input(self, string):
        self.lexer.input(string)

    def token(self):
        token = self.lexer.token()
        return token if token is None else token.type
