#!/usr/bin/env python3
import socket
import time
from datetime import datetime

UDP_PORT = 9998
INTERVAL = 1 # Expected interval of UDP heartbeats
TIMEOUT = .25 # Expected timeout value per pingdebug
LOGFILE = 'downstream_loss.log'

# Remote Session
# x=0;while true; do echo "heartbeat : $x" | ncat -u unit03.net 9998; x=`expr $x + 1`; sleep .5; done
#
# Expected remote message: 
#   heartbeat : {seq_no}

def write_log(msg):
    if tick_active: print()
    print(msg)
    with open(LOGFILE,'a') as f:
        _ = f.write(msg + '\n')

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', UDP_PORT))
    sock.settimeout(TIMEOUT+INTERVAL)
    SEQNO = None
    tick = 0
    tick_interval = 1
    tick_active = False
    print(f"NET DIAG: Listening for UDP packets on port {UDP_PORT}")
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode('utf-8',errors='ignore')
            if not msg.startswith('heartbeat : '):
                raise ValueError(f'Unexpected UDP message from {addr}: {msg}')
            current_seq = int(msg.split()[2])
            if SEQNO is None:
                SEQNO = current_seq - 1
            seq_diff = current_seq - (SEQNO)
            if not seq_diff == 1:
                write_log(f'[{datetime.now():%Y%m%d %H%M%S.%f}] Lost {seq_diff} downstream UDP packets')
            SEQNO = current_seq
            tick += 1
            if not tick % tick_interval:
                print('.',end='',flush=True)
                tick_active = True
                tick = 0
        except socket.timeout:
            # Handle timeout - continues the loop
            if tick_active:
                print()
                tick_active = False
            print(f'- Not receiving UDP packets...')
except KeyboardInterrupt:
    print("\nShutting down")
finally:
    sock.close()