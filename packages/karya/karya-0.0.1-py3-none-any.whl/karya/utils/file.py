import json
import os
import secrets
import string
import zipfile
from typing import List

import pathspec
import requests
import yaml

from .config import Config


class FileTree:
    PATHSPEC_PRESEDENCE_ORDER: List[str] = [
        ".nuignore",
        ".gitignore",
        ".dockerignore",
    ]

    def __init__(self):
        self.__load_path_spec()

    def __load_path_spec(self):
        spec_text: str = ""

        for pathspec_file in self.PATHSPEC_PRESEDENCE_ORDER:
            if os.path.isfile(pathspec_file):
                with open(pathspec_file) as file:
                    spec_text = file.read()
                    break

        self.spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, spec_text.splitlines())

    def get_tree(self) -> List[str]:
        return [file_path for file_path in self.spec.match_tree("./", negate=True)]


class Zipper:
    ZIP_BASE_DIRECTORY = "/tmp/"

    def __init__(self):
        self.file_paths: List[str] = FileTree().get_tree()
        self.zip_file_name: str = (
            f"open_nu_zip_"
            + "".join(
                [secrets.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(5)]
            )
            + ".zip"
        )

    def zip_files(self):
        zip_file = zipfile.ZipFile(self.ZIP_BASE_DIRECTORY + self.zip_file_name, mode="w")

        for file_path in self.file_paths:
            zip_file.write(file_path)

        zip_file.close()

    def upload_zip(self):
        config = None
        input_params = None
        # input_params
        with open("config.yaml", "r") as file:
            config = yaml.load(file, Loader=yaml.Loader)
        if os.path.exists("args.json"):
            with open("args.json", "r") as file:
                input_params = json.load(file)

        base_url = Config.get_base_url()
        auth_key = Config.get_auth_key()

        payload = {"config": config, "input_params": input_params}
        files = [("file", ("code.zip", open(self.ZIP_BASE_DIRECTORY + self.zip_file_name, "rb"), "zip"))]
        headers = {"X-Api-Key": auth_key}

        response = requests.request("POST", base_url, headers=headers, data=payload, files=files)


__all__ = ["Zipper"]
