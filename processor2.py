import pandas as pd

def process(file_path, color):
	df = pd.read_excel(file_path, usecols=[0,1,2], header=None, names=['x','y','z'])

	# adjust the resolution to 1
	df.x = (df.x/50).astype(int)
	df.y = (df.y/50).astype(int)

	# get values for use as index/columns later
	y_vals = [y*50 for y in range(df.y.min(), df.y.max()+1)]
	x_vals = [x*50 for x in range(df.x.min(), df.x.max()+1)]

	# this ensures the smallest value is 0
	df.x -= df.x.min()
	df.y -= df.y.min()

	# our initial grid is a 2d array where you can access elements using grid[y][x]
	# both x and y are ascending
	grid = [[None for x in range(df.x.max()+1)] for y in range(df.y.max()+1)]

	for row in df.itertuples():
		grid[row.y][row.x] = row.z



	# reverse the row order 
	result_df = pd.DataFrame(grid, index=y_vals, columns=x_vals)[::-1]

	writer = pd.ExcelWriter('results/grid.xlsx', engine='xlsxwriter')
	result_df.to_excel(writer, sheet_name='Grid')

	# conditional formatting
	if color:
		worksheet = writer.sheets['Grid']
		worksheet.conditional_format(1,1,df.y.max()+1,df.x.max()+1, {'type': '3_color_scale'})

	writer.save()


	results = {}

	# Property A 
	def prop_a(a,b):
		if a and b:
			return a - b
		return None
	# x direction
	results['PAX'] = [[prop_a(val, row[x+20]) if x+20<len(row) else None for x, val in enumerate(row)] for row in grid]
	# y direction
	results['PAY'] = [[prop_a(val, grid[y+20][x]) if y+20<len(grid) else None for x, val in enumerate(row)] for y, row in enumerate(grid)]
	
	# rate of change function
	def roc(a,b,c):
		if a and b and c:
			return a-(2*b)+c
		return None
	# Property B
	# x direction
	results['PBX'] = [[roc(row[x-20], val, row[x+20]) if x-20>=0 and x+20<len(row) else None for x, val in enumerate(row)] for row in grid]
	# y direction
	results['PBY'] = [[roc(grid[y-20][x], val, grid[y+20][x]) if y-20>=0 and y+20<len(grid) else None for x, val in enumerate(row)] for y, row in enumerate(grid)]

	# Property x
	# x direction
	results['PXX'] = [[roc(row[x-6], val, row[x+6]) if x-6>=0 and x+6<len(row) else None for x, val in enumerate(row)] for row in grid]
	# y direction
	results['PXY'] = [[roc(grid[y-6][x], val, grid[y+6][x]) if y-6>=0 and y+6<len(grid) else None for x, val in enumerate(row)] for y, row in enumerate(grid)]


	for r in results:
		frame = pd.DataFrame(results[r], index=y_vals, columns=x_vals)[::-1]
		writer = pd.ExcelWriter(f'results/{r}.xlsx', engine='xlsxwriter')
		frame.to_excel(writer, sheet_name='Grid')

		writer.save()


