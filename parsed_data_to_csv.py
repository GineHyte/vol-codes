import json
import codecs

RESULTS = json.load(codecs.open("results.json", "r+", encoding="utf-16")) # open the file
CODES = json.load(open("codes.json", "r+", encoding="utf-8")) # open the file

def transform_data1()-> dict:
    data = {}
    for category, games in RESULTS.items():
        data[category] = {}
        for game_name, game in games.items():
            for value in game:
                if value[2] not in data:
                    data[value[2]] = {}
                if category not in data[value[2]]:
                    data[value[2]][category] = {}
                if value[0] not in data[value[2]][category]:
                    data[value[2]][category][value[0]] = 0

                data[value[2]][category][value[0]] += 1
                
                if value[0] not in data[category]:
                    data[category][value[0]]= 0
                # if value[2] not in data[category][value[0]]:
                #     data[category][value[0]][value[2]] = 0
                # data[category][value[0]][value[2]] += 1
                data[category][value[0]] += 1
    return data



def table1_inner(data: dict) -> list:
    # count all technical move
    result = {}
    for category_or_tech, cat_data in data.items():
        if len(category_or_tech) != 1: continue
        for loc_cat, loc_cat_data in cat_data.items():
            for res, count in loc_cat_data.items():
                if category_or_tech not in result:
                    result[category_or_tech] = []
                result[category_or_tech].append(str(count))
                result[category_or_tech].append(f'{round(count*100/data[loc_cat][res])}%')

    return [x for x in result.values()]

def table1() -> list:
    data1 = transform_data1()
    res = table1_inner(data1)
    res.insert(0, ['Технічні прийоми', *['K', '%']*3])
    res.insert(0, ['Технічні прийоми', *[*['WIN']*2, *['LOS']*2]*3])
    res.insert(0, ['Технічні прийоми', *['\"Вік 13-15 років, разів за гру\"']*2, 
                   *['\"Вік 16-17 років, разів за гру\"']*2, *['\"Вік 18-19 років, разів за одну гру\"']*2])
    for i, code in enumerate(['a', 'b', 'c', 'd', 'e', 'h']):
        if i > len(res)-4: res.append([])
        res[i+3].insert(0, CODES[code]['_'])

    return res

def tdlist_to_csv(data:list) -> str:
    return '\n'.join([','.join(x) for x in data])

if __name__ == "__main__":
    with open('table1.csv', 'w', encoding="utf-16") as f:
        f.write(tdlist_to_csv(table1()))
    # for line in table1():
    #     print("|", end="")
    #     for value in line:
    #         print(value, end="|")
    #     print()
    #     print("-"*(len(''.join(line))+len(line)+1))
