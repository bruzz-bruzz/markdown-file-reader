from Node import Node
class Token():
    def __init__(self,value):
        self.val = value
        self.type = self.getType(value)
    def getType(self,val):
        val = val.split(' ')
        print(val)
        if val[0] == '---' or val[0] == '***':
            return Node(['hr'],'')
        elif val[0] == '>':
            return Node(['blockquote'],val[1])
        elif val[0] == '-' or val[0] == '*' or val[0] == '+':
            if val[1] == '[ ]' or val[1] == '[x]':
                return Node(['ul','checkbox'],val[2])
            return Node(['ul'],val[1])
        elif val[0] in '1234567890':
            return Node(['ol'],val[1])
        if val[0][0] == '#':
            return Node([f'h{val[0].count("#")}'],val[1])
        elif val[0][0] == '*' or val[0][0] == '_':
            c = val[0][0].count("*") or val[0][0].count("_")
            if c == 1:
                return Node(['em'],val[0][1:len(val[0]) - 1])
            elif c == 2:
                return Node(['strong'],val[1][1:len(val[0]) - 2])
            elif c == 3:
                return Node(['strong','em'],val[0][2:len(val[0]) - 3])
        elif val[0][0:2] == '~~':
            return Node(['del'],val[0][2:len(val[0]) - 2])
        elif val[0][0] == '`':
            return Node(['code'],val[0][1:len(val[0]) - 2])
        elif val[0][0] == '[':
            return Node([])
        elif val[0][0] == '!':
            return ['img']
