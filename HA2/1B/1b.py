def main():
    sA = "95F6"
    sB = "BB5D"
    dA = "54C8"
    dB = "A969"
    m = "2A6A"
    b = 0
    diningClub(sA,sB,dA,dB,m,b)

#Convert hex string to binary int
def toBin(data):
    return int(data,16)


def diningClub(sa,sb,da,db,m,b):
    if b == 1:
        xor = toBin(sa) ^ toBin(sb) ^ toBin(m)
        print(hex(xor)[2:].zfill(4))
    else:
        secretXor = toBin(sa) ^ toBin(sb)
        data = toBin(da) ^ toBin(db)
        xor = secretXor ^ data

        message = str(hex(xor)[2:]).zfill(4)
        secret = str(hex(secretXor)[2:]).zfill(4)

        print(secret+message)


if __name__ == "__main__":
    main()


