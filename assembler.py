import ctypes
import sys

#処理に必要なクラスの定義
import define
#命令と、それに応じた引数の設定
import instruction
#instructionで設定された設定を32bitのbinにする
import encode
#x0やraなどを具体的な数値へ変換
import regs
#binファイルとして出力
import export_bin
#コマンドライン引数の処理
import commandline_args

def get_file(filename = "untitled.rvi"):
    f = open(filename,'r')
    return f

def get_tokens_of_a_row(row: str):
    #コメントアウト以降を消去する
    row = row.split('#')[0]

    #コンマを空白へ置き換える
    row = row.replace(',',' ')

    #空白で分ける
    tokens = row.split()

    return tokens

#ファイルの内容を処理上余計なものを省いたstrの2次元配列で返す
def trim(rows):
    return_value = []

    for i in rows.readlines():
        tokens_of_a_row = get_tokens_of_a_row(i)

        #リストがからでなければ
        if(tokens_of_a_row != []):
            return_value.append(tokens_of_a_row)

    return return_value

#ラベルの検出、詳細の設定
def set_label(lines:list[str]):
    #ラベルの情報を格納する配列
    labels = []

    i = 0

    while i < len(lines):
        #もしトークンの最後が":"だったらラベルと認識する
        if(lines[i][0][-1] == ":"):
            new_label = define.label_info()
            #アドレスをプログラムカウンタに
            new_label.address = i*4
            #名前(":"の手前までとする)を代入
            new_label.name = lines[i][0][0:-1]
            #ラベルのリストに追加
            labels.append(new_label)

            #ラベルの行を、元の文から削除
            lines.pop(i)
            #削除してずれた分戻す
            i = i - 1

        i = i + 1

    return lines,labels

#指定された文字列(第一引数)がラベルであるかを確かめる
#ラベルだった場合、そのラベルが指し示すアドレスを返す
#ラベルでなかった場合、-1を返す

def is_this_a_label(string:str,labels:list[define.label_info()]):
    for i in labels:
        if(i.name == string):
            return i.address
    return -1

#指定されたラベル

def change_label_to_address(lines,labels):
    address = 0
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if(is_this_a_label(lines[i][j],labels) != -1):
                lines[i][j] = str(is_this_a_label(lines[i][j],labels)-address)
        address += 4

    return lines

def main():
    args = sys.argv
    file_input,file_output,options = commandline_args.getdetail(args)

    #ファイルの内容を取得
    file = get_file(file_input)
    #ファイルの内容のうち、余計なものを削除して分割し2次元配列に
    lines = trim(file)
    #ラベルの内容を設定
    lines,labels = set_label(lines)

    #検出したラベルの内容をもとにプログラム中のラベルをアドレスにすべて変換
    lines = change_label_to_address(lines,labels)

    #先に命令の情報を取得しておく
    instruction.get_defined_instructions()
    #レジスタの情報も取得しておく
    regs.get_defined_regs()

    codes = []

    for i in lines:
        info: define.instruction_info = instruction.set_instruction_info(i)
        #instruction.print_instruction_and_operands_info(info)
        #print(hex(code))
        code = encode.getcode(info)
        codes.append(code)

    export_bin.export_bin(codes,file_output)

#エントリポイント
if __name__ == "__main__":
    main()
