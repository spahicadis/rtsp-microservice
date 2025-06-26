import cv2
import base64
import threading
import redis
import json

r = redis.Redis(host='192.168.1.100', port=6379, decode_responses=True)

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

        if not ret:
            print("Logika za reconnect")

        self.buffer = base64.b64encode(buffer).decode('utf-8')

        cap.release()
        cv2.destroyAllWindows()

    def get_data(self):
        return {
            "id": self.id,
            "roi": self.roi,
            "capacity": self.capacity,
            "frame": self.buffer,
        }

#Creating stream instances

stream1 = Rtsp("Parking1", "rtsp://192.168.1.71/profile1", [(727.9869067103104, 1262.1931260229123), (866.7757774140747,
          1304.9645390070914), (1018.6579378068733, 1348.608837970539), (1174.0316421167477, 1388.7615930169113), (1400.9819967266767,
          1219.4217130387335), (981.996726677577, 1151.3366066557548)], 3)

stream2 = Rtsp("Parking2", "rtsp://192.168.1.111:1024/h264_ulaw.sdp",  [
    (82.29254740910731, 1265.6601038772787), (367.5443894190116,
          1258.7027418770372), (659.7535934291576, 1253.484720376856),
    (942.1065346056279, 1244.788017876554), (833.6876434351968,
          990.26452470105), (622.6476627612025, 992.5836453677972),
    (409.8683415871479, 995.4825462012312), (199.98792124652718,
          990.8443048677368)
        ], 3)

rtsp_list = [stream1, stream2]

#Reading frames

def read_frames():
    for rtsp in rtsp_list:
        rtsp.get_frame()
        r.set(rtsp.id, json.dumps(rtsp.get_data()))

    threading.Timer(5.0, read_frames).start()




















