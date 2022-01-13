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
            raise Exception(e)

    @staticmethod
    def _LOAD(args):

        try:
            print("\n-------- Executing the command '[LOAD]'Table name = [ "+args['TABLE']+" ] --------- ")
            responce = FILES.OpenFile("src\\CSV\\" + str(args['FROM']['str']), "CSV")

            if responce[0] is False:
                raise Exception(responce[1])

            tables.AddTable(args['TABLE'])

            CMSI.cmsIntrepeter(responce[1], args['TABLE'], tables)

            print('The table was read successfully')
            print("--------------------------------------------------------------------------------------------------\n")
            return None

        except Exception as e:
            raise Exception(e)

    @staticmethod
    def _SHOW(args):

        try:
            table = tables.GetTables()

            print("\n-------- Executing the command '[SHOW]' Table name = [ "+args['TABLE']+" ] -------- ")


            if args['TABLE'] in table:
                limit = 0
                LogicEval._PrintTable(table[args['TABLE']],limit)
                print("-------------------------------------------------------------------------------------------------\n")
            else:
                raise Exception("This table { "+args['TABLE']+" } does not exist in the database.")

            return None

        except Exception as e:
            raise Exception(e)

    @staticmethod
    def _DISCARD(args):

        try:
            print("-------- Executing the command '[DISCARD]' Table name = [ "+args['TABLE']+" ] - -------- ")
            tables.DeleteTable(args['TABLE'])
            print("The table {"+args['TABLE']+"} has been deleted successfully")
            print("--------------------------------------------------------------------------------------------------\n")
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def _SAVE(args):

        try:

            print("\n-------- Executing the command '[SAVE]' Table name = [ "+args['TABLE']+" ] --------- ")
            if args['TABLE'] in tables.GetTables():
                res = FILES.CreateFile("src\\CSV\\", args['AS']['str'], tables.GetTables()[args['TABLE']])
            else:
                raise Exception("This table { "+args['TABLE']+" } does not exist in the database.")

            print("The table {" + args['TABLE'] + "} was created successfully")
            print("------------------------------------------------------------------------------------------------\n")
            return None
        except Exception as e:
            raise Exception(e, "\n", args , "\n--------------------------------------------------------------------------------------------------\n")

    @staticmethod
    def _CreateTable(table, args):

        try:
            temp = {}
            position = 0
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
                    arP.append(position)
                position += 1

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
            raise Exception(e, " <-> ", table,"", args ,"\n--------------------------------------------------------------------------------------------------\n")

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

            if TableName in Tables:
                Tables = Tables[TableName]

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

                limit = 0
                if 'LIMIT' in args:
                    limit = args['LIMIT']

                LogicEval._PrintTable(CTable, int(limit))

            return None

        except Exception as e:
            raise Exception(e)

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
            print("---------------------------------------------------------------------------------------------------------------------------------------------------\n")

        except Exception as e:
            raise Exception(e)

    @staticmethod
    def _CreateFunction(ast):
        try:
            print("\n-------- Executing the command '[CREATE FUNCTION]' -------- ")

            if ast['FunctionName'] in LogicEval.Procedure:
                raise Exception("There is already a function created with this name")
            else:
                LogicEval.Procedure[ast['FunctionName']] = []

            for c in ast['ListofComands']:
                command = LogicEval._eval_operator(c)
                LogicEval.Procedure[ast['FunctionName']].append(command)

            print("THe function {"+ast['FunctionName']+"} was created and successfully added to the list of functions")
            print("--------------------------------------------------------------------------------------------------\n")
            return  None
        except Exception as e:
            raise Exception(e)

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

            print("--------------------------------------------------------------------------------------------------\n")

            return None

        except Exception as e:
            raise Exception(e)

    @staticmethod
    def _PrintTable(table, limit):

        try:
            arP = {}
            position = 0

            for x in table:
                arP[x] = position
                position += 1

            items = []

            leng = len(table[list(table.keys())[0]])
            if LogicEval.operators[">"]([limit, 0]):
               if LogicEval.operators[">"]([leng, limit]):
                    leng = limit

            for i in range(0, leng):
                temp = [i]
                for k, v in arP.items():
                    temp.append(table[k][i])
                items.append(temp)

            space = "{:<12} "
            for i in range(0, len(table)):
                space += "{:<25} "

            print(space.format('POS', *arP))


            for v in items:
                print(space.format(*v))

        except Exception as e:
            raise Exception(e)

    @staticmethod
    def evaluate(ast):

        if type(ast) is dict:
            return LogicEval._eval_Command(ast)

        if type(ast) is list:
            ans = None
            for a in ast:
                ans = LogicEval.evaluate(a)
            return ans

        raise Exception("Unknown AST type: {",type(ast),"}")

    @staticmethod
    def _eval_Command(ast):

        if 'Command' in ast:
            if ast['Command'] in LogicEval.Commands:
                command = LogicEval._eval_operator(ast)
                answer = LogicEval.Commands[ast['Command']](command)
                return answer
            else:
                raise Exception('This {'+ ast['Command'] +'} Command is not available')

        if 'Function' in ast:
            if 'PROCEDURE' in ast['Function']:
                answer = LogicEval._CreateFunction(ast)
                return answer

        raise Exception('Undefined AST', ast)

    @staticmethod
    def _eval_operator(ast):

        if 'args' in ast:
            if ast['args'] != ';':
                args = ast['args']
                ast.pop('args')
                ast = LogicEval._eval_operator({**ast, **args})
            else:
                ast['end'] = ast['args']
                ast.pop('args')


        if 'nCommands' in ast:
            ast['newCommands'] = LogicEval._eval_operator(ast['nCommands'])
            ast.pop('nCommands')

            if 'end' in ast['newCommands']:
                args = ast['newCommands']['end']
                ast['newCommands'].pop('end')
                if type(args) == str:
                    ast = {**ast, 'end': args}


        if 'WHERE' in ast:
            if 'args' in ast['WHERE']:
                args = ast['WHERE']['args']
                ast['WHERE'].pop('args')
                if type(args) == str:
                    ast ={**ast, 'end': args}
                else:
                    ast = LogicEval._eval_operator({**ast, **args})

            if 'AND' in ast:
                if 'opAND' not in ast:
                    ast['opAND'] = []

                if 'Condictions' in ast:
                    Condictions = ast['Condictions']
                    ast.pop('Condictions')
                    args = Condictions['args']
                    Condictions.pop('args')
                    ast['opAND'].append(Condictions)

                    if type(args) == str:
                        ast = {**ast, 'end': args}
                    else:
                        ast = LogicEval._eval_operator({**ast, **args})


        if 'end' in ast:
            if 'AND' in ast:
                if type(ast['AND']) == str:
                    ast.pop('AND')
                    ast['AND'] = ast['opAND']
                if 'opAND' in ast:
                    ast.pop('opAND')
            return ast

        raise Exception('Undefined Command', ast)

