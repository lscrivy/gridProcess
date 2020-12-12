import tkinter as tk
from tkinter import filedialog, messagebox
import processor

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
		tk.Label(self.frame, text=text, justify='left').grid(row=0,column=0,columnspan=2,padx=5)

		# criteria entries
		criteria = tk.LabelFrame(self.frame, text='Criteria')
		criteria.grid(row=1,column=0,columnspan=2,pady=(0,10))
		tk.Label(criteria, text='ABRfl Property A').grid(row=0,column=0,sticky='e')
		self.crit_A = tk.Entry(criteria, width=4)
		self.crit_A.grid(row=0,column=1,sticky='w')
		tk.Label(criteria, text='ABRfl Property B').grid(row=1,column=0,sticky='e')
		self.crit_B = tk.Entry(criteria, width=4)
		self.crit_B.grid(row=1,column=1,sticky='w')
		tk.Label(criteria, text='ABRfl Property x').grid(row=2,column=0,sticky='e')
		self.crit_x = tk.Entry(criteria, width=4)
		self.crit_x.grid(row=2,column=1,sticky='w')

		self.pathvar = tk.StringVar()
		self.pathvar.set('No file selected...')
		tk.Label(self.frame, textvariable=self.pathvar).grid(row=2,column=0,sticky='e')
		self.select = tk.Button(self.frame, text='Select file...', command=self.get_path)
		self.select.grid(row=2,column=1,sticky='w')

		self.go_button = tk.Button(self.frame, text='Process data', state='disabled', command=self.process)
		self.go_button.grid(row=3,column=0,columnspan=2,padx=5,pady=5)

	def get_path(self):
		self.file_path = filedialog.askopenfilename(filetypes=[('Excel files','.xlsx')])
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
		processor.process(self.file_path, criteria)
		self.go_button['state'] = 'disabled'
		self.pathvar.set('No file selected...')

if __name__ == '__main__':
	root = tk.Tk()
	root.title('Grid Processor')
	app = App(root)
	root.mainloop()