import network, socket, time, machine, sys, utime
from machine import Pin
sys.path.append('projet pompe') # Nom du dossier ou se trouve les fonctions à importer
import mdp, siteweb

#Variable to control 
intled = machine.Pin("LED", machine.Pin.OUT)
pompe = Pin(22, Pin.OUT)
intled.value(1)

#import SSID and PASSWORD from secrets.py 
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(mdp.ssid, mdp.password)

#Write html code for web browser
html=siteweb.html

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
 
# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
 
s = socket.socket()
s.bind(addr)
s.listen(1)
 
print('listening on', addr)

stateis = ""
 
# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)

        request = cl.recv(1024)

        request = str(request)
        led_on = request.find('/unpeu') # Variable based on the html link
        led_off = request.find('/beaucoup') # Variable based on the html link
        #print( 'led on = ' + str(led_on))
        #print( 'led off = ' + str(led_off))

        if led_on == 6:
            print("2 sec")
            intled.value(1)
            pompe.value(1)
            utime.sleep(3)
            pompe.value(0)
            intled.value(0)
            stateis = "La pompe fonctionne pendant 3 secondes"

        elif led_off == 6:
            intled.value(1)
            pompe.value(1)
            utime.sleep(5)
            pompe.value(0)
            intled.value(0)
            stateis = "La pompe fonctionne pendant 5 secondes"
                 
        response = html + stateis
        
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
 
    except OSError as e:
        cl.close()
        print('connection closed')