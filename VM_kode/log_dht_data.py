### nået til 2:30:23
import sqlite3
import json
from datetime import datetime, timedelta
import paho.mqtt.subscribe as subscribe


def create_table():
    query = """CREATE TABLE IF NOT EXISTS mark (
               datetime TEXT NOT NULL,
               temperature REAL NOT NULL,
               humidity REAL NOT NULL,
               moisture REAL NOT NULL,
               batteri REAL NOT NULL
               );""" 
    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except sqlite3.Error as sql_e:
        print(f'sqlite error ocurred {sql_e}')
    except Exception as e:
        print(f"Error occurrred {e}")
    finally:
        conn.close()
    


create_table()

def on_message_print(client, userdata, message):
    query="""INSERT INTO mark (datetime, temperature, humidity, moisture, batteri) VALUES (?,?,?,?,?)""" 

    now = datetime.utcnow()+timedelta(hours=1)
    now = now.strftime("%d/%m/%y %H:%M:%S")

    payload = message.payload.decode()
    payload_split = payload.split(",") 
    data = (now, payload_split[0], payload_split[1], payload_split[2], payload_split[3])# add split[3] for batteri

    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
    except sqlite3.Error as sql_e:
        print(f'sqlite error ocurred {sql_e}')
        conn.rollback()
    except Exception as e:
        print(f"Error occurrred {e}")
    finally:
        conn.close()

subscribe.callback(on_message_print, "markdata/", hostname="20.93.112.153", userdata={"message_count": 0})
