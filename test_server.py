from flask import Flask, Response
import threading
from frs import FRS
import os
import time
from collections import deque
from turbojpeg import TurboJPEG

class Testing():
    def __init__(self):
        super()
        self.fingerprint = FRS()
        self.jpeg = TurboJPEG()
        self.frame_queue = deque(maxlen=1)
        self.frame_queue.append('processing.jpg')

        web_server_thread = threading.Thread(target=self.create_web_server, args=())
        web_server_thread.name = 'Web Server Process'
        web_server_thread.start()

        self.process_video()

    def process_video(self, ):
        self.fingerprint.process_frame("msdv.mp4", self.frame_queue)

    def pump_frame(self, ):
        while True:
            if self.frame_queue is not None:
                frame = self.frame_queue[-1]
                if frame is not None:
                    encodedImage = self.jpeg.encode(frame)
                    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                        bytearray(encodedImage) + b'\r\n')
                    time.sleep(.3)

    def create_web_server(self, ):
        from flask_cors import CORS
        from waitress import serve
        app = Flask(__name__,static_folder=os.path.abspath("static/"))
        CORS(app)

        @app.after_request
        def add_header(r):
            r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            r.headers["Pragma"] = "no-cache"
            r.headers["Expires"] = "0"
            r.headers['Cache-Control'] = 'public, max-age=0'
            return r

        @app.route('/video_feed/')
        def video_feed():
            try:
                return Response(self.pump_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
            except Exception as e:
                print(e)
        
        try:
            serve(app, host='0.0.0.0', port=9000, threads=15) 
        except Exception as e:
            print(e)

Testing()