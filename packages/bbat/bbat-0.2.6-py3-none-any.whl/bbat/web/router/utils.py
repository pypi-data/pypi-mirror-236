


def success(data, msg="success"):
    return {"code": 0, "data": data, "msg": msg}

def error(msg="error"):
    return {"code": -1, "data": {}, "msg": msg}
