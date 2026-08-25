from Token import Token
from collections import deque
class Renderer():
    def __init__(self):
        self.data = ''
        self.renderData = ''
        self.specials = ['a','img']
        self.lists = ['li','ul','ol']
    def read(self):
        with open("test.md",'r') as f:
            self.data = deque(f.read().split('\n'))
    def render(self):
        def addLists(arr,typ):
            if not arr:
                return
            r = f"""
                <{typ}>
            """
            for x in arr:
                r += x
            r += f'</{typ}>'
            self.renderData += r
        isP = False
        arr = []
        idx = 0
        while idx < len(self.data) - 1:
            p = self.data[idx]
            if p.strip() != '':
                if idx > 0:
                    if self.data[idx - 1].strip() == '':
                        isP = True
                tok = Token(p)
                if isP and tok.type == '':
                    tok.val = p.strip()
                    tok.type = 'p'
                    isP = False
                arr.append(tok)
            idx += 1
        if self.data[len(self.data) - 1].strip() != '':
            tok = Token(self.data[len(self.data) - 1])
            if self.data[len(self.data) - 2].strip() == '':
                isP = True
            if isP and tok.type == '':
                tok.val = self.data[len(self.data) - 1].strip()
                tok.type = 'p'
                isP = False
            arr.append(tok)
        listNode = []
        listType = ''
        listEnd = False
        for x in arr:
            typ = x.type
            val = x.val
            if typ in self.lists:
                if listType and typ != listType:
                    addLists(listNode, listType)
                    listNode = []
                listType = typ
                listNode.append(f'<li>{val}</li>\n')
                listEnd = True
                continue

            if listEnd:
                addLists(listNode, listType)
                listNode = []
                listType = ''
                listEnd = False

            if typ not in self.specials:
                self.renderData += f'<{typ}>{val}</{typ}>\n'
            elif typ in self.specials:
                if typ == 'a':
                    if val['title'] != '':
                        self.renderData += f'<a href="{val["href"]}" title="{val["title"]}">{val["val"]}</a>\n'
                    else:
                        self.renderData += f'<a href="{val["href"]}">{val["val"]}</a>\n'
                elif typ == 'img':
                    if val['title'] != '':
                        self.renderData += f'<img src="{val["href"]}" alt="{val["val"]}" title="{val["title"]}">\n'
                    else:
                        self.renderData += f'<img src="{val["href"]}" alt="{val["val"]}">\n'
            print(x.val,x.type)
        if listEnd:
            addLists(listNode, listType)
    def save(self):
        with open("result.html",'w') as f:
            f.write(f"""
            <!DOCTYPE html>
            <html lang='en'>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>MD Viewer Result</title>
            </head>
            <body>
            {self.renderData}
            </body>
            </html>
                """)