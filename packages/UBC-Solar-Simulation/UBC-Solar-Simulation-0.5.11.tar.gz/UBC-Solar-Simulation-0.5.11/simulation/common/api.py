from abc import ABC, abstractmethod
import os
import numpy as np


class API(ABC):
    def __init__(self, key, name, simulation_hash):
        self.api_key = key
        self.api_name = name
        self.simulation_hash = simulation_hash

    @abstractmethod
    def download(self):
        input(f"Simulation would like to call {self.api_name}. Confirm by pressing any key.")
        raise NotImplementedError

    def retrieve_from_cache(self, cache_path) -> (dict, bool):
        # if the file exists, load path from file
        if os.path.isfile(cache_path):
            with np.load(cache_path) as cached_data:
                if np.array_equal(cached_data['hash_key'], self.simulation_hash):
                    return cached_data, True
        return None, False

