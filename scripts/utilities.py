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

def parse_list(list_str: str, sep: str = " ", begin: str = "[", end: str = "]"):
    return list_str.strip(begin + end).strip().split(sep)

def get_file_num(fpath):
    '''
    Get file number, assuming format of {FILENAME}_{NUMBER}.{EXTENSION}
    '''
    fname = os.path.basename(fpath)    # Get rid of preceeding path
    fname = os.path.splitext(fname)[0] # Get rid of file extension
    num = fname.split("_")[-1]
    return int(num) if num.isnumeric() else -1

def identify_file(directory, file_str, get_trait_fun = get_file_num, select_fun = max):
    """
    directory: directory to search
    file_str: string that identifies which files should be included in search
    get_trait_fun: funtion that extracts trait from file names to select on
    select_fun: function that selects file based on trait
    """
    options = [(get_trait_fun(fname), fname) for fname in os.listdir(directory) if file_str in fname]
    return select_fun(options)[1]