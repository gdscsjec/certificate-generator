import pandas as pd

# Enter the file name you want to parse, without extension.
file_name = ''

# This will read the csv file, if you have text file or another please change the code accordingly.
data = pd.read_csv(f'{file_name}.csv')

# Sets cannot have duplicate values, as we are generating certificates there is no point having duplicate values, hence set will ensure there are no duplicates.
names = set()

# Write the logic to map over the data and then add them to the names set.
# for i in range(1, 5):
#     column = data[f'Team Member {i} Name']
#     for name in column:
#         names.add(name.title().strip())

# Write to the file_name.txt with all the names, lower() will convert the file_name.txt to lower.
with open(f'{file_name}.txt'.lower(), 'w') as f:

    # Write the contents of names into file_name, while joining by \n i.e. new line character
    # Filter is optional, I had cases where Team members were only 2 or 3 hence other were blank.
    f.write('\n'.join(filter(lambda x: x != "-" and x != ".", names)))
    
    # Uncomment below if you just wanna join and not filter anything and comment the above line.
    # f.write('\n'.join(names))

