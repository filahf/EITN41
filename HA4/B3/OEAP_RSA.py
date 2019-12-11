from hashlib import sha1
from math import ceil

hLen = 20 #sha1 = 160 bits 160/8=20 => hLen = 20 
k = 128 # RSA = 1024 bit 1024/8=128

def MGF1(mgfSeed, maskLen):
    if(maskLen > 2 ** 32):
        return "Mask to long!"
    T = ""
    for counter in range(0, int(ceil(maskLen/hLen))):
        C = I2OSP(counter, 4)
        T += hash_function(mgfSeed + C)
    return T[:2*maskLen]

def hash_function(input):
    return sha1(bytearray.fromhex(input)).hexdigest()

def I2OSP(x, xLen):
    if(x >= 256 ** xLen ):
        return "integer too large"
    return hex(x)[2:].zfill(2*xLen)

def OAEP_encode(M,seed, L=""):
    # step a
    lHash = sha1(bytearray(L.encode())).hexdigest()
    # step b Generate a padding string PS consisting of k - mLen -2hLen - 2 zero octets.  The length of PS may be zero.
    PS = "".rjust(((k - int(len(M)/2) - 2*hLen) - 2)*2,'0')
    # step c        DB = lHash || PS || 0x01 || M.
    DB = lHash + PS + "01" + M
    #step e
    dbMask = MGF1(seed, k - hLen - 1)
    #step f
    maskedDB = hex(int(DB, 16) ^ int(dbMask, 16))[2:]
    #step g
    seedMask = MGF1(maskedDB, hLen)
    #step h     maskedSeed = seed \xor seedMask
    maskedSeed = hex(int(seed, 16) ^ int(seedMask, 16))[2:]
    #step i     EM = 0x00 || maskedSeed || maskedDB.
    EM = "00" + maskedSeed + maskedDB
    return EM

print(OAEP_encode("fd5507e917ecbe833878","1e652ec152d0bfcd65190ffc604c0933d0423381"))
