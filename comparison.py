import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

def get_grid(file_path):
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

	return grid

def compare(ref_file, comp_file):
	ref_grid = get_grid(ref_file)
	comp_grid = get_grid(comp_file)

	# flatten both lists
	ref_grid = [item for sublist in ref_grid for item in sublist]
	comp_grid = [item for sublist in comp_grid for item in sublist]

	ref_min = min([z for z in ref_grid if z!=None])
	ref_max = max([z for z in ref_grid if z!=None])
	comp_min = min([z for z in comp_grid if z!=None])
	comp_max = max([z for z in comp_grid if z!=None])

	# adjust the comp_grid values so that ref_min and comp_max are the same
	diff = comp_max-ref_min
	comp_grid = [z-diff if z!=None else None for z in comp_grid]

	# we need to know how many times to increment by 0.1 to get ref_max == comp_min
	inc = ref_max - comp_min + diff
	inc = int(inc/0.1)

	n = 0
	error_totals = []
	while n < inc:
		# calculate how much error there is between the two grids
		error = 0
		for ref, comp in zip(ref_grid, comp_grid):
			if ref and comp:
				error += abs(ref-comp)
		error_totals.append(error)
		# increment grid by 0.1mm
		comp_grid = [z+0.1 if z!=None else None for z in comp_grid]
		n += 1

	# find the position of the minimum error
	min_pos = np.argmin(error_totals)

	adjustment = -diff + (0.1*min_pos)

	print(adjustment)



if __name__ == '__main__':
	print('Floor Dynamics')
	compare('/Users/Scrivy/Downloads/Floor data/Leica ATS 600 Data (XYZ) (TT) v1.1.xlsx',
		'/Users/Scrivy/Downloads/Floor data/Floor Dynamics Data (XYZ) (TT) v1.2.csv')

	print('Plowman Craven')
	compare('/Users/Scrivy/Downloads/Floor data/Leica ATS 600 Data (XYZ) (TT) v1.1.xlsx',
		'/Users/Scrivy/Downloads/Floor data/Plowman Craven Data (XYZ) (TT) v1.2.csv')

	print('Muller Lobisch')
	compare('/Users/Scrivy/Downloads/Floor data/Leica ATS 600 Data (XYZ) (TT) v1.1.xlsx',
		'/Users/Scrivy/Downloads/Floor data/Muller Lobisch Data (XYZ) (TT) v1.2.csv')








