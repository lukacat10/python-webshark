from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass

from loader_wrapper import TSharkPcapLoaderWrapper
from tshark_loader import TSharkPcapLoader
from utils import norm


@dataclass
class ColorRule:
    filter_query: str
    background_color: list[int]
    foreground_color: list[int]


class TSharkPcapColors(TSharkPcapLoaderWrapper):
    def __init__(self, loader: TSharkPcapLoader) -> None:
        super().__init__(loader)
        with open("colors.txt", "r") as f:
            self.color_rules = f.read()

    @property
    def colors(self):
        result: list[ColorRule] = []
        for line in self.color_rules.splitlines():
            if not line.startswith("@"):
                continue
            _, name, filter_query, colors = line.split("@")
            bg_16bit, fg_16bit = colors.split("][")
            bg_16bit = bg_16bit[1:]
            fg_16bit = fg_16bit[:-1]
            foreground_color_8bit_arr = [norm(int(comp)) for comp in fg_16bit.split(",")]
            background_color_8bit_arr = [norm(int(comp)) for comp in bg_16bit.split(",")]
            result.append(
                ColorRule(
                    filter_query=filter_query,
                    background_color=background_color_8bit_arr,
                    foreground_color=foreground_color_8bit_arr,
                )
            )
        return result

    def _execute(self, filter_query: str, bg, fg):
        return self.loader.get_frames_with_filter(filter_query), bg, fg

    @property
    def frame_colors(self):
        frame_colors = {}
        tasks = [(rule.filter_query, rule.background_color, rule.foreground_color) for rule in self.colors]
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(self._execute, *task) for task in tasks]
            for future in as_completed(futures):
                result, background_color, foreground_color = future.result()
                for frame_number_str in result:
                    if frame_number_str not in frame_colors:
                        frame_colors[frame_number_str] = {
                            "foreground_color": foreground_color,
                            "background_color": background_color,
                        }
        return frame_colors
