from ipfabric import IPFClient

from pynetcheck import EXTRA

IPF, CONFIGS = None, []


if "configs" in EXTRA:
    CONFIGS = EXTRA["configs"]
elif not EXTRA.get("help", False):
    # Initiliaze IPF Client
    IPF = IPFClient()
