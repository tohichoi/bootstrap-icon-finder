from pathlib import Path

class IconInfo:
    def __init__(self, icon_path : Path = None):
        self.vendor: str = None
        self.file_name: str = None
        self.file_path: Path = None
        self.icon_name: str = None
        self.icon_class: str = None
        self.categories: set = set()
        self.tags: set = set()
        self.styles: set = set()
        self.friendly_name: str = None

        if icon_path:
            self.parse_icon_path(icon_path)

    def parse_icon_path(self, icon_file_path):
        self.vendor = 'bi' if 'bootstrap' in str(icon_file_path) else 'fa'
        self.file_name = icon_file_path.with_suffix('.svg').name
        self.file_path = icon_file_path
        self.icon_name = str(icon_file_path.with_suffix('').name)
        self.icon_class = self.vendor + '-' + self.icon_name
        self.categories = set()
        self.tags = set()

    def __str__(self):
        return f"{self.icon_class}"
