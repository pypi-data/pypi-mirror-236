Deskripsi singkat proyek Python yang luar biasa.

## Instalation

```bash
pip install mecs
```

## Examplae Usage

```python
# import package
from mecs import Stem

# Create stemmer
st = Stem.Stemmer()

# stem
term = "romana"
st.stemming(term)

print("kata Dasar : ", st.lemma)
# roma'

print("awalan : ", st.prefix)
# None

print("akhiran : ", st.suffix)
# na

print("nasal : ", st.nasal)
# None

```

## Demo

Live demo : https://www.demo.com
