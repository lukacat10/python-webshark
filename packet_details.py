from base64 import b64encode
from loader_wrapper import TSharkPcapLoaderWrapper
from utils import hexdump_to_bytes, recursive_4_space_hierarchy_parser


class TSharkPcapDetails(TSharkPcapLoaderWrapper):
    def get_layers(self, frame_number: int):
        process = self.loader.run(
            "-Y",
            f"frame.number == {frame_number}",
            "-V",
        )
        return recursive_4_space_hierarchy_parser(process.stdout.decode())

    def get_payload(self, frame_number: int):
        process = self.loader.run(
            "-Y",
            f"frame.number == {frame_number}",
            "-x",
        )
        return hexdump_to_bytes(process.stdout.decode())

    def get_frame_details(self, frame_number: int):
        return {
            "payload": b64encode(self.get_payload(frame_number)).decode(),
            "layers": self.get_layers(frame_number),
        }
