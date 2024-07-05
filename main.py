from fastapi import FastAPI
from colors import TSharkPcapColors
from packet_details import TSharkPcapDetails
from packet_list import TSharkPcapPacketList
from stats import TSharkPcapStats
from tshark_loader import TSharkPcapLoader
from settings import PCAP_PATH

app = FastAPI()

loader = TSharkPcapLoader(PCAP_PATH)
stats = TSharkPcapStats(loader)
details = TSharkPcapDetails(loader)
packet_list = TSharkPcapPacketList(loader, TSharkPcapColors(loader))


@app.get("/details")
async def get_details(frame: int):
    return details.get_frame_details(int(frame))


@app.get("/colored_packets")
async def get_colored_packets():
    return packet_list.colored_packets()
