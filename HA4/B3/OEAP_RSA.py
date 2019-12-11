from hashlib import sha1
from math import ceil

hLen = 20 #sha1 = 160 bits 160/8=20 => hLen = 20 
k = 128 # RSA = 1024 bits 1024/8=128

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

def OAEP_encode(M,seed):
    # step a
    L=""
    lHash = sha1(bytearray(L.encode())).hexdigest()
    # step b Generate a padding string PS consisting of k - mLen -2hLen - 2 zero octets.  The length of PS may be zero.
    PS = "".zfill(((k - int(len(M)/2) - 2*hLen) - 2)*2)
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

# EME-OAEP decoding:
def OAEP_decode(EM):
#a.  If the label L is not provided, let L be the empty string.
#    Let lHash = Hash(L), an octet string of length hLen (see
#    the note in Section 7.1.1).
    L=""
    lHash = sha1(bytearray(L.encode())).hexdigest()
    
#b.  Separate the encoded message EM into a single octet Y, an
#    octet string maskedSeed of length hLen, and an octet
#    string maskedDB of length k - hLen - 1 as EM = Y || maskedSeed || maskedDB.
    Y = EM[:2]
    maskedSeed = EM[2: (2*hLen + 2)]
    #maskedDB = EM[k - hLen - 1:] #antagligen fel här
    maskedDB = EM[hLen * 2 + 2:]

#c.  Let seedMask = MGF(maskedDB, hLen).
    seedMask = MGF1(maskedDB,hLen)
#d.  Let seed = maskedSeed \xor seedMask.
    seed = hex((int(maskedSeed,16) ^ int(seedMask,16)))[2:]
#e.  Let dbMask = MGF(seed, k - hLen - 1).
    dbMask = MGF1(seed, (k-hLen-1))
#f.  Let DB = maskedDB \xor dbMask.
    DB = hex((int(maskedDB,16) ^ int(dbMask,16)))[2:]
#g.  Separate DB into an octet string lHash' of length hLen, a
#    (possibly empty) padding string PS consisting of octets
#    with hexadecimal value 0x00, and a message M as DB = lHash' || PS || 0x01 || M.
    lHash_prime = DB[:hLen * 2]
    PS = DB[len(lHash_prime): ]

    print(lHash_prime)
    print(Y)


#    If there is no octet with hexadecimal value 0x01 to
#    separate PS from M, if lHash does not equal lHash', or if
#    Y is nonzero, output "decryption error" and stop.  (See
#    the note below.)
    if ((lHash != lHash_prime) or (Y != "00") ):
        return "decryption error"

#print(OAEP_encode("fd5507e917ecbe833878","1e652ec152d0bfcd65190ffc604c0933d0423381"))
#test MGF1
#print(MGF1("0123456789abcdef",30))
#Test decode
OAEP_decode("00255975c743f5f11ab5e450825d93b52a160aeef9d3778a18b7aa067f90b2178406fa1e1bf77f03f86629dd5607d11b9961707736c2d16e7c668b367890bc6ef1745396404ba7832b1cdfb0388ef601947fc0aff1fd2dcd279dabde9b10bfc51f40e13fb29ed5101dbcb044e6232e6371935c8347286db25c9ee20351ee82")
