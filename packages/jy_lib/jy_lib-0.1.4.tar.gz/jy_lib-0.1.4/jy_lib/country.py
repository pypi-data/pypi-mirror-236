# -*- coding: utf-8 -*-
"""全球国家及地区枚举"""
from collections import namedtuple
from enum import auto, Enum
from typing import Dict, List
from .base import ByKey

# https://www.nationsonline.org/oneworld/country_code_list.htm

field_names: List[str] = ["a3_code", "a2_code", "un_code", "en_name"]
CountryDetail = namedtuple(typename="CountryDetail", field_names=field_names)
tsv: str = """
AFG\tAF\t004\tAfghanistan
ALA\tAX\t248\tAland Islands
ALB\tAL\t008\tAlbania
DZA\tDZ\t012\tAlgeria
ASM\tAS\t016\tAmerican Samoa
AND\tAD\t020\tAndorra
AGO\tAO\t024\tAngola
AIA\tAI\t660\tAnguilla
ATA\tAQ\t010\tAntarctica
ATG\tAG\t028\tAntigua and Barbuda
ARG\tAR\t032\tArgentina
ARM\tAM\t051\tArmenia
ABW\tAW\t533\tAruba
AUS\tAU\t036\tAustralia
AUT\tAT\t040\tAustria
AZE\tAZ\t031\tAzerbaijan
BHS\tBS\t044\tBahamas
BHR\tBH\t048\tBahrain
BGD\tBD\t050\tBangladesh
BRB\tBB\t052\tBarbados
BLR\tBY\t112\tBelarus
BEL\tBE\t056\tBelgium
BLZ\tBZ\t084\tBelize
BEN\tBJ\t204\tBenin
BMU\tBM\t060\tBermuda
BTN\tBT\t064\tBhutan
BOL\tBO\t068\tBolivia
BIH\tBA\t070\tBosnia and Herzegovina
BWA\tBW\t072\tBotswana
BVT\tBV\t074\tBouvet Island
BRA\tBR\t076\tBrazil
VGB\tVG\t092\tBritish Virgin Islands
IOT\tIO\t086\tBritish Indian Ocean Territory
BRN\tBN\t096\tBrunei Darussalam
BGR\tBG\t100\tBulgaria
BFA\tBF\t854\tBurkina Faso
BDI\tBI\t108\tBurundi
KHM\tKH\t116\tCambodia
CMR\tCM\t120\tCameroon
CAN\tCA\t124\tCanada
CPV\tCV\t132\tCape Verde
CYM\tKY\t136\tCayman Islands
CAF\tCF\t140\tCentral African Republic
TCD\tTD\t148\tChad
CHL\tCL\t152\tChile
CHN\tCN\t156\tChina
HKG\tHK\t344\tHong Kong, SAR China
MAC\tMO\t446\tMacao, SAR China
CXR\tCX\t162\tChristmas Island
CCK\tCC\t166\tCocos (Keeling) Islands
COL\tCO\t170\tColombia
COM\tKM\t174\tComoros
COG\tCG\t178\tCongo (Brazzaville)
COD\tCD\t180\tCongo, (Kinshasa)
COK\tCK\t184\tCook Islands
CRI\tCR\t188\tCosta Rica
CIV\tCI\t384\tCôte d'Ivoire
HRV\tHR\t191\tCroatia
CUB\tCU\t192\tCuba
CYP\tCY\t196\tCyprus
CZE\tCZ\t203\tCzech Republic
DNK\tDK\t208\tDenmark
DJI\tDJ\t262\tDjibouti
DMA\tDM\t212\tDominica
DOM\tDO\t214\tDominican Republic
ECU\tEC\t218\tEcuador
EGY\tEG\t818\tEgypt
SLV\tSV\t222\tEl Salvador
GNQ\tGQ\t226\tEquatorial Guinea
ERI\tER\t232\tEritrea
EST\tEE\t233\tEstonia
ETH\tET\t231\tEthiopia
FLK\tFK\t238\tFalkland Islands (Malvinas)
FRO\tFO\t234\tFaroe Islands
FJI\tFJ\t242\tFiji
FIN\tFI\t246\tFinland
FRA\tFR\t250\tFrance
GUF\tGF\t254\tFrench Guiana
PYF\tPF\t258\tFrench Polynesia
ATF\tTF\t260\tFrench Southern Territories
GAB\tGA\t266\tGabon
GMB\tGM\t270\tGambia
GEO\tGE\t268\tGeorgia
DEU\tDE\t276\tGermany
GHA\tGH\t288\tGhana
GIB\tGI\t292\tGibraltar
GRC\tGR\t300\tGreece
GRL\tGL\t304\tGreenland
GRD\tGD\t308\tGrenada
GLP\tGP\t312\tGuadeloupe
GUM\tGU\t316\tGuam
GTM\tGT\t320\tGuatemala
GGY\tGG\t831\tGuernsey
GIN\tGN\t324\tGuinea
GNB\tGW\t624\tGuinea-Bissau
GUY\tGY\t328\tGuyana
HTI\tHT\t332\tHaiti
HMD\tHM\t334\tHeard and Mcdonald Islands
VAT\tVA\t336\tHoly See (Vatican City State)
HND\tHN\t340\tHonduras
HUN\tHU\t348\tHungary
ISL\tIS\t352\tIceland
IND\tIN\t356\tIndia
IDN\tID\t360\tIndonesia
IRN\tIR\t364\tIran, Islamic Republic of
IRQ\tIQ\t368\tIraq
IRL\tIE\t372\tIreland
IMN\tIM\t833\tIsle of Man
ISR\tIL\t376\tIsrael
ITA\tIT\t380\tItaly
JAM\tJM\t388\tJamaica
JPN\tJP\t392\tJapan
JEY\tJE\t832\tJersey
JOR\tJO\t400\tJordan
KAZ\tKZ\t398\tKazakhstan
KEN\tKE\t404\tKenya
KIR\tKI\t296\tKiribati
PRK\tKP\t408\tKorea (North)
KOR\tKR\t410\tKorea (South)
KWT\tKW\t414\tKuwait
KGZ\tKG\t417\tKyrgyzstan
LAO\tLA\t418\tLao PDR
LVA\tLV\t428\tLatvia
LBN\tLB\t422\tLebanon
LSO\tLS\t426\tLesotho
LBR\tLR\t430\tLiberia
LBY\tLY\t434\tLibya
LIE\tLI\t438\tLiechtenstein
LTU\tLT\t440\tLithuania
LUX\tLU\t442\tLuxembourg
MKD\tMK\t807\tMacedonia, Republic of
MDG\tMG\t450\tMadagascar
MWI\tMW\t454\tMalawi
MYS\tMY\t458\tMalaysia
MDV\tMV\t462\tMaldives
MLI\tML\t466\tMali
MLT\tMT\t470\tMalta
MHL\tMH\t584\tMarshall Islands
MTQ\tMQ\t474\tMartinique
MRT\tMR\t478\tMauritania
MUS\tMU\t480\tMauritius
MYT\tYT\t175\tMayotte
MEX\tMX\t484\tMexico
FSM\tFM\t583\tMicronesia, Federated States of
MDA\tMD\t498\tMoldova
MCO\tMC\t492\tMonaco
MNG\tMN\t496\tMongolia
MNE\tME\t499\tMontenegro
MSR\tMS\t500\tMontserrat
MAR\tMA\t504\tMorocco
MOZ\tMZ\t508\tMozambique
MMR\tMM\t104\tMyanmar
NAM\tNA\t516\tNamibia
NRU\tNR\t520\tNauru
NPL\tNP\t524\tNepal
NLD\tNL\t528\tNetherlands
ANT\tAN\t530\tNetherlands Antilles
NCL\tNC\t540\tNew Caledonia
NZL\tNZ\t554\tNew Zealand
NIC\tNI\t558\tNicaragua
NER\tNE\t562\tNiger
NGA\tNG\t566\tNigeria
NIU\tNU\t570\tNiue
NFK\tNF\t574\tNorfolk Island
MNP\tMP\t580\tNorthern Mariana Islands
NOR\tNO\t578\tNorway
OMN\tOM\t512\tOman
PAK\tPK\t586\tPakistan
PLW\tPW\t585\tPalau
PSE\tPS\t275\tPalestinian Territory
PAN\tPA\t591\tPanama
PNG\tPG\t598\tPapua New Guinea
PRY\tPY\t600\tParaguay
PER\tPE\t604\tPeru
PHL\tPH\t608\tPhilippines
PCN\tPN\t612\tPitcairn
POL\tPL\t616\tPoland
PRT\tPT\t620\tPortugal
PRI\tPR\t630\tPuerto Rico
QAT\tQA\t634\tQatar
REU\tRE\t638\tRéunion
ROU\tRO\t642\tRomania
RUS\tRU\t643\tRussian Federation
RWA\tRW\t646\tRwanda
BLM\tBL\t652\tSaint-Barthélemy
SHN\tSH\t654\tSaint Helena
KNA\tKN\t659\tSaint Kitts and Nevis
LCA\tLC\t662\tSaint Lucia
MAF\tMF\t663\tSaint-Martin (French part)
SPM\tPM\t666\tSaint Pierre and Miquelon
VCT\tVC\t670\tSaint Vincent and Grenadines
WSM\tWS\t882\tSamoa
SMR\tSM\t674\tSan Marino
STP\tST\t678\tSao Tome and Principe
SAU\tSA\t682\tSaudi Arabia
SEN\tSN\t686\tSenegal
SRB\tRS\t688\tSerbia
SYC\tSC\t690\tSeychelles
SLE\tSL\t694\tSierra Leone
SGP\tSG\t702\tSingapore
SVK\tSK\t703\tSlovakia
SVN\tSI\t705\tSlovenia
SLB\tSB\t090\tSolomon Islands
SOM\tSO\t706\tSomalia
ZAF\tZA\t710\tSouth Africa
SGS\tGS\t239\tSouth Georgia and the South Sandwich Islands
SSD\tSS\t728\tSouth Sudan
ESP\tES\t724\tSpain
LKA\tLK\t144\tSri Lanka
SDN\tSD\t736\tSudan
SUR\tSR\t740\tSuriname
SJM\tSJ\t744\tSvalbard and Jan Mayen Islands
SWZ\tSZ\t748\tSwaziland
SWE\tSE\t752\tSweden
CHE\tCH\t756\tSwitzerland
SYR\tSY\t760\tSyrian Arab Republic (Syria)
TWN\tTW\t158\tTaiwan, Republic of China
TJK\tTJ\t762\tTajikistan
TZA\tTZ\t834\tTanzania, United Republic of
THA\tTH\t764\tThailand
TLS\tTL\t626\tTimor-Leste
TGO\tTG\t768\tTogo
TKL\tTK\t772\tTokelau
TON\tTO\t776\tTonga
TTO\tTT\t780\tTrinidad and Tobago
TUN\tTN\t788\tTunisia
TUR\tTR\t792\tTurkey
TKM\tTM\t795\tTurkmenistan
TCA\tTC\t796\tTurks and Caicos Islands
TUV\tTV\t798\tTuvalu
UGA\tUG\t800\tUganda
UKR\tUA\t804\tUkraine
ARE\tAE\t784\tUnited Arab Emirates
GBR\tGB\t826\tUnited Kingdom
USA\tUS\t840\tUnited States of America
UMI\tUM\t581\tUS Minor Outlying Islands
URY\tUY\t858\tUruguay
UZB\tUZ\t860\tUzbekistan
VUT\tVU\t548\tVanuatu
VEN\tVE\t862\tVenezuela (Bolivarian Republic)
VNM\tVN\t704\tViet Nam
VIR\tVI\t850\tVirgin Islands, US
WLF\tWF\t876\tWallis and Futuna Islands
ESH\tEH\t732\tWestern Sahara
YEM\tYE\t887\tYemen
ZMB\tZM\t894\tZambia
ZWE\tZW\t716\tZimbabwe
"""
# a3_code   Alpha 3 Code
# a2_code   Alpha 2 Code
# un_code   UN Code
# en_name   Country
Items: List[CountryDetail] = [CountryDetail(*line.strip().split("\t")) for line in tsv.splitlines() if line]


