from dataclasses import dataclass, asdict

@dataclass
class Indicator:
    key: str
    state: str
    label: str = ''

    def __post_init__(self):
        self.label = self.key if self.label == '' else self.label

    def to_dict(self):
        return { self.key: asdict(self)}