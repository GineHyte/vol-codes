import json
import tkinter as tk

from typing import Tuple

PLAYERS = ["перемога захисник", "перемога блокуючий", "поразка захисник", "поразка блокуючий"]
PLAYERS_SYM = ["wz", "wy", "lz", "ly"]

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.geometry("1200x800")

        self.validate_command = self.register(self.validate_command_func)
        
        self.init_ui()
        self.load_data()

    def load_data(self):
        self.data = open("./codes.json", "r", encoding="utf-8")
        self.data = json.load(self.data)

    def validate_command_func(self, inp: str, widget_name: str) -> bool:
        i = int(widget_name.split("_")[1])
        result_label = self.nametowidget(f'result_label_{i}')
        hint_label = self.nametowidget(f'hint_label_{i}')

        result = self.get_command(f'{PLAYERS_SYM[i]}{inp}')
        result_label.config(text=result[0])
        if result[2]:
            hint_label.config(text=result[2])
        return result[1]

    def get_command(self, inp: str) -> Tuple[str, bool, str]:
        NOT_FOUND = "Not found!", False, ""
        if inp:
            inp = list(inp.lower().strip())
            res = []
            code = "a"
            for i in range(1, len(inp)+1):
                inp_s = inp.pop(0)
                hint = []
                match i:
                    case 1:
                        if inp_s in ["w", "l"]:
                            res.append(self.data[inp_s])
                            for k, it in self.data.items():
                                if k in ['w', 'l', 'a', 'b', 'c', 'd', 'e', 'h']: continue
                                hint.append(f"{k} - {it}")
                        else: return NOT_FOUND
                    case 2:
                        if inp_s in ["y", "z"]:
                            res.append(self.data[inp_s])
                            for k, it in self.data.items():
                                if k in ['w', 'l', 'y', 'z']: continue
                                hint.append(f"{k} - {it['_']}")
                        else: return NOT_FOUND
                    case 3:
                        code = inp_s
                        if code in self.data and "_" in self.data[code]:
                            res.append(self.data[code]["_"])
                            for k, it in self.data[code].items():
                                if k in ['_', 'func', 'zones']: continue
                                hint.append(f"{k} - {it}")
                        else: return NOT_FOUND
                    case 4:
                        if inp_s in self.data[code]:
                            res.append(self.data[code][inp_s])
                            if "func" in self.data[code].keys():
                                for k, it in self.data[code]["func"].items():
                                    hint.append(f"{k} - {it}")
                        else: return NOT_FOUND
                    case 5:
                        if "func" in self.data[code].keys():
                            if inp_s in self.data[code]['func'].keys():
                                res.append(self.data[code]['func'][inp_s])
                                if "zones" in self.data[code].keys():
                                    for k, it in self.data[code]["zones"].items():
                                        hint.append(f"{k} - {it}")
                            else: return NOT_FOUND
                        else: return NOT_FOUND
                    case 6:
                        if "zones" in self.data[code].keys():
                            if inp_s in self.data[code]["zones"]:
                                res.append(self.data[code]["zones"][inp_s])
                            else: return NOT_FOUND
                        else: return NOT_FOUND
                    case _:
                        return "Not found!" if not res else "\n".join(res), False, ""

            return "\n".join(res), True, "\n".join(hint)
        return "Start typing...", True, ""

    def submit_code1(self, e: tk.Event):
        inp = self.result_label.cget("text")
        with open("./results.json", "r+", encoding="utf-16") as f:
            results = json.load(f)
            if inp in results:
                print(f'Code already exists: {inp} - {results[inp]+1}')
                results[inp] += 1
            else:
                print(f'New code: {inp}')
                results[inp] = 1
            f.seek(0)
            json.dump(results, f, indent=4, ensure_ascii=False)
            f.truncate()

        e.widget.delete(0, tk.END)      

    def submit_code(self, e: tk.Event):
        i = int(e.widget._name.split("_")[1])
        inp = e.widget.get()
        category = self.category.get()
        game = self.game.get()
        with open("./results.json", "r+", encoding="utf-16") as f:
            if f.read() == "":
                results = {}
            else:
                f.seek(0)
                results = json.load(f)
            if category not in results:
                results[category] = {}
            if game not in results[category]:
                results[category][game] = []
            results[category][game].append(f'{PLAYERS_SYM[i]}{inp}')
            f.seek(0)
            json.dump(results, f, indent=4, ensure_ascii=False)
            f.truncate()

        e.widget.delete(0, tk.END)       

    def init_ui(self):
        tk.Label(self, text="Category:").grid(row=0, column=0, pady=10)
        self.category = tk.Entry(self)
        self.category.grid(row=0, column=1, pady=10)

        tk.Label(self, text="Game:").grid(row=1, column=0, pady=10)
        self.game = tk.Entry(self)
        self.game.grid(row=1, column=1, pady=10)


        for i, player in enumerate(PLAYERS):
            tk.Label(self, text=player).grid(row=3, column=0+i, pady=10, padx=10)
        
            entry = tk.Entry(self, name=f"entry_{i}",
                                validatecommand=(self.validate_command, "%P", "%W"), validate="key")
            entry.bind('<Return>', self.submit_code)
            entry.grid(row=4, column=0+i, pady=10, padx=10)
            
            tk.Label(self, name=f'result_label_{i}',
                     text="Start typing...").grid(row=5,
                     column=0+i, pady=10, padx=10)

            tk.Label(self, name=f'hint_label_{i}', text="Start typing...",
                     width=40, height=10).grid(row=6, 
                     column=0+i, pady=10, padx=10)

        
if __name__ == "__main__":
    app = MyApp()
    app.mainloop()