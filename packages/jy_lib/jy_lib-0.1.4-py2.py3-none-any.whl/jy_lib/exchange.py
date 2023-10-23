# -*- coding: utf-8 -*-
"""国内交易所及部分国外交易所枚举"""
from collections import namedtuple
from enum import auto, Enum
from typing import Dict, List
from .base import ByKey

# https://www.iso20022.org/market-identifier-codes
# https://www.tradinghours.com/mic?country[]=CN&page=1#results

field_names: List[str] = ["mic", "en_name", "cn_name", "acronym", "website"]
ExchangeDetail = namedtuple(typename="ExchangeDetail", field_names=field_names)
tsv: str = """
BJSE\tBEIJING STOCK EXCHANGE\t北京证券交易所\tBSE\twww.bse.cn
CCFX\tCHINA FINANCIAL FUTURES EXCHANGE\t中国金融期货交易所\tCFFEX\twww.cffex.com.cn
NEEQ\tNATIONAL EQUITIES EXCHANGE AND QUOTATIONS\t全国中小企业股份转让系统\tNEEQ\twww.neeq.com.cn
SGEX\tSHANGHAI GOLD EXCHANGE\t上海黄金交易所\tSGE\twww.sge.sh
XCFE\tCHINA FOREIGN EXCHANGE TRADE SYSTEM\t中国外汇交易系统\tCFETS\twww.chinamoney.com.cn
XDCE\tDALIAN COMMODITY EXCHANGE\t大连商品交易所\tDCE\twww.dce.com.cn
XINE\tSHANGHAI INTERNATIONAL ENERGY EXCHANGE\t上海国际能源交易中心\tINE\twww.ine.cn
XSGE\tSHANGHAI FUTURES EXCHANGE\t上海期货交易所\tSHFE\twww.shfe.com.cn
XSHE\tSHENZHEN STOCK EXCHANGE\t深圳证券交易所\tSZSE\twww.szse.cn
XSHG\tSHANGHAI STOCK EXCHANGE\t上海证券交易所\tSSE\twww.szse.cn
XZCE\tZHENGZHOU COMMODITY EXCHANGE\t郑州商品交易所\tZCE\twww.czce.com.cn
CBTS\tCME SWAPS MARKETS (CBOT)\t芝加哥期货交易所\tCBOT\twww.cmegroup.com
CECS\tCME SWAPS MARKETS (COMEX)\t纽约商品交易所\tCOMEX\twww.cmegroup.com
CMES\tCME SWAPS MARKETS (CME)\t芝加哥商业交易所\tCME\twww.cmegroup.com
NYMS\tCME SWAPS MARKETS (NYMEX)\t纽约商品交易所\tNYMEX\twww.cmegroup.com
XLME\tLONDON METAL EXCHANGE\t伦敦金属交易所\tLME\twww.lme.co.uk
XTKT\tTOKYO COMMODITY EXCHANGE\t东京商品交易所\tTOCOM\twww.tocom.or.jp
XSCE\tSINGAPORE COMMODITY EXCHANGE\t新加坡商品交易所\tSICOM\twww.sgx.com
"""

Items: List[ExchangeDetail] = [ExchangeDetail(*line.strip().split("\t")) for line in tsv.splitlines() if line]


class ByMic(ByKey):
    map: Dict[str, ExchangeDetail] = {getattr(item, field_names[0]): item for item in Items}


class ByAcronym(ByKey):
    map: Dict[str, ExchangeDetail] = {getattr(item, field_names[3]): item for item in Items}


class ExchangeMic(Enum, metaclass=ByMic):
    """交易所MIC枚举"""

    BJSE = auto()
    CCFX = auto()
    NEEQ = auto()
    SGEX = auto()
    XCFE = auto()
    XDCE = auto()
    XINE = auto()
    XSGE = auto()
    XSHE = auto()
    XSHG = auto()
    XZCE = auto()
    CBTS = auto()
    CECS = auto()
    CMES = auto()
    NYMS = auto()
    XLME = auto()
    XTKT = auto()
    XSCE = auto()


class ExchangeAcronym(Enum, metaclass=ByAcronym):
    """交易所简称枚举"""

    BSE = auto()
    CFFEX = auto()
    NEEQ = auto()
    SGE = auto()
    CFETS = auto()
    DCE = auto()
    INE = auto()
    SHFE = auto()
    SZSE = auto()
    SSE = auto()
    ZCE = auto()
    CBOT = auto()
    COMEX = auto()
    CME = auto()
    NYMEX = auto()
    LME = auto()
    TOCOM = auto()
    SICOM = auto()


# 数据完整性和一致性检验
ByMic.check(obj=ExchangeMic)
ByAcronym.check(obj=ExchangeAcronym)
