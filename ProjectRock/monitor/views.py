import json
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse, FileResponse, Http404
from . import sniffer

def dashboard_view(request):
    # Fetch runtime system network cards
    context = {
        "adapters": sniffer.get_available_adapters()
    }
    return render(request, 'monitor/dashboard.html', context)

def live_stream_view(request):
    def event_generator():
        while True:
            try:
                packet_data = sniffer.PACKET_QUEUE.get(timeout=1.0)
                yield f"data: {json.dumps(packet_data)}\n\n"
            except Exception:
                yield ": keep-alive\n\n"
                
    response = StreamingHttpResponse(event_generator(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    return response

def toggle_adapter_view(request):
    """Handles frontend operational state shifts (Start/Stop Capture)."""
    if request.method == "POST":
        data = json.loads(request.body)
        interface = data.get("adapter")
        action = data.get("action")
        
        if action == "START" and interface:
            sniffer.start_live_capture(interface)
            return JsonResponse({"status": "active", "message": f"Capturing traffic on {interface}"})
        else:
            sniffer.stop_live_capture()
            return JsonResponse({"status": "idle", "message": "Capture stopped cleanly."})
            
    return JsonResponse({"status": "failed"}, status=400)

def download_pcap(request):
    try:
        return FileResponse(open(sniffer.PCAP_PATH, 'rb'), content_type='application/vnd.tcpdump.pcap')
    except FileNotFoundError:
        raise Http404("Not found!")