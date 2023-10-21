import numpy as np
import pandas as pd
import glob
from typing import List, Union
from .constants import NetValueData


def ppwnvformatter(ppwnvdf, df=True) -> Union[List[NetValueData], pd.DataFrame]:
    """
    将ppwdbapi的净值数据转换为gytoolkit定义的净值数据
    """
    cols = [
        "date",
        "prodcode",
        "netvalue",
        "cum_netvalue",
        "prodname",
        "netasset",
        "shares",
    ]
    col_map = {
        "净值日期": "date",
        "备案编码": "prodcode",
        "单位净值": "netvalue",
        "累计净值": "cum_netvalue",
        "产品简称": "prodname",
    }
    ppwnvdf.rename(columns=col_map, inplace=True)
    ppwnvdf[["netasset","shares"]] = np.nan
    ppwnvdf = ppwnvdf[cols]
    if df:
        return ppwnvdf.set_index(["date","prodcode"])
    else:
        return [NetValueData(**row) for index,row in ppwnvdf.itertuples()]

def otcnvformatter(folder_path: str,df=True) -> Union[List[NetValueData], pd.DataFrame]:
    cols = [
        "date",
        "prodcode",
        "netvalue",
        "cum_netvalue",
        "prodname",
        "netasset",
        "shares",
    ]
    col_map = {
        "净值日期": "date",
        "产品编码": "prodcode",
        "最新净值": "netvalue",
        "累计净值": "cum_netvalue",
        "产品简称": "prodname",
    }
    otcnvdf = get_otc(folder_path)
    otcnvdf.rename(columns=col_map, inplace=True)
    otcnvdf[["netasset","shares"]] = np.nan
    otcnvdf = otcnvdf[cols]
    if df:
        return otcnvdf.set_index(["date","prodcode"])
    else:
        return [NetValueData(**row) for index,row in otcnvdf.itertuples()]


def get_otc(folder_path: str):
    file_paths = glob.glob(folder_path + "/*.xlsx")
    otc_nv_list = []
    for file in file_paths:
        otc_nv_list.append(
            pd.read_excel(file, header=8)[:-1][
                ["产品编码", "净值日期", "产品简称", "最新净值", "累计净值"]
            ].drop_duplicates(subset=["产品编码", "净值日期"], keep="last")
        )
    otc_nv = pd.concat(otc_nv_list).drop_duplicates(
        subset=["产品编码", "净值日期"], keep="last"
    )
    otc_nv["净值日期"] = pd.to_datetime(otc_nv["净值日期"])
    return otc_nv

# class NetValueManager:
#     def __init__(self) -> None:
#         self.api = {}
#         self.netvalues: List[NetValueData] = []

#     def set_ppwdbapi(self, username, password, addr):
#         ppwdbapi.login(username=username, password=password, addr=addr)
#         self.api["ppwdb"] = ppwdbapi

#     def set_mailapi(self, username, password):
#         mailclient = mailparser.MailClient(username=username, password=password)
#         self.api["mail"] = mailclient

#     def update_local_mail(self, local_mail_file, depth=50):
#         mail_api = self.api.get("mail")
#         if mail_api:
#             headers = mail_api.get_mail_header(lookin_depth=depth)
#             nv_list = mail_api.parse_mails(headers)
#             mail_api.save_netvalue(nv_list, local_mail_file)

#     def get_mail(self, local_mail_file):
#         mail_nv = pd.read_excel(local_mail_file)

#         nv_list = mail_nv.apply(
#             lambda row: NetValueData(
#                 date=row["date"],
#                 prodcode=row["prodcode"],
#                 netvalue=row["netvalue"],
#                 cum_netvalue=row["cum_netvalue"],
#                 prodname=row["prodname"],
#                 netasset=row["netasset"],
#                 shares=row["shares"],
#             ),
#             axis=1,
#         ).tolist()
#         self.netvalues.extend(nv_list)

#     def get_otc(self, folder_path: str):
#         file_paths = glob.glob(folder_path + "/*.xlsx")
#         otc_nv_list = []
#         for file in file_paths:
#             otc_nv_list.append(
#                 pd.read_excel(file, header=8)[:-1][
#                     ["产品编码", "净值日期", "产品简称", "最新净值", "累计净值"]
#                 ].drop_duplicates(subset=["产品编码", "净值日期"], keep="last")
#             )
#         otc_nv = pd.concat(otc_nv_list).drop_duplicates(
#             subset=["产品编码", "净值日期"], keep="last"
#         )
#         otc_nv["净值日期"] = pd.to_datetime(otc_nv["净值日期"])

#         nv_list = []
#         for row in otc_nv.itertuples():
#             nv = NetValueData(
#                 date=row["净值日期"],
#                 prodcode=row["产品编码"],
#                 prodname=row["产品简称"],
#                 netvalue=float(row["最新净值"]),
#                 cum_netvalue=float(row["累计净值"]),
#             )
#             nv_list.append(nv)
#         self.netvalues.extend(nv_list)

#     def get_local(self, file_path: str):
#         local_nv = pd.read_excel(file_path).drop_duplicates()
#         local_nv = local_nv.convert_dtypes(infer_objects=True)
#         local_nv["最新净值日期"] = pd.to_datetime(local_nv["最新净值日期"])

#         nv_list = local_nv.apply(
#             lambda row: NetValueData(
#                 date=row["最新净值日期"],
#                 prodcode=row["基金代码"],
#                 netvalue=row["最新净值"],
#                 cum_netvalue=row["最新累计净值"],
#                 netasset=row["基金资产净值"],
#                 shares=row["基金资产份额"],
#             ),
#             axis=1,
#         ).tolist()
#         self.netvalues.extend(nv_list)

#     def get_nv(self, codes: List[str], df=True):
#         funds = ppwdbapi.get_fund(reg_ids=codes)
#         net_values = ppwdbapi.get_netvalue(funds.index)

#         return self.source
