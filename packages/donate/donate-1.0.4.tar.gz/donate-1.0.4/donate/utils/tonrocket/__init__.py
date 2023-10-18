from .client import Client
from .testnet import Test_Client
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("started TonRocket")
logger.info("TonRocket - Crypto donate")