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

import json
import sqlite3

from pinkman.model.message import Message


class Database:
    """Database Class"""

    def connect(self, path):
        self.path = path

        self._connection = sqlite3.connect(self.path)

        return self._connection.total_changes

    def migrate(self):
        cursor = self._connection.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS mailbox (id TEXT, message TEXT, status TEXT, createdAt TEXT, updatedAt TEXT)"
        )

        cursor.close()

        self._connection.commit()

    def insert_message(self, message):
        cursor = self._connection.cursor()

        result = cursor.execute(
            "INSERT INTO mailbox VALUES (?, ?, ?, datetime('now'), datetime('now'))",
            (
                message.id,
                json.dumps(
                    {
                        "mailfrom": message.mailfrom,
                        "rcpttos": message.rcpttos,
                        "data": message.data,
                        "mail_options": message.mail_options,
                        "rcpt_options": message.rcpt_options,
                    }
                ),
                message.status,
            ),
        )

        cursor.close()

        self._connection.commit()

        return result.rowcount

    def update_message_status(self, id, status):
        cursor = self._connection.cursor()

        result = cursor.execute(
            "UPDATE mailbox SET status = ? WHERE id = ?", (status, id)
        )

        cursor.close()

        self._connection.commit()

        return result.rowcount

    def filter_messages(self, status, limit=10):
        result = []

        cursor = self._connection.cursor()

        rows = cursor.execute(
            "SELECT id, message, status, createdAt, updatedAt FROM mailbox WHERE status = ? LIMIT ?",
            (status, limit),
        ).fetchall()

        cursor.close()

        for row in rows:
            data = json.loads(row[1])

            message = Message(
                row[0],
                data["mailfrom"],
                data["rcpttos"],
                data["data"],
                data["mail_options"],
                data["rcpt_options"],
                row[2],
                row[3],
                row[4],
            )

            result.append(message)

        return result

    def delete_message(self, id):
        cursor = self._connection.cursor()

        cursor.execute("DELETE FROM mailbox WHERE id = ?", (id,))

        cursor.close()

        self._connection.commit()
