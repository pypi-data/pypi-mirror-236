import tkinter as tk
import tksheet
import numpy as np
from tkinter import filedialog
from os.path import normpath
import csv


class run(tk.Tk):
	def __init__(self, labels, resultlist):
		tk.Tk.__init__(self)
		column_1 = ["Top", "Bottom", "log EC50", "St. err. log EC50", "EC50 (M)" , "St. err. log EC50 (M)", "N"]
		data = np.c_[column_1, resultlist]
		#top = tk.Tk()
		self.title("Reults")
		self.grid_columnconfigure(0, weight = 1)
		self.grid_rowconfigure(0, weight = 1)
		self.sheet = tksheet.Sheet(self)
		self.sheet.grid(row = 0, column = 0, sticky = "nswe")
		self.sheet.set_sheet_data(data=data.tolist())
		self.sheet.set_all_cell_sizes_to_text()
		head_list = [" "] + labels
		self.sheet.headers(head_list)
		# table enable choices listed below:
		self.sheet.enable_bindings()
		self.geometry("600x600")
		
		#self.sheet.enable_bindings("all", "edit_header", "edit_index")
		self.sheet.popup_menu_add_command("Save sheet", self.save_sheet)
		self.mainloop()

	def save_sheet(self):
		#print(self.sheet.get_sheet_data(get_header = True, get_index = False))
		filepath = filedialog.asksaveasfilename(parent = self,
												title = "Save sheet as",
												filetypes = [('CSV File','.csv'),
															 ('TSV File','.tsv')],
												defaultextension = ".csv",
												confirmoverwrite = True)
		if not filepath or not filepath.lower().endswith((".csv", ".tsv")):
			return
		try:
			print("writing")
			with open(normpath(filepath), "w", newline = "", encoding = "utf-8") as fh:
				writer = csv.writer(fh,
									dialect = csv.excel if filepath.lower().endswith(".csv") else csv.excel_tab,
									lineterminator = "\n")
				writer.writerows(self.sheet.get_sheet_data(get_header = True, get_index = False))
		except:
			return
