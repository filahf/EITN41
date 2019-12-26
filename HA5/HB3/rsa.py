# RSAPrivateKey ::= SEQUENCE {
#     version           Version,
#     modulus           INTEGER,  -- n
#     publicExponent    INTEGER,  -- e 65537
#     privateExponent   INTEGER,  -- d
#     prime1            INTEGER,  -- p
#     prime2            INTEGER,  -- q
#     exponent1         INTEGER,  -- d mod (p-1)
#     exponent2         INTEGER,  -- d mod (q-1)
#     coefficient       INTEGER,  -- (inverse of q) mod p
#     otherPrimeInfos   OtherPrimeInfos OPTIONAL
#     }
from sympy import mod_inverse
import base64
import codecs

def create_rsa(p,q):
    version = 0
    n = p * q
    e = 65537
    d = mod_inverse(e, ((p-1)*(q-1)))
    p = p
    q = q
    exp_1 = d % (p-1)
    exp_2 = d % (q-1)
    coeff = mod_inverse(q,p)
    # print("n:",n)
    # print("e:",e)
    # print("d",d)
    # print("exp_1:",exp_1)
    # print("exp_2:",exp_2)
    # print("coeff:", coeff)
    return [version,n,e,d,p,q,exp_1,exp_2,coeff]

def hex_val(x):
    val = '0' * (len(hex(x)) % 2) + hex(x)[2:]
    return val


def DER_encode(integer):
    val = hex_val(integer)
    if int(val[0], 16) >= 8:
        val = '00' +  val
    length = hex_val(len(val) // 2)
    if len(val) // 2 >= 80:
        length = '8' + str(len(length) // 2) + length
    return '02' + length + val


def get_key(rsa):
    DER_encoded_key = ''
    for i in rsa:
        DER_encoded_key += DER_encode(i)
    length = hex_val(len(DER_encoded_key) // 2)
    if len(DER_encoded_key) // 2 >= 80:
        length = '8' + str(len(length) // 2) + length
    return '30' + length + DER_encoded_key



def main():
    p = 98239435950283871859290055251487823417858468872243454249930864805578758178601922742963328320272027144214094209587082053918934336062518442341992877622522975095332672112567412809022222298150735937575666451289198289595475505329663797607294450073623714366146233770815063244620511100933664529603308317292204043247
    q = 142950010864217314767307992548770427870292379949341933588213313483471076268376149766340472267258293905363403734515658759712661283726159237082904621242037416160623811509665846997478028753887769737935058395531128044278363768970450333912996628223224277024473587994306293012156601701313473093180049624680368750619
    rsa = create_rsa(p,q)
    der_key = get_key(rsa)
    #print(der_key)
    base64_key = base64.b64encode(bytearray.fromhex(der_key))
    print(base64_key)
    #integer = 123125178799915507986237205097259130069913581978440481287092269862722582825415764885395404700373597478040351248424188122928798954813713318253665668445868934260313334746406288738731274758696362147926304288060684145907171761722158294574908265142603731151159957470847588999852557825843626339009133881431992668061
    #print(DER_encode(integer))


if __name__ == "__main__":
    main()




