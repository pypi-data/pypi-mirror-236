from dataclasses import dataclass

import re,regex

LITERAL_REGEX= "(^|[^A-Za-z])(呼び径|MPa|mm|cm|m|高さ|長さ|幅)($|[^A-Za-z])"


def is_symbol(text):
    return True if not regex.match('([\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}A-Za-zー]+|\d+(,?\/?\.?\d+)?|\.)',text) else False

@dataclass
class Token:
    idx : int
    pos : int
    text : str
    is_symbol : bool
    is_element : bool
    
class Tokenizer:
    def __init__(self ) -> None:

        self.idx =-1    

    def split_symbol(self, text : str) -> list:
        '''
            Desc:
                文字列を記号とそれ以外の文字列に分割する
        '''
        tokens =[]
        tmp = []

        for t in  text:
            if is_symbol(t):
                tokens.append(''.join(tmp))
                tokens.append(t)
                tmp=[]
            else:
                tmp.append(t)
        tokens.append(''.join(tmp))
        tokens = [t for t in tokens if t != '']
        return tokens

    def tokenize(self,text : str, elements : list)-> list : 
        '''
            Desc:
                テキストから elements とそれ以外の文字列を分割し、トークンインスタンスのリストを作成

            Args:
                text(str) : 元のテキスト
                elements(list[str]) : 抽出したいelementのリスト
            Return:
                splited_tokens(list[Token]) : 分割されたトークンのリスト

        '''
        
        splited_tokens =  []

        pre_end = 0

        # SYMBOL_REGEXの記号、抽出したいelementとそれ以外で分割し、トークンインスタンスリストを作成

        for i in range(len(elements)):
            token_start = text.index(elements[i], pre_end)
            token_end = token_start + len(elements[i])

            #print(elements[i],token_start,token_end, pre_end, text[pre_end:token_start])
            # elementの前の文字列をトークン化
            if token_start != pre_end:
                token_txt  = text[pre_end : token_start]
                for t in self.split_symbol(token_txt):
                    token = self.create_token(t,token_start,False)
                    splited_tokens.append(token) 


            # elementをトークン化
            token_txt = text[token_start : token_end]
            token = self.create_token(token_txt,token_start,True)
            splited_tokens.append(token) 

            pre_end = token_end

        # 最後のelement以降の文字列をトークン化
        token_txt = text[token_end:]
        for t in self.split_symbol(token_txt):
            token = self.create_token(t,token_start,False)
            splited_tokens.append(token) 

        self.reset_idx()
        return splited_tokens
    def reset_idx(self,):
        self.idx = -1
    def create_token(self, text : str,pos, is_element : bool) -> Token:
        ''' 
            トークンインスタンスを作成
        '''
        is_sym = is_symbol(text)
        
        self.idx += 1
        return Token(self.idx,pos,text,  is_sym,is_element, )
 

