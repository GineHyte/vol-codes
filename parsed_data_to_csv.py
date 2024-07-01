import json
import codecs

import table1
import table2
import table3

RESULTS = json.load(codecs.open("results.json", "r+", encoding="utf-8")) # open the file
CODES = json.load(open("codes.json", "r+", encoding="utf-8")) # open the file

def tdlist_to_csv(data:list) -> str:
    """Converts a list of lists to a CSV string."""
    return '\n'.join([','.join(x) for x in data])

if __name__ == "__main__":
    # Write the tables to CSV files
    with open("./out/table1.csv", "w+", encoding="UTF-8") as f:
        f.write(tdlist_to_csv(table1.table(CODES, RESULTS)))

    with open("./out/table2.csv", "w+", encoding="UTF-8") as f:
        f.write(tdlist_to_csv(table2.table(CODES, RESULTS, "a", ["a", "b", "c", "d", "e", "h"])))

    with open("./out/table3.csv", "w+", encoding="UTF-8") as f:
        f.write(tdlist_to_csv(table3.table(CODES, RESULTS, "16-17", "a", ["a", "b", "c", "d", "e", "h"])))