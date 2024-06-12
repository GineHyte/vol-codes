import json
import tkinter as tk

from typing import Tuple

PLAYERS = ["перемога захисник", "перемога блокуючий", "поразка захисник", "поразка блокуючий"]
PLAYERS_SYM = ["wz", "wy", "lz", "ly"]
HISTORY_LEN = 5

class VolCodes(tk.Tk):
    """
    A custom Tkinter application for Voleyball Codes.

    Attributes:
        validate_command (function): The validation function for the entry widget.
        data (file): The file object for the codes.json file.

    Methods:
        __init__(): Initializes the VolCodes class.
        load_data(): Loads data from the codes.json file.
        validate_command_func(inp: str, widget_name: str) -> bool: Validates the command entered in the entry widget.
        get_command(inp: str) -> Tuple[str, bool, str]: Retrieves the command based on the input.
        delete_last(e): Deletes the last command entered in the history.
        submit_code(e: tk.Event): Submits the code entered in the entry widget.
        init_ui(): Initializes the user interface of the application.
    """
    def __init__(self):
        super().__init__()
        self.title("Voleyball Codes")
        self.geometry("1200x800")

        self.validate_command = self.register(self.validate_command_func)
        
        self.init_ui()

    def validate_command_func(self, inp: str, widget_name: str) -> bool:
        """
        Validates a command and updates the result and hint labels.

        Args:
            inp (str): The command input.
            widget_name (str): The name of the widget.

        Returns:
            bool: True if the command is valid, False otherwise.
        """
        i = int(widget_name.split("_")[1])
        result_label = self.nametowidget(f'result_label_{i}')
        hint_label = self.nametowidget(f'hint_label_{i}')

        result = self.get_command(f'{PLAYERS_SYM[i]}{inp}')
        result_label.config(text=result[0])
        if result[2]:
            hint_label.config(text=result[2])
        return result[1]

    def get_command(self, inp: str) -> Tuple[str, bool, str]:
        """
        Process the input command and return the corresponding result, success flag, and hint.

        Args:
            inp (str): The input command.

        Returns:
            Tuple[str, bool, str]: A tuple containing the result, success flag, and hint.

        """
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

    def delete_last(self, e) -> None:
        """
        Deletes the last element from the history label and updates the results file.

        Args:
            e: The event object triggered by the widget.

        Returns:
            None
        """
        i = int(e.widget._name.split("_")[-1])
        category = self.category.get()
        game = self.game.get()

        history = self.nametowidget(f'history_label_{i}')
        history_text = history.cget("text").split("\n")
        last_element = history_text.pop(-1) if history_text else None
        history.config(text="\n".join(history_text))

        with open("./results.json", "r+", encoding="utf-16") as f:
            if f.read() == "":
                return
            f.seek(0)
            results = json.load(f)
            for items in results[category][game]:
                if items == f'{PLAYERS_SYM[i]}{last_element}':
                    results[category][game].remove(items)
                    break
            f.seek(0)
            json.dump(results, f, indent=4, ensure_ascii=False)
            f.truncate()

    def submit_code(self, e: tk.Event):
        """
        Submits the code entered by the user and updates the history label and results file.

        Args:
            e (tk.Event): The event object triggered by the user action.

        Returns:
            None
        """
        i = int(e.widget._name.split("_")[1])
        inp = e.widget.get()
        category = self.category.get()
        game = self.game.get()

        history = self.nametowidget(f'history_label_{i}')
        history_text = history.cget("text").split("\n")
        if len(history_text) > HISTORY_LEN: history_text.pop(0)
        history_text.append(inp) if history_text else [inp]
        history.config(text="\n".join(history_text))

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
        """
        Initializes the user interface by creating and placing the necessary widgets on the screen.

        This method creates labels, entry fields, and buttons for each player in the PLAYERS list.
        It also binds event handlers to the entry fields and buttons.

        Parameters:
        - self: The current instance of the class.

        Returns:
        - None
        """
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
                     width=40, height=20).grid(row=6,
                     column=0+i, pady=10, padx=10)

            tk.Label(self, name=f'history_label_{i}', text="",
                     width=40, height=7).grid(row=7,
                     column=0+i, pady=10, padx=10)

            btn = tk.Button(self, name=f'delete_last_{i}', text="delete last",
                     width=10, height=2)

            btn.bind("<Button-1>", self.delete_last)

            btn.grid(row=8,
                     column=0+i, pady=10, padx=10)

if __name__ == "__main__":
    app = VolCodes()
    app.mainloop()
