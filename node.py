class Node:
    ip_ = ""
    port_ = 0
    info_ = {}
    def __init__(self, ip, port):
        self.ip_ = ip
        self.port_ = port

    def getIp(self):
        return self.ip_

    def getPort(self):
        return self.port_


    def update(self, info):
        self.info_ = info
