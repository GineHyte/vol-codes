def transform_data(results: dict)-> dict:
    data = {}
    for category, games in results.items():
        data[category] = {}
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
                    data[category][value[0]] = 0
                if value[1] not in data[category][value[0]]:
                    data[category][value[0]][value[1]] = 0
                data[category][value[0]][value[1]] += 1
                data[category][value[0]] += 1
    return data

def table_inner(data: dict, res_tech: str) -> list:
    # count all technical move
    result = {}
    for category_or_tech, cat_data in data.items():
        if len(category_or_tech) != 1: continue
        for cat_1, cat_1_data in cat_data.items():
            for cat_2, cat_2_data in cat_1_data.items():
                for cat_age, cat_age_data in cat_2_data.items():
                    for res, res_data in cat_age_data.items():
                        if res_tech not in result:
                            result[res_tech] = []
                        result[res_tech].append(str(res_data['y']/data[cat_age]))
                        result[res_tech].append(str(res_data['z']))

    return [x for x in result.values()]

def table(codes: dict, results: dict) -> list:
    data = transform_data(results)
    res = table_inner(data)
    res.insert(0, ['Технічні прийоми', *['K', '%']*3])
    res.insert(0, ['Технічні прийоми', *[*['WIN']*2, *['LOS']*2]*3])
    res.insert(0, ['Технічні прийоми', *['\"Вік 13-15 років, разів за гру\"']*2, 
                   *['\"Вік 16-17 років, разів за гру\"']*2, *['\"Вік 18-19 років, разів за одну гру\"']*2])
    for i, code in enumerate(['a', 'b', 'c', 'd', 'e', 'h']):
        if i > len(res)-4: res.append([])
        res[i+3].insert(0, codes[code]['_'])

    return res
