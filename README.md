# MixRNG

XOR bits from inbuilt and hardware CSRNG. This process ensures that the quality of entropy gathered is a strong as the strongest source. 

Hardcoded settings for OneRNG, if using different hardware check serial settings first.

http://onerng.info

---

## Usage

```python
from MixRNG import mixrng, extrng

random_xor_bytes = mixrng(32)

random_mixrng_bytes_only = extrng(32)

```



