import os
import re
import sys


def process(path, word):
    count = 0 
    children = 0

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("\\input{") and line.endswith("}"):
                pid = os.fork()
                if pid == 0:
                    f.close()
                    result = process(line[7:-1], word)
                    os._exit(result)
                children += 1
            else:
                count += sum(1 for w in re.findall(r"\w+", line) if w == word)

    for _ in range(children):
        _, status = os.wait()
        count += os.WEXITSTATUS(status)

    return count

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(f"Użycie: {sys.argv[0]} plik słowo")
    print(process(sys.argv[1], sys.argv[2]))
    