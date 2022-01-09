#logic_eval.py

from src.functions.interpeterCMS import CMSIntrepeter
from src.functions.filesManipulation import FileManipulation as FILES
from src.functions.dataclass import DicDataBase
from pprint import PrettyPrinter

pp = PrettyPrinter()
CMSI = CMSIntrepeter()
tables = DicDataBase()

class LogicEval:

    Commands = {
        "LOAD": lambda args:  LogicEval._LOAD(args),
        "SHOW": lambda args:  LogicEval._SHOW(args),
        "DISCARD": lambda args:  LogicEval._DISCARD(args),
        "SAVE": lambda args:  LogicEval._SAVE(args),
        "SELECT": lambda args:  LogicEval._SELECT(args),
        "CREATE": lambda args:  LogicEval._CREATE(args),
        "CALL":  lambda args:  LogicEval._CALL(args),
    }

    operators = {
        "=": lambda args: args[0] == args[1],
        "< >": lambda args: args[0] != args[1],
        "> =": lambda args: args[0] >= args[1],
        "< =": lambda args: args[0] <= args[1],
        ">": lambda args: args[0] > args[1],
        "<": lambda args: args[0] < args[1],
        "JOIN": lambda args: LogicEval._JOIN(args)
    }

    # ProcedureName -> ListOfProcedure
    Procedure = {}

    @staticmethod
    def _JOIN(args):

        try:

            Tables = tables.GetTables()

            if args['JOIN'] not in Tables:
                raise Exception("The table { " + args['JOIN'] + " } does not exist in the database")

            if args['column'] not in Tables[args['FROM']]:
                raise Exception("The column { " + args['column'] + " } does not exist in the table { " + args['FROM'] + " }")

            if args['column'] not in Tables[args['JOIN']]:
                raise Exception("The column { " + args['column'] + " } does not exist in the table { " + args['JOIN'] + " }")

            newTable = LogicEval._CreateTable(Tables[args['FROM']],  {'column': args['column'], 'rule': args['rule'], 'value': args['value']})

            newTable2 = LogicEval._CreateTable(Tables[args['JOIN']],
                                              {'column': args['column'], 'rule': args['rule'], 'value': args['value']})

            return {**newTable, **newTable2}

        except Exception as e:
            raise Exception(e, " <-> ", args + "\n-------------------------------------------------\n")

    @staticmethod
    def _LOAD(args):

        try:
            print("\n-------- Executing the command '[LOAD]'Table name = [ "+args['TABLE']+" ] --------- ")
            responce = FILES.OpenFile("src\\" + str(args['FROM']['str']), "CSV")

            if responce[0] is False:
                raise Exception(responce[1])

            tables.AddTable(args['TABLE'])

            CMSI.cmsIntrepeter(responce[1], args['TABLE'], tables)

            print('The table was read successfully')
            print("-------------------------------------------------\n")
            return None

        except Exception as e:
            raise Exception(e, "\n", args + "\n-------------------------------------------------\n")

    @staticmethod
    def _SHOW(args):

        try:
            table = tables.GetTables()

            print("\n-------- Executing the command '[SHOW]' Table name = [ "+args['TABLE']+" ] -------- ")


            if args['TABLE'] in table:
                LogicEval._PrintTable(table[args['TABLE']])
                print("-------------------------------------------------\n")
            else:
                raise Exception("This table { "+args['TABLE']+" } does not exist in the database.")

            return None

        except Exception as e:
            raise Exception(e, "\n", args + "\n-------------------------------------------------\n")

    @staticmethod
    def _DISCARD(args):

        try:
            print("-------- Executing the command '[DISCARD]' Table name = [ "+args['TABLE']+" ] - -------- ")
            tables.DeleteTable(args['TABLE'])
            print("The table {"+args['TABLE']+"} has been deleted successfully")
            print("-------------------------------------------------\n")
        except Exception as e:
            raise Exception(e, "\n", args + "\n-------------------------------------------------\n")

    @staticmethod
    def _SAVE(args):

        try:

            print("\n-------- Executing the command '[SAVE]' Table name = [ "+args['TABLE']+" ] --------- ")
            if args['TABLE'] in tables.GetTables():
                res = FILES.CreateFile("src\\", args['AS']['str'], tables.GetTables()[args['TABLE']])
            else:
                raise Exception("This table { "+args['TABLE']+" } does not exist in the database.")

            print("The table {" + args['TABLE'] + "} was created successfully")
            print("-------------------------------------------------\n")
            return None
        except Exception as e:
            raise Exception(e, "\n", args + "\n-------------------------------------------------\n")

    @staticmethod
    def _CreateTable(table, args):

        try:
            temp = {}
            postion = 0
            arP = []

            rule = ""
            value = ""

            if type(args['rule']) is list:
                rule = args['rule'][0]+" "+args['rule'][1]
            else:
                rule = args['rule']

            if type(args['value']) is dict:
                args['value'] = args['value']['str']

            # TEsta os elementos
            for x in table[args['column']]:
                if LogicEval.operators[rule]([x, args['value']]) is True:
                    arP.append(postion)
                postion += 1

            # Guarda no novo dic
            for key in table:
                temp[key] = []
                p = 0
                for l in table[key]:
                    if p in arP:
                        temp[key].append(l)
                    p += 1
            return temp
        except Exception as e:
            raise Exception(e, " <-> ", table,"", args +"\n-------------------------------------------------\n")

    @staticmethod
    def _SELECT(args):

        try:
            print("\n-------- Executing the command '[SELECT]' Table name = [ "+args['FROM']+" ] -------- ")
            TableName = args['FROM']
            Columns = args['list']


            if TableName not in tables.GetTables():
                raise Exception("The table { "+TableName+" } does not exist in the database")

            if 'JOIN' in args:
                Tables = LogicEval.operators["JOIN"](args)
            else:
                Tables = tables.GetTables()

            if 'WHERE' in args:
                newTable = {}
                if args['WHERE']['column'] in Tables[TableName]:
                    newTable = LogicEval._CreateTable(Tables[TableName], args['WHERE'])
                else:
                    raise Exception("The column { " + args['WHERE']['column'] + " } does not exist in the database")

                if 'AND' in args:
                    for x in args['AND']:
                        if x['column'] in Tables[TableName]:
                            newTable = LogicEval._CreateTable(newTable, x)
                        else:
                            raise Exception("The column { " + x['column'] + " } does not exist in the database")
                Tables = newTable

            CTable = {}
            for column in Columns:
                if column != '*':
                    if column not in Tables:
                        raise Exception("The table { "+column+" } does not exist in the database")
                    else:
                        CTable[column] = Tables[column]
                else:
                    CTable = Tables

            if args['Command'] == 'return':
                return CTable
            else:
                LogicEval._PrintTable(CTable)
                print("-------------------------------------------------\n")

            return None

        except Exception as e:
            raise Exception(e, " \n ", args + "\n-------------------------------------------------\n")

    @staticmethod
    def _CREATE(args):
        try:

            print("\n-------- Executing the command '[CREATE]'  -------- ")
            tables.AddTable(args['TABLE'])

            if 'newCommands' in args:
                newCommand = args['newCommands'].copy()
                newCommand['Command'] = "return"
                table = LogicEval.Commands[args['newCommands']['Command']](newCommand)
            elif 'JOIN' in args:
                table = LogicEval._JOIN(args)

            for key in table:
                tables.AddColumns(args['TABLE'], key)
                for value in table[key]:
                    tables.AddValues(args['TABLE'], key, value)

            print("The table {"+args['TABLE']+"} was created and successfully added to the database")
            print("--------------------------------------------------------------------------------------------------\n")

        except Exception as e:
            raise Exception(e, " \n ", args + "\n-------------------------------------------------\n")

    @staticmethod
    def _CreateFunction(ast):
        try:
            print("\n-------- Executing the command '[CREATE FUNCTION]' -------- ")

            if ast['FunctionName'] in LogicEval.Procedure:
                raise Exception("There is already a function created with this name")
            else:
                LogicEval.Procedure[ast['FunctionName']] = []

            for c in ast['ListofComands']:
                command = LogicEval._RArgs(c)
                LogicEval.Procedure[ast['FunctionName']].append(command)

            print("THe function {"+ast['FunctionName']+"} was created and successfully added to the list of functions")
            print("-------------------------------------------------\n")
            return  None
        except Exception as e:
            raise Exception(e, " \n ", ast + "\n-------------------------------------------------\n")

    @staticmethod
    def _CALL(ast):
        try:

            print("\n-------- Executing the command '[CALL FUNCTION]' -------- ")

            if ast['FunctionName'] not in LogicEval.Procedure:
                raise Exception("This function name does not exist in the list of created functions.")

            Commands = LogicEval.Procedure[ast['FunctionName']]

            for Command in Commands:
                LogicEval.Commands[Command['Command']](Command)

            print("The function {"+ast['FunctionName']+"} was called and managed to complete all operations")

            print("-------------------------------------------------\n")

            return None

        except Exception as e:
            raise Exception(e, " \n ", ast + "\n-------------------------------------------------\n")

    @staticmethod
    def _PrintTable(table):

        try:
            arP = {}
            postion = 0

            for x in table:
                arP[x] = postion
                postion += 1

            items = []
            leng = len(table[list(table.keys())[0]])
            for i in range(0, leng):
                temp = [i]
                for k, v in arP.items():
                    temp.append(table[k][i])
                items.append(temp)

            space = "{:<12} "
            for i in range(0, len(table)):
                space += "{:<40} "

            print(space.format('POS', *arP))


            for v in items:
                print(space.format(*v))

        except Exception as e:
            raise Exception(e, " <-> ", table, + "\n-------------------------------------------------\n")

    @staticmethod
    def evaluate(ast):

        if type(ast) is dict:
            return LogicEval._eval_operator(ast)

        if type(ast) is list:
            ans = None
            for a in ast:
                ans = LogicEval.evaluate(a)
            return ans

        raise Exception("Unknown AST type: {",type(ast),"}")

    @staticmethod
    def _RArgs(ast):
        x = True
        ast2 = ast
        dic = {}
        while x:
            dic = {}
            for key in ast2:
                if key == 'args':
                    for x in ast2[key]:
                         if x == "args":
                            dic['args'] = ast2[key]['args']
                         elif x == "Condictions":

                            if dic['AND'] == 'AND':
                                dic.pop('AND')
                                dic['AND'] = []

                            args = ast2[key]['Condictions']['args']
                            con = ast2[key]['Condictions']
                            con.pop('args')
                            dic['AND'].append(con)
                            dic['args'] = args

                         elif x == 'nCommands':

                            dic['newCommands'] = LogicEval._RArgs(ast2[key]['nCommands'])

                         elif x == 'AND':
                             pass

                         else:
                            dic[x] = ast2[key][x]
                else:
                    dic[key] = ast2[key]

            if 'WHERE' in dic:
                if 'args' in dic['WHERE']:

                    args = dic['WHERE']['args']
                    if 'AND' in dic['WHERE']['args']:
                        dic['AND'] = []


                    args = dic['WHERE']['args']
                    dic['WHERE'].pop('args')
                    dic['args'] = args

            if 'args' in dic:
                if dic['args'] == ';':
                    dic.pop('args')
                    dic['end'] = ';'
                ast2 = dic

            if 'end' in dic:
                x = False
            elif 'newCommands' in dic:
                x = False

        return dic

    @staticmethod
    def _eval_operator(ast):

        if 'Command' in ast:
            if ast['Command'] in LogicEval.Commands:
                command = LogicEval._RArgs(ast)
                anw = LogicEval.Commands[ast['Command']](command)
                return anw
            else:
                raise Exception('This {'+ ast['Command'] +'} Command is not available')

        if 'Function' in ast:
            if 'PROCEDURE' in ast['Function']:
                aws = LogicEval._CreateFunction(ast)
                return aws

        raise Exception('Undefined AST', ast)

