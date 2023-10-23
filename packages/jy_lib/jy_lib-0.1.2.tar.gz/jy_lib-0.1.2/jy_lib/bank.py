# -*- coding: utf-8 -*-
"""国内银行枚举"""
from collections import namedtuple
from enum import auto, Enum
from typing import List, Dict
from jy_enums.base import ByKey
# https://www.swift.com/

field_names: List[str] = ['swift_code', 'cn_name']
BankDetail = namedtuple(typename='BankDetail', field_names=field_names)
tsv: str = '''
BKCHCNBJ\t中国银行
ABOCCNBJ\t农业银行
PCBCCNBJ\t建设银行
COMMCNSH\t交通银行
CHBHCNBT\t渤海银行
CIBKCNBJ\t中信银行
CMBCCNBS\t招商银行
EVERCNBJ\t光大银行
MSBCCNBJ\t民生银行
HXBKCNBJ\t华夏银行
GDBKCN22\t广发银行
FJIBCNBA\t兴业银行
SPDBCNSH\t上海浦东发展银行
SDBCCNBJ\t国家开发银行
SZDBCNBS\t平安银行
HFBACNSD\t恒丰银行
HSBCCNSH\t汇丰银行（中国）有限公司
BEASCNSH\t东亚银行（中国）有限公司
SCBLCNSX\t渣打银行（中国）有限公司
HZCBCN2H\t杭州银行
HCCBCNBH\t哈尔滨银行
HASECNSH\t恒生银行
BJCNCNBJ\t北京银行
BKNBCN2N\t宁波银行
JZCBCNBJ\t锦州银行
CITICNSX\t花旗银行（中国）有限公司
DBSSCNSH\t星展银行（中国）有限公司
BKSHCNBJ\t河北银行
IBXHCNBA\t厦门国际银行
CBXMCNBA\t厦门银行
ZBBKCNBZ\t齐商银行
HSSYCNBH\t内蒙古银行
BOSHCNSH\t上海银行
WZCBCNSH\t温州银行
BOTKCNSH\t三菱东京日联银行（中国）有限公司
RZCBCNBD\t日照银行
BTCBCNBJ\t包头银行
IBKOCNBT\t韩国兴业银行（中国）有限公司
MHCBCNSH\t瑞穗银行（中国）有限公司
DEUTCNSH\t德意志银行（中国）有限公司
LWCBCNBJ\t莱商银行
ANZBCNSH\t澳大利亚及新西兰银行（中国）有限公司
SHBKCNBJ\t新韩银行（中国）有限公司
CZNBCNBJ\t国民银行（中国）有限公司
BKKBCNSH\t曼谷银行（中国）有限公司
CCBCCNBK\t长华商业银行
CKLBCNBJ\t昆仑银行
DYSHCNBJ\t东营银行
CIYUCNBA\t赤渝银行
FSBCCNSH\t富邦银行（中国）有限公司
ICBCCNBS\t大型国际商业银行
WPACCNSX\t西太平洋银行
QCCBCNBQ\t青岛银行
DECLCNBJ\t德州银行
FCBKCNSH\t第一商业银行
DSBACNBX\t大新银行（中国）有限公司
MSBKCN22\t摩根士丹利国际银行(中国)有限公司
TACBCNBS\t台湾合作银行
PSBCCNBJ\t中国邮政储蓄银行
BINHCN2N\t宁波商业银行
CHASCNBJ\t摩根大通银行（中国）有限公司
LCHBCN22\t创兴银行
UWCBCNSH\t国泰联合银行（中国）有限公司
YCCBCNBY\t宁夏银行
OUBKCNB1\t海外联合银行
LYCBCNBL\t临商银行
BOJJCNBJ\t九江银行
CHCCCNSS\t长沙银行
BOJSCNBN\t江苏银行
HNBKCNBS\t华南商业银行
KCCBCN2K\t富滇银行
SCBKCNBS\t上海商业银行
CRLYCNSH\t法国农业信贷银行（中国）有限公司
WFCBCNBN\t潍坊银行
RZBACNBJ\t瑞丰国际银行
UOVBCNSH\t联合海外银行（中国）有限公司
SBINCNSH\t印度国家银行
NJCBCNBN\t南京银行
BOFMCNBJ\t蒙特利尔银行（中国）有限公司
DLCBCNBD\t大连银行
BNPACNSH\t法国巴黎银行（中国）有限公司
SYCBCNBY\t盛京银行
TCCBCNBT\t天津银行
HRXJCNBC\t华容银行
MBTCCNBN\t大都会银行（中国）有限公司
RBOSCNS1\t苏格兰皇家银行
APGTCN21\t亚太银行
CTGBCN22\t重庆三峡银行
CCIBCNB1\t中国信贷产业银行
BOFMCNSH\t蒙特利尔银行（中国）有限公司
GDPBCN22\t广东南岳银行
SSVBCNSH\t浦发硅谷银行
ZCCBCN22\t珠海华润银行
WHCBCNBN\t汉口银行
WHBKCNBJ\t威海市商业银行
HVBKCNBJ\t友利银行（中国）有限公司
HFCBCNSH\t徽商银行
FXBKCNBJ\t阜新银行
TZBKCNBT\t泰州银行
YZBKCN2N\t鄞州银行
KWHKCNBS\t中信银行国际（中国）有限公司
SWEDCNSH\t瑞典银行
FZCBCNBS\t福建海下银行
BKJNCNBJ\t济宁银行
CQCBCN22\t重庆银行
COXICNBA\t联合商业银行
DEUTCNBJ\t德意志银行（中国）有限公司
YTCBCNSD\t烟台银行
ZJMTCNSH\t浙江民泰商业银行
NXBKCNBH\t南浔银行
EWBKCNSH\t华美银行（中国）有限公司
JHCBCNBJ\t金华银行
BOFMCN22\t蒙特利尔银行（中国）有限公司
LCOMCNBJ\t辽阳银行
GDHBCN22\t广东华兴银行
KRTHCNB1\t泰国国立银行
COBACNSX\t德国商业银行
YKCBCNBJ\t营口银行
SCBLCNB1\t渣打银行
SMBCCNSH\t三井住友银行（中国）有限公司
ZJCBCN2N\t浙商银行
CTBACNSH\t澳大利亚联邦银行
KREDCNSX\t比利时联合银行
LJBCCNBH\t龙江银行
BKQZCNBZ\t泉州银行
CBOCCNBC\t成都银行
CNMBCNBS\t中国商业银行
BSHLCNS1\t巴林银行
PASCCNSH\t锡耶纳蒙特银行
KWPBCNB1\t广东省银行
GZCBCN22\t广州银行
LSCCCNBL\t乐山市商业银行
GYCBCNSI\t贵阳银行
'''
BankDetails: List[BankDetail] = [BankDetail(*line.strip().split('\t')) for line in tsv.splitlines() if line]


