import os
import threading

lock = threading.Lock()


class File:
    def __init__(self, file_name):
        self.file_name = file_name
        self.content = load(file_name)

    def add(self, line):
        if line not in self.content:
            self.content.append(line)
            add(f'{line}\n', self.file_name)


def add(text: str, to: str) -> None:
    lock.acquire()
    open(to, 'a').write(text)
    lock.release()


def load(*file_names: str):
    lists = []
    for file_name in file_names:
        try:
            lists.append(open(file_name, 'r').read().strip().split('\n'))
        except FileNotFoundError:
            open(file_name, 'w').write('')
            lists.append([])
    return lists if len(lists) > 1 else lists[0]


def delete(text: str, from_file: str):
    with open(from_file, "r") as file_input:
        with open("temp.txt", "w") as output:
            for line in file_input.readlines():
                if line != text:
                    output.write(line)
    os.replace('temp.txt', from_file)
