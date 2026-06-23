# Project Rock

Project Rock is a high-performance network analysis and monitoring dashboard designed for real-time packet stream observation. It provides immediate insights into network traffic, protocol distribution, and session-level data.

## Features

* **Real-Time Packet Stream**: View live incoming network traffic with low-latency updates via Server-Sent Events (SSE).
* **Flow Tracking**: Automatically groups related packets into sessions based on Source/Destination IP and Port combinations.
* **Payload Inspector**: A tabbed inspection interface that allows you to view raw frame details, hex dumps, and reconstructed session payloads.
* **Protocol Breakdown**: Live visualization of protocol distribution (TCP, UDP, HTTP, DNS, TLS, etc.).
* **Traffic Analytics**: Visual representation of network throughput and top-talker identification.
* **Advanced Filtering**: Real-time filtering of the packet stream to isolate specific traffic patterns.

## Tech Stack

* **Frontend**: HTML5, CSS3 (Inter & JetBrains Mono fonts), JavaScript (Vanilla).
* **Communication**: Server-Sent Events (SSE) for live telemetry streaming.
* **Visualization**: Canvas API for real-time traffic throughput graphing.

## Getting Started
<img width="1466" height="802" alt="Screenshot 2026-06-23 at 11 57 31 PM" src="https://github.com/user-attachments/assets/888a6f01-16f5-4e50-a983-d6ffdeedec4c" />


### Prerequisites
* Ensure your backend provides a stream endpoint (e.g., `/stream/`) that emits JSON packet objects.
* Backend must include fields: `src`, `dst`, `srcPort`, `dstPort`, `proto`, `size`, `desc`, and `payload`.

### Installation
1. Clone the repository into your project directory.
2. Ensure your backend server is running and configured to serve the `dashboard.html` file.
3. Open the dashboard in your browser.
4. Select your network interface from the dropdown and click **Start Capture**.


## Running the Dashboard

Since the dashboard uses Django template tags (e.g., `{% if adapters %}`), you should run this within your Django project environment:

1.  **Configure Routes**: Ensure your Django `urls.py` points to the view that renders `dashboard.html` and handles the `/stream/` and `/toggle/` endpoints.
2.  **Start the Server**:
    ```bash
    python manage.py runserver
    ```
3.  **Access the Dashboard**: Open your web browser and navigate to the local address provided by your server (e.g., `http://127.0.0.1:8000/`).

## Initiating a Capture

Once the page is loaded:

* **Select Interface**: Use the dropdown menu in the top bar to select the network interface you want to monitor (e.g., `eth0`, `wlan0`, or `any`).
* **Start**: Click the **Start Capture** button.
* **Monitor**: You should immediately see packets populating the **Packet Stream** table.
* **Analyze**:
    * Click on a packet to view its details.
    * Use the **Payload** tab to see the reconstructed data stream for that specific session.
    * Use the filter input to refine your view (e.g., `ip.src == 192.168.1.1`).


## Usage

1.  **Capture**: Use the "Start Capture" button to initiate the network stream.
2.  **Filter**: Type expressions in the filter bar (e.g., `proto == TCP`) to narrow down displayed packets.
3.  **Inspect**: Click any row in the table to open the Details Panel.
    * **Details**: View metadata and protocol-specific info.
    * **Hex**: View raw hexadecimal data.
    * **Payload**: View the reassembled data stream for that specific session.
4.  **Clear**: Use the "Clear" button to reset the buffer and session flows.

## Roadmap
* [ ] Add export functionality for session payloads (PCAP).
* [ ] Implement persistent storage for historical captures.
* [ ] Add advanced geolocation for IP addresses.

---
*Built for network transparency and analysis.*
