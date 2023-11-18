def getdetail(args:list[str]):
    input_file = "untitled.rvi"
    output_file = "a.out"
    options = "options"

    if(len(args) >= 2):
        input_file = args[1]
    if(len(args) >= 3):
        output_file = args[2]
    if(len(args) >= 4):
        options = args[3:]

    return input_file,output_file,options
