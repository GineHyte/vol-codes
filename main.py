import json
import tkinter as tk

from typing import Tuple

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.geometry("800x400")

        self.validate_command = self.register(self.validate_command_func)
        
        self.init_ui()
        self.load_data()

    def load_data(self):
        self.data = open("./codes.json", "r", encoding="utf-8")
        self.data = json.load(self.data)

    def validate_command_func(self, inp: str) -> bool:
        if inp == "\n":
            self.result_label.config(text='aaaaaaaaaaaaaa')
            return False
        result = self.get_command(inp)
        self.result_label.config(text=result[0])
        if result[2]:
            self.hint_label.config(text=result[2])
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
                        return "Not found!" if not res else " ".join(res), False, ""

            return " ".join(res), True, "\n".join(hint)
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
        inp = e.widget.get()
        category = self.category.get()
        game = self.game.get()
        player = self.player.get()
        with open("./results.json", "r+", encoding="utf-16") as f:
            if f.read() == "":
                results = {}
            else:
                f.seek(0)
                results = json.load(f)
            if category not in results:
                results[category] = {}
            if game not in results[category]:
                results[category][game] = {}
            if player not in results[category][game]:
                results[category][game][player] = []
            results[category][game][player].append(inp)
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

        tk.Label(self, text="Player:").grid(row=2, column=0, pady=10)
        self.player = tk.Entry(self)
        self.player.grid(row=2, column=1, pady=10)

        self.entry = tk.Entry(self, 
                              validatecommand=(self.validate_command, "%P"), validate="key")
        self.entry.bind('<Return>', self.submit_code)
        self.entry.grid(row=0, column=2, columnspan=2, pady=10, padx=10)
        
        self.result_label = tk.Label(self, text="Start typing...")
        self.result_label.grid(row=1, column=2, columnspan=2, pady=10, padx=10)

        self.hint_label = tk.Label(self, text="Start typing...")
        self.hint_label.grid(row=2, column=2, columnspan=2, pady=10, padx=10)
        

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()