class ByA2Code(ByKey):
    map: Dict[str, CountryDetail] = {getattr(item, field_names[1]): item for item in Items}


class ByA3Code(ByKey):
    map: Dict[str, CountryDetail] = {getattr(item, field_names[0]): item for item in Items}


class CountryA3(Enum, metaclass=ByA3Code):
    """三字母国家代码枚举"""

    AFG = auto()
    ALA = auto()
    ALB = auto()
    DZA = auto()
    ASM = auto()
    AND = auto()
    AGO = auto()
    AIA = auto()
    ATA = auto()
    ATG = auto()
    ARG = auto()
    ARM = auto()
    ABW = auto()
    AUS = auto()
    AUT = auto()
    AZE = auto()
    BHS = auto()
    BHR = auto()
    BGD = auto()
    BRB = auto()
    BLR = auto()
    BEL = auto()
    BLZ = auto()
    BEN = auto()
    BMU = auto()
    BTN = auto()
    BOL = auto()
    BIH = auto()
    BWA = auto()
    BVT = auto()
    BRA = auto()
    VGB = auto()
    IOT = auto()
    BRN = auto()
    BGR = auto()
    BFA = auto()
    BDI = auto()
    KHM = auto()
    CMR = auto()
    CAN = auto()
    CPV = auto()
    CYM = auto()
    CAF = auto()
    TCD = auto()
    CHL = auto()
    CHN = auto()
    HKG = auto()
    MAC = auto()
    CXR = auto()
    CCK = auto()
    COL = auto()
    COM = auto()
    COG = auto()
    COD = auto()
    COK = auto()
    CRI = auto()
    CIV = auto()
    HRV = auto()
    CUB = auto()
    CYP = auto()
    CZE = auto()
    DNK = auto()
    DJI = auto()
    DMA = auto()
    DOM = auto()
    ECU = auto()
    EGY = auto()
    SLV = auto()
    GNQ = auto()
    ERI = auto()
    EST = auto()
    ETH = auto()
    FLK = auto()
    FRO = auto()
    FJI = auto()
    FIN = auto()
    FRA = auto()
    GUF = auto()
    PYF = auto()
    ATF = auto()
    GAB = auto()
    GMB = auto()
    GEO = auto()
    DEU = auto()
    GHA = auto()
    GIB = auto()
    GRC = auto()
    GRL = auto()
    GRD = auto()
    GLP = auto()
    GUM = auto()
    GTM = auto()
    GGY = auto()
    GIN = auto()
    GNB = auto()
    GUY = auto()
    HTI = auto()
    HMD = auto()
    VAT = auto()
    HND = auto()
    HUN = auto()
    ISL = auto()
    IND = auto()
    IDN = auto()
    IRN = auto()
    IRQ = auto()
    IRL = auto()
    IMN = auto()
    ISR = auto()
    ITA = auto()
    JAM = auto()
    JPN = auto()
    JEY = auto()
    JOR = auto()
    KAZ = auto()
    KEN = auto()
    KIR = auto()
    PRK = auto()
    KOR = auto()
    KWT = auto()
    KGZ = auto()
    LAO = auto()
    LVA = auto()
    LBN = auto()
    LSO = auto()
    LBR = auto()
    LBY = auto()
    LIE = auto()
    LTU = auto()
    LUX = auto()
    MKD = auto()
    MDG = auto()
    MWI = auto()
    MYS = auto()
    MDV = auto()
    MLI = auto()
    MLT = auto()
    MHL = auto()
    MTQ = auto()
    MRT = auto()
    MUS = auto()
    MYT = auto()
    MEX = auto()
    FSM = auto()
    MDA = auto()
    MCO = auto()
    MNG = auto()
    MNE = auto()
    MSR = auto()
    MAR = auto()
    MOZ = auto()
    MMR = auto()
    NAM = auto()
    NRU = auto()
    NPL = auto()
    NLD = auto()
    ANT = auto()
    NCL = auto()
    NZL = auto()
    NIC = auto()
    NER = auto()
    NGA = auto()
    NIU = auto()
    NFK = auto()
    MNP = auto()
    NOR = auto()
    OMN = auto()
    PAK = auto()
    PLW = auto()
    PSE = auto()
    PAN = auto()
    PNG = auto()
    PRY = auto()
    PER = auto()
    PHL = auto()
    PCN = auto()
    POL = auto()
    PRT = auto()
    PRI = auto()
    QAT = auto()
    REU = auto()
    ROU = auto()
    RUS = auto()
    RWA = auto()
    BLM = auto()
    SHN = auto()
    KNA = auto()
    LCA = auto()
    MAF = auto()
    SPM = auto()
    VCT = auto()
    WSM = auto()
    SMR = auto()
    STP = auto()
    SAU = auto()
    SEN = auto()
    SRB = auto()
    SYC = auto()
    SLE = auto()
    SGP = auto()
    SVK = auto()
    SVN = auto()
    SLB = auto()
    SOM = auto()
    ZAF = auto()
    SGS = auto()
    SSD = auto()
    ESP = auto()
    LKA = auto()
    SDN = auto()
    SUR = auto()
    SJM = auto()
    SWZ = auto()
    SWE = auto()
    CHE = auto()
    SYR = auto()
    TWN = auto()
    TJK = auto()
    TZA = auto()
    THA = auto()
    TLS = auto()
    TGO = auto()
    TKL = auto()
    TON = auto()
    TTO = auto()
    TUN = auto()
    TUR = auto()
    TKM = auto()
    TCA = auto()
    TUV = auto()
    UGA = auto()
    UKR = auto()
    ARE = auto()
    GBR = auto()
    USA = auto()
    UMI = auto()
    URY = auto()
    UZB = auto()
    VUT = auto()
    VEN = auto()
    VNM = auto()
    VIR = auto()
    WLF = auto()
    ESH = auto()
    YEM = auto()
    ZMB = auto()
    ZWE = auto()


