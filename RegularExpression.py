

import nafUtils

class RegularExpression(object):
    def __init__(self, input_string, regular_string):
        self.input_string = input_string
        self.regular_string = regular_string
        self.graph = None

    def matchOne(self):
        reg = self.regular_string
        str = self.input_string
        nfa_machine = nafUtils.nfa_builder(reg)
        self.graph = nafUtils.get_visualize(nfa_machine)
        return nafUtils.match(str, nfa_machine)
    def match(self):
        for i in range(len(self.input_string)):
            result = self.matchOne()
            if result:
                break
            self.input_string = self.input_string[1:]
        if len(result)==0:
            return "You should enter the correct expression"
        return "".join(result)

    def search(self, groupID):
        reg = self.regular_string
        str = self.input_string
        nfa_machine = nafUtils.nfa_builder(reg)
        self.graph = nafUtils.get_visualize(nfa_machine)

        resultSearch = nafUtils.search(str, nfa_machine, groupID)
        return "".join(resultSearch)

    def position(self):
        for i in range(len(self.input_string)):
            start = None
            end = None
            result = self.matchOne()
            for index, str in enumerate(self.input_string):
                if str == result[index]:
                    start = index
                if str != result[index]:
                    end = index-1
                if index == len(self.input_string)-1:
                    if str == self.input_string[-1]:
                        end = len(self.input_string)-1
                    if start is not None:
                        return True, start, end



    def split(self):
        for i in range(len(self.input_string)):
            result = self.matchOne()

            if result:
                break
            self.input_string = self.input_string[1:]
        if len(result) == 0:
            return "You should enter the correct expression"
        return "".join(result)