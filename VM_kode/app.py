import base64
from io import BytesIO
from matplotlib.figure import Figure
from flask import Flask, render_template
from get_mark_dht11 import get_mark_data
import paho.mqtt.publish as publish

app = Flask(__name__)      # app får nemmere ved at finde ud af hvor resourcer er på systemet og kan nemmere tilgås

def mark_temp():
    timestamps, temp, hum, moisture, batteri= get_mark_data(10)
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which="both", rotation=30)
    ax.set_facecolor("#000")
    ax.plot(timestamps, temp)
    ax.set_xlabel("timestamps")
    ax.set_ylabel("Temp i cels")
    fig.patch.set_facecolor("#fff")
    ax.tick_params(axis="x", colors="black")
    ax.tick_params(axis="y", colors="blue")
    ax.spines["left"].set_color("blue")
    ax.spines["right"].set_color("blue")
    ax.spines["top"].set_color("blue")
    ax.spines["bottom"].set_color("blue")
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def mark_hum():
    timestamps, temp, hum, moisture, batteri= get_mark_data(10)
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which="both", rotation=30)
    ax.set_facecolor("#3539")
    ax.plot(timestamps, hum, linestyle="dotted", c="#f11", linewidth="1.5", marker="o", mec="blue") # tjek matplotlib for flere styles osv.
    ax.set_xlabel("timestamps")
    ax.set_ylabel("humidity %")
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def mark_moist():
    timestamps, temp, hum, moist, batteri= get_mark_data(10)
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which="both", rotation=30)
    ax.set_facecolor("#3539")
    ax.plot(timestamps, moist, linestyle="dotted", c="#f11", linewidth="1.5", marker="o", mec="blue") # tjek matplotlib for flere styles osv.
    ax.set_xlabel("timestamps")
    ax.set_ylabel("moisture %")
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def mark_batteri():
    timestamps, temp, hum, moist, batteri = get_mark_data(1)
    data = batteri
    data = str(data).strip("[]")
    return data
    

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/mark')
def mark():
    mark_temperature = mark_temp()
    mark_humidity = mark_hum()
    mark_moisture = mark_moist()
    data = mark_batteri()
    return render_template('mark.html', mark_temperature = mark_temperature, mark_humidity = mark_humidity, mark_moisture = mark_moisture, data = data)

app.run(debug=True)            # denne funktion genstarter vores flask.py hvergang vi har lavet ændringer

