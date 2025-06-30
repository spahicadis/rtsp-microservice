import cv2
import threading
import redis
import pika
import json

#Connections
r = redis.Redis(host='192.168.1.100', port=6379, decode_responses=True)
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.100'))
channel = connection.channel()
channel.queue_declare(queue="rtsp_microservice", durable=True)

#Class for stream objects
class Rtsp:
    def __init__(self, rtsp_id, rtsp_url, rtsp_roi, capacity):
        self.id = rtsp_id
        self.rtsp = rtsp_url
        self.roi = rtsp_roi
        self.capacity = capacity
        self.buffer = None

    def get_frame(self):
        cap = cv2.VideoCapture(self.rtsp)

        if not cap.isOpened():
            print("Logika za reconnect")

        ret, frame = cap.read()

        if not ret:
            print("Logika za reconnect")

        ret, buffer = cv2.imencode('.jpg', frame)

        jpg_bytes = buffer.tobytes()

        if not ret:
            print("Logika za reconnect")

        channel.basic_publish(exchange='', routing_key='rtsp_microservice', body=jpg_bytes, properties=pika.BasicProperties(
            headers={
                'id': self.id,
                'roi': json.dumps(self.roi),
                'capacity': self.capacity,
            }
        ))

        cap.release()

#Creating Rtsp (stream) instances

stream1 = Rtsp("Parking1", "rtsp://192.168.1.71/profile1", [(785.5973813420617, 1285.7610474631742), (912.1658483360604,
          1323.2951445717395), (1062.302236770321, 1365.1936715766494), (1247.3540643753402, 1412.329514457173), (1462.0840152755036,
          1237.7523186033816), (1297.9814511729396, 1216.8030551009267), (1156.5739225313685, 1195.8537915984716), (1033.4969994544456,
          1173.1587561374788)], 3)

stream2 = Rtsp("Parking2", "rtsp://192.168.1.111:1024/h264_ulaw.sdp",  [(60.826032540675804, 1564.5572590738411), (365.3785982478095,
          1555.2643929912379), (668.2415519399244, 1548.505944931163), (963.0788485607002, 1537.1010638297862), (840.5819774718392,
          1265.0735294117637), (625.5788485607004, 1264.651126408009), (409.7309136420523, 1268.0303504380468), (192.61576971214004,
          1274.7887984981217)], 3)

rtsp_list = [stream1, stream2]

#Reading frames
def read_frames():
    for rtsp in rtsp_list:
        rtsp.get_frame()

    threading.Timer(5.0, read_frames).start()


if __name__ == "__main__":
    read_frames()




















