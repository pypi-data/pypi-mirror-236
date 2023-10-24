from tksheet import Sheet
import tkinter as tk
from tkinter import filedialog
import csv
from os.path import normpath
import io
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pyCRC_plot import CRC
import os
from pyCRC_plot import show_results
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

color_cycle = ["k", "r", "b", "g"] * 2
marker_cycle = ["o", "s", "v", "^"] * 2
fill_cycle = ["full"]*4 + ["none"]*4

print(fill_cycle)

class main_window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        datalist = []
        self.datalist = datalist
        labellist = []
        self.labellist = labellist
        self.withdraw()
        self.title("Data sheet")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)
        self.frame.grid_columnconfigure(4, weight=1)
        self.frame.grid_columnconfigure(5, weight=1)
        self.frame.grid_columnconfigure(6, weight=1)
        self.frame.grid_columnconfigure(7, weight=1)
        self.frame.grid_columnconfigure(8, weight=1)
        self.frame.grid_columnconfigure(10, weight=1)
        self.frame.grid_columnconfigure(11, weight=1)
        self.frame.grid_columnconfigure(12, weight=1)
        self.frame.grid_columnconfigure(13, weight=1)
        self.frame.grid_columnconfigure(14, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=20)
        self.sheet = Sheet(self.frame,
                           data=[[f"" for c in range(50)] for r in range(50)])
        self.sheet.enable_bindings("all",
                                   "single_select",
                                    "drag_select",
                                    "select_all",
                                    "column_select",
                                    "row_select",
                                   "edit_header",
                                   "edit_index")
        self.frame.grid(row=0, column=0, sticky="nswe", columnspan=15)
        self.sheet.grid(row=1, column=0, sticky="nswe", columnspan=15)
        self.sheet.popup_menu_add_command("Open csv", self.open_csv)
        self.sheet.popup_menu_add_command("Save sheet", self.save_sheet)
        self.sheet.popup_menu_add_command("Add to plot", self.add_crc2)

        # self.sheet.set_all_cell_sizes_to_text()
        self.sheet.set_options(auto_resize_columns=60)
        self.sheet.change_theme("light green")

        # Add headers
        head_list = ["X (log[])"] + [f"Y{i + 1}" for i in range(49)]
        self.head_list = head_list
        self.sheet.headers(head_list)

        # ADd buttons
        button1 = tk.Button(self.frame, text='Save CSV', command=(lambda: self.save_sheet()))
        button2 = tk.Button(self.frame, text='Open CSV', command=(lambda: self.open_csv()))
        #self.plot_options()
        button3 = tk.Button(self.frame, text='Check all CRCs', command=(lambda: self.check_crcs()))
        # button4 = tk.Button(self.frame, text='Add another CRC', command=(lambda:self.add_crc()))
        button1.grid(row=0, column=0, sticky="nswe", pady=2)
        button2.grid(row=0, column=1, sticky="nswe", pady=2)
        button3.grid(row=0, column=2, sticky="nswe", pady=2)
        # button4.grid(row = 0, column = 3, sticky = "nswe",pady = 2)
        plot_button = tk.Button(self.frame, text='Plot', command=(lambda: self.plot_crc()))
        plot_button.grid(row=0, column=4, sticky="nswe", pady=2, columnspan=2)

        reset_button = tk.Button(self.frame, text='Reset curves', command=(lambda: self.reset_list()))
        reset_button.grid(row=0, column=3, sticky="nswe", pady=2, columnspan=1)
        # Add entry boxes
        entry1 = tk.Entry(self.frame)
        entry1.insert(0, "CRC")
        self.entry1 = entry1
        entry1.grid(row=0, column=7, sticky="nswe", pady=10)
        label1 = tk.Label(self.frame, text='Plot title')
        label1.grid(row=0, column=6, sticky="nswe", pady=5)

        entry2 = tk.Entry(self.frame)
        self.entry2 = entry2
        entry2.grid(row=0, column=9, sticky="nswe", pady=10)
        entry2.insert(0, "log[Agonist]")
        label2 = tk.Label(self.frame, text='X label')
        label2.grid(row=0, column=8, sticky="nswe", pady=5)

        entry3 = tk.Entry(self.frame)
        self.entry3 = entry3
        entry3.grid(row=0, column=11, sticky="nswe", pady=10)
        entry3.insert(0, "Normalized response")
        label3 = tk.Label(self.frame, text='Y label')
        label3.grid(row=0, column=10, sticky="nswe", pady=5)

        # center the window and unhide
        self.update_idletasks()
        w = self.winfo_screenwidth()  # - 20
        h = self.winfo_screenheight()  # - 70
        size = (1000, 700)
        x = (w / 2 - size[0] / 2)
        y = h / 2 - size[1] / 2

        self.geometry("%dx%d+%d+%d" % (size + ((w / 2 - size[0] / 2), h / 2 - size[1] / 2)))
        self.deiconify()

    def save_sheet(self):
        filepath = filedialog.asksaveasfilename(parent=self,
                                                title="Save sheet as",
                                                filetypes=[('CSV File', '.csv'),
                                                           ('TSV File', '.tsv')],
                                                defaultextension=".csv",
                                                confirmoverwrite=True)
        if not filepath or not filepath.lower().endswith((".csv", ".tsv")):
            return
        try:
            with open(normpath(filepath), "w", newline="", encoding="utf-8") as fh:
                writer = csv.writer(fh,
                                    dialect=csv.excel if filepath.lower().endswith(".csv") else csv.excel_tab,
                                    lineterminator="\n")
                writer.writerows(self.sheet.get_sheet_data(get_header=False, get_index=False))
        except:
            return

    def open_csv(self):
        filepath = filedialog.askopenfilename(parent=self, title="Select a csv file")
        if not filepath or not filepath.lower().endswith((".csv", ".tsv")):
            return
        try:
            with open(normpath(filepath), "r") as filehandle:
                filedata = filehandle.read()
            self.sheet.set_sheet_data([r for r in csv.reader(io.StringIO(filedata),
                                                             dialect=csv.Sniffer().sniff(filedata),
                                                             skipinitialspace=False)])
        except:
            return

    def clean_data(self):
        data = self.sheet.get_sheet_data(get_header=False, get_index=False)
        df = pd.DataFrame(data)
        df.replace('', np.nan, inplace=True)
        df = df.dropna(how='all')
        df = df.dropna(how='all', axis=1)
        df = df.astype("float")
        return df

    def check_crcs(self):
        reslist = []
        df = self.clean_data()
        for i, cname in enumerate(df):
            column = df[cname]
            if i == 0:
                x = column
                continue
            X, fitted, results = CRC.fit_individual(x, column)
            reslist.append(results)
            fig = plt.figure()
            plt.plot(X, fitted, color="k")
            plt.scatter(x, column, color="k")
            plt.xlabel(self.entry2.get())
            plt.ylabel(self.entry3.get())
            plt.title(f"Y{i}")
            root2 = tk.Tk()
            root2.title(f"Y{i}")
            canvas = FigureCanvasTkAgg(fig, master=root2)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        show_results.run(labels=[f"Y{i + 1}" for i in range(len(reslist))], resultlist=np.array(reslist).T)
        # plt.show()

    def plot_crc(self):
        #        df = self.clean_data()
        if len(self.datalist) == 0:
            self.add_crc()
        title = self.entry1.get()
        data = self.sheet.get_sheet_data(get_header=False, get_index=False)
        x = pd.DataFrame(data)
        x = x.iloc[:, 0]
        x.replace('', np.nan, inplace=True)
        x = x.dropna(how='all')
        x = x.astype("float")

        i = 0
        resultlist = []
        fig = plt.figure()
        ax = fig.add_subplot(111)
        proxy_label = []
        proxy = []
        for df, label in zip(self.datalist, self.labellist):
            try:
                df.insert(0, column="X", value=x)
            except:
                df = df.loc[:, df.columns != 'X']
                df.insert(0, column="X", value=x)
            df = df.astype("float")
            x = df["X"]
            df = df.loc[:, df.columns != 'X']
            X, mean_curve, std_curve, mean_data, std_data, results = CRC.fit_hill(x, df)  # , label, title)
            resultlist.append(results)

            ax.fill_between(X, mean_curve - std_curve, mean_curve + std_curve,
                            color=color_cycle[i], alpha=0.1)
            line, = ax.plot(X, mean_curve, label=label, color=color_cycle[i])
            points = ax.errorbar(x, mean_data, yerr=std_data, fmt=marker_cycle[i], fillstyle=fill_cycle[i],capsize=3, color=color_cycle[i],label=label)
            proxy.append((line,points))
            proxy_label.append(label)
            i += 1
        plt.xlabel(self.entry2.get())
        plt.ylabel(self.entry3.get())
        plt.title(title)
        ax.legend(proxy,proxy_label)
        filename = title
        i = 1
        # Check if the file exists
        while True:
            if os.path.exists(f"{filename}.svg"):
                # If it does, remove it
                filename = f"{title}({i})"
                i += 1
            else:
                break
        fig.savefig(f"{filename}.svg")
        # plt.ioff()
        # plt.show(block = False)
        root2 = tk.Tk()
        root2.title("Plot")
        canvas = FigureCanvasTkAgg(fig, master=root2)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # plt.pause(0.01)
        show_results.run(labels=self.labellist, resultlist=np.array(resultlist).T)

    def reset_list(self):
        self.datalist = []
        self.labellist = []
        curves_text = tk.Label(self.canvas1, text=f'Curves added: {len(self.datalist)}')
        curves_text.grid(row=0, column=4, sticky="nswe", pady=2, columnspan=1)

    def add_crc(self):
        heads = self.head_list
        f = self.select_entry1.get().upper()
        l = self.select_entry2.get().upper()
        if f == "":
            f = "Y1"

        if l == "":
            l = "Y49"

        try:
            first = heads.index(f)
            last = heads.index(l) + 1
        except:
            root2 = tk.Tk()
            root2.title("Error")
            text = tk.Label(root2,
                            text=f"Error: {self.select_entry1.get().upper()} - {self.select_entry2.get().upper()}"
                                 " is not a valid column range", pady=5, padx=5)
            text.config(font=('helvetica bold', 14))
            text.pack()
            return

        label = self.plot_label.get()
        self.select_entry1.delete(0, "end")
        self.select_entry2.delete(0, "end")
        self.plot_label.delete(0, "end")

        data = self.sheet.get_sheet_data(get_header=False, get_index=False)
        df = pd.DataFrame(data)
        df = df.iloc[:, first:last]
        df.replace('', np.nan, inplace=True)
        df = df.dropna(how='all')
        df = df.dropna(how='all', axis=1)
        df = df.astype("float")
        self.datalist.append(df)
        self.labellist.append(label)
        curves_text = tk.Label(self.canvas1, text=f'Curves added: {len(self.datalist)}')
        curves_text.grid(row=0, column=4, sticky="nswe", pady=2, columnspan=1)

    def add_crc2(self):
        #data = self.sheet.get_sheet_data(get_header=False, get_index=False)
        #print(currently_selected)
        last_selected = self.sheet.get_all_selection_boxes_with_types()#get_currently_selected()
        rows = [last_selected[0][0][0],last_selected[0][0][2]]
        columns =  [last_selected[0][0][1], last_selected[0][0][3]]
        if last_selected[0][0][1] == 0:
            columns[0]=1

        data =  self.sheet.get_sheet_data(get_displayed=False,
                       get_header=False,
                       get_index=False,
                       get_index_displayed=True,
                       get_header_displayed=True,
                       only_rows=range(rows[0],rows[1]),
                       only_columns=range(columns[0],columns[1]))
        df = pd.DataFrame(data)
        df.replace('', np.nan, inplace=True)
        self.df = df
        top = tk.Tk()
        self.top_addcrc = top
        top.title("Adding CRC")
        L1 = tk.Label(top, text="Label")
        L1.pack()
        E1 = tk.Entry(top, bd =5)
        E1.pack()
        self.E1 = E1
        add = tk.Button(top, text='Add CRC', command=(lambda: self.add_label()))
        cancel = tk.Button(top, text='Cancel', command=(lambda: self.cancel()))
        add.pack()
        cancel.pack()


    def cancel(self):
        self.top_addcrc.destroy()

    def add_label(self):
        label_temp = self.E1.get()
        self.datalist.append(self.df)
        self.labellist.append(label_temp)
        self.top_addcrc.destroy()
