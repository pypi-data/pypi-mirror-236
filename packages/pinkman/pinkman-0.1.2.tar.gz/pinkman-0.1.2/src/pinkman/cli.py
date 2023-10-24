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

from pinkman import __version__
from pinkman.command.worker import Worker
from pinkman.command.server import Server


@click.group(help="🐺 An SMTP Server to forward Messages into A Backend System")
@click.version_option(version=__version__, help="Show the current version")
def main():
    pass


# Server command
@click.group(help="Server commands")
def server():
    pass


# Run server sub command
@server.command(help="Run the server")
@click.option(
    "-c",
    "--config",
    "config",
    type=click.STRING,
    default="",
    help="Server config file",
)
def run(config):
    return Server().run(config)


# Worker command
@click.group(help="Worker commands")
def worker():
    pass


# Run worker sub command
@worker.command(help="Run the worker")
@click.option(
    "-c",
    "--config",
    "config",
    type=click.STRING,
    default="",
    help="Server config file",
)
def run(config):
    return Worker().run(config)


# Register Commands
main.add_command(server)
main.add_command(worker)


if __name__ == "__main__":
    main()
