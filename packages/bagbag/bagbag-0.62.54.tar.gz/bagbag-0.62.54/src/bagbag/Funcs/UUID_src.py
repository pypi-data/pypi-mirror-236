import shortuuid

#print("load " + __file__.split('/')[-1])

def UUID() -> str:
    return shortuuid.uuid()

    