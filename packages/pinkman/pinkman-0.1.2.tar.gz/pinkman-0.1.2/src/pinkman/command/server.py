# MIT License
#
# Copyright (c) 2023 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import click
import asyncore

from pinkman.module.file import File
from pinkman.module.config import Config
from pinkman.module.mailbox import Mailbox
from pinkman.module.database import Database


class Server:
    """Server Command Class"""

    def __init__(self):
        self.file = File()
        self.config = Config()
        self.database = Database()

    def run(self, config_path):
        self.config.load(config_path)

        configs = self.config.get_configs()

        if not self.file.exists(configs["cache"]["path"]):
            self.database.connect(configs["cache"]["path"])
            self.database.migrate()
        else:
            self.database.connect(configs["cache"]["path"])

        click.echo("Server is up and running!")

        server = Mailbox(configs, self.database)
        asyncore.loop()
