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


sched_type = 'FIFO'   # FIFO/FAIR


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

        self.free_nodes = set()
        self.taskid_nodeid = {}

        self.cur_tasks = []
        self.next_task_id = 1

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
        self.free_nodes.add(id)
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
        index = self.free_nodes.pop()

        ip = self.nodes[index].getIp()
        port = self.nodes[index].getPort()
        print(ip, port)
        return ip, port,index

    # def scheduler(self, task_type, task_sz):
    #     next_index = -1
    #     wt = 0
    #     for id in self.nodes_vals.keys():
    #         if self.nodes_vals[id] > wt:
    #             next_index = id
    #             wt = self.nodes_vals[id]
    #     if next_index == -1:
    #         for id in self.nodes_vals.keys():
    #             self.nodes_vals[id] = self.nodes_weights[id]
    #         return self.scheduler(task_type, task_sz)
    #     self.nodes_vals[next_index] -= 1
    #
    #     index = self.node_ids[next_index]
    #     ip = self.nodes[index].getIp()
    #     port = self.nodes[index].getPort()
    #     print(ip, port)
    #     return ip, port
        
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
        print("available nodes num = ", len(self.ms.free_nodes))
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

    # make weight high node to front
    def add_task_by_weight(self,task):
        l = len(self.ms.cur_tasks)
        t = 0
        for i in range(l-1,-1,-1):
            if(task[1]>self.ms.cur_tasks[i][1]):
                t = i
            else:
                break
        self.ms.cur_tasks.insert(t,task)
        return

    # send target server info to client
    def RouteGuide(self, request, context):
        # if self.ms.getNodesNum() == 0:
        #     return master_pb2.RouteReply(ip = "", port = 555, thread_num = 2)
        # print("available nodes num = ", len(self.ms.free_nodes))
        flag = request.task_id    # 0 request ,1 task finish

        if flag == 1 :
            task__id = request.task_type
            node_id = self.ms.taskid_nodeid[task__id]

            self.ms.free_nodes.add(node_id)
            print("task=",task__id,"is finished,now free server nums =",self.ms.free_nodes)
            return master_pb2.RouteReply(ip="true", port=0)
        else:

            task_type = request.task_type
            task_sz = request.task_sz
            task_id = self.ms.next_task_id

            self.ms.next_task_id += 1
            print("cur task is task id = ", task_id,", weight = ", task_sz)
            if (len(self.ms.free_nodes) > 0):
                next_ip, next_port,nodeid = self.ms.scheduler(task_type, task_sz)
                self.ms.taskid_nodeid[task_id] = nodeid
            else:
                if sched_type == 'FIFO':
                    self.ms.cur_tasks.append([task_id,task_sz])
                else:
                    self.add_task_by_weight([task_id,task_sz])
                print("Waiting : no available server ,add to the task queue...")
                while True:
                    if len(self.ms.free_nodes) > 0:
                        if self.ms.cur_tasks[0][0] == task_id:
                            next_ip, next_port, nodeid = self.ms.scheduler(task_type, task_sz)
                            self.ms.cur_tasks.pop(0)
                            self.ms.taskid_nodeid[task_id] = nodeid
                            break
                    time.sleep(2)   # wait for available nodes

            print("task id = ", task_id,", weight = ", task_sz," schedle to", next_ip, next_port)
            return master_pb2.RouteReply(ip = next_ip, port = task_id)

    def getQ(self):
        return self.ms.getQueue()

if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
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