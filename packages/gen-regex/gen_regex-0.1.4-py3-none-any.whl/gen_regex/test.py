import pytest
from .core import  RegexGenerator,Tokenizer
import re

def excute(text,querys):

    print(text,querys)
    tk = Tokenizer()
    tokenized = tk.tokenize(text,querys)
    #for t in tokenized  :
    #    print(t)    

    gen = RegexGenerator()
    gen.run(text,tokenized)
    extracted_elements = []
    for p in gen.element_pattern:
        elm = re.findall(p,text)[0]
        extracted_elements.append(elm)
    return extracted_elements

def testcase_easy():
    S = '踏み台:M122'
    querys = ['踏み台','M122']
    assert querys == excute(S,querys)

def testcase_standard():
    S = 'サイズ/Rc1/8、-100cm、(方法/ねじ込み)空気、別尺ー・：100mm'
    querys = ["Rc", "1/8", '-100', '方法/ねじ込み', '空気', '100']

    assert querys == excute(S,querys)
def test_continue_same_patern():
    S = '1×10×234×111×456×999'
    querys = ['1', '10', '234', '111', '456', '999']
    assert querys == excute(S,querys)

def testcase_contain_many_newline():
    S = '【ねじ込み】23/8\n5/76,折りたたみ9/8(常時)\n\n2/48(非常時)mm'
    querys = ['ねじ込み', '23/8', '5/76', '折りたたみ', '9/8', '常時', '2/48', '非常時']

    assert querys == excute(S,querys)


def testcase_contain_many_space():
    S = '商品名 テスト商品 商品コード\n12345 単価 100 '
    querys = ['テスト商品', '12345', '100']
    

    assert querys == excute(S,querys)
def testcase_complex1():
    S = '呼び径50A長さ10m,最高温度:200℃\n適用圧力:1.0MPa,材質:SUS304'
    querys = ['50A', '10', '200', '1.0', 'SUS304']
    

    assert querys == excute(S,querys)

def testcase_complex2():
    S = '呼び径20A\nサイズ：67×155×49mm\n適用：圧力　0.01～0.7MPa'
    querys = ['20A', '67', '155', '49', '0.01', '0.7']
    
    assert querys == excute(S,querys)

def testcase_complex3():
    S = '品番:XXX-ABCD-1-XYZ-5-123\n寸法:L1000×W300×H500mm\n重量:10kg\nカラー:ブラック\n(特記事項:強度に優れる)'
    querys = ['1000', '300', '500', '10', 'ブラック', '強度に優れる']
    

    assert querys == excute(S,querys)

def testcase_complex4():
    S = '●仕様：自在ストッパー付●サイズ：キャスター：Φ100\n24.5(幅)mm取付高：125mmネジ径：9mm●重量：約550g(1個)●耐荷重：静止時：400走行移動時：80kg●材質：金具：スチール(亜鉛メッキ) 車輪：ゴム●使用温度範囲：-40～80℃●入数：2個●ねじサイズ：3/8” 16山'
    querys = ['自在ストッパー付','100\n24.5','静止時','400','走行移動時','80','3/8','16']
    

    assert querys == excute(S,querys)

def testcase_complex5():
    S = '-999×-999×-9/99×-999'
    querys = ['-999', '-999', '-9/99','-999']
    

    assert querys == excute(S,querys)

def testcase_complex6():
    S = '【ねじ込み】2/38\n【ねじ込み】23/8\n【ねじ込み】23.8'
    querys = ['ねじ込み', '2/38','ねじ込み','23/8','ねじ込み', '23.8'] 
    

    assert querys == excute(S,querys)
