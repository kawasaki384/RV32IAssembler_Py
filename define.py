class instruction_info:
    def __init__(self):
        self.opcode = 0
        self.funct3 = 0
        self.funct7 = 0
        self.imm = 0
        self.rd = 0
        self.rs1 = 0
        self.rs2 = 0
        self.shamt = 0
        self.type = 0
        self.offset = 0

class label_info:
    def __init__(self):
        self.name:str = 0
        self.address = 0

class row_info:
    def __init__(self):
        self.is_label :bool = 0
        self.instruction = instruction_info()
        self.label = label_info()
