
def filename_graph(Multi_conf, db_names, size):
    name = str(db_names[0])
    if Multi_conf:
        name += "_" + str(size)
    else :
        name += "_conf" + str(db_names[2]) + "_" + str(size)
    return name

def filename_heatmap(Multi_size, Multi_conf, db_names, tab_size):
    name = str(db_names[0])
    if not Multi_conf:
        name += "_conf" + str(db_names[2])
    name += "_" + str(tab_size[0])
    if Multi_size :
        name += "-" + str(tab_size[1])
    return name