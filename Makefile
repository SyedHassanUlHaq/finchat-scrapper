.PHONY: all $(COMPANIES)

COMPANIES = \
	KHC HSY K ADM MKC CLX TSN CASY USFD CAG SJM \
	PFGC TAP BG BRBR ACI HRL INGR COKE WBA

# Default target to run all
all: $(COMPANIES)

# Individual rules
KHC: main.py
	python3 main.py KHC https://finchat.io/company/NasdaqGS-KHC/investor-relations/ false

HSY: main.py
	python3 main.py HSY https://finchat.io/company/NYSE-HSY/investor-relations/ false

K: main.py
	python3 main.py K https://finchat.io/company/NYSE-K/investor-relations/ false

ADM: main.py
	python3 main.py ADM https://finchat.io/company/NYSE-ADM/investor-relations/ false

MKC: main.py
	python3 main.py MKC https://finchat.io/company/NYSE-MKC/investor-relations/ false

CLX: main.py
	python3 main.py CLX https://finchat.io/company/NYSE-CLX/investor-relations/ false

TSN: main.py
	python3 main.py TSN https://finchat.io/company/NYSE-TSN/investor-relations/ false

CASY: main.py
	python3 main.py CASY https://finchat.io/company/NasdaqGS-CASY/investor-relations/ false

USFD: main.py
	python3 main.py USFD https://finchat.io/company/NYSE-USFD/investor-relations/ false

CAG: main.py
	python3 main.py CAG https://finchat.io/company/NYSE-CAG/investor-relations/ false

SJM: main.py
	python3 main.py SJM https://finchat.io/company/NYSE-SJM/investor-relations/ false

PFGC: main.py
	python3 main.py PFGC https://finchat.io/company/NYSE-PFGC/investor-relations/ false

TAP: main.py
	python3 main.py TAP https://finchat.io/company/NYSE-TAP/investor-relations/ false

BG: main.py
	python3 main.py BG https://finchat.io/company/NYSE-BG/investor-relations/ false

BRBR: main.py
	python3 main.py BRBR https://finchat.io/company/NYSE-BRBR/investor-relations/ false

ACI: main.py
	python3 main.py ACI https://finchat.io/company/NYSE-ACI/investor-relations/ false

HRL: main.py
	python3 main.py HRL https://finchat.io/company/NYSE-HRL/investor-relations/ false

INGR: main.py
	python3 main.py INGR https://finchat.io/company/NYSE-INGR/investor-relations/ false

COKE: main.py
	python3 main.py COKE https://finchat.io/company/NasdaqGS-COKE/investor-relations/ false

WBA: main.py
	python3 main.py WBA https://finchat.io/company/NasdaqGS-WBA/investor-relations/ false
