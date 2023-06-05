from deepface import DeepFace
from pymongo import MongoClient
from scipy.spatial.distance import cosine
import cv2
from csv import writer, reader
import json

class FRS():
    def __init__(self):
        super()
        # self.frame_queue = frame_queue
        # cluster = MongoClient("mongodb+srv://frs:frs@frs.m4mcj4c.mongodb.net/?retryWrites=true&w=majority")
        # db = cluster["fingerprint"]
        # self.collection = db["fingerprint"]
        pass

    def process_face(self,image):
        # "VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"
        embedding_objs = DeepFace.represent(img_path = image, model_name = "Facenet512", enforce_detection = False)
        embedding = embedding_objs[0]["embedding"]
        tag = image[7:-4]
        # self.collection.insert_one({"fp":embedding,"tag":tag})
        with open('embeddings.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow([tag,embedding])
            f_object.close()
        # print(embedding)
        # print(image[7:-4])
        # dfs = DeepFace.find(img_path = image, db_path = "/home/kloudspot/Downloads/CricketLegends/adam_gilchrist/", model_name = "Facenet512")
        # print(dfs)

    def find_face(self,image):
        embedding_objs = DeepFace.represent(img_path = image, model_name = "Facenet512", enforce_detection = False)
        embedding = embedding_objs[0]["embedding"]
        # current_db = self.collection.find()
        with open('embeddings.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for face in csv_reader:
                simi = 1 - cosine(embedding,json.loads(face[1]))
                # print(simi)
                if simi >= 0.6:
                    read_obj.close()
                    return "found face "+face[0]
            read_obj.close()
        return ""

    def process_frame(self,video_path, frame_queue):
        cap = cv2.VideoCapture(video_path)
        count = 0
        while cap.isOpened():
            if count % 5 == 0:
                ret, frame = cap.read()
                embedding_objs = DeepFace.represent(img_path = frame, model_name = "Facenet512", enforce_detection = False)
                embedding = embedding_objs[0]["embedding"]
                xmin = embedding_objs[0]['facial_area']['x']
                ymin = embedding_objs[0]['facial_area']['y']
                xmax = embedding_objs[0]['facial_area']['w'] + xmin
                ymax = embedding_objs[0]['facial_area']['h'] + ymin
                face_found = 0
                with open('embeddings.csv', 'r') as read_obj:
                    csv_reader = reader(read_obj)
                    for face in csv_reader:
                        # print(face)
                        simi = 1 - cosine(embedding,json.loads(face[1]))
                        # print(simi)
                        if simi >= 0.6:
                            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
                            frame_queue.append(frame)
                            face_found = 1
                            break
                if not face_found:
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                    frame_queue.append(frame)
                # print(count)
            count += 1

            

# frs = FRS()
# frs.process_face("/home/kloudspot/Downloads/CricketLegends/adam_gilchrist/adam_gilchrist2841.jpg")