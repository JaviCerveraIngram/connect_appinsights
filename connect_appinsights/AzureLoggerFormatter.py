from typing import Optional

# noinspection PyPackageRequirements
from connect.logger import ILoggerFormatter, ILoggerWriter
# noinspection PyPackageRequirements
from connect.models import IdModel
# noinspection PyPackageRequirements
from connect.util import Collection


class AzureLoggerFormatter(ILoggerWriter):
    def __init__(self, request: Optional[IdModel] = None):
        super().__init__()
        self.current_request = '' if not request else (request.id + ' ')

    # noinspection PyPep8Naming
    def formatSection(self, _: int, sectionLevel: int, text: str) -> str:
        prefix = (''.rjust(sectionLevel, '#') + ' ') if sectionLevel > 0 else ''
        return self.current_request + prefix + text

    # noinspection PyPep8Naming
    def formatBlock(self, _: int, text: str) -> str:
        return self._maybe_eol() + text

    def _maybe_eol(self):
        return '\n' if self.current_request != '' else ''

    # noinspection PyPep8Naming
    def formatCodeBlock(self, _: int, text: str, __: str) -> str:
        return self._maybe_eol() + text

    # noinspection PyPep8Naming
    def formatList(self, _: int, list_: Collection) -> str:
        return self._maybe_eol() + list_.join('\n')

    # noinspection PyPep8Naming
    def formatTable(self, _: int, table: Collection) -> str:
        rows = [('| ' + row.join(' | ') + ' |') for row in table]
        return self._maybe_eol() + '\n'.join(rows)

    # noinspection PyPep8Naming
    def formatLine(self, _: int, text: str) -> str:
        return self.current_request + text

    # noinspection PyPep8Naming,PyMethodMayBeStatic
    def getFileExtension(self) -> str:
        return 'log'

    # noinspection PyPep8Naming,PyMethodMayBeStatic,PyTypeChecker
    def copy(self, request: Optional[IdModel]) -> ILoggerFormatter:
        return AzureLoggerFormatter(request)
