import rsa


def newKey(lens: int = 512) -> tuple[rsa.PublicKey,rsa.PrivateKey]:
    (pubkey, privkey) = rsa.newkeys(lens)
    return (pubkey, privkey)


def encrypt(pubkey, msg: str):
    return rsa.encrypt(msg.encode('utf-8'), pubkey)


def decrypt(privkey, msg):
    return rsa.decrypt(msg, privkey).decode('utf-8')


def newKeyToFile(lens: int = 512, pubkey:str="pubkey.txt", privkey:str="privkey.txt"):
    (pubkeys, privkeys) = newKey(lens)
    with open(pubkey, 'wb') as f:
        f.write(pubkeys.save_pkcs1())
    with open(privkey, 'wb') as f:
        f.write(privkeys.save_pkcs1())
