import msgpack

def dumpServerData(header:dict={},data:bytes=b"",code:int=1):
    datas = {
        "headers": header,
        "data": data,
        "code": code
    }
    return msgpack.packb(datas, use_bin_type=True)

def dumpClientData(path:str,headers:dict,data:bytes):
    datas = {
        "path": path,
        "headers": headers,
        "data": data
    }
    return msgpack.packb(datas, use_bin_type=True)

def loadServerData(data:bytes):
    datas = msgpack.unpackb(data, raw=False)
    return datas

def loadClientData(data:bytes):
    datas = msgpack.unpackb(data, raw=False)
    return datas