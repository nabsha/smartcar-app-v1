import json

from flask import Flask, Response
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import random
import cv2
import plotly.graph_objs as gobs
import smartcar
import psutil
from dash_extensions import Keyboard


external_stylesheets = ['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css']
smartcar = smartcar.SmartCar()

external_scripts = ['https://code.jquery.com/jquery-3.2.1.slim.min.js',
                    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
                    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js']

# Server definition

server = Flask(__name__)
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts,
                server=server)

# HEADER
# ======
#
# header = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Page 1", href="#")),
#         dbc.DropdownMenu(
#             children=[
#                 dbc.DropdownMenuItem("More pages", header=True),
#                 dbc.DropdownMenuItem("Page 2", href="#"),
#                 dbc.DropdownMenuItem("Page 3", href="#"),
#             ],
#             nav=True,
#             in_navbar=True,
#             label="More",
#         ),
#     ],
#     brand="smartcar-app-v1",
#     brand_href="#",
#     color="primary",
#     dark=True
# )


# COMPONENTS
# ==========

# Your components go here.


# INTERACTION
# ===========

# Your interaction goes here.


# APP LAYOUT
# ==========

# app.layout = html.Div(
#     children=[
#         html.H1(children="Avocado Analytics",),
#         html.P(
#             children="Analyze the behavior of avocado prices"
#             " and the number of avocados sold in the US"
#             " between 2015 and 2018",
#         ),
#         html.Img(src="/video_feed"),
#         dcc.Interval(
#             id='battery-interval-component',
#             interval=1 * 1000,  # in milliseconds
#             n_intervals=0
#         ),
#         daq.Gauge(
#             color="red",
#             id='battery-gauge',
#             label="Battery Left",
#             value=65,
#             min=0,
#             max=100,
#             units="Battery",
#         ),
#         daq.Gauge(
#             color="red",
#             id='cpu-gauge',
#             label="CPU %",
#             value=0,
#             min=0,
#             max=100
#         ),
#         daq.Gauge(
#             color="red",
#             id='mem-gauge',
#             label="Mem Util %",
#             value=0,
#             min=0,
#             max=100
#         ),
#     ]
# )


card = dbc.Card(
    [dbc.CardHeader("Header"), dbc.CardBody("Body", style={"height": 250})],
    className="h-100 mt-4",
)

battery_card = dbc.Card(
    [dbc.CardHeader("Battery"),
     dbc.CardBody(daq.Gauge(color="red",
            scale={'start': 5, 'interval': 0.25, 'labelInterval': 1},
            id='battery-gauge',
            label="Battery Left",
            value=7,
            min=5,
            max=9),
            style={"height": 250})],
    className="h-100 mt-4",
)

cpu_card = dbc.Card(
    [dbc.CardHeader("CPU %"),
     dbc.CardBody(daq.Gauge(color="red",
            id='cpu-gauge',
            label="CPU %",
            value=0,
            min=0,
            max=100),
            style={"height": 250})],
    className="h-100 mt-4",
)

mem_card = dbc.Card(
    [dbc.CardHeader("Mem %"),
     dbc.CardBody(daq.Gauge(color="red",
            id='mem-gauge',
            label="CPU %",
            value=0,
            min=0,
            max=100),
            style={"height": 250})],
    className="h-100 mt-4",
)

keypress_card = dbc.Card(
    [dbc.CardHeader("Keypressed"),
     dbc.CardBody([Keyboard(id="keyboard"), html.Div(id="key-pressed")],
            style={"height": 250})],
    className="h-100 mt-4",
)

@app.callback(
    Output("key-pressed", "children"),
    [Input("keyboard", "n_keydowns")],
    [State("keyboard", "keydown")],
)
def keydown(n_keydowns, event):
    if event['key'] == 'Escape':
        smartcar.flush_keypress_events()
    else:
        smartcar.enqueue_keypress_event(event['key'])
    return event['key']







video_feed_card = dbc.Card([dbc.CardHeader("Video Feed"),
                            dbc.CardBody(html.Img(src="/video_feed", width='100%'),style={"height": 250})],
                           className="h-100 mt-4")

ultrasonic_distance_card = dbc.Card(
    [dbc.CardHeader("Distance"),
     dbc.CardBody(daq.GraduatedBar(
            id='ultrasonic-bar',
            label="Default",
            value=6),
        style={"height": 250}),
     ],
    className="h-100 mt-4",
)
graph_card = dbc.Card(dbc.CardBody([dcc.Graph(style={"height": 200})] * 2))

app.layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col([video_feed_card], width=4),
            dbc.Col(
                [
                    dbc.CardDeck([battery_card, cpu_card, mem_card]),
                    dbc.CardDeck([keypress_card, ultrasonic_distance_card, card])
                ],
                width=8,
            ),
            dcc.Interval(
                id='battery-interval-component',
                interval=1 * 1000,  # in milliseconds
                n_intervals=0
            ),
        ]
    ),
    fluid=True,
)

@app.callback (Output('cpu-gauge', 'value'),
              [Input('battery-interval-component', 'n_intervals')])
def update_cpu_usage(value):
    return  psutil.cpu_percent() # randrange(100)


@app.callback (Output('battery-gauge', 'value'),
              [Input('battery-interval-component', 'n_intervals')])
def update_battery_level(value):
    return  smartcar.Power() # randrange(100)

@app.callback (Output('ultrasonic-bar', 'value'),
              [Input('battery-interval-component', 'n_intervals')])
def update_ultrasonic_distance(value):
    return  smartcar.get_ultrasonic_distance()

@app.callback (Output('mem-gauge', 'value'),
              [Input('battery-interval-component', 'n_intervals')])
def update_memory_util(value):
    return  psutil.virtual_memory().percent


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@server.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
#
#
# def random_color():
#     number_of_colors = 1
#
#     color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
#     return  dict(hex=color)
#
# @app.callback (Output('my-color-picker', 'value'),
#               [Input('battery-interval-component', 'n_intervals')])
# def update_color_value(value):
#     return  random_color()


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')