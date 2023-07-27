import errno, os, csv

def mkdir_p(path):
    """
    This is functionally equivalent to the mkdir -p [fname] bash command
    """
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def extract_params_cmd_log(path, exec_name):
    """
    Extract commandline parameters from run command.
    Works for Empirical config manager (Config.hpp)

    e.g. a cmd log containing,
        ./diagnostics-suite -DIAGNOSTIC struct-exploitation -POP_SIZE 500 -SEED 1055 -SELECTION lexicase -MAX_GENS 50000
    """
    content = None
    with open(path, "r") as fp:
        content = fp.read().strip()
    content = content.replace(f"./{exec_name}", "").strip()
    cmd_args = content.split(" ")
    cfg = {}
    for i in range(0, len(cmd_args), 2):
        assert i+1 < len(cmd_args)
        key = cmd_args[i].strip("-")
        cfg[key] = cmd_args[i+1]
    return cfg

def read_csv(file_path):
    """
    Read content of csv file into a list where each entry in the list is a dictionary
    with header:value entries.
    """
    content = None
    with open(file_path, "r") as fp:
        content = fp.read().strip().split("\n")
    header = content[0].split(",")
    content = content[1:]
    lines = [
        {header[i]: l[i] for i in range(len(header))}
        for l in csv.reader(
            content,
            quotechar='"',
            delimiter=',',
            quoting=csv.QUOTE_ALL,
            skipinitialspace=True
        )
    ]
    return lines