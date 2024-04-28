#MikiLang translator to python

def normalizeText(text) -> str:
    return text.replace(":", "").replace("\n", "").replace("TRUE", "True").replace("FALSE", "False")

def compileLine(lineRaw, linecount):
    line = lineRaw.split(" ")
    if lineRaw == "\n":
        return 0
    while line[0:4] == ['', '', '', '']:
        translated.write(f'    ')
        del line[0:4]
    if line[0:3].count('')>0:
        print(f'count: {line[0:3].count('')}')
        raise Exception(f'MikiLang Translator: {linecount}: Wrong tab number!')
    
    match normalizeText(line[0]):
        case "INT":
            if type(int(line[3][:-1])) != int:
                raise Exception(f'MikiLang Translator: {linecount}: INT value incorrect')
            translated.write(f'{line[1]} = {line[3][:-1]}')
        case "STRING":
            if type(line[3][:-1]) != str:
                raise Exception(f'MikiLang Translator: {linecount}: INT value incorrect')
            translated.write(f'{line[1]} = "{lineRaw[lineRaw.index('"')+1 : lineRaw.index('"', lineRaw.index('"')+1)]}"')
        case "BOOL":
            if line[3][:-1] == "TRUE":
                translated.write(f'{line[1]} = True')
            elif line[3][-2] == "FALSE":
                translated.write(f'{line[1]} = False')
            else:
                raise Exception(f'MikiLang Translator: {linecount}: BOOL value incorrect')
        case "WHILE":
            if line[-1] != "DO:\n":
                raise Exception(f'MikiLang Translator: {linecount}: WHILE statement not complete')

            text = f''
            for ele in line[1:-1]:
                text+=f' {normalizeText(ele)}'
            translated.write(f'while{text}:')
        case "IF" | "ELIF":
            text = f''
            for ele in line[1:]:
                text+=f' {normalizeText(ele)}'
            if line[0] == "IF":
                translated.write(f'if{text}:')
            else:
                translated.write(f'elif{text}:')
        case "ELSE":
            translated.write(f'else:')
        case "PRINT":
            translated.write(f'print({line[1]})')
        case _:
            translated.write(normalizeText(" ".join(line)))
file = open("mikilangCode.mlang", "r")
translated = open("mikilangCodeTranslated.py", "w")
linecount = 0
for line in file:
    compileLine(line, linecount)
    translated.write('\n')
    linecount+=1

file.close()
translated.close()