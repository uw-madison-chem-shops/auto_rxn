__all__ = ["Recipe"]


import pathlib
from dataclasses import dataclass
from typing import Dict, Union, Any, List

import pandas as pd


@dataclass
class Step:
    length: Union[int, float]
    setpoints: Dict[str, Union[int, float]]


class Recipe:
    def __init__(self, filepath):
        self._df = pd.read_csv(filepath)
        self.control_point_ids = [
            k for k in self._df.keys()[1:] if not k.endswith("fallback_position")
        ]
        self.fallback_position_ids = [
            k for k in self._df.keys()[1:] if k.endswith("fallback_position")
        ]
        # read in metadata row by row, until see recipe start
        self.metadata: Dict[str, Dict[str, str]] = {k: {} for k in self.control_point_ids}
        row_index = 0
        while True:
            row = self._df.loc[row_index]
            if row["Control Point ID"] == "RECIPE_STARTS_BELOW":
                break
            else:
                key = row["Control Point ID"]
                for id in self.control_point_ids:
                    self.metadata[id][key] = row[id]
            row_index += 1
        # now the rest of the dataframe contains recipe steps
        self.steps: List[Step] = []
        self.fallback_positions: List[Step] = []
        row_index += 1
        while True:
            try:
                row = self._df.loc[row_index]
                # setpoints
                length = row["Control Point ID"]
                setpoints = {k: row[k] for k in self.control_point_ids}
                step = Step(length=length, setpoints=setpoints)
                self.steps.append(step)
                # fallback positions
                setpoints = {
                    k.removesuffix(".fallback_position"): row[k]
                    for k in self.fallback_position_ids
                }
                step = Step(length=length, setpoints=setpoints)
                self.fallback_positions.append(step)
                row_index += 1
            except KeyError:
                break
        # attempt to coerce all to float
        for step in self.steps:
            for k, v in step.setpoints.items():
                try:
                    step.setpoints[k] = float(v)
                except ValueError:
                    continue
        for step in self.fallback_positions:
            for k, v in step.setpoints.items():
                try:
                    step.setpoints[k] = float(v)
                except ValueError:
                    continue

    def save(self, filepath) -> pathlib.Path:
        path = pathlib.Path(filepath)
        self._df.to_csv(path, index=False)
        return path
