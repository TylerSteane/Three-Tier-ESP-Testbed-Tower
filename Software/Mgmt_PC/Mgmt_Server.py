# |**********************************************************************;
# * Project           : ESP Testbed Tower -  Managment PC.
# *
# * Program name      : Mgmt_Server.py
# *
# * Author            : Tyler Steane
# *
# * Date created      : 21-06-2019
# *
# * Purpose           : Managment PC server, co-ordinates all Testbed towers distributing code an flash commands
# *
# * Dependencies      :  yaml & genlog (requires Matplotlib)
# *
# * Usage			  : python Mgmt_Server.py -config-file.yaml e.g.: 'Mgmt_Server.py Demo.yaml'
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision
# * 29-10-2018  M Trifilo    1      Initial implementation
# * 21-06-2019  T Steane     2      Imporved Logging, including HTML Dash Log. Added Log file read and formatting into dictioary. Improved configfile functionality. Improved thread handeling and ending sequance. General tweaks.
# *
# |**********************************************************************;

from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from threading import Thread
import yaml, select, logging, signal, time, os, re, argparse, threading, shutil
from collections import OrderedDict
from datetime import datetime
from genLog import compileLog

# Gets the IP of the device its running on. Mainly used for debugging
def get_ip():
    mgmtlog.debug('get_ip() Started')
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
    mgmtlog.debug('get_ip(): ' + IP)

#Sets up handling for incoming clients
def accept_incoming_connections( no_Towers):
	while no_Towers > 0: # wait for all towers to connect.
		mgmtlog.debug('accept_incoming_connections() Started')
		client, client_address = SERVER.accept() # Accept Client Connection Request
		mgmtlog.info("%s:%s has connected." % client_address)
		addresses[client] = client_address # Add client to addresses list
		new_thread = Thread(target=handle_client, args=(client,client_address))#create new thread
		threads.append(new_thread)# collect the threads created to check later.
		new_thread.start() # Start new thread
		no_Towers = no_Towers - 1# decrement number of towers

#Handles a single client connection
def handle_client(client, client_address):  # Takes client socket as argument.
	threadLocal.threadlog = logging.getLogger(client_address[0]) #name log with client IP address
	threadLocal.threadlog.setLevel(logging.INFO)
	threadLocal.fh = logging.FileHandler("log/Log-"+client_address[0]+datetime.now().strftime('_%Y%m%d_%H%M%S.log')+".log")
	threadLocal.threadlog.addHandler(threadLocal.fh)

    #mgmtlog.debug('handle_client(client) Started')
	threadLocal.threadlog.info('handle_client(client) Started')
	client.send(bytes("Name?", "utf8")) # Name Request
	name = client.recv(BUFSIZ).decode("utf8") # Name Response
	threadLocal.threadlog.info(name + " joined")
	global completed_towers
	if name in completed_towers:
		threadLocal.threadlog.info(name + " is Complete")
		while 1:
			continue
	else:
		completed_towers.append(name)
		logname = name + datetime.now().strftime('_%Y%m%d_%H%M%S.log')

		tower=int(re.search(r'\d+', name).group()) # Gives us Tower Number
		tower= tower_ips.index('192.168.0.1%02d'%tower) #Find the Tower Index number

		clients[client] = name # Add client to clients list
        # Transfer files listed in the configuration YAML
		for file in files:
			client.send(bytes('FILES!',"utf8")) # File Transfer Request
			filename = files[file]
			size = len(filename)
			size = bin(size)[2:].zfill(16) # encode filename size as 16 bit binary
			filesize = os.path.getsize(filename)
			filesize = bin(filesize)[2:].zfill(32) # encode filesize as 32 bit binary
			client.send(bytes(size,"utf8")) # Send Filename size
			client.send(bytes(filename,"utf8")) # Send Filename
			client.send(bytes(filesize,"utf8")) # Send File Size
			file_to_send = open(filename, 'rb')
			l = file_to_send.read()
			client.sendall(l) # Send File Data
			file_to_send.close()
			#mgmtlog.info(file + ' Sent')
			threadLocal.threadlog.info(file + ' Sent')
			done = False
			# Wait for transfer complete
			while done == False:
				if client.recv(BUFSIZ).decode("utf8") == 'Done':
					done = True
				else:
					continue # Transfer next file
        # Iterates through the tower_data array
		for esp in range(len(tower_data[tower])):
			client.send(bytes('Flash',"utf8"))
            # Creates a command to send to the tower
			command = 'Tower' + str(tower+1) + ' flash ' + str(re.search(r'\d+', tower_data[tower][esp][0]).group()) + ' ' + str(files[tower_data[tower][esp][1]])
			size = len(command)
			size = bin(size)[2:].zfill(32) # encode command size as 32 bit binary
			client.send(bytes(size,"utf8")) # Send command size
			# Send Command to client
			client.send(bytes(command,"utf8"))
			#mgmtlog.info(command)
			threadLocal.threadlog.info(command)
			# Waits for Pi to respond before sending next command
			result = 0 # 0=Flashing 1=Success 2=Failed 3= Ready for Next
			while result == 0:
				reply = client.recv(BUFSIZ).decode("utf8")
				mgmtlog.info(reply)
				threadLocal.threadlog.info(reply)
				if "seconds (effective" in reply and result == 0:
					line = str(re.search(r'\d+', tower_data[tower][esp][0]).group()) +", "+ str(files[tower_data[tower][esp][1]])+ ", "+ "1" + ", "+ datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ", "+ "Success"
					writeline_file(logname, line)
					result = 1
					while result == 1:
						reply = client.recv(BUFSIZ).decode("utf8")
						mgmtlog.info(reply)
						threadLocal.threadlog.info(reply)
						if reply == 'Done':
							result = 3
				elif reply == 'Done' and result == 0:
					line = str(re.search(r'\d+', tower_data[tower][esp][0]).group())+ ", " + str(files[tower_data[tower][esp][1]])+ ", "+ "0" + ", "+ datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ", " + "Failure - Check Device"
					writeline_file(logname, line)
					result = 2
		client.close()