class CountryA2(Enum, metaclass=ByA2Code):
    """双字母国家代码枚举"""

    AF = auto()
    AX = auto()
    AL = auto()
    DZ = auto()
    AS = auto()
    AD = auto()
    AO = auto()
    AI = auto()
    AQ = auto()
    AG = auto()
    AR = auto()
    AM = auto()
    AW = auto()
    AU = auto()
    AT = auto()
    AZ = auto()
    BS = auto()
    BH = auto()
    BD = auto()
    BB = auto()
    BY = auto()
    BE = auto()
    BZ = auto()
    BJ = auto()
    BM = auto()
    BT = auto()
    BO = auto()
    BA = auto()
    BW = auto()
    BV = auto()
    BR = auto()
    VG = auto()
    IO = auto()
    BN = auto()
    BG = auto()
    BF = auto()
    BI = auto()
    KH = auto()
    CM = auto()
    CA = auto()
    CV = auto()
    KY = auto()
    CF = auto()
    TD = auto()
    CL = auto()
    CN = auto()
    HK = auto()
    MO = auto()
    CX = auto()
    CC = auto()
    CO = auto()
    KM = auto()
    CG = auto()
    CD = auto()
    CK = auto()
    CR = auto()
    CI = auto()
    HR = auto()
    CU = auto()
    CY = auto()
    CZ = auto()
    DK = auto()
    DJ = auto()
    DM = auto()
    DO = auto()
    EC = auto()
    EG = auto()
    SV = auto()
    GQ = auto()
    ER = auto()
    EE = auto()
    ET = auto()
    FK = auto()
    FO = auto()
    FJ = auto()
    FI = auto()
    FR = auto()
    GF = auto()
    PF = auto()
    TF = auto()
    GA = auto()
    GM = auto()
    GE = auto()
    DE = auto()
    GH = auto()
    GI = auto()
    GR = auto()
    GL = auto()
    GD = auto()
    GP = auto()
    GU = auto()
    GT = auto()
    GG = auto()
    GN = auto()
    GW = auto()
    GY = auto()
    HT = auto()
    HM = auto()
    VA = auto()
    HN = auto()
    HU = auto()
    IS = auto()
    IN = auto()
    ID = auto()
    IR = auto()
    IQ = auto()
    IE = auto()
    IM = auto()
    IL = auto()
    IT = auto()
    JM = auto()
    JP = auto()
    JE = auto()
    JO = auto()
    KZ = auto()
    KE = auto()
    KI = auto()
    KP = auto()
    KR = auto()
    KW = auto()
    KG = auto()
    LA = auto()
    LV = auto()
    LB = auto()
    LS = auto()
    LR = auto()
    LY = auto()
    LI = auto()
    LT = auto()
    LU = auto()
    MK = auto()
    MG = auto()
    MW = auto()
    MY = auto()
    MV = auto()
    ML = auto()
    MT = auto()
    MH = auto()
    MQ = auto()
    MR = auto()
    MU = auto()
    YT = auto()
    MX = auto()
    FM = auto()
    MD = auto()
    MC = auto()
    MN = auto()
    ME = auto()
    MS = auto()
    MA = auto()
    MZ = auto()
    MM = auto()
    NA = auto()
    NR = auto()
    NP = auto()
    NL = auto()
    AN = auto()
    NC = auto()
    NZ = auto()
    NI = auto()
    NE = auto()
    NG = auto()
    NU = auto()
    NF = auto()
    MP = auto()
    NO = auto()
    OM = auto()
    PK = auto()
    PW = auto()
    PS = auto()
    PA = auto()
    PG = auto()
    PY = auto()
    PE = auto()
    PH = auto()
    PN = auto()
    PL = auto()
    PT = auto()
    PR = auto()
    QA = auto()
    RE = auto()
    RO = auto()
    RU = auto()
    RW = auto()
    BL = auto()
    SH = auto()
    KN = auto()
    LC = auto()
    MF = auto()
    PM = auto()
    VC = auto()
    WS = auto()
    SM = auto()
    ST = auto()
    SA = auto()
    SN = auto()
    RS = auto()
    SC = auto()
    SL = auto()
    SG = auto()
    SK = auto()
    SI = auto()
    SB = auto()
    SO = auto()
    ZA = auto()
    GS = auto()
    SS = auto()
    ES = auto()
    LK = auto()
    SD = auto()
    SR = auto()
    SJ = auto()
    SZ = auto()
    SE = auto()
    CH = auto()
    SY = auto()
    TW = auto()
    TJ = auto()
    TZ = auto()
    TH = auto()
    TL = auto()
    TG = auto()
    TK = auto()
    TO = auto()
    TT = auto()
    TN = auto()
    TR = auto()
    TM = auto()
    TC = auto()
    TV = auto()
    UG = auto()
    UA = auto()
    AE = auto()
    GB = auto()
    US = auto()
    UM = auto()
    UY = auto()
    UZ = auto()
    VU = auto()
    VE = auto()
    VN = auto()
    VI = auto()
    WF = auto()
    EH = auto()
    YE = auto()
    ZM = auto()
    ZW = auto()


# 数据完整性和一致性检验
ByA3Code.check(obj=CountryA3)
ByA2Code.check(obj=CountryA2)
