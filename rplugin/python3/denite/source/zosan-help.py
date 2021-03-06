from .base import Base
from itertools import filterfalse
from denite.base.kind import Base as Kind
from denite.kind.openable import Kind as Openable
from typing import Any
from pathlib import Path
from denite import util, process
from os.path import exists
import json


class Source(Base):
    def __init__(self, vim: Any) -> None:
        super().__init__(vim)
        self.name = 'zosan-help'
        self.library_name = vim.eval('g:zotero_filename')

    def on_init(self, context: dict) -> None:
        context['__proc'] = None

    def on_close(self, context: dict) -> None:
        if context['__proc']:
            context['__proc'].kill()
            context['__proc'] = None

    def gather_candidates(self, context: Any) -> list:
        try:
            with open(self.library_name) as fp:
                data_set = json.load(fp)
            data_set = list(filter(lambda x: 'title' in x, data_set))
            data_set = list(filter(lambda x: 'abstract' in x, data_set))
            self.data = [{'word': x['title'],
                          'abbr': x['title']}
                         for x in data_set]
            return self.data
        except FileNotFoundError:
            return [{'word':
                     'There is no Zotero file. Is there Zotero file..?'}]
        except:
            return [{'word': 'Something went wrong.'}]
