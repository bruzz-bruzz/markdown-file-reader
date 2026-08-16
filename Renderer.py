from Token import Token
class Renderer():
    def __init__(self):
        self.data = ''
    def read(self):
        with open("test.md",'r') as f:
            self.data = f.read().split('\n')
    def render(self):
        arr = []
        for x in self.data:
            arr.append(Token(x))
        for x in arr:
            print(x.val,x.type.type)
    def save(self):
        with open("result.html",'w') as f:
            self.data = ''