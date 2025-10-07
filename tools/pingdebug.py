#!/usr/bin/env python3
import subprocess
import time
import datetime
import csv
import signal
import sys
from pathlib import Path
from collections import deque

TARGET = "96.108.64.121"
INTERFACE = "eth8"
PACKET_SIZE = 100
INTERVAL = 0.25
REPORT_INTERVAL = 30 * 60
CSV_FILE = Path("ping_loss.csv")
LOGFILE = 'pingdebug.log'


class PingMonitor:
    def __init__(self):
        self.src_ip = self.get_interface_ip()
        self.sent = 0
        self.lost = 0
        self.start_time = datetime.datetime.now()
        self.last_report = time.time()
        self.ticks_active = False
        self.ticks_interval = 5
        self.ticks_current = 1
        self.ping_history = deque(maxlen=1000)
        self.init_csv()
        signal.signal(signal.SIGINT, self.signal_handler)

    def get_interface_ip(self):
        try:
            result = subprocess.run(
                ["ip", "addr", "show", INTERFACE],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            for line in result.stdout.split('\n'):
                if 'inet ' in line and not '127.' in line:
                    return line.split()[1].split('/')[0]
        except:
            pass
        return "unknown"

    def write_log(self,msg):
        print(msg, end='', flush=True)
        with open(LOGFILE,'a') as f:
            _ = f.write(msg)
    def init_csv(self):
        if CSV_FILE.exists(): return
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['datetime', 'src_ip', 'dest_ip', 'loss_type', 'loss_pct_1000'])

    def ping_once(self):
        try:
            result = subprocess.run([
                "ping", "-I", INTERFACE, "-i", str(INTERVAL), "-c", "1", "-s", str(PACKET_SIZE), "-W", "1", TARGET
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=INTERVAL)
            
            if result.returncode == 0:
                return True, None
            else:
                if "100% packet loss" in result.stdout:
                    return False, "dropped"
                elif "timeout" in result.stdout or "timeout" in result.stderr:
                    return False, "timeout"
                else:
                    return False, "other_failure"
        except Exception as e:
            if "timed out after" in str(e):
                return False, f'timeout > {int(e.timeout * 1000)}ms'
            return False, f"other_failure: {e}"

    def loss_pct(self):
        return (sum(1 for x in self.ping_history if not x) / len(self.ping_history)) * 100 if self.ping_history else 0
    
    def log_loss(self, loss_type):
        loss_pct = self.loss_pct()
        
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.src_ip,
                TARGET,
                loss_type,
                f"{loss_pct:.2f}"
            ])

    def print_report(self):
        if self.ticks_active:
            self.write_log('\n')
            self.ticks_active = False
        
        now = datetime.datetime.now()
        uptime = now - self.start_time
        loss_pct = (self.lost / self.sent * 100) if self.sent > 0 else 0
        self.write_log(
            f'\n'
            f'--- WAN Debug: Ping Report {now.strftime("%Y-%m-%d %H:%M:%S")} ---\n'
            f'Diag - TGT: {TARGET} - Freq: {INTERVAL*1000}ms - SRC: {self.src_ip} {INTERFACE}\n'
            f'Sent: {self.sent}, Lost {self.lost} ({loss_pct:.2f}%) - Total Uptime: {uptime}\n'
        )

    def signal_handler(self, signum, frame):
        self.print_report()
        sys.exit(0)
    
    def tick(self):
        self.ticks_active = True
        self.ticks_current += 1
        if self.ticks_current > self.ticks_interval:
            self.write_log(f'.')
            self.ticks_current = 1

    def run(self):
        self.print_report()
        while True:
            start_time = time.time()
            ok, reason = self.ping_once()
            self.sent += 1
            self.ping_history.append(ok)
            
            if not ok:
                self.lost += 1
                if self.ticks_active:
                    self.write_log('.\n')
                    self.ticks_active = False
                ts = datetime.datetime.now().strftime("%Y%m%d %H%M%S.%f")
                self.write_log(f"[{ts}] Packet loss: {reason} ({self.loss_pct():.2f})\n")
                self.log_loss(reason)
            else:
                self.tick()

            now = time.time()
            if now - self.last_report >= REPORT_INTERVAL:
                self.print_report()
                self.last_report = now
            delay_timer = INTERVAL - (time.time() - start_time)
            if delay_timer < 0: delay_timer = 0
            time.sleep(delay_timer)

if __name__ == "__main__":
    monitor = PingMonitor()
    monitor.run()