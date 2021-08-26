# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import cv2
import numpy as np
#
# PAGE="""\
# <html>
# <head>
# <title>Raspberry Pi - Surveillance Camera</title>
# </head>
# <body>
# <center><h1>Raspberry Pi - Surveillance Camera</h1></center>
# <center><img src="stream.mjpg" width="640" height="480"></center>
# </body>
# </html>
# """
#

# class StreamingHandler(server.BaseHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/':
#             self.send_response(301)
#             self.send_header('Location', '/index.html')
#             self.end_headers()
#         elif self.path == '/index.html':
#             content = PAGE.encode('utf-8')
#             self.send_response(200)
#             self.send_header('Content-Type', 'text/html')
#             self.send_header('Content-Length', len(content))
#             self.end_headers()
#             self.wfile.write(content)
#         elif self.path == '/stream.mjpg':
#             self.send_response(200)
#             self.send_header('Age', 0)
#             self.send_header('Cache-Control', 'no-cache, private')
#             self.send_header('Pragma', 'no-cache')
#             self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
#             self.end_headers()
#             try:
#                 while True:
#                     with output.condition:
#                         output.condition.wait()
#                         frame = output.frame
#                     self.wfile.write(b'--FRAME\r\n')
#                     self.send_header('Content-Type', 'image/jpeg')
#                     self.send_header('Content-Length', len(frame))
#                     self.end_headers()
#                     self.wfile.write(frame)
#                     self.wfile.write(b'\r\n')
#             except Exception as e:
#                 logging.warning(
#                     'Removed streaming client %s: %s',
#                     self.client_address, str(e))
#         else:
#             self.send_error(404)
#             self.end_headers()
#
# class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
#     allow_reuse_address = True
#     daemon_threads = True
#
#
# def start_camera():
#     global output, server
#     with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
#         output = StreamingOutput()
#         # Uncomment the next line to change your Pi's Camera rotation (in degrees)
#         # camera.rotation = 90
#         camera.start_recording(output, format='mjpeg')
#         try:
#             address = ('', 8000)
#             server = StreamingServer(address, StreamingHandler)
#             server.serve_forever()
#         finally:
#             camera.stop_recording()
#             camera.close()
#
# class StreamingOutput(object):
#     def __init__(self):
#         self.frame = None
#         self.buffer = io.BytesIO()
#         self.condition = Condition()
#
#     def write(self, buf):
#         if buf.startswith(b'\xff\xd8'):
#             # New frame, copy the existing buffer's content and notify all
#             # clients it's available
#             self.buffer.truncate()
#             with self.condition:
#                 self.frame = self.buffer.getvalue()
#                 self.condition.notify_all()
#             self.buffer.seek(0)
#         return self.buffer.write(buf)
#
# def gen():
#     # global output
#     stream = io.BytesIO()
#     with picamera.PiCamera(resolution='640x480', framerate=12) as camera:
#         # output = StreamingOutput()
#         # Uncomment the next line to change your Pi's Camera rotation (in degrees)
#         # camera.rotation = 90
#         # camera.start_recording(output, format='mjpeg')
#         camera.start_preview()
#
#         while True:
#             time.sleep(2)
#             camera.capture(stream, format='bgr')
#             # data = np.fromstring(stream.getvalue(), dtype=np.uint8)
#             # "Decode" the image from the array, preserving colour
#             # image = cv2.imdecode(data, 1)
#             image = stream.array
#             frame = image #.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

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

#
# if __name__=='__main__':
#     start_camera()
#
