from logging import getLogger, Formatter

# noinspection PyPackageRequirements
from connect.logger import ILoggerWriter
# noinspection PyPackageRequirements
from opencensus.ext.azure.log_exporter import AzureLogHandler
# noinspection PyPackageRequirements
from opencensus.ext.azure.trace_exporter import AzureExporter
# noinspection PyPackageRequirements
from opencensus.trace import config_integration
# noinspection PyPackageRequirements
from opencensus.trace.samplers import AlwaysOnSampler
# noinspection PyPackageRequirements
from opencensus.trace.tracer import Tracer


class AzureLoggerWriter(ILoggerWriter):
    LOGGER_NAME = 'appinsights-logger'

    def __init__(self, key: str):
        super().__init__()
        self.tracer = None
        self.handler = None
        config_integration.trace_integrations(['logging', 'requests'])
        if key:
            tracer = Tracer(
                exporter=AzureExporter(connection_string=key),
                sampler=AlwaysOnSampler()
            )
            handler = AzureLogHandler(connection_string=key)
            handler.setFormatter(Formatter('%(message)s'))
            logger = getLogger(self.__class__.LOGGER_NAME)
            logger.addHandler(handler)
            logger.propagate = False
            self._init(tracer, handler)
    
    def _init(self, tracer: Tracer, handler: AzureLogHandler) -> None:
        self.tracer = tracer
        self.handler = handler
    
    def copy(self) -> ILoggerWriter:
        writer = AzureLoggerWriter('')
        writer._init(self.tracer, self.handler)
        return writer

    # noinspection PyMethodMayBeStatic,PyPep8Naming
    def getFilename(self) -> str:
        return ''

    # noinspection PyMethodMayBeStatic,PyPep8Naming
    def setFilename(self, _: str) -> bool:
        return False

    # noinspection PyPep8Naming
    def writeLine(self, line: str) -> None:
        getLogger(self.__class__.LOGGER_NAME).info(line)
