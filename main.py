import tkinter as tk
from tkinter import filedialog
import processor

class App:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)

		self.file_path = ''

		text = '''
- This app converts x,y,z points to a grid
- Please ensure the file has no headers/text
- The first x coordinate should be in cell A1
		'''
		tk.Label(text=text, justify='left').pack(padx=5)
		self.select = tk.Button(text='Select file...', command=self.get_path)
		self.select.pack(pady=5)
		self.go_button = tk.Button(text='Process data', command=self.process)
		self.reset_button = tk.Button(text='back', command=self.reset)

	def get_path(self):
		self.file_path = filedialog.askopenfilename(filetypes=[('Excel files','.xlsx')])
		self.select.pack_forget()
		self.file_label = tk.Label(text=self.file_path)
		self.file_label.pack(pady=5)
		self.go_button.pack(pady=5)
		self.reset_button.pack(pady=5)

	def process(self):
		processor.process(self.file_path)
		self.reset()

	def reset(self):
		self.file_label.pack_forget()
		self.go_button.pack_forget()
		self.reset_button.pack_forget()
		self.select.pack(pady=5)


if __name__ == '__main__':
	root = tk.Tk()
	root.title('Grid Processor')
	app = App(root)
	root.mainloop()