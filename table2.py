def transform_data(results: dict)-> dict:
    data = {}
    for category, games in results.items():
        data[category] = {}
        data[category]['games_cout'] = len(games)
        for _, game_part in games.items():
            for value in game_part:
                if value[2] not in data:
                    data[value[2]] = {}
                if value[3] not in data[value[2]]:
                    data[value[2]][value[3]] = {}
                if category not in data[value[2]][value[3]]:
                    data[value[2]][value[3]][category] = {}
                if value[0] not in data[value[2]][value[3]][category]:
                    data[value[2]][value[3]][category][value[0]] = {}
                if value[1] not in data[value[2]][value[3]][category][value[0]]:
                    data[value[2]][value[3]][category][value[0]][value[1]] = 0

                data[value[2]][value[3]][category][value[0]][value[1]] += 1
                
                if value[0] not in data[category]:
                    data[category][value[0]] = {"_": 0}
                if value[1] not in data[category][value[0]]:
                    data[category][value[0]][value[1]] = {"_": 0}
                if value[2] not in data[category][value[0]][value[1]]:
                    data[category][value[0]][value[1]][value[2]] = 0
                data[category][value[0]][value[1]][value[2]] += 1
                data[category][value[0]][value[1]]["_"] += 1
                data[category][value[0]]["_"] += 1
    return data

def table_inner(data: dict, tech: str) -> list:
    # count all technical move
    result = {}
    for cat, cat_data in data[tech].items():
        if cat not in result:
            result[cat] = []
        for cat_age in ["13-15", "16-17", "18-19"]:
            if cat_age not in cat_data:
                continue
            for res in ["w", "l"]:
                if res not in cat_data[cat_age]:
                    result[cat].extend(['0']*2)
                    continue
                for player_type in ["y", "z"]:
                    if player_type not in cat_data[cat_age][res]:
                        result[cat].append('0')
                        continue
                    result[cat].append(str(cat_data[cat_age][res][player_type]/data[cat_age]['games_cout']).replace('.', ','))
                for player_type in ["y", "z"]:
                    if player_type not in cat_data[cat_age][res]:
                        continue
                    result[cat].append(f'{round(cat_data[cat_age][res][player_type]*100/data[cat_age][res][player_type][tech], 2)}%'.replace('.', ','))
    return result

def table(codes: dict, results: dict, codes_to_show: list, code_tech: str) -> list:
    data = transform_data(results)
    res_inner = table_inner(data, code_tech)
    res=[['Технічні прийоми', *['\"Вік 13-15 років, разів за гру\"']*8, 
         *['\"Вік 16-17 років, разів за гру\"']*8, *['\"Вік 18-19 років, разів за одну гру\"']*8],
         ['Технічні прийоми', *[*['WIN']*4, *['LOS']*4]*3],
         ['Технічні прийоми', *[*['K']*2, *['%']*2]*6],
         ['Технічні прийоми', *['Б', 'З']*12]]


    for i, code in enumerate(codes_to_show):
        if i > len(res)-5: res.append([])
        res[i+4].insert(0, codes[code_tech][code])
        res[i+4].extend(res_inner[code] if code in res_inner else ['0']*24)
    print('\n'.join([str(x) for x in res]))
    return res
