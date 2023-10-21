import logging
from django.conf import settings

_logger = logging.getLogger(__name__)


ACCRETE_UI_ACTIONS_TEMPLATE = getattr(
    settings, 'ACCRETE_UI_ACTIONS_TEMPLATE',
    'ui/partials/actions.html'
)
