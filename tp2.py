import os
import csv
import pandas as pd

# Get the size of the CSV file
with open('example.csv', 'w') as creating_new_csv_file: 
   pass 
file_size = os.path.getsize('example.csv')

# Check if the file is empty
meet_attendees = ["1111" , "2222" , "3333"]
if file_size == 0:
    print('The file is empty.')
    column_name = "Active_Attendees"
    with open('example.csv', mode='a', newline='') as file:

            # Create a writer object
        writer = csv.writer(file)

            # Write the data to the CSV file
        writer.writerow([column_name])

        
    df = pd.read_csv('example.csv')
        # Create a new list of values to insert into the column
    new_column_data = ["Asddvv" , "vfdbgrfg" ,"efrgtyuthrg"]

        # Append the new data to the desired column
    df[column_name] = df[column_name].append(pd.Series(new_column_data))

        # Write the updated DataFrame to a new CSV file
    df.to_csv('updated_example.csv', index=False)

else:
    column_name = "Active_Attendees"
    print('The file is not empty.')
    df = pd.read_csv('example.csv')
        # Create a new list of values to insert into the column
    new_column_data = ["Asddvv" , "vfdbgrfg" ,"efrgtyuthrg"]

    new_column_data = ["1111111" , "xxxxxxxxx"]

        # Append the new data to the desired column
    df[column_name] = df[column_name].append(pd.Series(new_column_data))

        # Write the updated DataFrame to a new CSV file
    df.to_csv('updated_example.csv', index=False)


