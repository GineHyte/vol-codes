import json
import sys
from docx import Document


class Table1:
    def transform_data(self, results: dict) -> dict:
        data = {}
        for category, games in results.items():
            data[category] = {}
            for _, game in games.items():
                for value in game:
                    try:
                        if value[2] not in data:
                            data[value[2]] = {}
                        if category not in data[value[2]]:
                            data[value[2]][category] = {}
                        if value[0] not in data[value[2]][category]:
                            data[value[2]][category][value[0]] = 0

                        data[value[2]][category][value[0]] += 1

                        if value[0] not in data[category]:
                            data[category][value[0]] = 0
                        data[category][value[0]] += 1
                        data[category]["games_count"] = len(games)
                    except Exception as e:
                        print("Error by {} value".format(value))
        # print("transformed data: ", json.dumps(data, sort_keys=True, indent=4))
        return data

    def table_inner(self, data: dict) -> list:
        """generates"""
        result = {}
        for category_or_tech, cat_data in data.items():
            if len(category_or_tech) != 1:
                continue
            for loc_cat in ["13-15", "16-17", "18-19"]:
                loc_cat_data = cat_data[loc_cat]
                try:
                    if category_or_tech not in result:
                        result[category_or_tech] = []
                    result[category_or_tech].append(
                        str(
                            round(
                                loc_cat_data["w"] / data[loc_cat]["games_count"] / 2, 2
                            )
                        ).replace(".", ",")
                    )
                    result[category_or_tech].append(
                        f'{round(loc_cat_data["w"]*100/data[loc_cat]["w"], 2)}%'.replace(
                            ".", ","
                        )
                    )
                    result[category_or_tech].append(
                        str(
                            round(
                                loc_cat_data["l"] / data[loc_cat]["games_count"] / 2, 2
                            )
                        ).replace(".", ",")
                    )
                    result[category_or_tech].append(
                        f'{round(loc_cat_data["l"]*100/data[loc_cat]["l"], 2)}%'.replace(
                            ".", ","
                        )
                    )
                except Exception as e:
                    print("Error by {} value".format(loc_cat_data))
        return [result[x] for x in ["a", "b", "c", "d", "e", "h"] if x in result]

    def table(self, codes: dict, results: dict) -> list:
        _data = self.transform_data(results)
        res = self.table_inner(_data)
        res.insert(0, ["Технічні прийоми", *["K", "%"] * 6])
        res.insert(0, ["Технічні прийоми", *[*["WIN"] * 2, *["LOS"] * 2] * 3])
        res.insert(
            0,
            [
                "Технічні прийоми",
                *["Вік 13-15 років, разів за гру"] * 4,
                *["Вік 16-17 років, разів за гру"] * 4,
                *["Вік 18-19 років, разів за одну гру"] * 4,
            ],
        )
        # print("table out: ", json.dumps(res, sort_keys=True, indent=4))
        for i, code in enumerate(["a", "b", "c", "d", "e", "h"]):
            if i > len(res) - 4:
                res.append([])
            res[i + 3].insert(0, codes[code]["_"])

        return res


class Table2:
    def transform_data(self, results: dict) -> dict:
        data = {}
        for category, games in results.items():
            data[category] = {}
            data[category]["games_count"] = len(games)
            for _, game_part in games.items():
                for value in game_part:
                    try:
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
                    except Exception as e:
                        print(value)
        # print("tr4ansformed data: ", json.dumps(data, sort_keys=True, indent=4))
        return data

    def table_inner(self, data: dict, tech: str) -> list:
        # count all technical move
        result = {}
        for cat, cat_data in data[tech].items():
            if cat not in result:
                result[cat] = []
            for cat_age in ["13-15", "16-17", "18-19"]:
                if cat_age not in cat_data:
                    result[cat].extend([*[*["0"] * 2, *["0%"] * 2] * 2])
                    continue
                for res in ["w", "l"]:
                    try:
                        if res not in cat_data[cat_age]:
                            result[cat].extend([*["0"] * 2, *["0%"] * 2])
                            continue
                        for player_type in ["y", "z"]:
                            if player_type not in cat_data[cat_age][res]:
                                result[cat].append("0")
                                continue
                            # print(
                            #     f"{tech}|{cat}|{cat_age}|{res}|{player_type}|K: {cat_data[cat_age][res][player_type]} / {data[cat_age]['games_count']} = {str(cat_data[cat_age][res][player_type]/data[cat_age]['games_count']).replace('.', ',')}"
                            # )
                            result[cat].append(
                                f"{str(cat_data[cat_age][res][player_type]/data[cat_age]['games_count']).replace('.', ',')}"
                            )
                        for player_type in ["y", "z"]:
                            if player_type not in cat_data[cat_age][res]:
                                result[cat].append("0%")
                                continue
                            # print(
                            #     f"{tech}|{cat}|{cat_age}|{res}|{player_type}|%: {cat_data[cat_age][res][player_type]} * 100 / {data[cat_age][res][player_type][tech]} = {str(round(cat_data[cat_age][res][player_type]*100/data[cat_age][res][player_type][tech], 2)).replace('.', '',)}%"
                            # )
                            result[cat].append(
                                f"{round(cat_data[cat_age][res][player_type]*100/data[cat_age][res][player_type][tech], 2)}%".replace(
                                    ".", ","
                                )
                            )
                    except Exception as e:
                        print(cat_data)
        return result

    def table(
        self, codes: dict, results: dict, code_tech: str, codes_to_show: list
    ) -> list:
        data = self.transform_data(results)
        res_inner = self.table_inner(data, code_tech)
        res = [
            [
                "Технічні прийоми",
                *["Вік 13-15 років, разів за гру"] * 8,
                *["Вік 16-17 років, разів за гру"] * 8,
                *["Вік 18-19 років, разів за одну гру"] * 8,
            ],
            ["Технічні прийоми", *[*["WIN"] * 4, *["LOS"] * 4] * 3],
            ["Технічні прийоми", *[*["K"] * 2, *["%"] * 2] * 6],
            ["Технічні прийоми", *["Б", "З"] * 12],
        ]

        # print(codes_to_show)
        # print(code_tech)
        for i, code in enumerate(codes_to_show):
            # print(codes[code_tech][code])
            if i > len(res) - 5:
                res.append([])
            res[i + 4].insert(0, codes[code_tech][code])
            res[i + 4].extend(res_inner[code] if code in res_inner else ["0"] * 24)
        # sys.exit()
        return res


