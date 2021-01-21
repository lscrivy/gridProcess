import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

def process(file_path, criteria, test_name):
	if file_path[-4:] == '.csv':
		df = pd.read_csv(file_path, usecols=[0,1,2], header=None, names=['x','y','z'])
	else:
		df = pd.read_excel(file_path, usecols=[0,1,2], header=None, names=['x','y','z'])


	# adjust the resolution to 1
	df.x = (df.x/50).apply(np.floor).astype(int)
	df.y = (df.y/50).apply(np.floor).astype(int)

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

	writer = pd.ExcelWriter(f'results/{test_name}.xlsx', engine='xlsxwriter')
	result_df.to_excel(writer, sheet_name='Grid of Heights')

	# conditional formatting
	worksheet = writer.sheets['Grid of Heights']
	worksheet.conditional_format(1,1,df.y.max()+1,df.x.max()+1, {'type':'2_color_scale', 'min_color':'#FFFFFF', 'max_color':'#000000'})
	worksheet.conditional_format(1,1,df.y.max()+1,df.x.max()+1, {'type':'3_color_scale'})




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

	# to count the errors for our summary file
	errors = {'Type':[],'Criteria':[],'Total Points':[],'Non-compliant Points':[],'Non-compliance %':[]}
	for r in results:
		frame = pd.DataFrame(results[r], index=y_vals, columns=x_vals)[::-1].round(2)
		sheet_name = f'ABRfl Property {r[1]} ({r[2].lower()})'
		frame.to_excel(writer, sheet_name=sheet_name)
		workbook = writer.book
		worksheet = writer.sheets[sheet_name]
		format1 = workbook.add_format({'bg_color':'red'})
		worksheet.conditional_format(1,1,df.y.max()+1,df.x.max()+1, 
			{'type': 'cell', 'criteria':'not between', 'minimum':-criteria[r], 'maximum':criteria[r], 'format':format1}
			)

		# find out how many errors there are
		errors['Type'].append(f'ABRfl Property {r[1]} ({r[2].lower()})')
		errors['Criteria'].append(f'-{criteria[r]} ≤ z ≤ {criteria[r]}')
		total_points = sum(len([z for z in row if z!=None]) for row in results[r])
		errors['Total Points'].append(total_points)
		error_count = sum(val <= -criteria[r] or val >= criteria[r] for val in [item for sublist in results[r] for item in sublist] if val)
		errors['Non-compliant Points'].append(error_count)
		errors['Non-compliance %'].append(round((error_count/total_points)*100 if total_points else 0, 2))


	errors_df = pd.DataFrame(errors)


	# summary file
	errors_df.to_excel(writer, sheet_name='Summary', index=False, startrow=3)

	workbook = writer.book
	worksheet = writer.sheets['Summary']

	worksheet.write(0, 0, test_name)
	worksheet.write(2, 0, 'Errors')
	worksheet.set_column(0,4,20)

	writer.save()



	# create contour maps
	plt.rcParams.update({'font.size':2})
	cont_x, cont_y = np.meshgrid(x_vals, y_vals)

	# grid
	fig, ax = plt.subplots()
	cmap = plt.cm.jet
	map = ax.contourf(cont_x, cont_y, grid, 200, cmap=cmap)
	ax.axis('scaled')
	fig.colorbar(map, fraction=0.046, pad=0.06, orientation='horizontal', shrink=.2, ticks=[-20,-15,-10,-5,0])
	plt.savefig(f'results/{test_name} Contour.png', bbox_inches='tight', dpi=1000)

	# criteria maps
	for r in results:
		fig, ax = plt.subplots()
		colors = ['red','white','red']
		cmap = matplotlib.colors.ListedColormap(colors)
		# array = np.array(results[r], dtype=np.float64)
		# boundaries = [np.nanmin(array), -criteria[r], criteria[r], np.nanmax(array)]
		boundaries = [-99999999999, -criteria[r], criteria[r], 99999999999]
		map = ax.contourf(cont_x, cont_y, results[r], levels=boundaries, cmap=cmap)
		ax.axis('scaled')
		plt.savefig(f'results/{test_name} {r}.png', bbox_inches='tight', dpi=1000)



def filter(criteria, test_name, y1, y2):
	results = {}

	results['grid'] = pd.read_excel(f'results/{test_name}.xlsx', sheet_name='Grid of Heights', index_col=0)
	results['PAX'] = pd.read_excel(f'results/{test_name}.xlsx', sheet_name='ABRfl Property A (x)', index_col=0)
	results['PBX'] = pd.read_excel(f'results/{test_name}.xlsx', sheet_name='ABRfl Property B (x)', index_col=0)
	results['PXX'] = pd.read_excel(f'results/{test_name}.xlsx', sheet_name='ABRfl Property X (x)', index_col=0)

	results = {n:frame.loc[frame.index.isin([y1,y2])] for n, frame in results.items()}
	writer = pd.ExcelWriter(f'results/{test_name} (y={y1}|{y2}).xlsx')

	# to count the errors for our summary file
	errors = {'Type':[],'Criteria':[],'Total Points':[],'Non-compliant Points':[],'Non-compliance %':[]}

	for r in results:
		if r == 'grid':
			results[r].to_excel(writer, sheet_name='Grid of Heights')

			# conditional formatting
			worksheet = writer.sheets['Grid of Heights']
			worksheet.conditional_format(1,1,2,len(results[r].columns), {'type': '3_color_scale'})
		else:
			sheet_name = f'ABRfl Property {r[1]} ({r[2].lower()})'
			results[r].to_excel(writer, sheet_name=sheet_name)
			workbook = writer.book
			worksheet = writer.sheets[sheet_name]
			format1 = workbook.add_format({'bg_color':'red'})
			worksheet.conditional_format(1,1,2,len(results[r].columns), 
				{'type': 'cell', 'criteria':'not between', 'minimum':-criteria[r], 'maximum':criteria[r], 'format':format1}
				)

			errors['Type'].append(f'ABRfl Property {r[1]} ({r[2].lower()})')
			errors['Criteria'].append(f'-{criteria[r]} ≤ z ≤ {criteria[r]}')
			total_points = results[r].count().sum()
			errors['Total Points'].append(total_points)
			error_count = results[r].where((results[r] <= -criteria[r]) | (results[r] >= criteria[r])).count().sum()
			# error_count = sum(val <= -criteria[r] or val >= criteria[r] for val in [item for sublist in results[r] for item in sublist] if val)
			errors['Non-compliant Points'].append(error_count)
			errors['Non-compliance %'].append(round((error_count/total_points)*100 if total_points else 0, 2))

	errors_df = pd.DataFrame(errors)

	# summary file
	errors_df.to_excel(writer, sheet_name='Summary', index=False, startrow=3)

	workbook = writer.book
	worksheet = writer.sheets['Summary']

	worksheet.write(0, 0, test_name)
	worksheet.write(2, 0, 'Errors')
	worksheet.set_column(0,4,20)

	writer.save()


# if __name__ == '__main__':
# 	filter({'PAX':1,'PBX':1,'PXX':1}, 'MyTest', -50, -1000)








