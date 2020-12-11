import pandas as pd

# pd.set_option('display.max_rows', None)

df = pd.read_excel('data.xlsx', usecols=[0,1,2], header=None, skiprows=6, names=['x','y','z'])

# adjust the resolution to 1
df.x = (df.x/50).astype(int)
df.y = (df.y/50).astype(int)

# this should ensure the smallest x value is 0
df.x = df.x - df.x.min()

# assuming x values start at 0...
result = [[None for x in range(df.x.max()+1)] for y in range(df.y.max()-df.y.min()+1)]

y_vals = list(set(df.y.tolist()))
y_vals.sort(reverse=True)

# we are assuming none of the y values were skipped???
for i, y in enumerate(y_vals):
	group = df.loc[df.y==y].sort_values('x')
	for index, row in group.iterrows():
		# swap row.z for (row.x, row.y) to check processing
		result[i][row.x.astype(int)] = row.z

result_df = pd.DataFrame(result)
result_df.to_excel('grid.xlsx')


