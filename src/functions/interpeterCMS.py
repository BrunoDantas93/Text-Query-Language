import ply.lex as plex

def CleanNewLine(self, t):
    if "\n" in t.value:
        t.value = t.value.replace("\n", "")
    return t


def CleanCOMMA(self, t):
    if t.value.endswith(","):
        t.value = t.value[:-1]

    if t.value.startswith(","):
        t.value = t.value[1:]
    return t


def CleanQUANTATION(self, t):
    if t.value.startswith("\"") and t.value.endswith("\""):
        t.value = t.value[:-1]
        t.value = t.value[1:]
    return t

class CMSIntrepeter:
    tokens = ("COMMENTS", "QUANTATION", "COMMA")
    t_ignore = " "

    def t_COMMENTS(self, t):
        r"\A\#[^\n]+(\n?)"
        pass

    def t_QUANTATION(self, t):
        r"(,?)\"[^\"]+(\"?)(\n?)"
        return t

    def t_COMMA(self, t):
        r"(,?)[^,]+"
        return t


    def t_error(self, t):
        raise Exception(f"Unexpected tokens: {t.value[:10]}")

    def __init__(self):
        self.lexer = None

    def cmsIntrepeter(self, contents, table, List, **kwargs):

        self.lexer = plex.lex(module=self, **kwargs)

        self.list = List

        Header = True
        header = []
        for line in contents:
            self.lexer.input(line)
            i = 0
            for token in iter(self.lexer.token, None):
                token = CleanNewLine(self, token)
                if token.value:
                    token = CleanCOMMA(self, token)
                    token = CleanQUANTATION(self, token)
                    if Header == True:
                        header.append(token.value)
                        self.list.AddColumns(table, token.value)
                    else:
                        self.list.AddValues(table, header[i], token.value)
                i = i + 1
            Header = False