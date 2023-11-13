import csv
def load_data(filename):
    with open(filename, 'r') as f:
        return list(csv.DictReader(f))

def extract_4th_column(filename):
    data = load_data(filename)
    fourth_column_values = [row[list(row.keys())[3]] for row in data]
    return fourth_column_values

#now need to sepearate the list on ont the commmas,
def separate_drinks(drinks_list):
    new_list = []
    for item in drinks_list:
        if isinstance(item, str):  # Make sure the item is a string
            drinks = item.split(", ")
            new_list.extend(drinks)
    return new_list



def remove_duplicates_ordered(original_list):
    seen = set()
    new_list = []
    for item in original_list:
        if item not in seen:
            seen.add(item)
            new_list.append(item)
    return new_list

lst_of_products_and_prices =(remove_duplicates_ordered(separate_drinks(extract_4th_column("Csv file path here"))))


product_dict = {}
for item in lst_of_products_and_prices:
    product_name, product_price = item.rsplit(' - ', 1)
    product_dict[product_name] = float(product_price)

print(product_dict)
print(len(product_dict))