# Write to file
def writeline_file(filename, data):
	filename = "log\\" + filename
	if os.path.exists(filename):
		append_write = 'a' # append if already exists
	else:
		append_write = 'w' # make a new file if not
	file = open(filename,append_write)
	file.write(data + '\n')
	file.close()

# Imports the YAML Config File
def import_config(configfile):
	mgmtlog.debug('import_config Started')
	with open(configfile, 'r') as stream:
		try:
			data = yaml.load(stream)
		except yaml.YAMLError as exc:
			mgmtlog.info(exc)
	return data
	stream.close
	mgmtlog.debug('import_config complete')
	mgmtlog.debug(data)

# Creates arrays from the YAML File, easier to iterate through
def get_tower_info():
    mgmtlog.debug('tower IPs and data array started')
    for header in config:
        if ('tower' in header.lower() and config[header] != None):
            tower_ips.append(config[header]['IP'])
            temp_list = []
            for key in config[header]:
                if (key.lower() !='ip' and config[header][key] != None):
                    temp_list.append([key, config[header][key]])
            tower_data.append(temp_list)
    mgmtlog.debug('tower ips : ' + str(tower_ips))
    mgmtlog.debug('tower data : ' + str(tower_data))

## Keep /Log/ upto date with the latest files.
if not os.path.exists('Log/'):
	os.makedirs('Log/')
if not os.path.exists('Log/old'):
	os.makedirs('Log/old')
src = 'Log/'
dst = 'Log/old/'
for f in os.listdir(src):
	shutil.move(src+f,dst)

# create logger with 'ESP Logger'
mgmtlog = logging.getLogger('Mgmt_Logger')
mgmtlog.setLevel(logging.DEBUG)
# create file handler which logs everything
fh = logging.FileHandler(datetime.now().strftime('Mgmt_Server_%Y%m%d_%H%M%S.log'))
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
mgmtlog.addHandler(fh)
mgmtlog.addHandler(ch)

## create Thread local data to create unique log files for each tower thread.

threadLocal = threading.local()

#Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument("config", help="YAML Configuration Filename")
args = parser.parse_args()

#Import config and build array
tower_ips = []
tower_data = []
completed_towers = []
config = import_config(args.config)
get_tower_info()
files = config['Files']

#Server Variables
clients = {}
addresses = {}
HOST = get_ip()
PORT = 5000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

mgmtlog.info("Chat server started on port " + str(PORT))
SERVER.listen(5)
mgmtlog.info("Waiting for connection...")
ACCEPT_THREAD = Thread(target=accept_incoming_connections, args=(len(tower_ips),))
threads = []# collect threads used to handel each tower.
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()

for thread in threads: #Wait for all Tower threads are finished
	thread.join()

SERVER.close()
#Copile HTML Log Dashboard
compileLog("Log/")
#Display Dashbaord.
os.system("start "+ os.path.abspath("log.html"))
