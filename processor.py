import pandas as pd

def process(file_path, criteria, test_name):
	if file_path[-4:] == '.csv':
		df = pd.read_csv(file_path, usecols=[0,1,2], header=None, names=['x','y','z'])
	else:
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

	# using zip df.to_dict('list') is about three times faster!
	# for row in df.itertuples():
	# 	grid[row.y][row.x] = row.z

	for row in zip(*df.to_dict('list').values()):
		grid[row[1]][row[0]] = row[2]



	# reverse the row order 
	result_df = pd.DataFrame(grid, index=y_vals, columns=x_vals)[::-1].round(2)

	writer = pd.ExcelWriter(f'results/{test_name} - Grid of Heights.xlsx', engine='xlsxwriter')
	result_df.to_excel(writer, sheet_name=test_name)

	# conditional formatting
	worksheet = writer.sheets[test_name]
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

	errors = {'type':[],'count':[]}
	for r in results:
		frame = pd.DataFrame(results[r], index=y_vals, columns=x_vals)[::-1].round(2)
		writer = pd.ExcelWriter(f'results/{test_name} - Property {r[1]} ({r[2].lower()}).xlsx', engine='xlsxwriter')
		frame.to_excel(writer, sheet_name=test_name)
		workbook = writer.book
		worksheet = writer.sheets[test_name]
		format1 = workbook.add_format({'bg_color':'red'})
		worksheet.conditional_format(1,1,df.y.max()+1,df.x.max()+1, 
			{'type': 'cell', 'criteria':'not between', 'minimum':-criteria[r], 'maximum':criteria[r], 'format':format1}
			)

		writer.save()

		# find out how many errors there are
		errors['type'].append(f'Property {r[1]} ({r[2].lower()})')
		errors['count'].append(sum(val <= -criteria[r] or val >= criteria[r] for val in [item for sublist in results[r] for item in sublist] if val))

	errors_df = pd.DataFrame(errors)
	errors_df.to_excel(f'results/{test_name} - Summary.xlsx')


def filter(criteria, test_name, y1, y2):
	results = {}

	results['grid'] = pd.read_excel(f'results/{test_name} - Grid of Heights.xlsx', index_col=0)
	results['PAX'] = pd.read_excel(f'results/{test_name} - Property A (x).xlsx', index_col=0)
	results['PBX'] = pd.read_excel(f'results/{test_name} - Property B (x).xlsx', index_col=0)
	results['PXX'] = pd.read_excel(f'results/{test_name} - Property X (x).xlsx', index_col=0)

	results = {n:frame.loc[frame.index.isin([y1,y2])] for n, frame in results.items()}
	
	for r in results:
		if r == 'grid':
			writer = pd.ExcelWriter(f'results/{test_name} - Grid of Heights (y={y1}or{y2}).xlsx', engine='xlsxwriter')
			results[r].to_excel(writer, sheet_name=test_name)

			# conditional formatting
			worksheet = writer.sheets[test_name]
			worksheet.conditional_format(1,1,2,len(results[r].columns), {'type': '3_color_scale'})

			writer.save()
		else:
			writer = pd.ExcelWriter(f'results/{test_name} - Property {r[1]} ({r[2].lower()}) (y={y1}or{y2}).xlsx', engine='xlsxwriter')
			results[r].to_excel(writer, sheet_name=test_name)
			workbook = writer.book
			worksheet = writer.sheets[test_name]
			format1 = workbook.add_format({'bg_color':'red'})
			worksheet.conditional_format(1,1,2,len(results[r].columns), 
				{'type': 'cell', 'criteria':'not between', 'minimum':-criteria[r], 'maximum':criteria[r], 'format':format1}
				)

			writer.save()


# if __name__ == '__main__':
# 	filter({'PAX':1,'PBX':1,'PXX':1}, 'MyTest', -50, -1000)








