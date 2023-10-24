"""A module to connect to yaml files or yaml strings"""
import os
from typing import Optional
import yaml
from TableauConMan.helpers import utils


class YamlConnector:
    """Class representing a connection to a yaml file or yaml string"""

    def __init__(
        self, file_path: Optional[str] = None, yaml_string: Optional[str] = None
    ):
        """

        :param file_path:
        :param yaml:
        """
        self._file_path = file_path
        self._yaml_string = yaml_string

    @property
    def file_path(self) -> Optional[str]:
        """

        :return:
        """
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        """

        :param value:
        """
        self._file_path = value

    @property
    def yaml_string(self) -> Optional[str]:
        """

        :return:
        """
        return self._yaml_string

    @yaml_string.setter
    def yaml_string(self, value):
        """

        :param value:
        """
        self._yaml_string = value

    def get_yaml(self):
        """

        :param object:
        :return:
        """
        if self._file_path is not None:
            file_path_parts = os.path.split(self._file_path)
            search_path = file_path_parts[0]
            file_name = file_path_parts[1]
            jinja_environment = utils.get_jinja_environment(search_path)

            try:
                file_text_list = yaml.safe_load(
                    jinja_environment.get_template(file_name).render()
                )
                return file_text_list
            except yaml.YAMLError as exc:
                print(exc)
                return None

        elif self._yaml_string is not None:
            jinja_environment = utils.get_jinja_environment("string")
            file_text = self._yaml_string
            try:
                file_text_list = yaml.safe_load(
                    jinja_environment.from_string(file_text).render()
                )
                return file_text_list
            except yaml.YAMLError as exc:
                print(exc)
                return None
