# -*- coding: utf-8 -*-
"""全球货币枚举"""
from collections import namedtuple
from enum import Enum, auto
from typing import Dict, List
from base import ByKey

# https://www.iso.org/iso-4217-currency-codes.html

field_names: List[str] = ["alphabetic_code", "en_name", "numeric_code", "minor_unit"]
CurrencyDetail = namedtuple(typename="CurrencyDetail", field_names=field_names)
tsv: str = """
AED\tUAE Dirham\t784\t2
AFN\tAfghani\t971\t2
ALL\tLek\t008\t2
AMD\tArmenian Dram\t051\t2
ANG\tNetherlands Antillean Guilder\t532\t2
AOA\tKwanza\t973\t2
ARS\tArgentine Peso\t032\t2
AUD\tAustralian Dollar\t036\t2
AWG\tAruban Florin\t533\t2
AZN\tAzerbaijan Manat\t944\t2
BAM\tConvertible Mark\t977\t2
BBD\tBarbados Dollar\t052\t2
BDT\tTaka\t050\t2
BGN\tBulgarian Lev\t975\t2
BHD\tBahraini Dinar\t048\t3
BIF\tBurundi Franc\t108\t0
BMD\tBermudian Dollar\t060\t2
BND\tBrunei Dollar\t096\t2
BOB\tBoliviano\t068\t2
BRL\tBrazilian Real\t986\t2
BSD\tBahamian Dollar\t044\t2
BTN\tNgultrum\t064\t2
BWP\tPula\t072\t2
BYN\tBelarusian Ruble\t933\t2
BZD\tBelize Dollar\t084\t2
CAD\tCanadian Dollar\t124\t2
CDF\tCongolese Franc\t976\t2
CHF\tSwiss Franc\t756\t2
CLP\tChilean Peso\t152\t0
CNY\tYuan Renminbi\t156\t2
COP\tColombian Peso\t170\t2
CRC\tCosta Rican Colon\t188\t2
CUC\tPeso Convertible\t931\t2
CUP\tCuban Peso\t192\t2
CVE\tCabo Verde Escudo\t132\t2
CZK\tCzech Koruna\t203\t2
DJF\tDjibouti Franc\t262\t0
DKK\tDanish Krone\t208\t2
DOP\tDominican Peso\t214\t2
DZD\tAlgerian Dinar\t012\t2
EGP\tEgyptian Pound\t818\t2
ERN\tNakfa\t232\t2
ETB\tEthiopian Birr\t230\t2
EUR\tEuro\t978\t2
FJD\tFiji Dollar\t242\t2
FKP\tFalkland Islands Pound\t238\t2
GBP\tPound Sterling\t826\t2
GEL\tLari\t981\t2
GHS\tGhana Cedi\t936\t2
GIP\tGibraltar Pound\t292\t2
GMD\tDalasi\t270\t2
GNF\tGuinean Franc\t324\t0
GTQ\tQuetzal\t320\t2
GYD\tGuyana Dollar\t328\t2
HKD\tHong Kong Dollar\t344\t2
HNL\tLempira\t340\t2
HTG\tGourde\t332\t2
HUF\tForint\t348\t2
IDR\tRupiah\t360\t2
ILS\tNew Israeli Sheqel\t376\t2
INR\tIndian Rupee\t356\t2
IQD\tIraqi Dinar\t368\t3
IRR\tIranian Rial\t364\t2
ISK\tIceland Krona\t352\t0
JMD\tJamaican Dollar\t388\t2
JOD\tJordanian Dinar\t400\t3
JPY\tYen\t392\t0
KES\tKenyan Shilling\t404\t2
KGS\tSom\t417\t2
KHR\tRiel\t116\t2
KMF\tComorian Franc \t174\t0
KPW\tNorth Korean Won\t408\t2
KRW\tWon\t410\t0
KWD\tKuwaiti Dinar\t414\t3
KYD\tCayman Islands Dollar\t136\t2
KZT\tTenge\t398\t2
LAK\tLao Kip\t418\t2
LBP\tLebanese Pound\t422\t2
LKR\tSri Lanka Rupee\t144\t2
LRD\tLiberian Dollar\t430\t2
LSL\tLoti\t426\t2
LYD\tLibyan Dinar\t434\t3
MAD\tMoroccan Dirham\t504\t2
MDL\tMoldovan Leu\t498\t2
MGA\tMalagasy Ariary\t969\t2
MKD\tDenar\t807\t2
MMK\tKyat\t104\t2
MNT\tTugrik\t496\t2
MOP\tPataca\t446\t2
MRU\tOuguiya\t929\t2
MUR\tMauritius Rupee\t480\t2
MVR\tRufiyaa\t462\t2
MWK\tMalawi Kwacha\t454\t2
MXN\tMexican Peso\t484\t2
MYR\tMalaysian Ringgit\t458\t2
MZN\tMozambique Metical\t943\t2
NAD\tNamibia Dollar\t516\t2
NGN\tNaira\t566\t2
NIO\tCordoba Oro\t558\t2
NOK\tNorwegian Krone\t578\t2
NPR\tNepalese Rupee\t524\t2
NZD\tNew Zealand Dollar\t554\t2
OMR\tRial Omani\t512\t3
PAB\tBalboa\t590\t2
PEN\tSol\t604\t2
PGK\tKina\t598\t2
PHP\tPhilippine Peso\t608\t2
PKR\tPakistan Rupee\t586\t2
PLN\tZloty\t985\t2
PYG\tGuarani\t600\t0
QAR\tQatari Rial\t634\t2
RON\tRomanian Leu\t946\t2
RSD\tSerbian Dinar\t941\t2
RUB\tRussian Ruble\t643\t2
RWF\tRwanda Franc\t646\t0
SAR\tSaudi Riyal\t682\t2
SBD\tSolomon Islands Dollar\t090\t2
SCR\tSeychelles Rupee\t690\t2
SDG\tSudanese Pound\t938\t2
SEK\tSwedish Krona\t752\t2
SGD\tSingapore Dollar\t702\t2
SHP\tSaint Helena Pound\t654\t2
SLE\tLeone\t925\t2
SLL\tLeone\t694\t2
SOS\tSomali Shilling\t706\t2
SRD\tSurinam Dollar\t968\t2
SSP\tSouth Sudanese Pound\t728\t2
STN\tDobra\t930\t2
SVC\tEl Salvador Colon\t222\t2
SYP\tSyrian Pound\t760\t2
SZL\tLilangeni\t748\t2
THB\tBaht\t764\t2
TJS\tSomoni\t972\t2
TMT\tTurkmenistan New Manat\t934\t2
TND\tTunisian Dinar\t788\t3
TOP\tPa’anga\t776\t2
TRY\tTurkish Lira\t949\t2
TTD\tTrinidad and Tobago Dollar\t780\t2
TWD\tNew Taiwan Dollar\t901\t2
TZS\tTanzanian Shilling\t834\t2
UAH\tHryvnia\t980\t2
UGX\tUganda Shilling\t800\t0
USD\tUS Dollar\t840\t2
UYU\tPeso Uruguayo\t858\t2
UYW\tUnidad Previsional\t927\t4
UZS\tUzbekistan Sum\t860\t2
VED\tBolívar Soberano\t926\t2
VES\tBolívar Soberano\t928\t2
VND\tDong\t704\t0
VUV\tVatu\t548\t0
WST\tTala\t882\t2
XAF\tCFA Franc BEAC\t950\t0
XCD\tEast Caribbean Dollar\t951\t2
XOF\tCFA Franc BCEAO\t952\t0
XPF\tCFP Franc\t953\t0
YER\tYemeni Rial\t886\t2
ZAR\tRand\t710\t2
ZMW\tZambian Kwacha\t967\t2
ZWL\tZimbabwe Dollar\t932\t2
"""

