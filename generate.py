import os
import bcrypt
import git
import datetime as dt
import uuid
import random


def createHeader():
    chars = list(x for x in range(ord('A'), ord('Z') + 1))

    header = '|X|'

    for c in chars:
        header += chr(c) + '|'

    header += os.linesep
    header += '|'

    for i in range(0, len(chars) + 1):
        header += ':-------:|'

    return header


def createContent():
    width, height = 26, 26

    #  0 ...  9  A ...  Z
    # 48 ... 57 65 ... 90

    result = [[random.randint(48, 83) for x in range(width)] for y in range(height)]
    result = list([y + 7 if y > 57 else y for y in x] for x in result)

    return result


def add_to_content(content, numbers):
    line = os.linesep
    for idx, j in enumerate(numbers):
        line += '|{0:0>3}|'.format(idx + 1)
        line += '|'.join([chr(x) for x in j])
        line += '|'

        content += line
        line = os.linesep
    return content


def run():
    header = createHeader()
    numbers = createContent()

    repo = git.Repo(os.getcwd())
    master = repo.head.reference
    commit = master.commit

    previousNumber, newNumber = None, None

    for i in range(0, 1):
        changeLine = random.randint(0, len(numbers))
        changeColumn = random.randint(0, len(numbers[changeLine]))

        content = ''
        content = add_to_content(content, numbers)

        content = header + content

        target_path = os.path.join(os.getcwd(), 'README.md')
        with open(target_path, 'wb') as file:
            file.write(str.encode(content, encoding='utf-8'))

        print('{0} {1}'.format(commit.hexsha, commit.message))

        if previousNumber:
            print('({0};{1}): {2} -> {3}'.format(changeLine, changeColumn, previousNumber, newNumber))

        repo.index.add([target_path])

        if repo.is_dirty(working_tree=True, untracked_files=True):
            print("is_dirty")

        commit = repo.index.commit('commit  {0}@{1}'.format(uuid.uuid4(), dt.datetime.now()), head=True)

        print('{0} {1}'.format(commit.hexsha, commit.message))

        previousNumber = numbers[changeLine][changeColumn]
        newNumber = numbers[changeLine][changeColumn] = random.randint(0, 9)


if __name__ == '__main__':
    run()
