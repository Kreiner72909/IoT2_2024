import sqlite3
from datetime import datetime
from time import sleep

def get_mark_data(number_of_rows):
        query="""SELECT * FROM mark ORDER BY datetime DESC; """ 
        datetimes = []
        temperature = []
        humidities = []
        moisture = []
        batteri = []
        try:
            conn = sqlite3.connect("database/sensor_data.db")
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchmany(number_of_rows)
            for row in reversed(rows):
                 datetimes.append(row[0])
                 temperature.append(row[1])
                 humidities.append(row[2])
                 moisture.append(row[3])
                 batteri.append(row[4])
            return datetimes, temperature, humidities, moisture, batteri

        except sqlite3.Error as sql_e:
            print(f'sqlite error ocurred {sql_e}')
            conn.rollback()

        except Exception as e:
            print(f"Error occurrred {e}")

        finally:
            conn.close()

get_mark_data(10)