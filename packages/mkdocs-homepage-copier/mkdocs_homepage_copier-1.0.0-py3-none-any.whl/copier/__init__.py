import os
import shutil

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin


class HomepageCopier(BasePlugin):
    config_scheme = (
        ("src", config_options.Type(str, default="README.md")),
        ("dest", config_options.Type(str, default="docs/index.md")),
        ("copy", config_options.Type(bool, default=True)),
        ("extras", config_options.Type(list, default=[])),
    )

    def clean_up(self):
        if os.path.exists(self.config["dest"]):
            os.remove(self.config["dest"])

        for extra in self.config["extras"]:
            if os.path.exists(extra["dest"]):
                os.remove(extra["dest"])

    def on_config(self, config):
        self.clean_up()

        if self.config["copy"]:
            shutil.copy(self.config["src"], self.config["dest"])

        for extra in self.config["extras"]:
            if "copy" not in extra or extra["copy"]:
                shutil.copy(extra["src"], extra["dest"])

        return config

    def on_post_build(self, config):
        self.clean_up()

    def on_build_error(self, error):
        self.clean_up()
