from concurrent import futures
import time
import grpc
import master_pb2
import master_pb2_grpc
from multiprocessing import Process, Manager
import queue
import json
from node import Node
import sys




def recordHeartBeat(q, file):
    with open(file, 'w') as f:
        while True:
            data = q.get()
            print("writing")
            data_str = json.dumps(data)
            f.write(data_str + "\n")
            f.flush()

class Master():
    def __init__(self):
        self.nodes = {}
        self.nodes_weights = {}
        self.nodes_vals = {}
        self.last_index = 0
        self.node_ids = []
        self.recodQ = Manager().Queue()
        

    def getQueue(self):
        return self.recodQ

    def generateID(self, ip, port):
        return len(self.node_ids)

    def join(self, ip, port, weight):
        id = self.generateID(ip, port)
        if id in self.nodes:
            return False
        self.nodes[id] = Node(ip, port)
        self.nodes_weights[id] = weight
        self.nodes_vals[id] = weight
        self.node_ids.append(id)
        return id, True
    def leave(self, id):
        if id not in self.nodes:
            return False
        self.nodes.pop(id)
        return True

    def updateInfo(self, id, info):
        if id not in self.nodes:
            print("invalid ")
            return False
        self.recodQ.put(info)
        self.nodes[id].update(info)
        return True

    def scheduler(self, task_type, task_sz):
        next_index = -1
        wt = 0
        for id in self.nodes_vals.keys():
            if self.nodes_vals[id] > wt:
                next_index = id
                wt = self.nodes_vals[id]
        if next_index == -1:
            for id in self.nodes_vals.keys():
                self.nodes_vals[id] = self.nodes_weights[id]
            return self.scheduler(task_type, task_sz)
        self.nodes_vals[next_index] -= 1

        index = self.node_ids[next_index]
        ip = self.nodes[index].getIp()
        port = self.nodes[index].getPort()
        print(ip, port)
        return ip, port
        
    def getNodesNum(self):
        return len(self.nodes)
class MasterService(master_pb2_grpc.MasterServicer):
    ms = Master()
    # worker node join to the cluster
    # send the server port and ip to master
    def Join(self, request, context):
        ip = request.ip
        port = request.port
        weight = request.weight
        print("new join ",ip, port)
        id, res = self.ms.join(ip, port, weight)
        print("join id is ", id)
        return master_pb2.JoinReply(id = id,success = res)
        
    def Leave(self, request, context):
        id = request.id
        res = self.ms.leave(id)
        return master_pb2.LeaveReply(res)

    def PushState(self, request, context):
        id = request.id
        print("heartbeat id is ", id)
        info = {}
        info['id'] = request.id
        info['utx'] = request.utx
        info['cpu_usage'] = request.cpu_usage
        info['task_id'] = request.task_id
        info['io_perf'] = request.io_perf
        info['pro_perf'] = request.pro_perf
        info['task_st'] = request.task_st
        info['task_ed'] = request.task_ed
        
        # if request.task_st != 0:
            # print(request.task_id, request.io_perf, request.pro_perf, request.task_st, request.task_ed)
        # else:
            # print(id, request.utx ,request.cpu_usage)
        # print(id, request.io_perf, request.pro_perf)
        self.ms.updateInfo(id, info)
        return master_pb2.SateReply()  
    
    # send target server info to client
    def RouteGuide(self, request, context):
        if self.ms.getNodesNum() == 0:
            return master_pb2.RouteReply(ip = "", port = 555, thread_num = 2)
        print("nodes num = ", self.ms.getNodesNum())
        task_type = request.task_type
        task_sz = request.task_sz
        print("cur task is", task_type, task_sz)
        next_ip, next_port = self.ms.scheduler(task_type, task_sz)
        print("schedle ", next_ip, next_port)
        return master_pb2.RouteReply(ip = next_ip, port = next_port)

    def getQ(self):
        return self.ms.getQueue()

if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    service = MasterService()
    master_pb2_grpc.add_MasterServicer_to_server(service, server)
    #bind a port 
    server.add_insecure_port('[::]:50051')
    server.start()
    recordP = Process(target = recordHeartBeat, args = (service.getQ(), "heartbeat"))
    recordP.start()
    try:
        while True:
            time.sleep(60*60*24) 
    except KeyboardInterrupt:
        server.stop(0)