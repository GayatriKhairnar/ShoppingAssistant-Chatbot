import mysql.connector
global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="50Shades@",
    database="pandeyji_eatery"
)

# Function to call the MySQL stored procedure and insert an order item
def get_order_status(order_id):
    cursor = cnx.cursor()

    # Executing the SQL query to fetch the order status
    query = "SELECT status FROM order_tracking WHERE order_id = %s"
    cursor.execute(query, (order_id,))

    # Fetching the result
    result = cursor.fetchone()
    print(result)
    # Closing the cursor
    cursor.close()

    # Returning the order status
    if result:
        return result[0]
    else:
        return None
# get_order_status(40)

def get_next_order_id():
    cursor = cnx.cursor()

    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    result = cursor.fetchone()[0]
    cursor.close()

    if result is None:
        return 1
    else:
        return result+1
    
def insert_order_item(food_items,quantity, order_id):
    try:
        cursor=cnx.cursor()

        cursor.callproc('insert_order_item',(food_items,quantity,order_id))

        cnx.commit()
        cursor.close()

        print("Order item inserted successfully!")

        return 1
    
    except mysql.connector.Error as err:
        print(f"Erro inserting order item:{err}")
        cnx.rollback()
        return -1
    
    except Exception as e:
        print(f"An error occured:{e}")

        cnx.rollback()
        return -1
    
def get_total_order_price(order_id):
    cursor = cnx.cursor()
    query = "SELECT get_total_order_price(%s)"
    cursor.execute(query,(order_id,))

    result = cursor.fetchone()[0]
    cursor.close()
    return result

def insert_order_tracking(order_id, status):
    cursor=cnx.cursor()
    insert_query= "INSERT INTO order_tracking(order_id,status) VALUES (%s,%s)"

    cursor.execute(insert_query,(order_id,status))
    cnx.commit()
    cursor.close()



