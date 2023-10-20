from dataclasses import dataclass

@dataclass
class TurpCounter:

    specimen_weight: int
    num_cassette_low_end: int = 6
    num_cassette_high_end: int = 8

    def __post_init__(self) -> None:
        x = len([n for n in range(12, max(12, self.specimen_weight), 5)])

        self.num_cassette_low_end += x
        self.num_cassette_high_end += x