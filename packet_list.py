
from colors import TSharkPcapColors
from loader_wrapper import TSharkPcapLoaderWrapper
from tshark_loader import TSharkPcapLoader
from utils import rgb_to_hex


class TSharkPcapPacketList(TSharkPcapLoaderWrapper):
    def __init__(self, loader: TSharkPcapLoader, colors: TSharkPcapColors) -> None:
        super().__init__(loader)
        self.colors = colors

    @property
    def packets(self):
        process = self.loader.run(
            "-T",
            "fields",
            "-E",
            "separator=|",
            "-e",
            "frame.number",
            "-e",
            "frame.time_relative",
            "-e",
            "ip.src",
            "-e",
            "ip.dst",
            "-e",
            "ipv6.src",
            "-e",
            "ipv6.dst",
            "-e",
            "eth.src",
            "-e",
            "eth.dst",
            "-e",
            "_ws.col.Protocol",
            "-e",
            "frame.len",
            "-e",
            "_ws.col.Info",
        )
        rows = []
        for line in process.stdout.decode().splitlines():
            (
                frame_number,
                timestamp,
                v4_src,
                v4_dst,
                v6_src,
                v6_dst,
                eth_src,
                eth_dst,
                protocol,
                length,
                info,
            ) = line.split("|")
            row = {
                "frame_number": frame_number,
                "timestamp": timestamp,
                "src": v4_src or v6_src or eth_src,
                "dst": v4_dst or v6_dst or eth_dst,
                "protocol": protocol,
                "length": length,
                "info": info,
            }
            rows.append(row)
        return rows

    def colored_packets(self):
        rows = self.packets
        frame_colors = self.colors.frame_colors
        processed_rows = []
        for row in rows:
            num_str = str(row["frame_number"])
            foreground_color = rgb_to_hex(frame_colors[num_str]["foreground_color"])
            background_color = rgb_to_hex(frame_colors[num_str]["background_color"])
            processed_row = {
                "foreground_color": foreground_color,
                "background_color": background_color,
                "frame_number": row["frame_number"],
                "time": row["time"],
                "src": row["src"],
                "dst": row["dst"],
                "protocol": row["protocol"],
                "length": row["length"],
                "info": row["info"],
            }
            processed_rows.append(processed_row)
        return processed_rows