class Table3:
    def transform_data(self, results: dict, codes: dict) -> dict:
        data = {}
        for category, games in results.items():
            data[category] = {}
            data[category]["games_cout"] = len(games)
            for _, game_part in games.items():
                for value in game_part:
                    if len(value) != 6:
                        continue
                    game_res, amplua, tech1, tech2, act, zone = list(value)

                    try:
                        zone = str(int(zone))
                    except ValueError:
                        zone = str(ord(zone) - 96)

                    if tech1 not in data[category]:
                        data[category][tech1] = {}
                    if tech2 not in data[category][tech1]:
                        data[category][tech1][tech2] = {
                            f"{x}_zone": {"w": {"y": 0, "z": 0}, "l": {"y": 0, "z": 0}}
                            for x in codes[tech1]["zones"].keys()
                        }
                    if act not in data[category][tech1][tech2]:
                        data[category][tech1][tech2][act] = {
                            x: {"w": {"y": 0, "z": 0}, "l": {"y": 0, "z": 0}}
                            for x in codes[tech1]["zones"].keys()
                        }

                    data[category][tech1][tech2][act][zone][game_res][amplua] += 1
                    data[category][tech1][tech2][f"{zone}_zone"][game_res][amplua] += 1
        # print("transformed data: ", json.dumps(data, sort_keys=True, indent=4))
        return data

    def table_inner(self, data: dict, cat: str, tech1: str) -> list:
        # count all technical move
        result = {}
        for tech2, tech2_data in data[cat][tech1].items():
            for zone_act, zone_act_data in tech2_data.items():
                if "zone" in zone_act:
                    for game_res in ["w", "l"]:
                        for amplua in ["y", "z"]:
                            if tech2 not in result:
                                result[tech2] = {}
                            if "_" not in result[tech2]:
                                result[tech2]["_"] = []
                            if game_res in zone_act_data:
                                result[tech2]["_"].append(
                                    str(zone_act_data[game_res][amplua])
                                    if amplua in zone_act_data[game_res]
                                    else "0"
                                )
                else:
                    for zone, zone_data in zone_act_data.items():
                        for game_res in ["w", "l"]:
                            for amplua in ["y", "z"]:
                                if tech2 not in result:
                                    result[tech2] = {}
                                if zone_act not in result[tech2]:
                                    result[tech2][zone_act] = []
                                if game_res in zone_data:
                                    result[tech2][zone_act].append(
                                        str(zone_data[game_res][amplua])
                                        if amplua in zone_data[game_res]
                                        else "0"
                                    )

        return result

    def table(
        self,
        codes: dict,
        results: dict,
        cat: str,
        code_tech: str,
        codes_to_show: list = None,
    ) -> list:
        if not codes_to_show:
            codes_to_show = list(codes[code_tech].keys())
            codes_to_show.remove("zones")
            codes_to_show.remove("_")
            codes_to_show.remove("func")

        data = self.transform_data(results, codes)
        res_inner = self.table_inner(data, cat, code_tech)
        header = [
            [
                "Напрям руху м'яча",
                *[
                    x2
                    for x1 in [[x] * 4 for x in codes[code_tech]["zones"].values()]
                    for x2 in x1
                ],
            ],
            [
                "Результат гри",
                *[*["WIN"] * 2, *["LOS"] * 2] * len(codes[code_tech]["zones"]),
            ],
            ["Амплуа гравчині", *[*["Б", "З"] * 2] * len(codes[code_tech]["zones"])],
        ]
        res = []

        for code in codes_to_show:
            if code not in res_inner:
                continue
            res.append(res_inner[code]["_"])
            res[-1].insert(0, codes[code_tech][code])
            for func_n, func in codes[code_tech]["func"].items():
                if func_n == "counter":
                    continue
                if func_n not in res_inner[code]:
                    continue
                res.append(res_inner[code][func_n])
                res[-1].insert(0, func)
        return [*header, *res]
