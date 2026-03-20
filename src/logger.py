from loguru import logger
import os

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

logger.add(
    "logs/research_log_{time}.log",
    rotation="5 MB",
    retention="7 days",
    level="INFO"
)


def get_logger():
    return logger
