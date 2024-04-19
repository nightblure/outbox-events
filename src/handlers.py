import logging

from src.events import Event2, Event1

logger = logging.getLogger(__name__)


def e1_handler(e: Event1):
    logger.warning('Success handling of event 1!')
    logger.info('Event data:')
    logger.info(e)


def e2_handler(e: Event2):
    logger.warning('Success handling of event 2!')
    logger.info('Event data:')
    logger.info(e)
