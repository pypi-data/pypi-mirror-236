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


class Message:
    """Message Model"""

    def __init__(
        self,
        id,
        mailfrom,
        rcpttos,
        data,
        mail_options,
        rcpt_options,
        status,
        created_at,
        updated_at,
    ):
        self._id = id
        self._mailfrom = mailfrom
        self._rcpttos = rcpttos
        self._data = data
        self._mail_options = mail_options
        self._rcpt_options = rcpt_options
        self._status = status
        self._created_at = created_at
        self._updated_at = updated_at

    @property
    def id(self):
        return self._id

    @property
    def status(self):
        return self._status

    @property
    def mailfrom(self):
        return self._mailfrom

    @property
    def rcpttos(self):
        return self._rcpttos

    @property
    def data(self):
        return self._data

    @property
    def mail_options(self):
        return self._mail_options

    @property
    def rcpt_options(self):
        return self._rcpt_options

    @property
    def created_at(self):
        return self._created_at

    @property
    def updated_at(self):
        return self._updated_at

    @status.setter
    def status(self, status):
        self._status = status

    @mailfrom.setter
    def mailfrom(self, mailfrom):
        self._mailfrom = mailfrom

    @rcpttos.setter
    def rcpttos(self, rcpttos):
        self._rcpttos = rcpttos

    @data.setter
    def data(self, data):
        self._data = data

    @mail_options.setter
    def mail_options(self, mail_options):
        self._mail_options = mail_options

    @rcpt_options.setter
    def rcpt_options(self, rcpt_options):
        self._rcpt_options = rcpt_options
