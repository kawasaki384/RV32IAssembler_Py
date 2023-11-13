reg_list = {}

def get_defined_regs(filename = "regs"):
    global reg_list

    file = open(filename,'r').readlines()

    #辞書で元の値を数値として登録
    for i in file:
        reg_list[i.split()[0]] = i.split()[1]

#レジスタを数字を意味するstringへと変換
#-1以外:レジスタに対応する数値
#-1:レジスタに対応する数値が見つからなかった
def change_regs_to_str(reg: str):
    #もし文字列がレジスタのリストに含まれていたら
    if(reg in reg_list):
        return reg_list[reg]
    else:
        return -1
