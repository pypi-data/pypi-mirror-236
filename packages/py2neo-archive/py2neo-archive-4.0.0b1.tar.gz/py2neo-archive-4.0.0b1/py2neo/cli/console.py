#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright 2011-2017, Nigel Small
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import atexit
from code import InteractiveConsole
import codecs
from getpass import getpass
import readline
from os import getenv
import os.path
from platform import python_implementation, python_version, system
from sys import stderr, exit

from neo4j.v1 import ServiceUnavailable

from py2neo import GraphService, Unauthorized, Forbidden, __version__ as py2neo_version, CypherSyntaxError, \
    ClientError
from py2neo.cypher.lang import cypher_keywords, cypher_first_words

from .colour import cyan

WELCOME = """\
Py2neo {py2neo_version} ({python_implementation} {python_version} on {system})
Press [TAB] to auto-complete, type "/help" for more information or type
"/exit" to exit the console.
""".format(
    py2neo_version=py2neo_version,
    python_implementation=python_implementation(),
    python_version=python_version(),
    system=system(),
)
DEFAULT_HISTORY_FILE = os.path.expanduser("~/.py2neo_history")
DEFAULT_WRITE = stderr.write

HELP = """\
The py2neo console accepts both raw Cypher and slash commands and supports
basic auto-completion. Available slash commands are listed below:

/exit
/help
/play <cypher file>
/push (for adding parameters; not yet implemented)

Report bugs to py2neo@nige.tech
"""


class SimpleCompleter(object):

    node_labels = None
    relationship_types = None
    matches = None

    def __init__(self, graph_service, options):
        self.graph = graph_service.graph
        self.keywords = sorted(options)

    def complete(self, text, state):
        if state == 0:
            # This is the first time for this text, so build a match list.
            if text:
                self.node_labels = self.graph.node_labels
                self.relationship_types = self.graph.relationship_types
                dictionary = self.node_labels | self.relationship_types | set(self.keywords)
                upper_text = text.upper()
                self.matches = [word for word in dictionary if word and word.upper().startswith(upper_text)]
            else:
                self.matches = self.keywords[:]

        # Return the state'th item from the match list,
        # if we have that many.
        try:
            response = self.matches[state] + " "
        except IndexError:
            response = None
        return response


class Console(InteractiveConsole):

    services = None
    graph_service = None

    def __init__(self, write=DEFAULT_WRITE, history_file=DEFAULT_HISTORY_FILE):
        InteractiveConsole.__init__(self)
        self.write = write
        self.write(WELCOME)
        self.services = {}

        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(history_file)
            except IOError:
                pass

            def save_history():
                readline.set_history_length(1000)
                readline.write_history_file(history_file)

            atexit.register(save_history)

        self.connect("localhost", getenv("NEO4J_USER", "neo4j"), getenv("NEO4J_PASSWORD"))
        self.join("localhost")

    def interact(self, banner="", *args, **kwargs):
        InteractiveConsole.interact(self, banner, *args, **kwargs)

    def prompt(self):
        if self.buffer:
            return "\x01\x1b[32m\x02...\x01\x1b[0m\x02 "
        else:
            return "\x01\x1b[32;1m\x02>>>\x01\x1b[0m\x02 "

    def raw_input(self, prompt=""):
        return InteractiveConsole.raw_input(self, self.prompt())

    def runsource(self, source, filename="<input>", symbol="single"):
        try:
            source = source.lstrip()
            if not source:
                return 0
            words = source.strip().split()
            first_word = words[0]
            if first_word.startswith("/"):
                return self.run_slash_command(source)
            elif first_word.upper() in cypher_first_words:
                try:
                    return self.run_cypher_source(source)
                except CypherSyntaxError as error:
                    message = error.args[0]
                    if message.startswith("Unexpected end of input") or message.startswith("Query cannot conclude with"):
                        return 1
                    else:
                        self.write("Syntax Error: %s\n" % error.args[0])
                        return 0
            else:
                self.write("Syntax Error: Invalid input %s\n" % repr(first_word).lstrip("u"))
                return 0
        finally:
            self.write("\n")

    def run_cypher_source(self, source):
        try:
            result = self.graph_service.graph.run(source)
        except ClientError as error:
            self.write("{:s}\n".format(error))
            return 0
        else:
            plan = result.plan()

        result.dump(stderr, colour=True)

        if plan:
            self.write(cyan(repr(plan)))
            self.write("\n")
        return 0

    def run_slash_command(self, source):
        words = source.strip().split()
        command = words[0].lower()
        if command == "/help":
            self.help()
        elif command == "/exit":
            exit(0)
        elif command == "/connect":
            self.connect(words[1])
        elif command == "/push":
            pass  # push params
        elif command == "/play":
            with codecs.open(words[1], encoding="utf-8") as fin:
                source = fin.read()
            return self.run_cypher_source(source)
        else:
            self.write("Syntax Error: Invalid slash command '%s'\n" % command)
        return 0

    def help(self):
        self.write(HELP)

    def connect(self, host, user="neo4j", password=None):
        while True:
            graph_service = GraphService(host=host, user=user, password=password, bolt=True)
            try:
                _ = graph_service.kernel_version
            except Unauthorized:
                password = getpass("Enter password for user %s: " % user)
            except Forbidden:
                if graph_service.password_change_required():
                    self.write("Password expired\n")
                    new_password = getpass("Enter new password for user %s: " % user)
                    password = graph_service.change_password(new_password)
                else:
                    raise
            except ServiceUnavailable:
                self.write("Cannot connect to %s\n" % graph_service.address.host)
                exit(1)
            else:
                self.write("Connected to %s\n" % host)
                self.services[host] = graph_service
                return

    def join(self, host):
        self.graph_service = self.services[host]
        readline.set_completer(SimpleCompleter(self.graph_service, cypher_keywords).complete)


def main():
    Console().interact()
