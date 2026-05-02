import subprocess
import json

PATH = f'homebrew/'
replacer = lambda x: x.replace('../..', '../../..')

names = ['piece/bestiary/', 'piece/items/', 'piece/spells/']
names = list(map(lambda item: PATH + item + 'index-list/index.html', names))
sl = {}

for item in names:
    if 'bestiary' in item:
        sl[item] = [" href='/", lambda x: (x[x.index(" href='/") + 8:-29]).rstrip("'")]
    elif 'items' in item:
        sl[item] = [" href='/", lambda x: (x[x.index(" href='/") + 8:-29]).rstrip("'")]
    elif 'spells' in item:
        sl[item] = ['"link": "', lambda x: x[23:-3].replace('\\', '')]

print(*names, sep='\n')

keys = ['homebrew', 'bestiary', 'items', 'spells']
ans = []
breaks = []
remakes = []
for name in names:
    with open(name, encoding="utf-8") as file:
        for string in file.readlines():
            if sl[name][0] in string:

                temp = sl[name][1](string)
                try:
                    lines = []
                    with open(temp + 'index.html', 'r', encoding="utf-8") as file2:
                        lines = file2.readlines()

                    for ind in range(len(lines)):
                        p = lines[ind]
                        lines[ind] = replacer(lines[ind])
                    if len(lines) < 100:
                        breaks.append(temp)
                        break

                    with open(temp + 'index.html', 'w', encoding="utf-8") as file2:
                        for string in lines:
                            file2.write(string)
                    remakes.append(temp)

                except FileNotFoundError:
                    ans.append(string)

print(len(ans))
# subprocess.run([f'wget --exclude-directories=dnd.su/beta, dnd.su/ennin, dnd.su/img, dnd.su/avatar --convert-links --restrict-file-names=windows https://dnd.su/items/1-adamantine-armor/'], shell=True)