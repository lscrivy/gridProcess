import pandas as pd

def process(file_path):
	df = pd.read_excel(file_path, usecols=[0,1,2], header=None, names=['x','y','z'])

	# adjust the resolution to 1
	df.x = (df.x/50).astype(int)
	df.y = (df.y/50).astype(int)

	# get y values for use as index later
	y_vals = [y*50 for y in range(df.y.min(), df.y.max()+1)]
	x_vals = [x*50 for x in range(df.x.min(), df.x.max()+1)]
	# print(y_vals)
	# print(x_vals)

	# this should ensure the smallest x / y value is 0
	df.x = (df.x - df.x.min())
	df.y = (df.y - df.y.min())

	# assuming x values start at 0...
	result = [[None for x in range(df.x.max()+1)] for y in range(df.y.max()+1)]

	for row in df.itertuples():
		result[row.y][row.x] = row.z

	# make a dataframe and then reverse the row order
	result_df = pd.DataFrame(result, index=y_vals, columns=x_vals)[::-1]

	# result_df.to_excel('results/grid.xlsx', header=False, index=False)

	writer = pd.ExcelWriter('results/grid.xlsx', engine='xlsxwriter')
	result_df.to_excel(writer, sheet_name='Sheet1')

	worksheet = writer.sheets['Sheet1']

	worksheet.conditional_format(1,1,df.y.max()+1,df.x.max()+1, {'type': '3_color_scale'})

	writer.save()