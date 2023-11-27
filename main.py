import io, tokenize, os, platform

is_windows = True if platform.system() == "Windows" else False

def clear():
    if is_windows:
        os.system("cls")
    else:
        os.system("clear")

def remove_docs(source):
    io_obj = io.StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        if token_type == tokenize.COMMENT:
            pass
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
                if prev_toktype != tokenize.NEWLINE:
                    if start_col > 0:
                        out += token_string
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    out = '\n'.join(l for l in out.splitlines() if l.strip())
    return out

if __name__ == '__main__':
    clear()
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, help="The folder to obfuscate")
    args = parser.parse_args()


    # walk through folder
    all_files = []
    for root, dirs, files in os.walk(args.folder):
        for file in files:
            if file.endswith(".py"):
                all_files.append(os.path.join(root, file))
    # remove docs
    for file in all_files:
        print(file)
        with open(file, "r") as f:
            code = f.read()
            code = remove_docs(code)
        with open(file, "w") as f:
            f.write(code)
