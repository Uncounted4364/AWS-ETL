import csv

# Replace 'your_file.csv' with the path to your CSV file
csv_file_path = 'chesterfield_25-08-2021_09-00-00.csv'

# Open the CSV file
with open(csv_file_path, 'r') as file:
    # Create a CSV reader object for a dictionary
    csv_reader = csv.DictReader(file)

    # Iterate through each row in the CSV file
    for row in csv_reader:
        # Each 'row' is a dictionary representing a row in the CSV file
        print(row)
        # Access data using column names, e.g., row['column_name']