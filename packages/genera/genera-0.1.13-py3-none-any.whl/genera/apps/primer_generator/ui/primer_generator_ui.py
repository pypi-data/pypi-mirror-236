import genera

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from typing import List


class PrimerGeneratorUI(genera.classes.UI):
    def __init__(self, settings={}):
        super().__init__()
        self.settings = genera.utils.settings.merge(
            [genera.utils.settings.load(__file__, "ui.json"), settings]
        )
        self.root = None
        self.load_file_path = None
        self.save_file_path = None
        self.post_load_file_function = None

    def init_ui(self):
        self.root = tk.Tk()
        self.root.title(self.settings["title"])

        self.elements["load_file_button"] = ttk.Button(
            self.root,
            text=self.settings["load_file_label"],
            command=self.load_fragments,
        )
        self.elements["load_file_button"].grid(row=0, columnspan=2, pady=25)
        row_counter = 1
        for input_tag in self.settings["T_inputs"]:
            ttk.Label(self.root, text=self.settings["T_inputs"][input_tag]).grid(
                row=row_counter, column=0
            )
            self.elements[f"{input_tag}_input"] = tk.Spinbox(
                self.root, from_=0, to=100, increment=self.settings["T_input_increment"]
            )
            self.elements[f"{input_tag}_input"].delete(0, "end")
            self.elements[f"{input_tag}_input"].insert(0, str(self.settings[input_tag]))
            self.elements[f"{input_tag}_input"].grid(row=row_counter, column=1)
            row_counter += 1

        for input_tag in self.settings["length_inputs"]:
            ttk.Label(self.root, text=self.settings["length_inputs"][input_tag]).grid(
                row=row_counter, column=0
            )
            self.elements[f"{input_tag}_input"] = tk.Spinbox(
                self.root, from_=0, to=100, increment=1
            )
            self.elements[f"{input_tag}_input"].delete(0, "end")
            self.elements[f"{input_tag}_input"].insert(0, str(self.settings[input_tag]))
            self.elements[f"{input_tag}_input"].grid(row=row_counter, column=1)
            row_counter += 1

        self.force_GC_state = tk.IntVar()
        self.elements["force_GC_end_toggle"] = ttk.Checkbutton(
            self.root,
            text=self.settings["force_GC_end_label"],
            variable=self.force_GC_state,
        )
        self.force_GC_state.set(self.settings["force_GC_end"])
        self.elements["force_GC_end_toggle"].grid(row=row_counter, columnspan=2)
        row_counter += 1

        self.elements["save_file_button"] = ttk.Button(
            self.root,
            text=self.settings["save_file_label"],
            command=self.write_primers,
        )
        self.elements["save_file_button"].grid(row=row_counter, columnspan=2, pady=25)
        self.elements["save_file_button"].config(state="disabled")
        row_counter += 1

        ttk.Separator(self.root, orient="horizontal").grid(
            row=row_counter, columnspan=2, sticky="ew", padx=5, pady=25
        )
        row_counter += 1

        self.elements["check_primers_input"] = tk.Text(self.root, height=5, width=40)
        self.elements["check_primers_input"].grid(row=row_counter, columnspan=2)
        row_counter += 1

        self.elements["check_primers_button"] = ttk.Button(
            self.root, text="Check primers"
        )
        self.elements["check_primers_button"].grid(
            row=row_counter, columnspan=2, pady=25
        )

        self.load_file_path = tk.StringVar()
        self.save_file_path = tk.StringVar()

    def load_fragments(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                (self.settings["load_file_type"], self.settings["load_file_ext"])
            ]
        )
        self.load_file_path.set(file_path)

    def write_primers(self):
        file_path = filedialog.asksaveasfilename(
            filetypes=[
                (self.settings["save_file_type"], self.settings["save_file_ext"])
            ]
        )
        self.save_file_path.set(file_path)

    def init_check_primers_window(self, columns, values):
        self.check_primers_window = tk.Toplevel(self.root)
        self.check_primers_window.title("Primer properties")
        self.elements["table"] = ttk.Treeview(
            self.check_primers_window, columns=columns, show="headings"
        )
        for col in columns:
            self.elements["table"].heading(col, text=col)
            self.elements["table"].column(col, width=200)
        for data_row in values:
            self.elements["table"].insert("", tk.END, values=data_row)
        self.elements["table"].pack()
