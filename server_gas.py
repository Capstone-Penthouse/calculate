# server_gas.py
import socket
import calculate_fee
import math


def write_utf8(s, sock):
    encoded = s.encode(encoding='utf-8')
    sock.sendall(len(encoded).to_bytes(4, byteorder="big"))
    sock.sendall(encoded)
    
# host ip 주소 변경
host = '172.20.10.3'
port = 8000

server_sock = socket.socket(socket.AF_INET)
server_sock.bind((host, port))
server_sock.listen(1)

print("기다리는 중")
client_sock, addr = server_sock.accept()
print('Connected by', addr)


data1 = client_sock.recv(1024)
data1_d = data1.decode()

data = data1_d[2:].split('+')
manage_gas = int(data[0])
before_gas = int(data[1])
select_gas = int(data[2])
new_gas = int(data[3])
if len(data[4]) > 0 :
    usage_before_input = int(data[4])
else :
    usage_before_input = 0
if len(data[5]) > 0 :
    enter_new_g = int(data[5])
else :
    enter_new_g = 0
if len(data[6]) > 0:
    iljo_level = int(data[6])
else:
    iljo_level = 0

print(manage_gas, before_gas, select_gas, new_gas, usage_before_input, enter_new_g)

sd_gy, under_gy, avg_gy, over_gy = calculate_fee.sd_gy, calculate_fee.under_gy, calculate_fee.avg_gy, calculate_fee.over_gy
sd_gs, under_gs, avg_gs, over_gs = calculate_fee.sd_gs, calculate_fee.under_gs, calculate_fee.avg_gs, calculate_fee.over_gs
sd_gw, under_gw, avg_gw, over_gw = calculate_fee.sd_gw, calculate_fee.under_gw, calculate_fee.avg_gw, calculate_fee.over_gw

usage_before_g = 0
new_avg_g = 0

if manage_gas ==1:
    new_gy = 0
    new_gs = 0
    new_gw = 0
elif manage_gas == 2:
    if before_gas == 1:
        usage_before_g = usage_before_input
    elif before_gas == 2:
        if select_gas == 1:
            usage_before_g = under_gy
        elif select_gas == 2:
            usage_before_g = avg_gy
        elif select_gas == 3:
            usage_before_g = over_gy
    if new_gas == 1:
        new_avg_g = enter_new_g
        new_gy, new_gs, new_gw = calculate_fee.calculate_new(usage_before_g, new_avg_g, sd_gy, sd_gs, sd_gw, avg_gy,
                                                             avg_gs, avg_gw)
    elif new_gas == 2:
        new_avg_g = avg_gy
        new_gy, new_gs, new_gw = calculate_fee.calculate_new(usage_before_g, new_avg_g, sd_gy, sd_gs, sd_gw, avg_gy, avg_gs, avg_gw)
        print(new_gy)

        if iljo_level == 100:
            new_gy = new_gy * 0.8
            new_es = new_gs * 0.8
            new_gw = new_gw * 0.8
        elif iljo_level >= 90:
            new_gy = new_gy * 0.85
            new_es = new_gs * 0.85
            new_gw = new_gw * 0.85
        elif iljo_level >= 80:
            new_gy = new_gy * 0.9
            new_es = new_gs * 0.9
            new_gw = new_gw * 0.9
        elif iljo_level >= 70:
            new_gy = new_gy * 0.95
            new_es = new_gs * 0.95
            new_gw = new_gw * 0.95
        elif iljo_level >= 60:
            new_gy = new_gy
            new_es = new_gs
            new_gw = new_gw
        elif iljo_level >= 50:
            new_gy = new_gy * 1.05
            new_es = new_gs * 1.05
            new_gw = new_gw * 1.05
        elif iljo_level >= 40:
            new_gy = new_gy * 1.1
            new_es = new_gs * 1.1
            new_gw = new_gw * 1.1
        elif iljo_level >= 30:
            new_gy = new_gy * 1.15
            new_es = new_gs * 1.15
            new_gw = new_gw * 1.15
        elif iljo_level >= 20:
            new_gy = new_gy * 1.2
            new_es = new_gs * 1.2
            new_gw = new_gw * 1.2
        else:
            new_gy = new_gy * 1.5
            new_es = new_gs * 1.5
            new_gw = new_gw * 1.5

    if new_gy < 1110:
        new_gy = 1100
    if new_gs < 1110:
        new_gs = 1100
    if new_gw < 1110:
        new_gw = 1100

new_gy = math.trunc(new_gy)
new_gs = math.trunc(new_gs)
new_gw = math.trunc(new_gw)

new_gy = str(new_gy)
new_gs = str(new_gs)
new_gw = str(new_gw)

print(new_gy, new_gs, new_gw)

write_utf8(new_gy, client_sock)
write_utf8(new_gs, client_sock)
write_utf8(new_gw, client_sock)

client_sock.close()
server_sock.close()


