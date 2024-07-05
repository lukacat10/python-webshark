from pathlib import Path
import subprocess


class TSharkPcapLoader:
    EXECUTABLE_PATH = Path(r"C:\Program Files\Wireshark\tshark.exe")

    def __init__(self, capture_file_path: Path) -> None:
        self.capture_file_path = capture_file_path

    def run(self, *args):
        return subprocess.run(
            [
                str(self.EXECUTABLE_PATH.absolute()),
                "-r",
                str(self.capture_file_path.absolute()),
                *args,
            ],
            capture_output=True,
        )

    def get_frames_with_filter(self, filter_query: str):
        process = self.run(
            "-Y",
            filter_query,
            "-T",
            "fields",
            "-e",
            "frame.number",
        )
        out = process.stdout.decode()
        if out != "":
            return out.splitlines()
        return []
