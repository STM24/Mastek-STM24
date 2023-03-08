import csv
import pandas as pd

csv_data = []

column_name = "Active_Attendees"
with open('example.csv', mode='a', newline='') as file:

            # Create a writer object
    writer = csv.writer(file)

            # Write the data to the CSV file
    writer.writerow([column_name])





# Open the CSV file
with open('example.csv', mode='r') as file:

    # Create a reader object
    reader = csv.reader(file)

    # Store the contents of the file in a variable  
    csv_data = [row for row in reader]

# Print the contents of the variable
print(csv_data)

meet_attendees = ["1111" , "2222" , "3333"]

if column_name in csv_data:
    df = pd.read_csv('example.csv')
        # Create a new list of values to insert into the column
    new_column_data = list(meet_attendees)

    new_column_data = ["dv" , "fdv" , "drcr"]
        # Append the new data to the desired column
    df['Active_Attendees'] = df['Active_Attendees'].append(pd.Series(new_column_data))

        # Write the updated DataFrame to a new CSV file
    df.to_csv('updated_example.csv', index=False)
# else:
#     column_name = "Active_Attendees"
#     with open('example.csv', mode='a', newline='') as file:

#             # Create a writer object
#         writer = csv.writer(file)

#             # Write the data to the CSV file
#         writer.writerow([column_name])
        
#     df = pd.read_csv('example.csv')
#         # Create a new list of values to insert into the column
#     new_column_data = list(meet_attendees)

#         # Append the new data to the desired column
#     df[column_name] = df[column_name].append(pd.Series(new_column_data))

#         # Write the updated DataFrame to a new CSV file
#     df.to_csv('updated_example.csv', index=False)
#         # **********************