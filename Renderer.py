class Renderer():
    def __init__(self):
        self.data = ''
    def read(self):
        with open("test.md",'r') as f:
            self.data = f.read()
    def render(self):
        with open("result.html",'w') as f:
            