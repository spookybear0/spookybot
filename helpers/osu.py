

def mod_to_num(mods):
    total = 0
    
    if mods == "":
        return 0

    if "NoFail" in mods:    total += 1<<0
    if "Easy" in mods:    total += 1<<1
    if "Hidden" in mods:    total += 1<<3
    if "HardRock" in mods:    total += 1<<4
    if "SuddenDeath" in mods:    total += 1<<5
    if "DoubleTime" in mods:    total += 1<<6
    if "Relax" in mods:    total += 1<<7
    if "HalfTime" in mods:    total += 1<<8
    if "Nightcore" in mods:    total += 1<<9
    if "Flashlight" in mods:    total += 1<<10
    if "SpunOut" in mods:    total += 1<<12
    if "Perfect" in mods:    total += 1<<14
    
    mods = mods.upper()
    
    if "NF" in mods:    total += 1<<0
    if "EZ" in mods:    total += 1<<1
    if "HD" in mods:    total += 1<<3
    if "HR" in mods:    total += 1<<4
    if "SD" in mods:    total += 1<<5
    if "DT" in mods:    total += 1<<6
    if "RX" in mods:    total += 1<<7
    if "HT" in mods:    total += 1<<8
    if "NC" in mods:    total += 1<<9
    if "FL" in mods:    total += 1<<10
    if "SO" in mods:    total += 1<<12
    if "PF" in mods:    total += 1<<14

    return int(total)

def num_to_mod(num):
    mod_list = []

    if num & 1<<0:   mod_list.append("NF")
    if num & 1<<1:   mod_list.append("EZ")
    if num & 1<<3:   mod_list.append("HD")
    if num & 1<<4:   mod_list.append("HR")
    if num & 1<<5:   mod_list.append("SD")
    if num & 1<<9:   mod_list.append("NC")
    elif num & 1<<6: mod_list.append("DT")
    if num & 1<<7:   mod_list.append("RX")
    if num & 1<<8:   mod_list.append("HT")
    if num & 1<<10:  mod_list.append("FL")
    if num & 1<<12:  mod_list.append("SO")
    if num & 1<<14:  mod_list.append("PF")
    if num & 1<<15:  mod_list.append("4 KEY")
    if num & 1<<16:  mod_list.append("5 KEY")
    if num & 1<<17:  mod_list.append("6 KEY")
    if num & 1<<18:  mod_list.append("7 KEY")
    if num & 1<<19:  mod_list.append("8 KEY")
    if num & 1<<20:  mod_list.append("FI")
    if num & 1<<24:  mod_list.append("9 KEY")
    if num & 1<<25:  mod_list.append("10 KEY")
    if num & 1<<26:  mod_list.append("1 KEY")
    if num & 1<<27:  mod_list.append("3 KEY")
    if num & 1<<28:  mod_list.append("2 KEY")

    return "".join(mod_list)