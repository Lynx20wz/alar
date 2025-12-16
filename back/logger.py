import sys
from loguru import logger

logger.remove()
logger.add(
    sink=sys.stdout,
    level='INFO',
    format='{time:H:mm:ss} | "{function}" | {line} ({module}) | <level>{level}</level> | {message}',
)
