import tkinter as tk
from tkinter import filedialog
import processor2

class App:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.frame.pack()

		self.file_path = ''

		text = '''
- This app converts x,y,z points to a grid
- Please ensure the input file has no headers
- The first x coordinate should be in cell A1
		'''
		tk.Label(self.frame, text=text, justify='left').grid(row=0,column=0,columnspan=2)
		self.pathvar = tk.StringVar()
		self.pathvar.set('No file selected...')
		tk.Label(self.frame, textvariable=self.pathvar).grid(row=1,column=0)
		self.select = tk.Button(self.frame, text='Select file...', command=self.get_path)
		self.select.grid(row=1,column=1)

		self.color = tk.IntVar()
		tk.Checkbutton(self.frame, text='Colour grid ', variable=self.color, onvalue=1, offvalue=0).grid(row=2,column=0,columnspan=2)

		self.go_button = tk.Button(self.frame, text='Process data', state='disabled', command=self.process)
		self.go_button.grid(row=3,column=0,columnspan=2)

	def get_path(self):
		self.file_path = filedialog.askopenfilename(filetypes=[('Excel files','.xlsx')])
		if self.file_path:
			self.pathvar.set(self.file_path)
			self.go_button['state'] = 'normal'

	def process(self):
		processor2.process(self.file_path, self.color.get())
		self.go_button['state'] = 'disabled'
		self.pathvar.set('No file selected...')

if __name__ == '__main__':
	root = tk.Tk()
	root.title('Grid Processor')
	app = App(root)
	root.mainloop()