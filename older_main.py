import machine
pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]


html = """
HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: closed\r\n\r\n
<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body> <h1>ESP8266 Pins</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""

import network
ap_if = network.WLAN(network.AP_IF)
ap_if.active(True)
print(ap_if.ifconfig())

import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
try:
    s.bind(addr)
    s.listen(1)
    print('listening on', addr)

    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
        response = html % '\n'.join(rows)
        cl.send(bytes(response,'utf8'))
        cl_file.close() #NOTE this step may be needed
        cl.close()
finally:
    s.close()
