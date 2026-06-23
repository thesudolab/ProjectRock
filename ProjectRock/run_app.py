# run_app.py
import threading
import os
import sys
from monitor.sniffer import LinuxNetworkEngine

def start_sniffer_thread():
    # Swap 'eth0' or 'wlan0' out matching your targeted active adapter index link
    engine = LinuxNetworkEngine(interface="eth0")
    engine.start_capture()

if __name__ == "__main__":
    if os.getuid() != 0:
        sys.exit("[!] Critical Error: Bootstrapper execution script requires root (sudo) clearance.")
        
    # Start Scapy network tap inside decoupled daemon space
    sniffer_thread = threading.Thread(target=start_sniffer_thread, daemon=True)
    sniffer_thread.start()
    
    # Fire up production deployment development web engine binding to all available channels
    os.system("python3 manage.py runserver 0.0.0.0:8000")