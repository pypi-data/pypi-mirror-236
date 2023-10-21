# Account to card implementation with Universal bank

Support Group - <a href="https://t.me/+Ng1axYLNyBAyYTRi">Telegram</a> <br/>

## Installation

```shell
pip install ubk-pkg
```

### Test-Credentials

```
Card Numer: 8600 4829 5296 4119
Card Numer: 9860 2301 0122 3272
```

## Documentation
- [Account2Card](#account2card)
- [StatusCheck](#statuscheck)
- [CancelCheck](#cancelcheck)

# Methods

## Account2Card

```python
from pprint import pprint

from ubk.client import UniPosAPI
from ubk.types.request import RequestTransferCreditCreate


ubk_client = UniPosAPI(
    url="api-url",
    token="access-token"
)

resp = ubk_client.account2card(
    params=RequestTransferCreditCreate(
        number="8600482952964119",
        amount=1000
    )
)

resp_data = resp.to_dict()

pprint(resp_data)
```

## StatusCheck

```python
from pprint import pprint

from ubk.client import UniPosAPI
from ubk.types.request import RequestTransferCreditState


ubk_client = UniPosAPI(
    url="api-url",
    token="access-token"
)

resp = ubk_client.status_check(
    params=RequestTransferCreditState(
        ext_id="ext_id",
    )
)

resp_data = resp.to_dict()

pprint(resp_data)
```

## CancelCheck

```python
from pprint import pprint

from ubk.client import UniPosAPI
from ubk.types.request import RequestTransferCreditCancel


ubk_client = UniPosAPI(
    url="api-url",
    token="access-token"
)

resp = ubk_client.cancel_check(
    params=RequestTransferCreditCancel(
        ext_id="ext_id"
    )
)

resp_data = resp.to_dict()

pprint(resp_data)

```