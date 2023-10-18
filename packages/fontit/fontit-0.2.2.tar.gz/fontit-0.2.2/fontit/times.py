import os
from pathlib import Path

this_repo_path = Path(os.path.abspath(__file__))
zh_default_font = this_repo_path.parent.joinpath('fonts').joinpath('times.ttf').absolute()
zh_default_font = str(zh_default_font)

