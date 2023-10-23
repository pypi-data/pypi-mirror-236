# -_- coding: utf-8 -_-

Deskripsi singkat proyek Python yang luar biasa.

## Instalation

```bash
pip install mecs
```

## Examplae Usage

```python
# import mecs package
from mecs import Stem

# Create stemmer
st = Stem.Stemmer()

# stem
term = "kaadâ'anna"
st.stemming(term)

print("kata Dasar : ", st.lemma)
# adâ'

print("awalan : ", st.prefix)
# ka

print("akhiran : ", st.suffix)
# anna

print("nasal : ", st.nasal)
# None

```
