#規定値をとる引数は最後に！
def export_bin(codes: list[int],filename:str = "a.out"):
    file = open(filename,'wb')
    for i in codes:
        file.write(i.to_bytes(4,"little"))

