from products_and_prices_dict import get_products
from unique_branches import get_unique_branches
from normalise_clean_data import get_normalised_transactions
from datetime import datetime

import psycopg2
import os
from dotenv import load_dotenv

# Load data from external files or functions
products = get_products()
branches = get_unique_branches()
payment_types = ['CASH', 'CARD']
transactions = get_normalised_transactions()

# Load environment variables from .env file
load_dotenv()
host_name = os.environ.get("pg_host")
database_name = os.environ.get("pg_db")
user_name = os.environ.get("pg_user")
user_password = os.environ.get("pg_pass")

def setup_db_connection():
    # Establish a connection and create a cursor
    connection = psycopg2.connect(
        host=host_name,
        user=user_name,
        password=user_password,
        database=database_name
    )
    cursor = connection.cursor()
    return connection, cursor


def insert_products_db(products):
    try:
        connection, cursor = setup_db_connection()
        
        # Insert products into the 'products' table
        for product in products:
            sql = """INSERT INTO products (product_name, product_price) VALUES (%s, %s) RETURNING productID"""
            data_values = (product['name'], product['price'])
            
            cursor.execute(sql, data_values)
            # Fetch the last inserted product_id
            product['product_id'] = cursor.fetchone()[0]
            connection.commit()
        
        cursor.close()
        
        return products            
        
    except Exception as ex:
        print('Failed to:', ex)

# Call the function to insert products into the database
products = insert_products_db(products)

def insert_branches_db(branches):
    try:
        connection, cursor = setup_db_connection()
        
        # Insert branches into the 'branch' table
        for branch in branches:
            sql = """INSERT INTO branch (branch_name) VALUES (%s) RETURNING branchID"""
            cursor.execute(sql, (branch['branch_name'],))
            # Fetch the last inserted branch_id
            branch['branch_id'] = cursor.fetchone()[0]
            connection.commit()
        
        cursor.close()
        
        return branches            
        
    except Exception as ex:
        print('Failed to:', ex)

# Call the function to insert branches into the database
branches = insert_branches_db(branches)


def insert_payment_type_db(payment_types):
    try:
        connection, cursor = setup_db_connection()
        
        # Insert payment types into the 'payment_type' table
        for i in range(len(payment_types)):
            sql = """INSERT INTO payment_type (type_name) VALUES (%s) RETURNING payment_typeID"""
            cursor.execute(sql, (payment_types[i],))
            # Fetch the last inserted payment_type_id
            payment_types[i] = {'payment_type_id': cursor.fetchone()[0], 'type_name': payment_types[i]}
            connection.commit()
        
        cursor.close()
        
        return payment_types            
        
    except Exception as ex:
        print('Failed to:', ex)

# Call the function to insert payment types into the database
payment_types = insert_payment_type_db(payment_types)



# Inserting transaction data into the 'transactions' table
def insert_transactions_db(transactions):
    try:
        connection, cursor = setup_db_connection()
        
        for transaction in transactions:
            # Get branch_id and payment_type_id using the fetched values
            branch_id = next(branch['branch_id'] for branch in branches if branch['branch_name'] == transaction['location'])
            payment_type_id = next(type['payment_type_id'] for type in payment_types if type['type_name'] == transaction['payment_type'])
            total_cost = transaction['total']
        
            # Format the date as needed
            date_object = datetime.strptime(transaction['date'], '%d/%m/%Y %H:%M')
            formatted_date = date_object.strftime('%Y-%m-%d %H:%M')
            
            # Insert transaction data into the 'transactions' table
            sql = """INSERT INTO transactions (branchID, payment_typeID, total_cost, order_datetime) VALUES (%s, %s, %s, %s) RETURNING orderID"""
            data = (branch_id, payment_type_id, total_cost, formatted_date)
            cursor.execute(sql, data)
            # Fetch the last inserted order_id
            transaction['order_id'] = cursor.fetchone()[0]
            connection.commit()
            
        cursor.close()
        return transactions
    
    except Exception as ex:
        print('Failed to:', ex)

# Call the function to insert transactions into the database
transactions = insert_transactions_db(transactions)

# Inserting basket data into the 'basket' table
def insert_basket_db(transactions):
    try:
        connection, cursor = setup_db_connection()
        for transaction in transactions:
            order_id = transaction["order_id"]
            for current_product in transaction["basket"]:
                product_id = next(product["product_id"] for product in products if product["name"] == current_product["product"])
                quantity = current_product["quantity"]
                # Insert basket data into the 'basket' table
                sql = """INSERT INTO basket (orderID, productID, quantity) VALUES (%s, %s, %s)"""
                data = (order_id, product_id, quantity)
                cursor.execute(sql, data)
                connection.commit()
        cursor.close()
    except Exception as ex:
        print('Failed to:', ex)

# Call the function to insert basket data into the database
insert_basket_db(transactions)