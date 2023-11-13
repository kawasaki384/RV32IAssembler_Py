import define

def convert_str_to_num(string: str):
    if(len(string) < 2): return int(string)
    if(string[0] == '0' and string[1] == 'x'): return int(string,16)
    if(string[0] == '0' and string[1] == 'b'): return int(string,2)
    
    return int(string,10)

def convert_bin_to_num(string: str):
    return int(string,2)

# オペランド、命令の情報からタイプBの機械語を生成します。
def type_B(info: define.instruction_info()):
    output:int = 0
    output |= (convert_bin_to_num(info.opcode) & 0b1111111)
    output |= ((convert_str_to_num(info.offset) >> 11) & 0b1) << 7
    output |= ((convert_str_to_num(info.offset) >> 1) & 0b1111) << 8
    output |= (convert_bin_to_num(info.funct3) & 0b111) << 12
    output |= (convert_str_to_num(info.rs1) & 0b11111) << 15
    output |= (convert_str_to_num(info.rs2) & 0b11111) << 20
    output |= ((convert_str_to_num(info.offset) >> 5) & 0b111111) << 25
    output |= ((convert_str_to_num(info.offset) >> 12) & 0b1) << 31

    return output


# オペランド、命令の情報からタイプRの機械語を生成します。
def type_R(info: define.instruction_info()):

    output:int = 0
    output |= (convert_bin_to_num(info.opcode) & 0b1111111)
    output |= (convert_str_to_num(info.rd) & 0b11111) << 7
    output |= (convert_bin_to_num(info.funct3) & 0b111) << 12
    output |= (convert_str_to_num(info.rs1) & 0b11111) << 15
    output |= (convert_str_to_num(info.rs2) & 0b11111) << 20
    output |= (convert_bin_to_num(info.funct3) & 0b1111111) << 25

    return output


# オペランド、命令の情報からタイプIの機械語を生成します。
def type_I(info: define.instruction_info()):
    output:int = 0
    #LOAD系命令の時はimmidiateではなくoffsetに値が代入される
    if(info.opcode == "0010011"):
        output |= (convert_bin_to_num(info.opcode) & 0b1111111)
        output |= (convert_str_to_num(info.rd) & 0b11111) << 7
        output |= (convert_bin_to_num(info.funct3) & 0b111) << 12
        output |= (convert_str_to_num(info.rs1) & 0b11111) << 15
        output |= (convert_str_to_num(info.imm) & 0b111111111111) << 20
    else:
        output |= (convert_bin_to_num(info.opcode) & 0b1111111)
        output |= (convert_str_to_num(info.rd) & 0b11111) << 7
        output |= (convert_bin_to_num(info.funct3) & 0b111) << 12
        output |= (convert_str_to_num(info.rs1) & 0b11111) << 15
        output |= (convert_str_to_num(info.offset) & 0b111111111111) << 20

    return output


# オペランド、命令の情報からタイプSの機械語を生成します。
def type_S(info: define.instruction_info()):
    output:int = 0
    output |= (convert_bin_to_num(info.opcode) & 0b1111111)
    output |= (convert_str_to_num(info.offset) & 0b11111) << 7
    output |= (convert_bin_to_num(info.funct3) & 0b111) << 12
    output |= (convert_str_to_num(info.rs1) & 0b11111) << 15
    output |= (convert_str_to_num(info.rs2) & 0b11111) << 20
    output |= ((convert_str_to_num(info.offset) >> 5) & 0b1111111) << 25

    return output


# オペランド、命令の情報からタイプUの機械語を生成します。
def type_U(info: define.instruction_info()):

    output:int = 0
    output |= (convert_bin_to_num(info.opcode) & 0b1111111)
    output |= (convert_str_to_num(info.rd) & 0b11111) << 7
    output |= (convert_str_to_num(info.imm) & 0b11111111111111111111) << 12

    return output


# オペランド、命令の情報からタイプJの機械語を生成します。
def type_J(info: define.instruction_info()):

    output:int = 0
    output |= (convert_bin_to_num(info.opcode) & 0b1111111)
    output |= (convert_str_to_num(info.rd) & 0b11111) << 7
    output |= ((convert_str_to_num(info.offset) >> 12) & 0b11111111) << 12
    output |= ((convert_str_to_num(info.offset) >> 11) & 0b1) << 20
    output |= ((convert_str_to_num(info.offset) >> 1) & 0b1111111111) << 21
    output |= ((convert_str_to_num(info.offset) >> 20) & 0b1) << 31

    return output


# オペランド、命令の情報からタイプI(5bit)の機械語を生成します。
def type_I5(info: define.instruction_info()):

    output:int = 0
    output |= (convert_bin_to_num(info.opcode) & 0b1111111)
    output |= (convert_str_to_num(info.rd) & 0b11111) << 7
    output |= (convert_bin_to_num(info.funct3) & 0b111) << 12
    output |= (convert_str_to_num(info.rs1) & 0b11111) << 15
    output |= (convert_str_to_num(info.shamt) & 0b11111) << 20
    output |= (convert_bin_to_num(info.funct3) & 0b1111111) << 25

    return output


def getcode(info: define.instruction_info):
    code:int = 0
    if(info.type == "B"):
        code = type_B(info)
    elif(info.type == "R"):
        code = type_R(info)
    elif(info.type == "I"):
        code = type_I(info)
    elif(info.type == "S"):
        code = type_S(info)
    elif(info.type == "U"):
        code = type_U(info)
    elif(info.type == "J"):
        code = type_J(info)
    elif(info.type == "I5"):
        code = type_I5(info)

    return code
