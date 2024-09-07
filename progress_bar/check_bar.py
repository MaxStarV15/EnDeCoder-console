from typing import List
from random import randint


def check_bar(name: str, values: List[int]) -> bool:
    pattern = "{name}: \t[{res}] {done}/{undone}"
    res = list()
    done = "#" # █
    not_done = "-" # .

    for value in values:
        res.append(done if bool(value) else not_done)

    print(pattern.format(name=name, res=''.join(res), done=sum(values), undone=len(values)))
    return bool