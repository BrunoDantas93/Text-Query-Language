class DicDataBase(dict):

    def __init__(self):
        self.Tables = {}

    def AddTable(self, value):
        if value not in self.Tables:
            self.Tables[value] = {}
        else:
            raise Exception("This table {",value,"} is already in the database")

    def AddColumns(self, table, value):
        if value not in self.Tables[table]:
            self.Tables[table][value] = []
        else:
            raise Exception("This column {",value,"} already exists in this table {",table,"}")

    def AddValues(self, table, column, value):
        if column in self.Tables[table]:
            try:
                self.Tables[table][column].append(float(value))
            except Exception:
                self.Tables[table][column].append(value)
        else:
            raise Exception("This column {", value, "} not exist in this  table {", table, "}")

    def DeleteTable(self, table):
        if table in self.Tables:
            self.Tables.pop(table)
        else:
            raise Exception("This table { " + table + " } it's not in the database")

    def GetTables(self):
        return self.Tables.copy()