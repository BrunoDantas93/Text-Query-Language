from src.functions.logic_grammar import LogicGrammar
from src.functions.filesManipulation import FileManipulation as fm
from src.functions.logic_eval import LogicEval as le
from pprint import PrettyPrinter

pp = PrettyPrinter()
lg = LogicGrammar()
lg.build()

class Menu:


    options = {
        "1": lambda args: Menu._FileReader(),
        "2": lambda args: Menu._ImputCMD(),
        "3": lambda args: exit("See you later")
    }

    @staticmethod
    def _MenuC():
            print("+-----------------------------------------------------------------------------------+")
            print("|                       [1] -> Read commands from a txt file.                       |")
            print("|                       [2] -> Read the commands by CMD imput                       |")
            print("|                       [3] -> Exit the program                                     |")
            print("+-----------------------------------------------------------------------------------+")
            while True:
                try:
                    choice = input("What is the name of the folder it belongs to process? -> ")
                    if int(choice) > 0 and int(choice) < 4:
                            Menu.options[choice](choice)
                            break
                    else:
                        print("The value entered is not valid")

                except Exception as e:
                    raise Exception(e)

    @staticmethod
    def _FileReader():
            print("For the file to be detected and read has to be inside the Commands folder and the CSVs in the CSV folder")

            try:
                fileName = input("What is the name of the file that has the commands? -> ")
                rresponce = fm.ValidFile("src\\Commands\\"+fileName, "txt")
                if rresponce[0] is False:
                    raise Exception(rresponce[1])

                with open("src\\Commands\\"+fileName, "r") as file:
                    contents = file.read()

                ans = lg.parse(contents)
                pp.pprint(ans)
                le.evaluate(ans)
            except Exception as e:
                raise Exception(e)

    @staticmethod
    def _ImputCMD():
        print("For the file to be detected and read it must be inside the CSV folder")
        print('Type "[EXIT]" to exit the input reader')
        for expr in iter(lambda: input("Command >> "), ""):
            try:
                if expr == 'EXIT':
                    break
                else:
                    ans = lg.parse(expr)
                    pp.pprint(ans)
                    le.evaluate(ans)
            except Exception as e:
                raise Exception(e)

    @staticmethod
    def CallMenu():
        while True:
            try:
                Menu._MenuC()
            except Exception as e:
                print(f'\033[91m-> {e}\033[0m')