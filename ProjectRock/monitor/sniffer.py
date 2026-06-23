import os
import sys
import socket
import queue
import threading
from datetime import datetime

PACKET_QUEUE = queue.Queue(maxsize=5000)
LOG_DIR = "./logs"
PCAP_PATH = f"{LOG_DIR}/live_capture.pcap"

# System-agnostic Scapy compilation setup
try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP, DNS, DNSQR, PcapWriter, conf, get_if_list
    if sys.platform.startswith("linux"):
        conf.use_pcap = False  # Optimize natively for Linux raw rings
    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False

# Global variables to control background worker thread states
_capture_thread = None
_stop_signal = threading.Event()
_current_writer = None

def get_available_adapters():
    """Dynamically fetches all active hardware network interfaces on the machine."""
    if not HAS_SCAPY:
        return ["lo0", "en0", "eth0 (Mock)"]
    try:
        interfaces = get_if_list()
        # Clean out obvious system internal loopback anomalies for scannability
        return sorted([iface for iface in interfaces if iface not in ['lo', 'lo0']])
    except Exception:
        return ["eth0", "wlan0"]

class DynamicNetworkSniffer:
    def __init__(self, interface):
        global _current_writer
        self.interface = interface
        os.makedirs(LOG_DIR, exist_ok=True)
        
        if HAS_SCAPY:
            try:
                _current_writer = PcapWriter(PCAP_PATH, append=False, sync=True)
            except Exception:
                _current_writer = None

    def process_packet(self, packet):
        global _current_writer
        if _stop_signal.is_set():
            return True # Returning True inside Scapy sniff breaks the loop cleanly
            
        if not packet.haslayer(IP):
            return

        # 1. Archive raw binary packet immediately
        if _current_writer:
            try:
                _current_writer.write(packet)
            except Exception:
                pass

        # 2. Extract metrics for the UI layout
        ip = packet[IP]
        proto = "TCP" if packet.haslayer(TCP) else "UDP" if packet.haslayer(UDP) else "ICMP" if packet.haslayer(ICMP) else "IP"
        
        desc = "IP Routing Traffic"
        if packet.haslayer(DNS) and packet.haslayer(DNSQR):
            desc = f"DNS Resolution: {packet[DNSQR].qname.decode('utf-8', errors='ignore').strip('.')}"

        payload = {
            "time": datetime.now().strftime('%H:%M:%S.%f')[:-3],
            "src": ip.src,
            "dst": ip.dst,
            "proto": proto,
            "size": f"{len(packet)} Bytes",
            "desc": desc
        }

        try:
            PACKET_QUEUE.put_nowait(payload)
        except queue.Full:
            try:
                PACKET_QUEUE.get_nowait()
                PACKET_QUEUE.put_nowait(payload)
            except queue.Empty:
                pass

    def run(self):
        if not HAS_SCAPY:
            return
        sniff(iface=self.interface, prn=self.process_packet, stop_filter=lambda p: _stop_signal.is_set(), store=False)

def start_live_capture(interface):
    """Safely transitions threads to begin capturing data on a new link adapter target."""
    global _capture_thread, _stop_signal
    stop_live_capture() # Clear previous background session instances
    
    _stop_signal.clear()
    # Wipe queue state clean for the new adapter stream
    while not PACKET_QUEUE.empty():
        try:
            PACKET_QUEUE.get_nowait()
        except queue.Empty:
            break
            
    sniffer = DynamicNetworkSniffer(interface)
    _capture_thread = threading.Thread(target=sniffer.run, daemon=True)
    _capture_thread.start()

def stop_live_capture():
    """Signals background worker loops to break execution cleanly."""
    global _stop_signal, _current_writer
    _stop_signal.set()
    if _current_writer:
        try:
            _current_writer.close()
        except Exception:
            pass