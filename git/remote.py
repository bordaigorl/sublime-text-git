from __future__ import absolute_import, unicode_literals, print_function, division

import sublime
from . import GitWindowCommand

class GitRemoteCommand(GitWindowCommand):

    def list_remote(self):
        self.run_command(['git', 'remote', '-v'], self.show_remote)

    def show_remote(self, result):
        _remote_hash = {}
        for line in result.strip().split('\n'):
            remote_name, remote_url = [ field.strip() for field in line.split()[:2]]
            _remote_hash[remote_name] = remote_url

        self.results = [ list(item) for item in _remote_hash.items() ]
        self.quick_panel(self.results, self.panel_done, sublime.MONOSPACE_FONT)

    def panel_done(self, picked):
        print(picked)


class GitRemoteAddCommand(GitRemoteCommand):
    def run(self):
        v = self.get_window().show_input_panel('Remote', '', self.remote_add, None, None)
        v.run_command("insert_snippet", {"contents": "${1:name} ${2:url}"})

    def remote_add(self, remote_string):
        if ' ' not in remote_string:
            sublime.status_message('Usage remote_name remote_url')
            return

        remote_params = [ param.strip() for param in remote_string.split(' ', 1)]

        self.run_command(['git', 'remote', 'add'] + remote_params)


class GitRemoteRemoveCommand(GitRemoteCommand):
    def run(self):
        self.list_remote()

    def panel_done(self, picked):
        if picked >= len(self.results) or picked < 0:
            return
        remote = self.results[picked]
        self.run_command(['git', 'remote' , 'rm', remote[0]])


class GitRemoteShowCommand(GitRemoteCommand):

    def run(self):
        self.list_remote()

    def panel_done(self, picked):
        if picked >= len(self.results) or picked < 0:
            return
        remote = self.results[picked]
        self.run_command(['git', 'remote' , 'show', remote[0]])
