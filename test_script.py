import javalang
import os

def find_log_statements(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        code = f.read()
    try:
        tree = javalang.parse.parse(code)
    except:
        return []

    results = []
    for path, node in tree.filter(javalang.tree.MethodInvocation):
        if node.qualifier == "logger" and node.member in ["error", "info", "warn"]:
            arg_strs = [str(arg) for arg in node.arguments]
            results.append((file_path, node.position.line, node.member, ", ".join(arg_strs)))
    return results

def scan_dir_ast(directory):
    all_logs = []
    for dirpath, _, filenames in os.walk(directory):
        for file in filenames:
            if file.endswith(".java"):
                full_path = os.path.join(dirpath, file)
                logs = find_log_statements(full_path)
                all_logs.extend(logs)
    return all_logs

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    args = parser.parse_args()

    logs = scan_dir_ast(args.directory)
    for file, line, level, message in logs:
        print(f"{file}:{line} [{level.upper()}] {message}")