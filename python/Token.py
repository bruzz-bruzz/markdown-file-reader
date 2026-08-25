from collections import deque
class Token():
    def __init__(self,value):
        self.KEYS = {
            '#':"h1",
            '##':"h2",
            '###':"h3",
            '####':"h4",
            '#####':"h5",
            '######':'h6',
            '>':"blockquote",
            '**':"strong",
            '__':"strong",
            '*':"em",
            '_':"em",
            '`':"code",
            '[':"a",
            '!':"img",
            '-':"ul",
            '+':"ul",
            '1':"ol",
            '2':"ol",
            '3':"ol",
            '4':'ol',
            '5':"ol",
            '6':"ol",
            '7':"ol",
            '8':"ol",
            "9":"ol",
            '0':"ol"
        }
        self.blocks = ['h1','h2','h3','h4','h5','h6','p','blockquote']
        self.inlines = ['strong','em','code']
        self.specials = ['a','img']
        self.lists = ['li']
        self.val = ''
        self.type = self.getType(value)
    def getType(self,val):
        if val == '___' or val == '***' or val == '---':
            self.val = ''
            return 'hr'
        key = ''
        val = deque(list(val))
        p = ''
        while val:
            p = val.popleft()
            if key + p not in self.KEYS.keys():
                val.appendleft(p)
                break
            key += p
        typ = ''
        if key == '*':
            if val[0] == ' ':
                self.val = ''.join([x for x in val]).strip()
                return 'ul'
            typ = 'em'
        elif key in self.KEYS.keys():
            typ = self.KEYS[key]
            if typ == 'ol':
                val.popleft()
        else:
            typ = ''
        if typ not in self.inlines and typ not in self.specials and typ not in self.lists:
            self.val = ''.join([x for x in val]).strip()
        elif typ in self.inlines:
            l = len(key)
            p = ''.join([x for x in val])
            self.val = p[:len(p) - l].strip()
        elif typ in self.specials:
            self.val = {
                'href':"",
                "val":"",
                'title':""
            }
            if typ == 'a':
                p = deque(list(''.join([x for x in val]).strip()))
                val = ''
                while len(p) > 0:
                    po = p.popleft()
                    if po == ']':
                        break
                    val += po
                self.val['val'] = val
                href = ''
                hasTitle = False
                while len(p) > 0:
                    po = p.popleft()
                    if po == ' ':
                        hasTitle = True
                        break
                    href += po if po != '(' and po != ')' else ''
                self.val['href'] = href
                if hasTitle:
                    p = ''.join([x for x in p]).strip()
                    p = p[:len(p) - 1]
                    self.val['title'] = p.strip('"')
            elif typ == 'img':
                p = deque(list(''.join([x for x in val]).strip()))
                p.popleft()
                val = ''
                while len(p) > 0:
                    po = p.popleft()
                    if po == ']':
                        break
                    val += po
                self.val['val'] = val
                p.popleft()
                file = ''
                hasTitle = False
                while len(p) > 0:
                    po = p.popleft()
                    if po == ' ':
                        hasTitle = True
                        break
                    file += po
                file = file[:len(file) - 1] if file[len(file) - 1] == ')' else file
                self.val['href'] = file
                if hasTitle:
                    p = ''.join([x for x in p]).strip()
                    p = p[:len(p) - 1]
                    self.val['title'] = p.strip('"')
        return typ