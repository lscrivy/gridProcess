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

	result = [[None for x in range(df.x.max()+1)] for y in range(df.y.max()+1)]

	for row in df.itertuples():
		result[row.y][row.x] = row.z

	# reverse the row order 
	result_df = pd.DataFrame(result, index=y_vals, columns=x_vals)[::-1]

	writer = pd.ExcelWriter('results/grid.xlsx', engine='xlsxwriter')
	result_df.to_excel(writer, sheet_name='Grid')

	# conditional formatting
	if color:
		worksheet = writer.sheets['Grid']
		worksheet.conditional_format(1,1,df.y.max()+1,df.x.max()+1, {'type': '3_color_scale'})

	writer.save()