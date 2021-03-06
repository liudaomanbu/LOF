import time
import requests
import re
import pytz
from datetime import datetime


class LOF:
    def __init__(self):
        # 可注释掉不需要的数据
        self.s = {
            "代码": "fund_id",
            "名称": "fund_nm",
            "现价": "price",
            "涨幅": "increase_rt",
            "基金净值": "fund_nav",
            "实时估值": "estimate_value",
            "溢价率": "discount_rt",
        }
        # 可在列表中添加想要监控的LOF
        self.LOFList = [161005, 163402, 163417, 165309]
        self.LOFList.sort()

        self.session = requests.Session()
        header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",}
        self.session.headers.update(header)
        self.urlBase = "https://www.jisilu.cn/data/lof/detail/"
        self.urlLOF = "https://www.jisilu.cn/data/lof/stock_lof_list/?___jsl=LST___t="

        self.apiKey = "ServerChanKey"
    

    def getInfo(self, id):
        r = self.session.get(self.urlLOF + str(int(time.time())*1000))
        if r.status_code == 200:
            r = r.json()
        else:
            return
        rows = [row["cell"] for row in r["rows"] if int(row["id"]) in self.LOFList]

        res = []
        for row in rows:
            s = {}
            for key, value in self.s.items():
                s[key] = row[value]
            res.append(s)
        return res

    def md(self, info):
        if not info: return
        res = ["| " + " | ".join(list(info[0])) + " |"]
        res.append("| " + " :---: | " * (len(info[0]) - 1) + " :---: |")
        for i in info:
            res.append("| " + " | ".join(list(i.values())) + " |")
        res = "\n".join(res)
        return res

    def message(self, key, title, body):
        msg_url = "https://sc.ftqq.com/{}.send?text={}&desp={}".format(key, title, body)
        requests.get(msg_url)

    def main(self):
        info = self.getInfo(id)
        md = self.md(info)
        self.message(self.apiKey, "LOF-溢价: " + datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%m-%d %H:%M"), md)


if __name__ == "__main__":
    lof = LOF()
    lof.main()