class RegexGenerator:

    def __init__(self, literal_regex = None) -> None:
        self.meta_char = ['\n',' ']
        self.element_pattern = []
        self.literal_regex = literal_regex if literal_regex else LITERAL_REGEX

    def is_lit(self, text : str) -> bool:
        return True if re.match(self.literal_regex, text)  else False

    def gen_regex(self,text ,is_full):
        '''
            正規表現を生成
            Args: 
                text(str) : 対象のテキスト
                is_full(bool) : Trueの場合、汎用マッチ、Falseの場合、数字かそれ以外の一文字マッチの正規表現を生成
        '''
        if self.is_lit(text):
            return text
        if text in self.meta_char:
            return self.cvt_meta_char(text)
        if is_symbol(text):
            return re.escape(text)
        
        if is_full:
            '''
            if re.search(r"^\d+(\.\d+)?$", text):
                return r"\d.*?"
            elif regex.search(r"^[\p{Script=Han}\p{Script=Katakana}\p{Script=Hiragana}A-Za-zー]+$", text):
                return r"\D.*?"
            else :
                return r".+?"
            '''
            return r".+?"
        else:
            if re.search(r"^\d+(\.?\/?\d+)?$", text):
                return r"\d"
            elif regex.search(r"^[\p{Script=Han}\p{Script=Katakana}\p{Script=Hiragana}A-Za-zー]+$", text):
                return r"\D"
            else : return text


    def cvt_meta_char(self, text : str) -> str:
        if text == "\n": return "\\n"
        if text == " ":return "\\s"


   
    def gen_capture_regex(self, text  ) -> str:
        ''' 抽出したいテキストを正規表現に変換'''

        #if re.match("^\d+/\d+$",text):return "(\d+/\d+)"
        if re.match("^\d+(\.?\/?\d+)?$",text):return "(\d.*?)"
        elif regex.match("^[\p{Script=Han}\p{Script=Katakana}\p{Script=Hiragana}A-Za-zー]+$",text):return "(\D.*?)"
        elif re.search('\n',text): return "([\s\S]+?)"
        else: return "(.+?)"

    def cvt_capture_regex(self, text,token,gen_re) -> str:
        '''
            キャプチャの正規表現を .+? に変換
        '''
        re_list = ["\d+/\d+","\d.*?","\D.*?","[\s\S]+?"]

        #gen_re = re.sub('(\.\+\?){2,}', '.+?', gen_re)
        for r in re_list:
            try_re = gen_re.replace(r,f".+?")
            if try_re == gen_re: continue
            if self.check_regex(text,token,try_re): 
                return try_re
        return gen_re
    
    def check_regex(self, text, token : str, gen_re: str) -> bool:
        '''
            正規表現がテキストにマッチするか確認 (抽出したテキストのposition check (start,end) )
        '''
        element = token.text
        text_pos = token.pos
        for m in re.finditer(gen_re, text):
            '''
            print(f"regex : {gen_re}")
            print(f"match index : {m.start(1)}-{m.end(1)} == gt : {text_pos}-{text_pos + len(element) }")
            print(f"extracted element : {m.group(1)} == gt : {element}")
            print()
            '''
            if m.start(1) == text_pos and m.end(1) == text_pos + len(element) :
                return True
            else:
                return False 
    



    def run(self, text,tokens : list[Token] ) -> None:

        '''
            Desc:
                テキストとトークンのリストから、抽出したいテキストの正規表現を生成
                最初に抽出したいテキストをキャプチャする正規表現と、両脇の１文字マッチの正規表現を生成し、マッチチェック
                マッチできなければ、現在のトークンの左トークンの正規表現を逐次結合してマッチチェックをする。
                同時に、左側のトークンがsymbolであれば、それに .+, .+?, [\s\S]+ を連結してマッチチェック(マッチすればシンプルな正規表現になる)
            Args:
                text(str) : テキスト
                tokens(list[Token]) : トークン化されたテキストのリスト
        '''
        for token in tokens:
            if not  token.is_element: continue

            idx = token.idx
            
            # 現在のトークンindex ±1 のleft,right トークンテキストを正規表現を生成
            left_re = "^" if idx-1 < 0 \
                                    else self.gen_regex( tokens[idx-1].text,is_full=False)
            right_re = '$' if idx+1 >= len(tokens) \
                                    else  self.gen_regex(tokens[idx+1].text ,is_full=False)

            cap_re = self.gen_capture_regex(token.text)

            #print(left_re,cap_re,right_re)

            #print("==== Try match minimal regex")

            concat_cap_re = left_re + cap_re + right_re
            if self.check_regex(text,token,concat_cap_re): 
                concat_cap_re = self.cvt_capture_regex(text,token,concat_cap_re)
                self.element_pattern.append(concat_cap_re)
                continue


            #print("==== Try match concat regex with left element")
            # 1. left_re(full) + cap_re + right_re でマッチするか確認
            # 2. left.text がsymbolであれば、それに .+, .+?, [\s\S]+ を連結してマッチを試みる
            # 3. element_pattern[-1] != "" であれば、break
            # 4. 1.に戻る
            concat_cap_re =  cap_re + right_re
            self.element_pattern.append("")
            for i in range(max(idx-1,0),-1,-1):

                left_re = self.gen_regex(tokens[i].text,is_full=True)
                concat_cap_re = left_re + concat_cap_re

                if not is_symbol(tokens[i].text):
                    if self.check_regex(text,token,concat_cap_re):
                        self.element_pattern[-1] = concat_cap_re
                        break


                for add_pttn in ['.+', '.+?', '[\s\S]+', '[\s\S]+?',]:
                    added_re = add_pttn + concat_cap_re
                    if self.check_regex(text,token,added_re):
                        self.element_pattern[-1] = added_re
                        break

                if self.element_pattern[-1] != "": break
                    
            self.element_pattern[-1] = self.cvt_capture_regex(text,token,self.element_pattern[-1])

        #print(self.element_pattern)
def main():
    text = """幅:100mm 長さ:1000mm


    厚さ:1.0mm(※冷却時は0.5mm程度縮みます)、高さ100非常"""
    text = "A:100mm、B:1000mm、C:100mm、D:100非常"
    elements = ["幅","100","長さ","1000","厚さ","1.0","100","非常"]
    elements = ["A","100","B","1000","C","100","D","100","非常"]
    tokenizer = Tokenizer()
    tokenized = tokenizer.tokenize(text,elements)
    #tokenized = tokenizer.split_symbol(text)

    for t in tokenized  :
        print(t)


    gen = RegexGenerator()
    gen.run(text,tokenized)


def test_tokenize( ):
    # test tokenize
    text = '2心・5'
    elements = [ '2', "5"]
    
    


    tokenizer = Tokenizer()

    tokenized = tokenizer.tokenize(text,elements)
    for t in tokenized  :
        print(t)    


    gen = RegexGenerator()
    gen.run(text,tokenized)
    extracted_elements = []
    for i in range(len(elements)):
        p = gen.element_pattern[i]       
        elm = re.findall(p,text)[0]

        assert elm == elements[i]
    
    print(gen.element_pattern)
