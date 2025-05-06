.PHONY: all $(COMPANIES)

COMPANIES = \
	KHC HSY K ADM MKC CLX TSN CASY USFD CAG SJM \
	PFGC TAP BG BRBR ACI HRL INGR COKE WBA LW CPB CELH POST BFB DAR SAM BFA IFF

# Default target to run all
all: \
	APPF_sec_filings \
	S_sec_filings \
	PATH_sec_filings \
	GLOB_sec_filings \
	DLB_sec_filings \
	SNDK_sec_filings \
	AVT_sec_filings \
	PEGA_sec_filings \
	DXC_sec_filings \
	IAC_sec_filings \
	ALGM_sec_filings \
	ZI_sec_filings

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
	
LW: main.py
	python3 main.py LW https://finchat.io/company/NYSE-LW/investor-relations/ false

CPB: main.py
	python3 main.py CPB https://finchat.io/company/NasdaqGS-CPB/investor-relations/ false

CELH: main.py
	python3 main.py CELH https://finchat.io/company/NasdaqCM-CELH/investor-relations/ false

POST: main.py
	python3 main.py POST https://finchat.io/company/NYSE-POST/investor-relations/ false

BFB: main.py
	python3 main.py BFB https://finchat.io/company/NYSE-BF.B/investor-relations/ false

DAR: main.py
	python3 main.py DAR https://finchat.io/company/NYSE-DAR/investor-relations/ false

SAM: main.py
	python3 main.py SAM https://finchat.io/company/NYSE-SAM/investor-relations/ false

BFA: main.py
	python3 main.py BFA https://finchat.io/company/NYSE-BF.B/investor-relations/ false

IFF: main.py
	python3 main.py IFF https://finchat.io/company/NYSE-IFF/investor-relations/ false

PM: main.py
	python3 main.py PM https://finchat.io/company/NYSE-PM/investor-relations/ false

PEP: main.py
	python3 main.py PEP https://finchat.io/company/NasdaqGS-PEP/investor-relations/ false

MO: main.py
	python3 main.py MO https://finchat.io/company/NYSE-MO/investor-relations/ false

MO_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/MO_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/MO_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/MO_investor_relations_sec.json

CVS: main.py
	python3 main.py CVS https://finchat.io/company/NYSE-CVS/investor-relations/ false

CVS_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/CVS_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/CVS_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/CVS_investor_relations_sec.json

MCK: main.py
	python3 main.py MCK https://finchat.io/company/NYSE-MCK/investor-relations/ false

MCK_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/MCK_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/MCK_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/MCK_investor_relations_sec.json

COR: main.py
	python3 main.py COR https://finchat.io/company/NYSE-COR/investor-relations/ false

COR_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/COR_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/COR_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/COR_investor_relations_sec.json

CDNS: main.py
	python3 main.py CDNS https://finchat.io/company/NasdaqGS-CDNS/investor-relations/ false

CDNS_sec_filings: sec_scraper.py
	python3 sec_scraper.py CDNS

CDNS_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/CDNS_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/CDNS_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/CDNS_investor_relations_sec.json

APP: main.py
	python3 main.py APP https://finchat.io/company/NasdaqGS-APP/investor-relations/ false

APP_sec_filings: sec_scraper.py
	python3 sec_scraper.py APP

APP_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/APP_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/APP_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/APP_investor_relations_sec.json

SNPS: main.py
	python3 main.py SNPS https://finchat.io/company/NasdaqGS-SNPS/investor-relations/ false

SNPS_sec_filings: sec_scraper.py
	python3 sec_scraper.py SNPS

SNPS_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/SNPS_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/SNPS_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/SNPS_investor_relations_sec.json

DASH: main.py
	python3 main.py DASH https://finchat.io/company/NasdaqGS-DASH/investor-relations/ false

DASH_sec_filings: sec_scraper.py
	python3 sec_scraper.py DASH

DASH_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/DASH_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/DASH_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/DASH_investor_relations_sec.json

FTNT: main.py
	python3 main.py FTNT https://finchat.io/company/NasdaqGS-FTNT/investor-relations/ false

FTNT_sec_filings: sec_scraper.py
	python3 sec_scraper.py FTNT

FTNT_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/FTNT_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/FTNT_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/FTNT_investor_relations_sec.json

ROP: main.py
	python3 main.py ROP https://finchat.io/company/NasdaqGS-ROP/investor-relations/ false

ROP_sec_filings: sec_scraper.py
	python3 sec_scraper.py ROP

ROP_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/ROP_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/ROP_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/ROP_investor_relations_sec.json

MSTR: main.py
	python3 main.py MSTR https://finchat.io/company/NasdaqGS-MSTR/investor-relations/ false

MSTR_sec_filings: sec_scraper.py
	python3 sec_scraper.py MSTR

MSTR_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/MSTR_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/MSTR_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/MSTR_investor_relations_sec.json

ADSK: main.py
	python3 main.py ADSK https://finchat.io/company/NasdaqGS-ADSK/investor-relations/ false

ADSK_sec_filings: sec_scraper.py
	python3 sec_scraper.py ADSK

ADSK_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/ADSK_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/ADSK_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/ADSK_investor_relations_sec.json

WDAY: main.py
	python3 main.py WDAY https://finchat.io/company/NasdaqGS-WDAY/investor-relations/ false

WDAY_sec_filings: sec_scraper.py
	python3 sec_scraper.py WDAY

WDAY_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/WDAY_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/WDAY_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/WDAY_investor_relations_sec.json

