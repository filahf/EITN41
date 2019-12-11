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
    # Step A. If the label L is not provided, let L be the empty string.
    # Let lHash = Hash(L), an octet string of length hLen (see
    # the note below).
    L=""
    lHash = sha1(bytearray(L.encode())).hexdigest()
    # Step B. Generate a padding string PS consisting of k - mLen -2hLen - 2 zero octets.  The length of PS may be zero.
    PS = "".zfill(((k - int(len(M)/2) - 2*hLen) - 2)*2)
    # Step C. concatenate lHash, PS, a single octet with hexadecimal
    # value 0x01, and the message M to form a data block DB of
    # length k - hLen - 1 octets as  DB = lHash || PS || 0x01 || M.
    DB = lHash + PS + "01" + M
    #Step D. Given in int assignment
    #Step E. Let dbMask = MGF(seed, k - hLen - 1).
    dbMask = MGF1(seed, k - hLen - 1)
    #Step F. Let maskedDB = DB \xor dbMask.
    maskedDB = hex(int(DB, 16) ^ int(dbMask, 16))[2:]
    #Step G. Let seedMask = MGF(maskedDB, hLen).
    seedMask = MGF1(maskedDB, hLen)
    #Step H.  Let maskedSeed = seed \xor seedMask.
    maskedSeed = hex(int(seed, 16) ^ int(seedMask, 16))[2:]
    #Step I.  Concatenate a single octet with hexadecimal value 0x00,
    #maskedSeed, and maskedDB to form an encoded message EM of
    #length k octets as   EM = 0x00 || maskedSeed || maskedDB.
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
    tmp_len = hLen * 2
    lHash_prime = DB[:tmp_len]
    PS = DB[tmp_len: tmp_len + DB[tmp_len:].find("01") + 2]
    M = DB[tmp_len + len(PS):]


#    If there is no octet with hexadecimal value 0x01 to
#    separate PS from M, if lHash does not equal lHash', or if
#    Y is nonzero, output "decryption error" and stop.  (See
#    the note below.)
    if(lHash != lHash_prime or Y != "00" or DB.find("01") == -1):
        return "decryption error"
    else:
        return M
    

#test MGF1
#print(MGF1("9b4bdfb2c796f1c16d0c0772a5848b67457e87891dbc8214",21))

#test Encode
#print(OAEP_encode("c107782954829b34dc531c14b40e9ea482578f988b719497aa0687","1e652ec152d0bfcd65190ffc604c0933d0423381"))

#Test decode
print(OAEP_decode("0063b462be5e84d382c86eb6725f70e59cd12c0060f9d3778a18b7aa067f90b2178406fa1e1bf77f03f86629dd5607d11b9961707736c2d16e7c668b367890bc6ef1745396404ba7832b1cdfb0388ef601947fc0aff1fd2dcd279dabde9b10bfc51efc06d40d25f96bd0f4c5d88f32c7d33dbc20f8a528b77f0c16a7b4dcdd8f"))
