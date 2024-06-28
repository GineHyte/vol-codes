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

def table_inner(data: dict, cat: str, tech1: str) -> list:
    # count all technical move
    result = {}
    for tech2, tech2_data in data[cat][tech1].items():
        for zone_act, zone_act_data in tech2_data.items():
            if "zone" in zone_act:
                for amplua in ['y', 'z']:
                    if tech2 not in result: result[tech2] = {}
                    if '_' not in result[tech2]: result[tech2]['_'] = []
                    result[tech2]["_"].append(str(zone_act_data[amplua]) if amplua in zone_act_data else "0")
            else:
                for zone, zone_data in zone_act_data.items():
                    for amplua in ['y', 'z']:
                        if tech2 not in result: result[tech2] = {}
                        if zone_act not in result[tech2]: result[tech2][zone_act] = []
                        result[tech2][zone_act].append(str(zone_data[amplua]) if amplua in zone_data else "0")

    return result

def table(codes: dict, results: dict, cat: str, code_tech: str, codes_to_show: list=None) -> list:
    if not codes_to_show: 
        codes_to_show = list(codes[code_tech].keys())
        codes_to_show.remove('zones')
        codes_to_show.remove('_')
        codes_to_show.remove('func')
    
    data = transform_data(results, codes)
    res_inner = table_inner(data, cat, code_tech)
    header = [['Напрям руху м\'яча', *[x2 for x1 in [[x]*2 for x in codes[code_tech]['zones'].values()] for x2 in x1]],
         ['Амплуа гравчині', *['Б', 'З']*len(codes[code_tech]['zones'])]]
    res = []

    for code in codes_to_show:
        if code not in res_inner: continue
        res.append(res_inner[code]['_'])
        res[-1].insert(0, codes[code_tech][code])
        for func_n, func in codes[code_tech]['func'].items():
            if func_n == 'counter': continue
            if func_n not in res_inner[code]: continue
            res.append(res_inner[code][func_n])
            res[-1].insert(0, func)
    return [*header, *res]
