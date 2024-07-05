from tshark_loader import TSharkPcapLoader


class TSharkPcapLoaderWrapper:
    def __init__(self, loader: TSharkPcapLoader) -> None:
        self.loader = loader
