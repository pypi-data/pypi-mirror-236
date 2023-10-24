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

import smtpd
import uuid

from pinkman.model.message import Message


class Mailbox(smtpd.SMTPServer):
    """Mailbox Module"""

    def __init__(self, configs, database):
        super().__init__(
            (configs["server"]["hostname"], configs["server"]["port"]), None
        )
        self.configs = configs
        self.database = database

    def process_message(
        self, peer, mailfrom, rcpttos, data, mail_options=[], rcpt_options=[]
    ):
        message = Message(
            str(uuid.uuid4()),
            mailfrom,
            rcpttos,
            data.decode("utf-8"),
            mail_options,
            rcpt_options,
            "PENDING",
            None,
            None,
        )

        self.database.insert_message(message)
