
from pcapfile import savefile
from itertools import groupby
import socket
import struct

#Remove mix entries from the list
def filter(list, mix_ip):
    filtered_list = []
    for x in list:
        if(x != mix_ip):
            filtered_list.append(x)
    return filtered_list
#divide the list into chunks based on the size of the mix
def chunks(list, size):
    return [list[i * size:(i + 1) * size] for i in range((len(list) + size - 1) // size )]

#get disjoint sets
def disjoint(list, partners):
    sets = []
    for i in list:
        marker = True
        for y in sets:
            if len(set(i) & set(y)) != 0:
                marker = False
        if marker == True:
            sets.append(i)
            #list.remove(i)
    return sets[:partners]
#Find partners by excluding
def exclude(chunks, sets):
    for i in chunks:
        interesting_sets = []
        for j in sets:
            if not (len(set(i) & set(j)) == 0):
                interesting_sets.append(j)
        if len(interesting_sets) == 1:
            temp_list = list(set(interesting_sets[0]) & set(i))
            sets.remove(interesting_sets[0])
            sets.append(temp_list)
    return sets


# https://stackoverflow.com/questions/5619685/conversion-from-ip-string-to-integer-and-backward-in-python
# Ipv4 address to Int
def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]
#Get the size of the mix
def get_mix_size(list):
    lst = []
    for n,c in groupby(list):
        num,count = n,sum(1 for i in c)
        lst.append((num,count))

    return max([y for x,y in lst])
#Read packets from file and tidy them up.
def packets(nazir_ip,mix_ip):
    ingoing = []
    outgoing = []

    for pkt in capfile.packets:
        ip_src = pkt.packet.payload.src.decode('UTF8')
        ip_dst = pkt.packet.payload.dst.decode('UTF8')
        ingoing.append(ip_src)
        outgoing.append(ip_dst)
    mix_size = get_mix_size(ingoing)
    #print("Mix size: ", ingoing)

    filtered_ingoing = filter(ingoing,mix_ip)
    filtered_outgoing = filter(outgoing,mix_ip)
    chunked_ingoing = chunks(filtered_ingoing,mix_size)
    chunked_outgoing = chunks(filtered_outgoing,mix_size)

    interesting_chunks = []
    for x in chunked_ingoing:
        for y in x:
            if(y == nazir_ip):
                interesting_chunks.append(chunked_outgoing[chunked_ingoing.index(x)])

    return interesting_chunks

file_path = 'HA2/2B/cia.log.1339.pcap'
nazir_ip = "161.53.13.37"
mix_ip = "11.192.206.171"
partners = 12

testcap = open(file_path, 'rb')
capfile = savefile.load_savefile(testcap, layers=2, verbose=True)
interesting_chunks = packets(nazir_ip,mix_ip)
dis_set = disjoint(interesting_chunks,partners)
dis_set = exclude(interesting_chunks,dis_set)
#Calculate the sum of the ip addresses
ipsum = 0
for i in dis_set:
    ipsum += ip2int(i[0])

print("Nazir ip", nazir_ip)
print("Number of partners: ", partners )
print("Sum of ip",ipsum)

