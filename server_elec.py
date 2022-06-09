# server_elec.py
import socket
import calculate_fee
import math


def write_utf8(s, sock):
    encoded = s.encode(encoding='utf-8')
    sock.sendall(len(encoded).to_bytes(4, byteorder="big"))
    sock.sendall(encoded)
    
# host ip 주소 변경
host = '172.20.10.3'
port = 8080

server_sock = socket.socket(socket.AF_INET)
server_sock.bind((host, port))
server_sock.listen(1)

print("기다리는 중")
client_sock, addr = server_sock.accept()
print('Connected by', addr)


data1 = client_sock.recv(1024)
data1_d = data1.decode()

data = data1_d[2:].split('+')
manage_elec = int(data[0])
before_elec = int(data[1])
select_elec = int(data[2])
new_elec = int(data[3])

if len(data[4]) > 0 :
    usage_before_input = int(data[4])
else :
    usage_before_input = 0
if len(data[5]) > 0 :
    enter_new_e = int(data[5])
else :
    enter_new_e = 0

if len(data[6]) > 0:
    iljo_level = int(data[6])
else:
    iljo_level = 0

print(manage_elec, before_elec, select_elec, new_elec, usage_before_input, enter_new_e)

sd_ey, under_ey, avg_ey, over_ey = calculate_fee.sd_ey, calculate_fee.under_ey, calculate_fee.avg_ey, calculate_fee.over_ey
sd_es, under_es, avg_es, over_es = calculate_fee.sd_es, calculate_fee.under_es, calculate_fee.avg_es, calculate_fee.over_es
sd_ew, under_ew, avg_ew, over_ew = calculate_fee.sd_ew, calculate_fee.under_ew, calculate_fee.avg_ew, calculate_fee.over_ew

usage_before_e = 0
new_avg_e = 0

if manage_elec ==1:
    new_ey = 0
    new_es = 0
    new_ew = 0
elif manage_elec == 2:
    if before_elec == 1:
        usage_before_e = usage_before_input
    elif before_elec == 2:
        if select_elec == 1:
            usage_before_e = under_ey
        elif select_elec == 2:
            usage_before_e = avg_ey
        elif select_elec == 3:
            usage_before_e = over_ey

    if new_elec == 1:
        new_avg_e = enter_new_e
        new_ey, new_es, new_ew = calculate_fee.calculate_new(usage_before_e, new_avg_e, sd_ey, sd_es, sd_ew, avg_ey,
                                                             avg_es, avg_ew)
    elif new_elec == 2:
        new_avg_e = avg_ey
        new_ey, new_es, new_ew = calculate_fee.calculate_new(usage_before_e, new_avg_e, sd_ey, sd_es, sd_ew, avg_ey, avg_es, avg_ew)
        print(new_ey)

        if iljo_level == 100:
            new_ey = new_ey * 0.8
            new_es = new_es * 0.8
            new_ew = new_ew * 0.8
        elif iljo_level >= 90:
            new_ey = new_ey * 0.85
            new_es = new_es * 0.85
            new_ew = new_ew * 0.85
        elif iljo_level >= 80:
            new_ey = new_ey * 0.9
            new_es = new_es * 0.9
            new_ew = new_ew * 0.9
        elif iljo_level >= 70:
            new_ey = new_ey * 0.95
            new_es = new_es * 0.95
            new_ew = new_ew * 0.95
        elif iljo_level >= 60:
            new_ey = new_ey
            new_es = new_es
            new_ew = new_ew
        elif iljo_level >= 50:
            new_ey = new_ey * 1.05
            new_es = new_es * 1.05
            new_ew = new_ew * 1.05
        elif iljo_level >= 40:
            new_ey = new_ey * 1.1
            new_es = new_es * 1.1
            new_ew = new_ew * 1.1
        elif iljo_level >= 30:
            new_ey = new_ey * 1.15
            new_es = new_es * 1.15
            new_ew = new_ew * 1.15
        elif iljo_level >= 20:
            new_ey = new_ey * 1.2
            new_es = new_es * 1.2
            new_ew = new_ew * 1.2
        else:
            new_ey = new_ey * 1.5
            new_es = new_es * 1.5
            new_ew = new_ew * 1.5

    if new_ey < 920:
        new_ey = 910
    if new_es < 920:
        new_es = 910
    if new_ew < 920:
        new_ew = 910

new_ey = math.trunc(new_ey)
new_es = math.trunc(new_es)
new_ew = math.trunc(new_ew)

new_ey = str(new_ey)
new_es = str(new_es)
new_ew = str(new_ew)

print(new_ey, new_es, new_ew)

write_utf8(new_ey, client_sock)
write_utf8(new_es, client_sock)
write_utf8(new_ew, client_sock)


client_sock.close()
server_sock.close()


