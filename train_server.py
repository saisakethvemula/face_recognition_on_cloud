from flask import Flask, render_template, request, render_template_string, jsonify
import threading
from frs import FRS
import os
import time

class Training():
    def __init__(self):
        super()
        self.fingerprint = FRS()

        web_server_thread = threading.Thread(target=self.create_web_server, args=())
        web_server_thread.name = 'Web Server Process'
        web_server_thread.start()

        fp_thread = threading.Thread(target=self.train_faces())
        fp_thread.name = 'Fingerprint process'
        fp_thread.start()

    def train_faces(self,):
        if not os.path.isdir("images"):
            os.makedirs("images")
        while True:
            images = os.listdir("images/")
            if len(images) == 0:
                time.sleep(2)
                continue
            for image in images:
                self.fingerprint.process_face("images/"+image)
                os.remove("images/"+image)

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

        @app.route('/')
        def main():
            return render_template('fakeui.html')

        @app.route('/train', methods=['POST'])
        def get_image():
            tag = request.form["face_tag"]
            file = request.files['image']
            file.save(os.getcwd()+"/images/"+tag+".jpg")
            # self.fingerprint.process_face("images/"+tag+".jpg")
            # return render_template('fakeui.html')
            return jsonify({'msg':'training is progress'})

        @app.route('/identify', methods=['POST'])
        def identify_face():
            file = request.files['image']
            file.save(os.getcwd()+"/identify.jpg")
            res = self.fingerprint.find_face("identify.jpg")
            return jsonify({'msg': res})
            html = render_template_string(open("templates/alert.html").read(), input=res)
            return html

        try:
            serve(app, host='0.0.0.0', port=8888,threads=15) 
        except Exception as e:
            print(e)

Training()
