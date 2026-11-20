from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEMO_CASES = ('length1_1', 'length1_2', 'length1_3', 'length2_1', 'length3_1')

@dataclass
class Config:
    output: Path = ROOT
    model: str = ''
    base_url: str = 'https://openai.rc.asu.edu/v1'
    max_tokens: int = 6000
    reasoning_effort: str = 'none'
    k: int = 5
    sample_rows: int = 12
    timeout: int = 120
    api_timeout: int = 3600
    replay_only: bool = False

CONFIG = Config()
