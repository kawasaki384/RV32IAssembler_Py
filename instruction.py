import define
import regs

#命令の情報を格納する二次元配列
insts_list = []
#命令、pseudo命令の検出が完了したかのフラグ
was_get_defined_instructions_executed = 0

def get_defined_instructions(filename = "insts"):
    insts = open(filename,'r').readlines()

    list_insts = []

    for i in insts:
        token = i.split()
        list_insts.append(token)

    global insts_list
    insts_list = list_insts

    #実行フラグを1へ
    global was_get_defined_instructions_executed
    was_get_defined_instructions_executed = 1

#displacement with register => disp_with_reg
def get_register(disp_with_reg: str):
    value = disp_with_reg
    value = value.replace('(',' ')
    value = value.replace(')',' ')
    return value.split()[1]

#displacement with register => disp_with_reg
def get_offset(disp_with_reg: str):
    value = disp_with_reg
    value = value.replace('(',' ')
    value = value.replace(')',' ')
    return value.split()[0]

#引数の命令が実際に存在するかどうかを確かめる
#ある場合、その命令のtypeを返し、さらにpseudoinstructionの場合は1を返す
#ない場合、0を返す
def is_there_this_function(name:str):
    for i in insts_list:
        if(i[0] == name):
            return i[3]
        
    return 0

#命令の名前に応じたリストを返す
#なかったら0
def get_list(name:str):
    for i in insts_list:
        if(i[0] == name):
            return i
    return 0

#命令のオペコード、type、ある場合はfunct3,funct7を設定する
def set_instruction_detail(instruction: str):
    return_value = define.instruction_info()
    info = get_list(instruction)

    #Opcodeを設定
    return_value.opcode = info[1]

    #もしfunct3が定義されていたら
    if(info[2] != "-1"):
        return_value.funct3 = info[2]

    #typeを設定
    return_value.type = info[3]

    #もしfunct7が定義されていたら
    if(len(info) == 5):
        return_value.funct7 = info[4]

    return return_value

#lui,auipcだけ
def set_opr_U(inst_info: define.instruction_info(),operands: list[str]):
    inst_info.rd = regs.change_regs_to_str(operands[0])
    inst_info.imm = operands[1]

#jal一個だけ
def set_opr_J(inst_info: define.instruction_info(),operands: list[str]):
    inst_info.rd = regs.change_regs_to_str(operands[0])
    inst_info.offset = operands[1]

#load系、op_imm系、その他のjalrに分けられる
def set_opr_I(inst_info: define.instruction_info(),operands: list[str]):
    #op_imm系の命令
    if(inst_info.opcode == "0010011"):
        inst_info.rd = regs.change_regs_to_str(operands[0])
        inst_info.rs1 = regs.change_regs_to_str(operands[1])
        inst_info.imm = operands[2]
    #load系の命令
    elif(inst_info.opcode == "0000011"):
        inst_info.rd = regs.change_regs_to_str(operands[0])
        #ディスプレースメント付きレジスタ間接指定
        inst_info.offset = get_offset(operands[1])
        inst_info.rs1 = regs.change_regs_to_str(get_register(operands[1]))
    #それ以外はjalr
    else:
        inst_info.rd = regs.change_regs_to_str(operands[0])
        inst_info.rs1 = regs.change_regs_to_str(operands[1])
        inst_info.offset = operands[2]

def set_opr_B(inst_info: define.instruction_info(),operands: list[str]):
    inst_info.rs1 = regs.change_regs_to_str(operands[0])
    inst_info.rs2 = regs.change_regs_to_str(operands[1])
    inst_info.offset = operands[2]

def set_opr_I5(inst_info: define.instruction_info(),operands: list[str]):
    inst_info.rd = regs.change_regs_to_str(operands[0])
    inst_info.rs1 = regs.change_regs_to_str(operands[1])
    inst_info.shamt = operands[2]
    
def set_opr_S(inst_info: define.instruction_info(),operands: list[str]):
    inst_info.rs2 = regs.change_regs_to_str(operands[0])
    #ディスプレースメント付きレジスタ間接指定
    inst_info.offset = get_offset(operands[1])
    inst_info.rs1 = regs.change_regs_to_str(get_register(operands[1]))

def set_opr_B(inst_info: define.instruction_info(),operands: list[str]):
    inst_info.rs1 = regs.change_regs_to_str(operands[0])
    inst_info.rs2 = regs.change_regs_to_str(operands[1])
    inst_info.offset = operands[2]

def set_opr_R(inst_info: define.instruction_info(),operands: list[str]):
    inst_info.rd = regs.change_regs_to_str(operands[0])
    inst_info.rs1 = regs.change_regs_to_str(operands[1])
    inst_info.rs2 = regs.change_regs_to_str(operands[2])

def set_opr_info(inst_info: define.instruction_info(),operands: list[str]):
    if(inst_info.type == "U"):
        set_opr_U(inst_info,operands)
    elif(inst_info.type == "J"):
        set_opr_J(inst_info,operands)
    elif(inst_info.type == "I"):
        set_opr_I(inst_info,operands)
    elif(inst_info.type == "B"):
        set_opr_B(inst_info,operands)
    elif(inst_info.type == "I5"):
        set_opr_I5(inst_info,operands)
    elif(inst_info.type == "S"):
        set_opr_S(inst_info,operands)
    elif(inst_info.type == "R"):
        set_opr_R(inst_info,operands)


def get_inst_and_opr_info(instruction:str,type:str,operands: list[str]):
    #instructionのinfoの設定
    inst_info = set_instruction_detail(instruction)

    #Operandのinfoの設定
    set_opr_info(inst_info,operands)

    return inst_info

def print_instruction_and_operands_info(inst_and_opr: define.instruction_info()):
    print("funct3:" + str(inst_and_opr.funct3))
    print("funct7:" + str(inst_and_opr.funct7))
    print("imm:" + str(inst_and_opr.imm))
    print("opcode:" + str(inst_and_opr.opcode))
    print("rd:" + str(inst_and_opr.rd))
    print("rs1:" + str(inst_and_opr.rs1))
    print("rs2:" + str(inst_and_opr.rs2))
    print("shamt:" + str(inst_and_opr.shamt))
    print("type:" + str(inst_and_opr.type))
    print("offset:" + str(inst_and_opr.offset))
    print("")


def set_instruction_info(row):
    inst_and_opr = define.instruction_info() 
    
    #get_defined_instructionsを実行していないとこの関数は実行できない
    if(was_get_defined_instructions_executed == 0):
        print("Error")

    #ある列のうち、0番目を命令
    instruction = row[0]
    #それ以降をOperandとする
    operands = row[1:]

    type = is_there_this_function(instruction)

    if(type == 0):
        print(f"命令が存在しません:{instruction}")
    else:
        inst_and_opr = get_inst_and_opr_info(instruction,type,operands)

    return inst_and_opr