MRVL: main.py
	python3 main.py MRVL https://finchat.io/company/NasdaqGS-MRVL/investor-relations/ false

MRVL_sec_filings: sec_scraper.py
	python3 sec_scraper.py MRVL

MRVL_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/MRVL_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/MRVL_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/MRVL_investor_relations_sec.json

SNOW: main.py
	python3 main.py SNOW https://finchat.io/company/NYSE-SNOW/investor-relations/ false

SNOW_sec_filings: sec_scraper.py
	python3 sec_scraper.py SNOW

SNOW_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/SNOW_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/SNOW_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/SNOW_investor_relations_sec.json

CTSH: main.py
	python3 main.py CTSH https://finchat.io/company/NasdaqGS-CTSH/investor-relations/ false

CTSH_sec_filings: sec_scraper.py
	python3 sec_scraper.py CTSH

CTSH_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/CTSH_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/CTSH_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/CTSH_investor_relations_sec.json

GLW: main.py
	python3 main.py GLW https://finchat.io/company/NYSE-GLW/investor-relations/ false

GLW_sec_filings: sec_scraper.py
	python3 sec_scraper.py GLW

GLW_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/GLW_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/GLW_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/GLW_investor_relations_sec.json

TEAM: main.py
	python3 main.py TEAM https://finchat.io/company/NasdaqGS-TEAM/investor-relations/ false

TEAM_sec_filings: sec_scraper.py
	python3 sec_scraper.py TEAM

TEAM_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/TEAM_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/TEAM_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/TEAM_investor_relations_sec.json

NET: main.py
	python3 main.py NET https://finchat.io/company/NYSE-NET/investor-relations/ false

NET_sec_filings: sec_scraper.py
	python3 sec_scraper.py NET

NET_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/NET_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/NET_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/NET_investor_relations_sec.json

IT: main.py
	python3 main.py IT https://finchat.io/company/NYSE-IT/investor-relations/ false

IT_sec_filings: sec_scraper.py
	python3 sec_scraper.py IT

IT_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/IT_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/IT_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/IT_investor_relations_sec.json

DDOG: main.py
	python3 main.py DDOG https://finchat.io/company/NasdaqGS-DDOG/investor-relations/ false

DDOG_sec_filings: sec_scraper.py
	python3 sec_scraper.py DDOG

DDOG_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/DDOG_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/DDOG_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/DDOG_investor_relations_sec.json

ANSS: main.py
	python3 main.py ANSS https://finchat.io/company/NasdaqGS-ANSS/investor-relations/ false

ANSS_sec_filings: sec_scraper.py
	python3 sec_scraper.py ANSS

ANSS_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/ANSS_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/ANSS_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/ANSS_investor_relations_sec.json

HUBS: main.py
	python3 main.py HUBS https://finchat.io/company/NYSE-HUBS/investor-relations/ false

HUBS_sec_filings: sec_scraper.py
	python3 sec_scraper.py HUBS

HUBS_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/HUBS_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/HUBS_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/HUBS_investor_relations_sec.json

GDDY: main.py
	python3 main.py GDDY https://finchat.io/company/NYSE-GDDY/investor-relations/ false

GDDY_sec_filings: sec_scraper.py
	python3 sec_scraper.py GDDY

GDDY_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/GDDY_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/GDDY_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/GDDY_investor_relations_sec.json

TYL: main.py
	python3 main.py TYL https://finchat.io/company/NYSE-TYL/investor-relations/ false

TYL_sec_filings: sec_scraper.py
	python3 sec_scraper.py TYL

TYL_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/TYL_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/TYL_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/TYL_investor_relations_sec.json

MPWR: main.py
	python3 main.py MPWR https://finchat.io/company/NasdaqGS-MPWR/investor-relations/ false

MPWR_sec_filings: sec_scraper.py
	python3 sec_scraper.py MPWR

MPWR_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/MPWR_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/MPWR_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/MPWR_investor_relations_sec.json

HPQ: main.py
	python3 main.py HPQ https://finchat.io/company/NYSE-HPQ/investor-relations/ false

HPQ_sec_filings: sec_scraper.py
	python3 sec_scraper.py HPQ

HPQ_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/HPQ_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/HPQ_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/HPQ_investor_relations_sec.json

DELL: main.py
	python3 main.py DELL https://finchat.io/company/NYSE-DELL/investor-relations/ false

DELL_sec_filings: sec_scraper.py
	python3 sec_scraper.py DELL

DELL_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/DELL_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/DELL_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/DELL_investor_relations_sec.json

CDW: main.py
	python3 main.py CDW https://finchat.io/company/NasdaqGS-CDW/investor-relations/ false

CDW_sec_filings: sec_scraper.py
	python3 sec_scraper.py CDW

CDW_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/CDW_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/CDW_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/CDW_investor_relations_sec.json

ARM: main.py
	python3 main.py ARM https://finchat.io/company/NasdaqGS-ARM/investor-relations/ false

ARM_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/ARM_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/ARM_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/ARM_investor_relations_sec.json

MKSI: main.py
	python3 main.py MKSI https://finchat.io/company/NasdaqGS-MKSI/investor-relations/ false

MKSI_combine: combine.py
	python3 combine.py /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/MKSI_sec_filings.json /home/syed-hassan-ul-haq/repos/finchat-scrapper/JSONS/MKSI_investor_relations.json -o /home/syed-hassan-ul-haq/repos/finchat-scrapper/Completed/MKSI_investor_relations_sec.json

BIRK: main.py
	python3 main.py BIRK https://finchat.io/company/NYSE-BIRK/investor-relations/ false