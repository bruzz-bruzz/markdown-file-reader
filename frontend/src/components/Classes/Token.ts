import {Deque} from '@datastructures-js/deque'
export default class Token{
    keys:Record<string,string>;
    blocks:string[];
    inlines:string[];
    specials:string[];
    lists:string[];
    val:string;
    type:string | {
        'href':string,
        'val':string,
        'title':string
    };
    constructor(value:string){
        this.keys = {
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
        this.blocks = ['h1','h2','h3','h4','h5','h6','p','blockquote']
        this.inlines = ['strong','em','code']
        this.specials = ['a','img']
        this.lists = ['li']
        this.val = ''
        this.type = this.getType(value)
    }
    getType(val:string){
        if(val === '___' || val === '***' || val === '---'){
            this.val = ''
            return 'hr'
        }
        let key = ''
        let deque = new Deque<string>(Array.from(val))
        console.log(Object.keys(this.keys))
        while(val.length > 0){
            let p:string = deque.popFront() as string
            if(Array.from(Object.keys(this.keys)).includes(key + p)){
                deque.pushBack(p)
            }
            key += p
        }
        let typ = ''
        if(key === '*'){
            if(val[0] == ' '){
                this.val = deque.toArray().join("").trim()
                return 'ul'
            }
            typ = 'em'
        } else if(Object.keys(this.keys).includes(key)){
            typ = this.keys[key]
            if(typ === 'ol'){
                deque.popFront()
            }
        } else { typ = '' }
        if(!this.inlines.includes(typ) && !this.specials.includes(typ) && this.lists.includes(typ)){
            this.val = deque.toArray().join("").trim()
        } else if(this.inlines.includes(typ)){
            let l = key.length
            let p = deque.toArray().join("")
            this.val = p.slice(0,p.length - l).trim()
        } else if(this.specials.includes(typ)){
            this.val = {
                "href":"",
                "val":"",
                "title":""
            }
            if(typ === 'a'){
                let p:any = new Deque(Array.from(deque.toArray().join("").trim()))
                let val = ''
                while(p.size() > 0){
                    let po = p.popFront()
                    if(po === ']'){
                        break
                    }
                    val += po
                }
                this.val["val"] = val
                let href = ''
                let hasTitle = false
                while(p.size() > 0){
                    let po = p.popFront()
                    if(po === ' '){
                        hasTitle = true
                        break
                    }
                    href += po !== '(' && po !== ')' ? po : ''
                }
                this.val["href"] = href
                if(hasTitle === true){
                    p = p.toArray().join("").trim()
                    p = p.slice(0,p.size() - 1)
                    let str = 'a'
                    this.val["title"] = p.trim('"')
                }
            } else if(typ === 'img'){
                let p:any = new Deque(Array.from(deque.toArray().join("").trim()))
                p.popFront()
                let val = ''
                while(p.size() > 0){
                    let po = p.popFront()
                    if(po === ']'){
                        break
                    }val += po
                }
                this.val["val"] = val
                p.popFront()
                let file = ''
                let hasTitle = false
                while(p.size() > 0){
                    let po = p.popFront()
                    if(po === ' '){
                        hasTitle = true
                        break
                    }file += po
                }
                file = file[file.length - 1] === ')' ? file.slice(0,file.length - 1) : file
                this.val["href"] = file
                if(hasTitle === true){
                    p = p.toArray().join("").trim()
                    p = p.slice(0,p.length - 1)
                    this.val["title"] = p.trim('"')
                }
            }
        }
        return typ
    }
}