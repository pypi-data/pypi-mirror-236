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

import requests

from pinkman.module.database import Database


class Backend:
    """Backend Class"""

    def __init__(self):
        pass

    def log(self, message):
        print(
            "New message received with id {} and from {}".format(
                message.id, message.mailfrom
            )
        )

        return True

    def http(self, remote, message):
        data = {
            "id": message.id,
            "mailfrom": message.mailfrom,
            "rcpttos": message.rcpttos,
            "data": message.data,
            "mailOptions": message.mail_options,
            "rcptOptions": message.rcpt_options,
            "createdAt": message.created_at,
            "updatedAt": message.updated_at,
        }

        headers = {
            "Content-Type": "application/json",
            "X-API-Key": remote.apikey,
        }

        if remote.method.upper() == "PUT":
            try:
                response = requests.put(remote.url, headers=headers, json=data)
            except Exception as e:
                raise Exception("Remote backend responds with error: {}".format(str(e)))

            if response.status_code // 100 != 2:
                raise Exception(
                    "Remote backend responds with invalid status code {}".format(
                        response.status_code
                    )
                )

        else:
            try:
                response = requests.post(remote.url, headers=headers, json=data)
            except Exception as e:
                raise Exception("Remote backend responds with error: {}".format(str(e)))

            if response.status_code // 100 != 2:
                raise Exception(
                    "Remote backend responds with invalid status code {}".format(
                        response.status_code
                    )
                )

        return True