Items: List[CurrencyDetail] = [CurrencyDetail(*line.strip().split("\t")) for line in tsv.splitlines() if line]


class ByAlphabeticCode(ByKey):
    map: Dict[str, CurrencyDetail] = {getattr(item, field_names[0]): item for item in Items}


class CurrencyAlphabeticCode(Enum, metaclass=ByAlphabeticCode):
    """交易所MIC枚举"""

    AED = auto()
    AFN = auto()
    ALL = auto()
    AMD = auto()
    ANG = auto()
    AOA = auto()
    ARS = auto()
    AUD = auto()
    AWG = auto()
    AZN = auto()
    BAM = auto()
    BBD = auto()
    BDT = auto()
    BGN = auto()
    BHD = auto()
    BIF = auto()
    BMD = auto()
    BND = auto()
    BOB = auto()
    BRL = auto()
    BSD = auto()
    BTN = auto()
    BWP = auto()
    BYN = auto()
    BZD = auto()
    CAD = auto()
    CDF = auto()
    CHF = auto()
    CLP = auto()
    CNY = auto()
    COP = auto()
    CRC = auto()
    CUC = auto()
    CUP = auto()
    CVE = auto()
    CZK = auto()
    DJF = auto()
    DKK = auto()
    DOP = auto()
    DZD = auto()
    EGP = auto()
    ERN = auto()
    ETB = auto()
    EUR = auto()
    FJD = auto()
    FKP = auto()
    GBP = auto()
    GEL = auto()
    GHS = auto()
    GIP = auto()
    GMD = auto()
    GNF = auto()
    GTQ = auto()
    GYD = auto()
    HKD = auto()
    HNL = auto()
    HTG = auto()
    HUF = auto()
    IDR = auto()
    ILS = auto()
    INR = auto()
    IQD = auto()
    IRR = auto()
    ISK = auto()
    JMD = auto()
    JOD = auto()
    JPY = auto()
    KES = auto()
    KGS = auto()
    KHR = auto()
    KMF = auto()
    KPW = auto()
    KRW = auto()
    KWD = auto()
    KYD = auto()
    KZT = auto()
    LAK = auto()
    LBP = auto()
    LKR = auto()
    LRD = auto()
    LSL = auto()
    LYD = auto()
    MAD = auto()
    MDL = auto()
    MGA = auto()
    MKD = auto()
    MMK = auto()
    MNT = auto()
    MOP = auto()
    MRU = auto()
    MUR = auto()
    MVR = auto()
    MWK = auto()
    MXN = auto()
    MYR = auto()
    MZN = auto()
    NAD = auto()
    NGN = auto()
    NIO = auto()
    NOK = auto()
    NPR = auto()
    NZD = auto()
    OMR = auto()
    PAB = auto()
    PEN = auto()
    PGK = auto()
    PHP = auto()
    PKR = auto()
    PLN = auto()
    PYG = auto()
    QAR = auto()
    RON = auto()
    RSD = auto()
    RUB = auto()
    RWF = auto()
    SAR = auto()
    SBD = auto()
    SCR = auto()
    SDG = auto()
    SEK = auto()
    SGD = auto()
    SHP = auto()
    SLE = auto()
    SLL = auto()
    SOS = auto()
    SRD = auto()
    SSP = auto()
    STN = auto()
    SVC = auto()
    SYP = auto()
    SZL = auto()
    THB = auto()
    TJS = auto()
    TMT = auto()
    TND = auto()
    TOP = auto()
    TRY = auto()
    TTD = auto()
    TWD = auto()
    TZS = auto()
    UAH = auto()
    UGX = auto()
    USD = auto()
    UYU = auto()
    UYW = auto()
    UZS = auto()
    VED = auto()
    VES = auto()
    VND = auto()
    VUV = auto()
    WST = auto()
    XAF = auto()
    XCD = auto()
    XOF = auto()
    XPF = auto()
    YER = auto()
    ZAR = auto()
    ZMW = auto()
    ZWL = auto()


# 数据完整性和一致性检验
ByAlphabeticCode.check(obj=CurrencyAlphabeticCode)
