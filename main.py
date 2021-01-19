import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import processor

class App:
	def __init__(self, master):
		self.master = master
		self.frame = ttk.Frame(self.master)
		self.frame.pack()

		self.file_path = ''

		text = '''Title Text...
info about using this app etc. etc.'''

		ttk.Label(self.frame, text=text, justify='center').grid(row=0,column=0,columnspan=2,padx=10,pady=10)

		ttk.Label(self.frame, text='Test name: ').grid(row=1,column=0,sticky='e')
		self.test_name = ttk.Entry(self.frame, width=10)
		self.test_name.grid(row=1,column=1,sticky='w')

		# criteria entries
		criteria = ttk.LabelFrame(self.frame, text='Criteria', padding=(10,2,10,10))
		criteria.grid(row=2,column=0,columnspan=2,padx=10,pady=10,sticky='nsew')
		ttk.Label(criteria, text='ABRfl Property A: ').grid(row=0,column=0,sticky='w')
		self.crit_A = ttk.Entry(criteria, width=4)
		self.crit_A.grid(row=0,column=1,sticky='w')
		ttk.Label(criteria, text='ABRfl Property B: ').grid(row=1,column=0,sticky='w')
		self.crit_B = ttk.Entry(criteria, width=4)
		self.crit_B.grid(row=1,column=1,sticky='w')
		ttk.Label(criteria, text='ABRfl Property X: ').grid(row=2,column=0,sticky='w')
		self.crit_x = ttk.Entry(criteria, width=4)
		self.crit_x.grid(row=2,column=1,sticky='w')

		# create two tabs
		tab_parent = ttk.Notebook(self.frame)
		tab_parent.grid(row=3,column=0,columnspan=2,sticky='nsew')
		tab1 = ttk.Frame(tab_parent, padding=20)
		tab2 = ttk.Frame(tab_parent, padding=20)
		tab_parent.add(tab1, text='Process', sticky='nsew')
		tab_parent.add(tab2, text='Y Filter', sticky='nsew')

		# tab 1
		self.pathvar = tk.StringVar()
		self.pathvar.set('No file selected...')
		ttk.Label(tab1, textvariable=self.pathvar, padding=(0,0,0,10)).pack()
		self.select = ttk.Button(tab1, text='Select file...', width=10, command=self.get_path)
		self.select.pack()
		self.go_button = ttk.Button(tab1, text='Process data', width=10, state='disabled', command=self.process)
		self.go_button.pack(padx=50)

		# tab 2
		yframe1 = ttk.Frame(tab2)
		yframe1.pack()
		ttk.Label(yframe1, text='y1: ').pack(side='left')
		self.y1 = ttk.Entry(yframe1, width=5)
		self.y1.pack(side='left')
		yframe2 = ttk.Frame(tab2)
		yframe2.pack()
		ttk.Label(yframe2, text='y2: ').pack(side='left')
		self.y2 = ttk.Entry(yframe2, width=5)
		self.y2.pack(side='left')
		ttk.Button(tab2, text='Filter', command=self.filter).pack(side='bottom')

	def get_path(self):
		self.file_path = filedialog.askopenfilename(filetypes=[('Excel','.xlsx'),('CSV','.csv')])
		if self.file_path:
			if len(self.file_path) < 30:
				self.pathvar.set(self.file_path)
			else:
				self.pathvar.set(self.file_path[:26]+'...')
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
	root.style.configure('.', font=('Microsoft Sans Serif', 14))
	app = App(root)
	root.mainloop()