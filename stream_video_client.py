import numpy as np

import stream_video_pb2
import stream_video_pb2_grpc

import master_pb2
import master_pb2_grpc

import grpc
import json
import random
import cv2 as cv
import asyncio


vedio_path = "test.mp4"

def getTaskID():
    return random.randint(0,100)


def prepareCap():
    frameWidth = 640
    frameHight = 480
    #to do change the path to the real mp4 file 
    cap = cv.VideoCapture(vedio_path)
    cap.set(3,frameWidth)
    cap.set(4,frameHight)
    cap.set(10,130)
    return cap

def generate_frame(cap, count):
    for _ in range(count):
        ret, img = cap.read()
        if not ret:
            print("read error ")
            continue
        img_encode = cv.imencode('.jpg', img)[1].tobytes()
        data_encode = np.array(img_encode)
        str_encode = data_encode.tobytes()
        sz = len(str_encode)
        yield stream_video_pb2.Fream(size = sz, fream = str_encode)


async def face_detection(stub_, count):
    cap = prepareCap()
    frame_iteartor = generate_frame(cap, count)
    result = await stub_.FaceDetection(frame_iteartor)
    return result

async def canny(stub_, count):
    cap = prepareCap()
    frame_iteartor = generate_frame(cap, count)
    result = await stub_.Canny(frame_iteartor)
    return result



async def find_server(stub):
    # task_sz is the weight of the task
    # task id  = 0 request server ; =1 finish the task
    res = await stub.RouteGuide(master_pb2.RouteRequest(task_id = 0, task_sz = 10000, task_type = 50))
    return res.ip, res.port

async def main() -> None:
    #build a channel with master
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = master_pb2_grpc.MasterStub(channel)
        ip, task_id = await find_server(stub)
        # port is task id
    print(ip, task_id)
    # build a channel with worker
    async with grpc.aio.insecure_channel(str(ip) + ":" + str(50050)) as channel:
        stub = stream_video_pb2_grpc.VideoStreamStub(channel)
        # await push_stream(stub, 10000)
        await face_detection(stub, 100000)

    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = master_pb2_grpc.MasterStub(channel)
        await stub.RouteGuide(master_pb2.RouteRequest(task_id=1, task_sz=0, task_type=task_id))
    # told master task id finished

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())