class BySwiftCode(ByKey):
    map: Dict[str, BankDetail] = {getattr(item, field_names[0]): item for item in BankDetails}


class BankSC(Enum, metaclass=BySwiftCode):
    BKCHCNBJ = auto()
    ABOCCNBJ = auto()
    PCBCCNBJ = auto()
    COMMCNSH = auto()
    CHBHCNBT = auto()
    CIBKCNBJ = auto()
    CMBCCNBS = auto()
    EVERCNBJ = auto()
    MSBCCNBJ = auto()
    HXBKCNBJ = auto()
    GDBKCN22 = auto()
    FJIBCNBA = auto()
    SPDBCNSH = auto()
    SDBCCNBJ = auto()
    SZDBCNBS = auto()
    HFBACNSD = auto()
    HSBCCNSH = auto()
    BEASCNSH = auto()
    SCBLCNSX = auto()
    HZCBCN2H = auto()
    HCCBCNBH = auto()
    HASECNSH = auto()
    BJCNCNBJ = auto()
    BKNBCN2N = auto()
    JZCBCNBJ = auto()
    CITICNSX = auto()
    DBSSCNSH = auto()
    BKSHCNBJ = auto()
    IBXHCNBA = auto()
    CBXMCNBA = auto()
    ZBBKCNBZ = auto()
    HSSYCNBH = auto()
    BOSHCNSH = auto()
    WZCBCNSH = auto()
    BOTKCNSH = auto()
    RZCBCNBD = auto()
    BTCBCNBJ = auto()
    IBKOCNBT = auto()
    MHCBCNSH = auto()
    DEUTCNSH = auto()
    LWCBCNBJ = auto()
    ANZBCNSH = auto()
    SHBKCNBJ = auto()
    CZNBCNBJ = auto()
    BKKBCNSH = auto()
    CCBCCNBK = auto()
    CKLBCNBJ = auto()
    DYSHCNBJ = auto()
    CIYUCNBA = auto()
    FSBCCNSH = auto()
    ICBCCNBS = auto()
    WPACCNSX = auto()
    QCCBCNBQ = auto()
    DECLCNBJ = auto()
    FCBKCNSH = auto()
    DSBACNBX = auto()
    MSBKCN22 = auto()
    TACBCNBS = auto()
    PSBCCNBJ = auto()
    BINHCN2N = auto()
    CHASCNBJ = auto()
    LCHBCN22 = auto()
    UWCBCNSH = auto()
    YCCBCNBY = auto()
    OUBKCNB1 = auto()
    LYCBCNBL = auto()
    BOJJCNBJ = auto()
    CHCCCNSS = auto()
    BOJSCNBN = auto()
    HNBKCNBS = auto()
    KCCBCN2K = auto()
    SCBKCNBS = auto()
    CRLYCNSH = auto()
    WFCBCNBN = auto()
    RZBACNBJ = auto()
    UOVBCNSH = auto()
    SBINCNSH = auto()
    NJCBCNBN = auto()
    BOFMCNBJ = auto()
    DLCBCNBD = auto()
    BNPACNSH = auto()
    SYCBCNBY = auto()
    TCCBCNBT = auto()
    HRXJCNBC = auto()
    MBTCCNBN = auto()
    RBOSCNS1 = auto()
    APGTCN21 = auto()
    CTGBCN22 = auto()
    CCIBCNB1 = auto()
    BOFMCNSH = auto()
    GDPBCN22 = auto()
    SSVBCNSH = auto()
    ZCCBCN22 = auto()
    WHCBCNBN = auto()
    WHBKCNBJ = auto()
    HVBKCNBJ = auto()
    HFCBCNSH = auto()
    FXBKCNBJ = auto()
    TZBKCNBT = auto()
    YZBKCN2N = auto()
    KWHKCNBS = auto()
    SWEDCNSH = auto()
    FZCBCNBS = auto()
    BKJNCNBJ = auto()
    CQCBCN22 = auto()
    COXICNBA = auto()
    DEUTCNBJ = auto()
    YTCBCNSD = auto()
    ZJMTCNSH = auto()
    NXBKCNBH = auto()
    EWBKCNSH = auto()
    JHCBCNBJ = auto()
    BOFMCN22 = auto()
    LCOMCNBJ = auto()
    GDHBCN22 = auto()
    KRTHCNB1 = auto()
    COBACNSX = auto()
    YKCBCNBJ = auto()
    SCBLCNB1 = auto()
    SMBCCNSH = auto()
    ZJCBCN2N = auto()
    CTBACNSH = auto()
    KREDCNSX = auto()
    LJBCCNBH = auto()
    BKQZCNBZ = auto()
    CBOCCNBC = auto()
    CNMBCNBS = auto()
    BSHLCNS1 = auto()
    PASCCNSH = auto()
    KWPBCNB1 = auto()
    GZCBCN22 = auto()
    LSCCCNBL = auto()
    GYCBCNSI = auto()


# 数据完整性和一致性检验
BySwiftCode.check(obj=BankSC)
