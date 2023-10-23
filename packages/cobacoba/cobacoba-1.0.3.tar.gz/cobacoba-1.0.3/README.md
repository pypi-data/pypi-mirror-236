Deskripsi singkat proyek Python yang luar biasa.

## Instalation

```bash
pip install mecs
```

## Examplae Usage

```python
\# import mecs package
from mecs import Stem

\# Create stemmer
st = Stem.Stemmer()

\#stem
kataAwal1 = "kaadâ'anna"
st.stemming(kataAwal1)

print("kata Awal : ", kataAwal1)
print("kata Dasar : ", st.lemma)
print("awalan : ", st.prefix)
print("akhiran : ", st.suffix)
print("nasal : ", st.nasal)
```
