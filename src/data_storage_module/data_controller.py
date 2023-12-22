import json
import os

from src.configuration import logger


class DataStorage:
    script_dir = os.path.dirname(os.path.abspath(__file__))

    COURSE = os.path.join(script_dir, "data/courses")
    TOPICS = os.path.join(script_dir, "data/topics")


class DataController:

    @staticmethod
    def _get_file_path(path: str, uuid: str) -> str:
        return os.path.join(path, f"{uuid}.json")

    @staticmethod
    def store_data(data, path, uuid):
        file_path = DataController._get_file_path(path, uuid)
        logger.info(f"Writing data to file: {file_path}")
        with open(file_path, "w") as file:
            file.write(json.dumps(data))

    def find_file(self, data_storage: str, target_file: str):
        target_file = f"{target_file}.json"
        for root, dirs, files in os.walk(data_storage):
            if target_file in files:
                return os.path.join(root, target_file)
        return None

    def get_data(self, uuid):
        file_path = self.find_file(DataStorage.script_dir, uuid)
        if not file_path:
            return None

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        return data
