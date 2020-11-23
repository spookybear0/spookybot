
def parse_args(params: str) -> list:
    params = params.split(" ")
    newparams = []
    i = 0
    for p in params:
        global is_three
        global is_two
        if p.startswith('"'):
            if params[i+1].endswith('"'):
                p = params[i] + " " + params[i+1]
                p = p.replace('"', "")
                is_two = True
                is_three = False
            elif params[i+2].endswith('"'):
                p = params[i] + " " + params[i+1] + " " + params[i+2]
                p = p.replace('"', "")
                is_three = True
                is_two = False
        else:
            is_two = False
            is_three = False
        newparams.insert(i, p)
        i += 1
    if is_three:
        newparams.pop(-1)
        newparams.pop(-1)
    elif is_two:
        newparams.pop(-1)
    return newparams