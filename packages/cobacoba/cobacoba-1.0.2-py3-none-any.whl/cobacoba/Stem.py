class Stemmer:
    def __init__(self):
        self.lemma = None
        self.suffix = None
        self.prefix = None
        self.nasal = None

    def cf(self, data):  # proses merubah seluruh huruf besar menjadi huruf kecil//
        return data.lower()

    def tokenizing(
        self, data_cf
    ):  # proses mengahpus simbol yang tida diperlukan dan merubah kalimat menjadi term berdasarkan spasi'''
        # allowedChar = "abcdefghijklmnopqrstuvwxyz0123456789âèḍ '-.,"
        allowedChar = "abcdefghijklmnopqrstuvwxyz0123456789âḍè '-.,"
        temp = ""
        for char in data_cf:
            if char in allowedChar:
                if char == "." or char == ",":
                    temp += " " + char
                else:
                    temp += char
        return temp.split()

    def ceIdentification(self, token):
        affixes = ["na", "da", "sa", "ra", "nga", "eng", "ma", "dha"]
        targetIndices = []
        for i in range(len(token)):  # proses rule based term ce'
            if token[i] == "cè'":
                targetIndices.append(i + 1)

        for j in targetIndices:  # identifikasi imbuan pada term setelah term ce'''
            for affixTerm in affixes:
                if token[j].endswith(affixTerm):
                    if affixTerm == "dha":
                        token[j] = token[j].replace("ddha", "t")
                    else:
                        token[j] = token[j].replace(affixTerm, "")
                    break
        return token

    def ghalluIdentification(self, token):  # proses identifikasi term ghallu
        demonstrative = [
            "rèya",
            "jarèya",
            "arèya",
            "jariya",
            "jiya",
            "jajiya",
            "jeh",
            "rowa",
            "arowa",
            "juwa",
        ]
        se = ["sè"]
        targetIndices = []
        for i in range(len(token)):
            if token[i] == "ghallu" and token[i - 2] in se:
                targetIndices.append(i - 1)
            elif token[i] == "ghallu" and token[i - 2] in demonstrative:
                targetIndices.append(i - 1)
            elif token[i] == "ghallu" and token[i - 1].startswith(
                "ta"
            ):  # contoh term = tamera
                targetIndices.append(i - 1)
                token[i - 1] = token[i - 1][2 : (len(token[i - 1]))]

        # indekstarget = rajah, kene'
        for j in targetIndices:
            token[j], token[j + 1] = token[j + 1], token[j]

        return token

    def repetitive(self, term):
        temp = term.split("-")
        if (
            temp[0] == temp[1]
        ):  # term Ulang Sempurna. contoh term: mogha-mogha, #revisi pengecekan term ulang sempurna
            return {"kd": temp[1], "prefix": "", "suffix": ""}
        else:
            if temp[0].startswith("e"):
                if temp[0].startswith("e") and temp[1].endswith(
                    "aghi"
                ):  # term Ulang Dwi Lingga Berimbuhan e- dan -aghi.contoh term: ekol-pokolaghi
                    return {
                        "kd": temp[1][: temp[1].index("aghi")],
                        "prefix": "di",
                        "suffix": "kan",
                    }
                else:
                    return {
                        "kd": temp[1],
                        "prefix": "di",
                        "suffix": "",
                    }  # term Ulang Dwi Lingga Berimbuhan e-. contoh term: ero-soro
            elif temp[0].startswith(
                "a"
            ):  # term Ulang Dwi Lingga Tidak Berimbuhan a-. contoh term: areng-sareng
                if temp[0].startswith("a") and temp[1].endswith(
                    "an"
                ):  # term Ulang Dwi Lingga Berimbuhan a- dan -an.contoh term: aka'-berka'an
                    return {
                        "kd": temp[1][: temp[1].index("an")],
                        "prefix": "ber",
                        "suffix": "an",
                    }
                else:
                    return {"kd": temp[1], "prefix": "ber", "suffix": ""}
            elif temp[1].endswith(
                "na"
            ):  # term Ulang Dwi Lingga Berimbuhan -na. contoh term: ca-kancana
                return {
                    "kd": temp[1][: temp[1].index("na")],
                    "prefix": "",
                    "suffix": "nya",
                }
            elif temp[1].endswith("an"):
                return {
                    "kd": temp[1][: temp[1].index("an")],
                    "prefix": "",
                    "suffix": "an",
                }  # term Ulang Dwi Lingga Berimbuhan -an. contoh term: ca-kancaan
            elif temp[1].endswith("ân"):
                return {
                    "kd": temp[1][: temp[1].index("ân")],
                    "prefix": "",
                    "suffix": "an",
                }
            elif temp[1].endswith("a"):
                return {"kd": temp[1][: temp[1].index("a")], "prefix": "", "suffix": ""}
            elif temp[1].endswith(
                temp[0]
            ):  # term Ulang Dwi Lingga Tidak Berimbuhan. #contoh term: ku-buku,
                return {"kd": temp[1], "prefix": "", "suffix": ""}

    def affixInfix(self, term):
        term = term.replace("ten", "t")
        self.prefix = "ten"
        return {
            "kd": term,
            "prefix": "di",
        }  # contoh term: tenolong-->tolong-->ditolong, tenompang-->tompang-ditumpang (sisipan 'en')

    def affixPrefix(self, term):
        return {"kd": term[1:], "prefix": "ter"}

    def paPrefix(self, term):
        self.suffix = "pa"
        return {"kd": term[2 : term.index("na")], "suffix": "annya"}

    def kaPrefix(self, term):
        if term.startswith("ka") and term.endswith("ânna"):
            self.prefix = "ka"
            self.suffix = "ânna"
            return {
                "kd": term[2 : term.index("ânna")],
                "prefix": "ke",
                "suffix": "annya",
            }
        elif term.startswith("ka") and term.endswith("anna"):
            self.prefix = "ka"
            self.suffix = "anna"
            return {
                "kd": term[2 : term.index("anna")],
                "prefix": "ke",
                "suffix": "annya",
            }
        elif term.startswith("ka") and term.endswith("an"):
            self.prefix = "ka"
            self.suffix = "an"
            return {"kd": term[2 : term.index("an")], "prefix": "ke", "suffix": "an"}
        elif term.startswith("ka") and term.endswith("ân"):
            self.prefix = "ka"
            self.suffix = "ân"
            return {"kd": term[2 : term.index("ân")], "prefix": "ke", "suffix": "an"}

    def nasalPrefix(self, term, dictionary):
        if term.startswith("nge"):
            term = term.replace("nge", "")
            self.nasal = "nge"
            return {"kd": term, "prefix": "me", "suffix": ""}
        elif term.startswith("ng"):
            temp = term + ""
            temp = temp.replace("ng", "")
            self.nasal = "ng"
            if temp in dictionary.keys():
                if temp.endswith("è"):
                    return {"kd": temp, "prefix": "me", "suffix": "i"}
                else:
                    return {"kd": temp, "prefix": "me", "suffix": ""}
            else:
                temp2 = term + ""
                temp2 = term.replace("ng", "gh")
                if temp2 in dictionary.keys():
                    return {"kd": temp2, "prefix": "meng", "suffix": ""}
                else:
                    temp3 = term + ""
                    temp3 = term.replace("ng", "k")
                    if temp3 in dictionary.keys():
                        return {"kd": temp3, "prefix": "meng", "suffix": ""}
        elif term.startswith("ny"):
            temp = term + ""
            temp = temp.replace("ny", "c")
            self.nasal = "ny"
            if temp in dictionary.keys():
                return {"kd": temp, "prefix": "men", "suffix": ""}
            else:
                temp2 = term + ""
                temp2 = term.replace("ny", "j")  # nyajhal --> jajhal
                if temp2 in dictionary.keys():
                    return {"kd": temp2, "prefix": "men", "suffix": ""}
                else:
                    temp3 = term + ""
                    temp3 = term.replace("ny", "s")  # nyabun --> sabun
                    if temp3 in dictionary.keys():
                        return {"kd": temp3, "prefix": "meny", "suffix": ""}
                    # add thoriq
                    else:
                        self.nasal = None
                        return {"kd": term, "prefix": "", "suffix": ""}
        elif term.startswith("m"):
            temp = list(term)
            temp[0] = "b"
            newTerm = "".join(temp)
            self.nasal = "m"
            if newTerm in dictionary.keys():
                return {"kd": newTerm, "prefix": "mem", "suffix": ""}
            else:
                temp[0] = "p"
                newTerm = "".join(temp)
                return {"kd": newTerm, "prefix": "mem", "suffix": ""}
        elif term.startswith("n"):
            temp = list(term)
            temp[0] = "t"
            newTerm = "".join(temp)

            if newTerm in dictionary.keys():
                self.nasal = "n"
                return {"kd": newTerm, "prefix": "men", "suffix": ""}
            # add thoriq
            else:
                return {"kd": term, "prefix": "", "suffix": ""}

    def affix(self, term, dictionary):
        if term.endswith("na"):
            if term.startswith("sa") and term.endswith("na"):
                temp = term + ""
                temp = temp[2:]
                temp = temp.replace("na", "")
                # print(temp)
                if temp in dictionary.keys():
                    self.prefix = "sa"
                    self.suffix = "na"
                    return {"kd": temp, "prefix": "se", "suffix": "nya"}
                else:
                    temp2 = term + ""
                    temp2 = term.replace("na", "")
                    self.suffix = "na"
                    if temp2 in dictionary.keys():
                        return {"kd": temp2, "prefix": "", "suffix": "nya"}
            elif term.endswith("ânna"):
                self.suffix = "ânna"
                return {
                    "kd": term[: term.index("ânna")],
                    "prefix": "",
                    "suffix": "annya",
                }
            elif term.endswith("anna"):
                self.suffix = "anna"
                return {
                    "kd": term[: term.index("anna")],
                    "prefix": "",
                    "suffix": "annya",
                }
            else:
                # add thoriq
                self.suffix = "na"
                return {"kd": term[: term.index("na")], "prefix": "", "suffix": "nya"}
        elif term.endswith("aghi"):
            self.suffix = "aghi"
            if term.startswith("e") and term.endswith("aghi"):
                self.prefix = "e"
                return {
                    "kd": term[1 : term.index("aghi")],
                    "prefix": "di",
                    "suffix": "kan",
                }
            elif term.startswith("è") and term.endswith("aghi"):
                self.prefix = "è"
                return {
                    "kd": term[1 : term.index("aghi")],
                    "prefix": "di",
                    "suffix": "kan",
                }
            elif term.startswith("a") and term.endswith("aghi"):
                self.prefix = "a"
                return {
                    "kd": term[1 : term.index("aghi")],
                    "prefix": "meng",
                    "suffix": "kan",
                }
            else:
                return {"kd": term[: term.index("aghi")], "prefix": "", "suffix": "kan"}
        elif term.startswith("ta"):
            self.prefix = "ta"
            return {"kd": term[2:], "prefix": "ter", "suffix": ""}
        elif term.startswith("ma"):
            self.prefix = "ma"
            return {"kd": term[2:], "prefix": "memper", "suffix": ""}
        elif term.startswith("ka"):
            self.prefix = "ka"
            if term.startswith("ka") and term.endswith("'"):
                return {"kd": term[2:], "prefix": "ber", "suffix": ""}
            else:
                return {"kd": term[2:], "prefix": "ter", "suffix": ""}
        elif term.startswith("sa"):
            if term.startswith("sa") and term.endswith("sa"):
                self.prefix = "sa"
                self.suffix = "sa"
                return {
                    "kd": term[2 : term.index("sa")],
                    "prefix": "se",
                    "suffix": "nya",
                }
            else:
                # add thoriq
                if term[2:] in dictionary:
                    self.prefix = "sa"
                    return {"kd": term[2:], "prefix": "se", "suffix": ""}
                else:
                    return {"kd": term, "prefix": "", "suffix": ""}

        elif term.startswith("pa"):
            self.prefix = "pa"
            return {"kd": term[2:], "prefix": "pe", "suffix": ""}
        elif term.startswith("pe"):
            self.prefix = "pe"
            return {"kd": term[2:], "prefix": "pe", "suffix": ""}
        elif term.endswith("è"):
            self.suffix = "è"
            return {"kd": term[: term.index("è")], "prefix": "", "suffix": "kan"}
        elif term.endswith("an"):
            if term.startswith("a") and term.endswith("an"):
                self.suffix = "an"
                self.prefix = "a"
                return {"kd": term[1 : term.index("an")], "prefix": "ber", "suffix": ""}
            elif term.startswith("pa") and term.endswith("an"):
                return {"kd": term[2 : term.index("an")], "prefix": "", "suffix": ""}
            elif term.startswith("sa") and term.endswith("an"):
                self.prefix = "sa"
                self.suffix = "an"
                return {
                    "kd": term[2 : term.index("an")],
                    "prefix": "se",
                    "suffix": "an",
                }
            else:
                return {"kd": term[: term.index("an")], "prefix": "", "suffix": "an"}
        elif term.endswith("ân"):
            if term.endswith("ân"):
                self.suffix = "ân"
                return {"kd": term[: term.index("ân")], "prefix": "", "suffix": "an"}
            elif term.startswith("a") and term.endswith("ân"):
                self.prefix = "a"
                return {"kd": term[1 : term.index("ân")], "prefix": "ber", "suffix": ""}
            # elif term.startswith('ka') and term.endswith("'ân"):
            # return {'kd':term[2:term.index("ân")],'prefix':'','suffix':'an'}
            elif term.startswith("ka") and term.endswith("ân"):
                self.prefix = "ka"
                self.suffix = "ân"
                return {
                    "kd": term[2 : term.index("ân")],
                    "prefix": "ke",
                    "suffix": "an",
                }
        elif term.endswith("ra"):
            self.suffix = "ra"
            return {"kd": term[: term.index("ra")], "prefix": "", "suffix": "nya"}
        elif term.endswith("sa"):
            self.suffix = "sa"
            return {"kd": term[: term.index("sa")], "prefix": "", "suffix": "nya"}
        elif term.endswith("èpon"):
            self.suffix = "èpon"
            return {"kd": term[: term.index("èpon")], "prefix": "", "suffix": "nya"}
        elif term.startswith("e"):
            if term.startswith("epa"):
                self.prefix = "epa"
                return {"kd": term[3:], "prefix": "dipe", "suffix": ""}
            else:
                self.prefix = "e"
                return {"kd": term[1:], "prefix": "di", "suffix": ""}
        elif term.startswith("è"):
            if term.startswith("èpa"):
                self.prefix = "èpa"
                return {"kd": term[3:], "prefix": "dipe", "suffix": ""}
            else:
                self.prefix = "è"
                return {"kd": term[1:], "prefix": "di", "suffix": ""}
        elif term.startswith("a"):
            self.prefix = "a"
            return {"kd": term[1:], "prefix": "ber", "suffix": ""}

    def stemming(self, kalimat):
        # import json
        # with open('lemmata.json', 'r',encoding='utf-8') as file:
        #     # Membaca JSON dari file
        #     data = json.load(file)
        from lemma import data

        dictionary = {}
        for i in range(len(data)):
            dictionary[data[i]["basic_lemma"]] = True
        # kalimat = self.ghalluIdentification(self.ceIdentification(self.tokenizing(self.cf(kalimat))))
        hasil = ""
        for term in kalimat.split():
            # print(term)
            if term == ".":
                hasil = hasil[: len(hasil) - 1]
                hasil += ". "
            elif term == ",":
                hasil = hasil[: len(hasil) - 1]
                hasil += ", "
            else:
                if term == "ghallu":
                    hasil += "terlalu "
                else:
                    if "-" in term:
                        temp = self.repetitive(term)
                    #                     hasil += temp['prefix']+dictionary[temp['kd']][0] + \
                    #                         "-"+dictionary[temp['kd']][0]+temp['suffix']+" "
                    else:
                        if term not in dictionary.keys():
                            if term.startswith("pa") and term.endswith("na"):
                                temp = self.paPrefix(term)
                                self.lemma = temp["kd"]
                                # hasil += dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.startswith("ka") and term.endswith("ân"):
                                temp = self.kaPrefix(term)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.startswith("ka") and term.endswith("an"):
                                temp = self.kaPrefix(term)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.startswith("ka") and term.endswith("ânna"):
                                temp = self.kaPrefix(term)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.startswith("ka") and term.endswith("anna"):
                                temp = self.kaPrefix(term)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.startswith("ten"):
                                temp = self.affixInfix(term)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+" "
                            elif term.startswith("ny"):
                                temp = self.nasalPrefix(term, dictionary)
                                self.lemma = temp["kd"]
                                # if temp['prefix'] == 'meny':
                                #     hasil += temp['prefix']+dictionary[temp['kd']][0][1:]+" "
                                # else:
                                #     hasil += temp['prefix']+dictionary[temp['kd']][0]+" "
                            elif term.startswith("nge"):
                                temp = self.nasalPrefix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.startswith("ng"):
                                temp = self.nasalPrefix(term, dictionary)
                                self.lemma = temp["kd"]
                                # if temp['kd'].startswith('k'):
                                #     hasil += temp['prefix']+dictionary[temp['kd']][0][1:]+temp['suffix']+" "
                                # else:
                                #     hasil += temp['prefix']+dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.endswith("na"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.endswith("aghi"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.startswith("ta"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+" "
                            elif term.startswith("ma"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+" "
                            elif term.startswith("ka"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+" "
                            elif term.startswith("sa"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.startswith("pa"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+" "
                            elif term.startswith("pe"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+" "
                            elif term.endswith("è"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.endswith("an"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.endswith("ân"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.endswith("ra"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.endswith("sa"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.endswith("èpon"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.startswith("a"):
                                if term == kalimat[-1]:
                                    temp = self.affixPrefix(term)
                                    self.lemma = temp["kd"]
                                    # hasil += temp['prefix']+dictionary[temp['kd']][0]+" "
                                else:
                                    temp = self.affix(term, dictionary)
                                    self.lemma = temp["kd"]
                                    # hasil += temp['prefix']+dictionary[temp['kd']][0]+" "
                            elif term.startswith("e"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.startswith("è"):
                                temp = self.affix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0]+temp['suffix']+" "
                            elif term.startswith("m"):
                                temp = self.nasalPrefix(term, dictionary)
                                self.lemma = temp["kd"]
                                # if temp['kd'].startswith('b'):
                                #     hasil += temp['prefix']+dictionary[temp['kd']][0]+" "
                                # else:
                                #     hasil += temp['prefix']+dictionary[temp['kd']][0][1:]+" "
                            elif term.startswith("n"):
                                temp = self.nasalPrefix(term, dictionary)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+dictionary[temp['kd']][0][1:]+" "
                            else:
                                hasil += term + " "
                                self.lemma = term

                        else:
                            # hasil += dictionary[term][0]+" "
                            self.lemma = term

    #         if(kalimat.index(term)==0):
    #             hasil = hasil.capitalize()

    #         indeks = len(hasil)-1
    #         while hasil[indeks] != "." and indeks >= 0:
    #             indeks -= 1
    #         if indeks > 0:
    #             text_temp = hasil[:indeks+2]
    #             last_word = hasil[indeks+2:len(hasil)].capitalize()

    #             hasil = text_temp + last_word
    # self.lemma = stem
    # return self.lemma


# stem = Stemmer()
# # stem.stemming("alako")
# stem.stemming("kaadâ'anna")
# print(stem.lemma)
# print(stem.prefix)
# print(stem.suffix)
# print(stem.nasal)
# tes2 = stemming("Alè' toju' èadâ'")
# tes2 = stemming("alè' toju' èadâ'")