'''

    def plot_options(self):
        # Configure the layout
        root = tk.Tk()
        canvas1 = tk.Canvas(root, width=400, height=300)
        root.title("Plotting window")
        self.canvas1 = canvas1
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_columnconfigure(3, weight=1)
        root.grid_columnconfigure(4, weight=2)

        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
        canvas1.grid(row=0, column=0, sticky="nswe", columnspan=4, rowspan=3)

        entry_text = tk.Label(canvas1, text='First and last column to plot (i.e. Y1 Y5)')
        entry_text.grid(row=0, column=0, sticky="nswe", pady=2, columnspan=2)

        select_entry1 = tk.Entry(canvas1)
        self.select_entry1 = select_entry1
        select_entry1.grid(row=1, column=0, sticky="nswe", pady=2, padx=2)

        select_entry2 = tk.Entry(canvas1)
        self.select_entry2 = select_entry2
        select_entry2.grid(row=1, column=1, sticky="nswe", pady=2, padx=2)

        label_text = tk.Label(canvas1, text='Curve label')
        label_text.grid(row=0, column=3, sticky="nswe", pady=2, columnspan=1)

        plot_label = tk.Entry(canvas1)
        self.plot_label = plot_label
        plot_label.grid(row=1, column=3, sticky="nswe", pady=2, padx=2)

        add_button = tk.Button(canvas1, text='Add CRC', command=(lambda: self.add_crc()))
        add_button.grid(row=1, column=4, sticky="nswe", pady=2, columnspan=1)

        plot_button = tk.Button(canvas1, text='Plot', command=(lambda: self.plot_crc()))
        plot_button.grid(row=2, column=0, sticky="nswe", pady=2, columnspan=3)

        reset_button = tk.Button(canvas1, text='Reset curves', command=(lambda: self.reset_list()))
        reset_button.grid(row=2, column=3, sticky="nswe", pady=2, columnspan=1)
'''




if __name__ == "__main__":
    app = main_window()
    app.mainloop()
