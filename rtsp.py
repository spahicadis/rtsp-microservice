import cv2
import threading
import pika
import json

#Connections
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

stream1 = Rtsp("Parking1", "rtsp://192.168.1.71/profile1", [(838.2322713257961, 1218.293936279547), (616.2384378211713,
          1358.0678314491256), (743.6793422404929, 1381.0894141829385), (895.7862281603284, 1404.1109969167517), (1079.958890030832,
          1430.4213771839663), (1269.8869475847887, 1230.6269270298042), (1103.8026721479953, 1228.1603288797528), (964.0287769784168,
          1224.0493319630004)], 3)

stream2 = Rtsp("Parking2", "rtsp://192.168.1.119:1024/h264_ulaw.sdp",  [(200.9510026876162, 346.9919371511266), (321.5216043001859,
          344.5110605747363), (441.5960305974776, 342.526359313624), (563.6551581558815, 340.54165805251176), (508.08352284473824,
          265.1230101302459), (422.74136861691113, 266.11536076080205), (338.3915650196401, 266.6115360760801), (256.5226379987594,
          265.1230101302459)], 3)

rtsp_list = [stream1, stream2]

#Reading frames
def read_frames():
    for rtsp in rtsp_list:
        rtsp.get_frame()

    threading.Timer(5.0, read_frames).start()


if __name__ == "__main__":
    read_frames()




















