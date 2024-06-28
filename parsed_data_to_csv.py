import json
import codecs

import table1
import table2
import table3

RESULTS = json.load(codecs.open("results.json", "r+", encoding="utf-16")) # open the file
CODES = json.load(open("codes.json", "r+", encoding="utf-8")) # open the file



def tdlist_to_csv(data:list) -> str:
    return '\n'.join([','.join(x) for x in data])

if __name__ == "__main__":
    data = table3.transform_data(RESULTS, CODES)
    res = table3.table(CODES, RESULTS, "16-17", 'a')
    print(res)
    with open('table3.csv', 'w', encoding="utf-16") as f:
        f.write(tdlist_to_csv(res))
