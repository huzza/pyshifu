from __future__ import absolute_import, division, print_function, unicode_literals
from pyshifu.core.shell import Shell

from pyshifu.core.exception.base_exception import ShifuException


class Shifu(Shell):
    def __init__(self):
        super(Shifu, self).__init__()

    def new(self, name, work_dir=None):
        try:
            self._init_working_directory(work_dir, name)
        except ShifuException as exception:
            print (exception.get_message())

    def init(self):
        self._run_command("init", "stats")

    def stats(self):
        self._run_command("stats", "norm")

    def norm(self):
        self._run_command("norm", "varsel")

    def varsel(self):
        self._run_command("varsel", "train")

    def train(self):
        self._run_command("train", "eval")

    def eval(self):
        self._run_command("eval")

