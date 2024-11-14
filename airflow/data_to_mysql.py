import pandas as pd
import mysql.connector
from sklearn.datasets import fetch_california_housing

# Fetch the California Housing dataset
data = fetch_california_housing()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

# Connect to MySQL
connection = mysql.connector.connect(
    host='localhost',
    user='mluser',
    password='mlpassword',
    database='housing_db'
)
cursor = connection.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS housing_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        MedInc FLOAT, HouseAge FLOAT, AveRooms FLOAT, AveBedrms FLOAT,
        Population FLOAT, AveOccup FLOAT, Latitude FLOAT, Longitude FLOAT, target FLOAT
    )
''')

# Insert data into MySQL
for _, row in df.iterrows():
    cursor.execute('''
        INSERT INTO housing_data (MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude, target)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', tuple(row))
connection.commit()

print("Data inserted into MySQL successfully.")

# Close connection
cursor.close()
connection.close()