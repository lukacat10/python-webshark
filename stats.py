import re

from loader_wrapper import TSharkPcapLoaderWrapper


class TSharkPcapStats(TSharkPcapLoaderWrapper):
    @property
    def size(self):
        return self.loader.capture_file_path.stat().st_size

    @property
    def stats(self):
        process = self.loader.run(
            "-qz",
            "io,stat,0,frame.number",
        )
        start_time, end_time, frame_number, byte_count = next(
            re.finditer(
                r"(?:\|\s*([0-9]*\.?[0-9]*)\s+(?:<>)?\s?(?:([0-9]*\.?[0-9]*)|(?:Dur))\s*(?:\|\s+([0-9]*)\s+)(?:\|\s+([0-9]*)\s+)+\|\r\n)",
                process.stdout.decode(),
            )
        ).groups()
        return start_time, end_time, frame_number, byte_count

    @property
    def frame_count(self):
        _, _, frame_number, _ = self.stats
        return int(frame_number)

    @property
    def duration(self):
        _, duration, _, _ = self.stats
        return float(duration)

    @property
    def name(self):
        return self.loader.capture_file_path.name

    def get_details(self):
        return {
            "file_name": self.name,
            "duration": round(self.duration),
            "file_size": self.size,
            "frame_count": self.frame_count,
        }
