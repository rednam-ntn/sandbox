#%%
import spacy
nlp = spacy.load("en_vectors_web_lg")
tokens = nlp("dog cat banana afskfsd")

for token in tokens:
    print(token.text, token.has_vector, token.vector_norm)


#%%
tokens = nlp("CANON SINGAPORE PTE LTD\n1 FUSIONOPOLIS PLACE #15-10 GALAXIS\nSINGAPORE 138522")
for token in tokens:
    print(token.text, token.has_vector, token.vector_norm)

#%%
tokens = nlp(
    "CAN O N I N DI A P R I VAT EL I M I T ED\n"
    "EC N O .0596062443, C/ O F EDEX T S CS\n"
    "S U R VEY N O . 820/ 17KU T HAM BAKKAM VI L L .\n"
    "CHET T I P EDU , CHEN N AI602105\n"
    "N DI"
)

for token in tokens:
    print(token.text, token.has_vector, token.vector_norm)

#%%
tokens = nlp("CHEN N AI")

for token in tokens:
    print(token.text, token.has_vector, token.vector_norm)


#%%
a = "PORT： KAOHSIUNG PORT IN TAIWAN DESTINATION：GENOVA PORT, ITALY"

#%%
from unidecode import unidecode

unidecode("：")

#%%
ord(":") == ord(unidecode("："))


#%%
":" in unidecode("PORT： KAOHSIUNG PORT IN TAIWAN DESTINATION：GENOVA PORT, ITALY")

#%%
unidecode(
    "B/L不用秀 H.S.CODE NO.5402.20"
    "提單上請SHOW出目的地AGENT'S AND"
    "ON BOARD NOTATION並簽字"
)

#%%
ord("不")

#%%
character = "："
print(f"'{character}' have HTML-code: {ord(character)}")
print(f"decoded to '{unidecode(character)}'")

if unidecode(character) and len(unidecode(character)) == 1:
    print(f"with HTML-code: {ord(unidecode(character))}")

#%%


#%%
from test_1 import WORDS_PDF
import re

# %%

words_only = "".join([word[4] for page_words in WORDS_PDF for word in page_words])
print(words_only)
unicode_words_only = re.sub(r"�", "", words_only)

# %%
