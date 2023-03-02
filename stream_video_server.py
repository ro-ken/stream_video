import asyncio
import grpc
import stream_video_pb2
import stream_video_pb2_grpc

import master_pb2
import master_pb2_grpc
import random
import numpy as np
from cv2 import cv2 as cv 

master_addr = 'localhost:50051'
this_server_ip = 'localhost'

def get_rand():
    return random.randint(0, 55555)

class VideoStreamServicer(stream_video_pb2_grpc.VideoStreamServicer):
    def __init__(self):
        self.loadModel()
    def loadModel(self):
        self.faceCascade = cv.CascadeClassifier("Image/haarcascade_frontalface_default.xml")

    def SendFream(self, request, context):
        nparr = np.frombuffer(request.fream, np.uint8)
        img = cv.imdecode(nparr, cv.IMREAD_COLOR)
        imgResise = cv.resize(img, (500,400))
        imgGray = cv.cvtColor(imgResise, cv.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(imgResise, 1.1, 4)
        for (x, y, w, h) in faces:
            cv.rectangle(imgResise, (x, y), (x + w, y + h), (255, 0, 0), 1)
        
        return stream_video_pb2.Result()
        
    def PushStream(self, request_iterator, context):
        for fream in request_iterator:
            print(fream.size)
        return stream_video_pb2.Result()
    
    async def PushAndPull(self, request_iterator, unused_context):
        async for req in request_iterator:
            nparr = np.frombuffer(req.fream, np.uint8)
            img = cv.imdecode(nparr, cv.IMREAD_COLOR)
            imgResise = cv.resize(img, (500,400))
            imgGray = cv.cvtColor(imgResise, cv.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(imgResise, 1.1, 4)
            for (x, y, w, h) in faces:
                cv.rectangle(imgResise, (x, y), (x + w, y + h), (255, 0, 0), 1)
            img_encode = cv.imencode('.jpg', imgResise)[1].tobytes()
            data_encode = np.array(img_encode)
            str_encode = data_encode.tobytes()
            yield stream_video_pb2.Fream(size = len(str_encode), fream = str_encode)

    def FaceDetection(self, request_iterator, context):
        ri = get_rand()
        print("----first task arrived----")
        for req in request_iterator:
            nparr = np.frombuffer(req.frame, np.uint8)
            img = cv.imdecode(nparr, cv.IMREAD_COLOR)
            imgResise = cv.resize(img, (500,400))
            imgGray = cv.cvtColor(imgResise, cv.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(imgResise, 1.1, 4)
            for (x, y, w, h) in faces:
                cv.rectangle(imgResise, (x, y), (x + w, y + h), (255, 0, 0), 1)
            cv.imshow('FaceDetection{}'.format(ri), imgResise)
            cv.waitKey(1)
        cv.destroyAllWindows()
        return stream_video_pb2.Result()
    def Canny(self, request_iterator, context):
        print("----second task arrived----")
        count = 0
        for req in request_iterator:
            nparr = np.frombuffer(req.frame, np.uint8)
            img = cv.imdecode(nparr, cv.IMREAD_COLOR)
            blur = cv.GaussianBlur(img, (3, 3), 0)  
            canny = cv.Canny(blur, 50, 150)  
            # cv.imshow('Canny', canny)
            # cv.waitKey(1)
            count = count + 1
            if count % 100 == 0:
                print("second task is running now frame is: {}".format(count))
        cv.destroyAllWindows()
        return stream_video_pb2.Result()

async def push_state(stub, id):
    await stub.PushState(master_pb2.StateRequest(id = id, cpu_usage = 50))

async def join(ip, port, stub, wt):
    res = await stub.Join(master_pb2.JoinRequest(ip = ip,port = port, weight = wt))
    return res.id
# 1. join to the cluster and send local ip and port to the master
async def heartBeatTimer(ip, port, weight):
    # insecure_channel build a channel with master
    async with grpc.aio.insecure_channel(master_addr) as channel:
        stub = master_pb2_grpc.MasterStub(channel)
        # rpc, join to the cluster
        id = await join(ip, port, stub, weight) 
    while True:
        await asyncio.sleep(5)
        # heart message
        async with grpc.aio.insecure_channel(master_addr) as channel:
            stub = master_pb2_grpc.MasterStub(channel)
            await push_state(stub, id)        



async def serve() -> None:
    server = grpc.aio.server()
    stream_video_pb2_grpc.add_VideoStreamServicer_to_server(
                                    VideoStreamServicer(), server)
    server.add_insecure_port('[::]:50050')
    await server.start()
    await server.wait_for_termination()



async def main(ip, port, weight):
    await asyncio.gather(
        heartBeatTimer(ip, port, weight),
        serve()
    )

if __name__ == "__main__":
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    # service = StreamService()
    # service.loadModel()
    # stream_video_pb2_grpc.add_VideoStreamServicer_to_server(service, server)  
    # server.add_insecure_port('[::]:50051')
    # server.start()
    
    # try:
    #     while True:
    #         time.sleep(60*60*24) 
    # except KeyboardInterrupt:
    #     server.stop(0)
    # asyncio.get_event_loop().run_until_complete(serve())
    
    # server local ip and port
    asyncio.run(main(this_server_ip, 50050, 2))
