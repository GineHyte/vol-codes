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
    # with open('table1.csv', 'w', encoding="utf-16") as f:
    #     f.write(tdlist_to_csv(table1.table(CODES, RESULTS)))

    print(table2.transform_data(RESULTS))
    # for line in table1():
    #     print("|", end="")
    #     for value in line:
    #         print(value, end="|")
    #     print()
    #     print("-"*(len(''.join(line))+len(line)+1))
