import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import processor

class App:
	def __init__(self, master):
		self.master = master
		self.frame = ttk.Frame(self.master)
		self.frame.pack()

		self.file_path = ''

		text = '''- This app converts x,y,z points to a grid
- Please ensure the input file has no headers
- The first x coordinate should be in cell A1'''

		ttk.Label(self.frame, text=text, justify='left').grid(row=0,column=0,columnspan=2,padx=10,pady=(10,5))

		# criteria entries
		criteria = ttk.LabelFrame(self.frame, text='Criteria')
		criteria.grid(row=1,column=0,columnspan=2,padx=10,pady=(0,10),sticky='nsew')
		ttk.Label(criteria, text='ABRfl Property A: ').grid(row=0,column=0,sticky='e')
		self.crit_A = ttk.Entry(criteria, width=4)
		self.crit_A.grid(row=0,column=1,sticky='w')
		ttk.Label(criteria, text='ABRfl Property B: ').grid(row=1,column=0,sticky='e')
		self.crit_B = ttk.Entry(criteria, width=4)
		self.crit_B.grid(row=1,column=1,sticky='w')
		ttk.Label(criteria, text='ABRfl Property x: ').grid(row=2,column=0,sticky='e')
		self.crit_x = ttk.Entry(criteria, width=4)
		self.crit_x.grid(row=2,column=1,sticky='w')

		ttk.Label(self.frame, text='Test name: ').grid(row=2,column=0,sticky='e')
		self.test_name = ttk.Entry(self.frame)
		self.test_name.grid(row=2,column=1,sticky='w')

		# create two tabs
		tab_parent = ttk.Notebook(self.frame)
		tab_parent.grid(row=3,column=0,columnspan=2)
		tab1 = ttk.Frame(tab_parent)
		tab2 = ttk.Frame(tab_parent)
		tab_parent.add(tab1, text='Processing')
		tab_parent.add(tab2, text='Y Filter')

		# tab 1
		self.pathvar = tk.StringVar()
		self.pathvar.set('No file selected...')
		ttk.Label(tab1, textvariable=self.pathvar).grid(row=3,column=0,sticky='e')
		self.select = ttk.Button(tab1, text='Select file...', command=self.get_path)
		self.select.grid(row=3,column=1,sticky='w')
		self.go_button = ttk.Button(tab1, text='Process data', state='disabled', command=self.process)
		self.go_button.grid(row=4,column=0,columnspan=2,padx=5,pady=5)

		# tab 2
		ttk.Label(tab2, text='y1: ').grid(row=0,column=0,sticky='e')
		self.y1 = ttk.Entry(tab2)
		self.y1.grid(row=0,column=1,sticky='w')
		ttk.Label(tab2, text='y2: ').grid(row=1,column=0,sticky='e')
		self.y2 = ttk.Entry(tab2)
		self.y2.grid(row=1,column=1,sticky='w')
		ttk.Button(tab2, text='Filter', command=self.filter).grid(row=2,column=0,columnspan=2,sticky='nsew')

	def get_path(self):
		self.file_path = filedialog.askopenfilename(filetypes=[('Excel','.xlsx'),('CSV','.csv')])
		if self.file_path:
			self.pathvar.set(self.file_path)
			self.go_button['state'] = 'normal'

	def process(self):
		criteria = {}
		try:
			criteria['PAX'] = criteria['PAY'] = float(self.crit_A.get())
			criteria['PBX'] = criteria['PBY'] = float(self.crit_B.get())
			criteria['PXX'] = criteria['PXY'] = float(self.crit_x.get())
		except:
			messagebox.showerror('Error', 'Invalid Criteria!')
			return
		processor.process(self.file_path, criteria, self.test_name.get())
		self.go_button['state'] = 'disabled'
		self.pathvar.set('No file selected...')

	def filter(self):
		try:
			y1 = int(self.y1.get())
			y2 = int(self.y2.get())
		except:
			messagebox.showerror('Error', 'y values must be integers!')
			return
		criteria = {}
		try:
			criteria['PAX'] = criteria['PAY'] = float(self.crit_A.get())
			criteria['PBX'] = criteria['PBY'] = float(self.crit_B.get())
			criteria['PXX'] = criteria['PXY'] = float(self.crit_x.get())
		except:
			messagebox.showerror('Error', 'Invalid Criteria!')
			return
		processor.filter(criteria, self.test_name.get(), y1, y2)

if __name__ == '__main__':
	root = tk.Tk()
	root.title('Grid Processor')
	root.style = ttk.Style()
	root.style.theme_use('default')
	app = App(root)
	root.mainloop()