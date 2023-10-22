from fetchfox.apis import coingeckocom
from fetchfox.apis.cardano import muesliswap
from fetchfox.constants.book import (
    BOOK_TOKEN_ASSET_ID,
    BOOK_TOKEN_ASSET_NAME,
    BOOK_TOKEN_POLICY_ID,
    BOOK_TOKEN_FINGERPRINT,
)
from fetchfox.constants.currencies import ADA

policy_id = BOOK_TOKEN_POLICY_ID
asset_name = BOOK_TOKEN_ASSET_NAME
asset_id = BOOK_TOKEN_ASSET_ID
fingetprint = BOOK_TOKEN_FINGERPRINT

cardanoscan_url = f"https://cardanoscan.io/token/{asset_id}"
cexplorer_url = f"https://cexplorer.io/asset/{fingetprint}"
minswap_url = f"https://app.minswap.org/swap?currencySymbolA={policy_id}&tokenNameA={asset_name}&currencySymbolB=&tokenNameB="


def price() -> float:
    return muesliswap.price(asset_id)


def usd() -> float:
    return price() * coingeckocom.usd(ADA)
