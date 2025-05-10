.PHONY: all $(COMPANIES)


# Default target to run all
all: \
		KDP \
		KHC \
		KO \
		KR \
		KVUE \
		LW \
		MCK \
		MDLZ \
		MKC \
		MKSI \
		MNST \
		MO \
		MPWR \
		MU \

# Individual rules
KDP:
	python3 sec_scraper.py KDP

KHC:
	python3 sec_scraper.py KHC

KO:
	python3 sec_scraper.py KO

KR:
	python3 sec_scraper.py KR

KVUE:
	python3 sec_scraper.py KVUE

LW:
	python3 sec_scraper.py LW

MCK:
	python3 sec_scraper.py MCK

MDLZ:
	python3 sec_scraper.py MDLZ

MKC:
	python3 sec_scraper.py MKC

MKSI:
	python3 sec_scraper.py MKSI

MNST:
	python3 sec_scraper.py MNST

MO:
	python3 sec_scraper.py MO

MPWR:
	python3 sec_scraper.py MPWR

MU:
	python3 sec_scraper.py MU