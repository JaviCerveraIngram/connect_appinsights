from logging import getLogger, Formatter, ERROR, WARNING, INFO, DEBUG, CRITICAL
from typing import Optional

# noinspection PyPackageRequirements
from connect.logger import ILoggerWriter, Logger
# noinspection PyPackageRequirements
from connect.models import IdModel
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
        self.logger = getLogger(self.__class__.LOGGER_NAME)
        self.extra = None
        config_integration.trace_integrations(['logging', 'requests'])
        if key:
            tracer = Tracer(
                exporter=AzureExporter(connection_string=key),
                sampler=AlwaysOnSampler()
            )
            handler = AzureLogHandler(connection_string=key)
            handler.setFormatter(Formatter('%(message)s'))
            self.logger.setLevel(INFO)
            self.logger.addHandler(handler)
            self.logger.propagate = False
            self._init(tracer, handler)
    
    def _init(self, tracer: Tracer, handler: AzureLogHandler) -> None:
        self.tracer = tracer
        self.handler = handler

    # noinspection PyMethodMayBeStatic,PyPep8Naming
    def setFilename(self, _: str) -> bool:
        return False

    # noinspection PyMethodMayBeStatic,PyPep8Naming
    def getFilename(self) -> str:
        return ''

    # noinspection PyPep8Naming
    def writeLine(self, level: int, line: str) -> None:
        levels = {
            Logger.LEVEL_ERROR: ERROR,
            Logger.LEVEL_WARNING: WARNING,
            Logger.LEVEL_INFO: INFO,
            Logger.LEVEL_DEBUG: DEBUG
        }
        python_level = levels[level] if level in levels else CRITICAL
        self.logger.log(python_level, line, extra=self.extra)

    def copy(self, request: Optional[IdModel]) -> ILoggerWriter:
        writer = AzureLoggerWriter('')
        writer._init(self.tracer, self.handler)
        if request:
            writer.extra = {
                'custom_dimensions': {
                    'Request': request.id,
                    'Provider': self._get_request_provider_id(request),
                    'Hub': self._get_request_hub_id(request),
                    'Marketplace': self._get_request_marketplace_id(request),
                    'Product': self._get_request_product_id(request),
                    'TierAccount': self._get_request_tier_account_id(request),
                    'Connection': self._get_request_connection_id(request),
                    'Vendor': self._get_request_vendor_id(request),
                    'ExternalId': self._get_request_external_id(request),
                }
            }
        else:
            writer.extra = None
        return writer

    @staticmethod
    def _get_request_provider_id(request: Optional[IdModel]) -> Optional[str]:
        provider = request.provider if hasattr(request, 'provider') else \
            request.asset.connection.provider if hasattr(request, 'asset') else \
            request.configuration.connection.provider if hasattr(request, 'configuration') else \
            None
        return provider.id if provider else None

    @staticmethod
    def _get_request_hub_id(request: Optional[IdModel]) -> Optional[str]:
        hub = request.asset.connection.hub if hasattr(request, 'asset') else \
            request.configuration.connection.hub if hasattr(request, 'configuration') else \
            None
        return hub.id if hub else None

    @staticmethod
    def _get_request_marketplace_id(request: Optional[IdModel]) -> Optional[str]:
        marketplace = request.marketplace if hasattr(request, 'marketplace') else \
            request.contract.marketplace if hasattr(request, 'contract') else \
            request.configuration.marketplace if hasattr(request, 'configuration') else \
            None
        return marketplace.id if marketplace else None

    @staticmethod
    def _get_request_product_id(request: Optional[IdModel]) -> Optional[str]:
        product = request.product if hasattr(request, 'product') else \
            request.asset.product if hasattr(request, 'asset') else \
            request.configuration.product if hasattr(request, 'configuration') else \
            None
        return product.id if product else None

    @staticmethod
    def _get_request_tier_account_id(request: Optional[IdModel]) -> Optional[str]:
        tier_account = request.asset.tiers.customer if hasattr(request, 'asset') else \
            request.configuration.account if hasattr(request, 'configuration') else \
            None
        return tier_account.id if tier_account else None

    @staticmethod
    def _get_request_connection_id(request: Optional[IdModel]) -> Optional[str]:
        connection = request.asset.connection if hasattr(request, 'asset') else \
            request.configuration.connection if hasattr(request, 'configuration') else \
            None
        return connection.id if connection else None

    @staticmethod
    def _get_request_vendor_id(request: Optional[IdModel]) -> Optional[str]:
        vendor = request.vendor if hasattr(request, 'vendor') else \
            request.asset.connection.vendor if hasattr(request, 'asset') else \
            request.configuration.connection.vendor if hasattr(request, 'configuration') else \
            None
        return vendor.id if vendor else None

    @staticmethod
    def _get_request_external_id(request: Optional[IdModel]) -> Optional[str]:
        return request.externalId if hasattr(request, 'externalId') else \
            request.asset.externalId if hasattr(request, 'asset') else \
            None
