# coinraven - wrapper to send and service cyptocurrencies easily


**This tool is still in development and currently not intended to be used for production!**

Coinraven is a simple wrapper over richard kiss' [Pycoin](https://github.com/richardkiss/pycoin/). It makes sending and receving bitcoins easily by providing a easy and flexible interface.


## How to use?


### Initialize coin

```pycon
>>> from coinraven.coins import Bitcoin
>>> from coinraven.services import InsightAPI
>>>
>>> network_apis = [InsightAPI("XTN"), ]
>>>
>>> bitcoin = Bitcoin(PRIVATE_KEY_HERE, network_apis, testnet=True)
```

### Basic tasks

```pycon
>>> bitcoin.address
'myFv99uppGLqtLp4ckEr4mF7fc8pww7AFQ'
>>>
>>> bitcoin.get_unspents()
[Spendable<997.9 mbtc "5e28dd9d1ca501215aa00985b657e6b0d2c64ae0cea3ce4d274c4d9095d7c9f7:1" 0/0/0>]
>>>
>>> bitcoin.get_transactions()
[Tx [5e28dd9d1ca501215aa00985b657e6b0d2c64ae0cea3ce4d274c4d9095d7c9f7] (v:1) [TxIn<816e2f6ff0ab93fca0e4829215a6b8c340ac1c7366a8fd76d26f7c579d103fe3[0] "[30450221008de574f23979e260ce85bb19ce9aa2b6ff6bd8dec6850fb4c4eba5fe10e88a6f02207bb5cfc781e248edd417227569ce3defcb51a69fdb45f442e9ac8fdca3f0d49e01] [04310bad914811a05626bb568d1d18506a6ac8894bf2ee308e4efee94cde9ea8a19901fed10c5c70cec59fdef4330969a8857f77f1a4dbebf98aa3599a55b39623]">, TxIn<62c0ea8c82a2dbef93bd77c4656295147413c90fb2c36e977a6a82f53383cbf8[1] "[304402204f536fed45159c6f3846721f592ff8f1981b6f5a4403b1b29c65193d3801f1aa022058f2f509e876a7aeec3b64dbd5b0a7f2d1dd918492da0b4adfed2985919bfe7801] [04310bad914811a05626bb568d1d18506a6ac8894bf2ee308e4efee94cde9ea8a19901fed10c5c70cec59fdef4330969a8857f77f1a4dbebf98aa3599a55b39623]">] [TxOut<3E+2 mbtc "OP_DUP OP_HASH160 [7a33d860e213e3f91847bf2c7461790306233b0f] OP_EQUALVERIFY OP_CHECKSIG">, TxOut<997.9 mbtc "OP_DUP OP_HASH160 [c29a3a21dd8fa1af74f23ac2f5c22abdd873f792] OP_EQUALVERIFY OP_CHECKSIG">], Tx [816e2f6ff0ab93fca0e4829215a6b8c340ac1c7366a8fd76d26f7c579d103fe3] (v:1) [TxIn<62c0ea8c82a2dbef93bd77c4656295147413c90fb2c36e977a6a82f53383cbf8[0] "[304402206bb88ecfd822dad6dedf87a7bf0014a13a900bd146caba421df8fc66dd29130b0220240446278e68f6e78aba1b04e98a719c9bd75d603f981dcbebf5ee0ff15877b101] [04d433fc444cd044a70cb733be978939e4632dfef3b9a6918f0257dae240455b5c30209b9ff9cf8c8f73e4ef9815646429574d0c95749e2f35f21b2207b1b24ceb]">] [TxOut<299 mbtc "OP_DUP OP_HASH160 [c29a3a21dd8fa1af74f23ac2f5c22abdd873f792] OP_EQUALVERIFY OP_CHECKSIG">], Tx [62c0ea8c82a2dbef93bd77c4656295147413c90fb2c36e977a6a82f53383cbf8] (v:1) [TxIn<1b509d9256d1dda4069b4b9c89e24c41e1f347f798830f13b186231a8ae84bd6[0] "[3045022100ca6b7fe6eb12f30c7b87ad30c39fba73d21b9942327cd6c835ad0939ea8e237f022018361532ca7d550cc817fe0bce6650972f13dce5305b8ca4c6bccaec54ed288e01] [04310bad914811a05626bb568d1d18506a6ac8894bf2ee308e4efee94cde9ea8a19901fed10c5c70cec59fdef4330969a8857f77f1a4dbebf98aa3599a55b39623]">] [TxOut<3E+2 mbtc "OP_DUP OP_HASH160 [7a33d860e213e3f91847bf2c7461790306233b0f] OP_EQUALVERIFY OP_CHECKSIG">, TxOut<999.9 mbtc "OP_DUP OP_HASH160 [c29a3a21dd8fa1af74f23ac2f5c22abdd873f792] OP_EQUALVERIFY OP_CHECKSIG">], Tx [1b509d9256d1dda4069b4b9c89e24c41e1f347f798830f13b186231a8ae84bd6] (v:1) [TxIn<362cd31fd5600d1812077150333e80cb8763be7cba622ba42984c965f9924fff[1] "[0014641bee314c4f2532c6452d61a614edab65f06fd4]">] [TxOut<1.3E+3 mbtc "OP_DUP OP_HASH160 [c29a3a21dd8fa1af74f23ac2f5c22abdd873f792] OP_EQUALVERIFY OP_CHECKSIG">, TxOut<1953296.02362 mbtc "OP_HASH160 [b04b134f14739f78f3199f681fe74443455ff90a] OP_EQUAL">]]
>>>
```

### Send coins

```pycon
>>> from coinraven.tx import Payable
>>> payables = [Payable("mrf6qj7huouMtg3t5SUJkWnGHJ2XjfgwtW", 4 * 1e7),]
>>>
>>> bitcoin.send(payables, 2000000)
'{"txid":"8049f018e70b80a4b8cf261b8117bffda6973c2e067e479b607e7c924f447b79"}'
>>>
```

The above code sends 0.4 bitcoins to `mrf6qj7huouMtg3t5SUJkWnGHJ2XjfgwtW` with `0.02` bitcoins as fee and returns the leftover bitcoins to the sender address (`bitcoin.address`) if `change_address` is not passed. All values are in satoshis.

You can see the transaction [here](https://test-insight.bitpay.com/tx/8049f018e70b80a4b8cf261b8117bffda6973c2e067e479b607e7c924f447b79).
