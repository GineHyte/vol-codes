def transform_data(results: dict, codes: dict)-> dict:
    data = {}
    for category, games in results.items():
        data[category] = {}
        data[category]['games_cout'] = len(games)
        for _, game_part in games.items():
            for value in game_part:
                game_res, amplua, tech1, tech2, act, zone = list(value)

                if tech1 not in data[category]: data[category][tech1] = {}
                if tech2 not in data[category][tech1]: data[category][tech1][tech2] = {f'{x}_zone': {"y": 0, "z": 0} for x in codes[tech1]['zones'].keys()}
                if act not in data[category][tech1][tech2]: data[category][tech1][tech2][act] = {x: {"y": 0, "z": 0} for x in codes[tech1]['zones'].keys()}

                data[category][tech1][tech2][act][zone][amplua] += 1
                data[category][tech1][tech2][f'{zone}_zone'][amplua] += 1
    return data

def table_inner(data: dict, cat:str, tech1: str) -> list:
    # count all technical move
    result = {}
    for tech2, tech2_data in data[cat][tech1].items():
        for zone_act, zone_act_data in tech2_data.items():
            if "zone" in zone_act:
                for amplua in ['y', 'z']:
                    if tech2 not in result: result[tech2] = {}
                    if '_' not in result[tech2]: result[tech2]['_'] = []
                    result[tech2]["_"].append(zone_act_data[amplua] if amplua in zone_act_data else 0)
            else:
                for zone, zone_data in zone_act_data.items():
                    for amplua in ['y', 'z']:
                        if tech2 not in result: result[tech2] = {}
                        if zone_act not in result[tech2]: result[tech2][zone_act] = []
                        result[tech2][zone_act].append(zone_data[amplua] if amplua in zone_data else 0)

    return result

def table(codes: dict, results: dict, codes_to_show: list, code_tech: str) -> list:
    data = transform_data(results)
    print(str(data).replace('\'', '"'))
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
    return res
