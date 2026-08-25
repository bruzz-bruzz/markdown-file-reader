import Token from './Token'
import {Deque} from '@datastructures-js/deque'
export default class Renderer{
    data:Deque<string>;
    renderData:string;
    specials:string[];
    lists:string[]
    constructor(data:string){
        this.data = new Deque(data.split('\n'))
        this.renderData = ''
        this.specials = ['a','img']
        this.lists = ['li','ul','ol']
    }
    render(){
        function addLists(arr:string[],typ:string){
            if(arr.length === 0){
                return
            }
            let r = 
            `
            <${typ}>
            `
            for(let x of arr){
                r += x
            }
            r += `</${typ}>`
            return r
        }
        let isP = false
        let arr = []
        let idx = 0
        while(idx < this.data.size() - 1){
            let tmpArr = this.data.toArray()
            let p = tmpArr[idx]
            if(p.trim() !== ''){
                if(idx > 0){
                    if(tmpArr[idx - 1].trim() == ''){
                        isP = true
                    }
                }
                let tok = new Token(p)
                if(isP === true && tok.type === ''){
                    tok.val = p.trim()
                    tok.type = 'p'
                    isP = false
                }
                arr.push(tok)
            }
            idx += 1
        }
        if(this.data[this.data.length - 1].trim() !== '')
    }
}