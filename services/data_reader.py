"""
data_reader.py
数据读取服务 - [100只全球核心股常驻版] L1超大容量高速缓存 + L2双云端聚合引擎
"""

import os
import json
import pandas as pd
import yfinance as yf
import urllib.request
import urllib.parse
import re
import ssl
from datetime import datetime

class Stock:
    def __init__(self, code, data):
        self.code = code
        self.name = "" 
        self.data = data
        if data is not None and not data.empty and 'Close' in data.columns:
            self.latest_price = float(data['Close'].iloc[-1])
        else:
            self.latest_price = 0.0

class DataReader:
    def __init__(self):
        self.history_file = "history.json"
        
        # 💡 [L1 100只全球核心热门股高速缓存]：0毫秒延迟，断网百分百直达
        self.stock_map = {
            # ===== A股热门股 (50只) =====
            "立昂微": "605358.SS", "沪硅产业": "688126.SS", "中芯国际": "688981.SS", "宁德时代": "300750.SZ",
            "紫金矿业": "601899.SS", "赤峰黄金": "600988.SS", "湖南黄金": "002155.SZ", "新易盛": "300502.SZ",
            "贵州茅台": "600519.SS", "茅台": "600519.SS", "五粮液": "000858.SZ", "比亚迪": "002594.SZ",
            "中国平安": "601318.SS", "招商银行": "600036.SS", "长江电力": "600900.SS", "北方华创": "002371.SZ",
            "隆基绿能": "601012.SS", "通威股份": "600438.SS", "阳光电源": "300274.SZ", "工业富联": "601138.SS",
            "海康威视": "002415.SZ", "美的集团": "000333.SZ", "格力电器": "000651.SZ", "药明康德": "603259.SS",
            "爱尔眼科": "300015.SZ", "东方财富": "300059.SZ", "中信证券": "600030.SS", "万科A": "000002.SZ",
            "保利发展": "600048.SS", "中国建筑": "601668.SS", "中国神华": "601088.SS", "中国石油": "601857.SS",
            "中国石化": "600028.SS", "中国中免": "601888.SS", "恒瑞医药": "600276.SS", "迈瑞医疗": "300760.SZ",
            "牧原股份": "002714.SZ", "海天味业": "603288.SS", "泸州老窖": "000568.SZ", "山西汾酒": "600809.SS",
            "洋河股份": "002304.SZ", "顺丰控股": "002352.SZ", "京东方A": "000725.SZ", "TCL科技": "000100.SZ",
            "三安光电": "600703.SS", "闻泰科技": "600745.SS", "兆易创新": "603986.SS", "韦尔股份": "603501.SS",
            "长电科技": "600584.SS", "科大讯飞": "002230.SZ", "歌尔股份": "002241.SZ", "立讯精密": "002475.SZ",

            # ===== 美股热门股 (50只) =====
            # 科技巨头与半导体
            "苹果": "AAPL", "微软": "MSFT", "谷歌": "GOOGL", "亚马逊": "AMZN",
            "特斯拉": "TSLA", "Meta": "META", "META": "META", "英伟达": "NVDA",
            "超微半导体": "AMD", "AMD": "AMD", "高通": "QCOM", "英特尔": "INTC",
            "博通": "AVGO", "阿斯麦": "ASML", "台积电": "TSM", "美光科技": "MU",
            "应用材料": "AMAT", "泛林集团": "LRCX", "科磊": "KLAC", "超微电脑": "SMCI",
            # 中概股龙头
            "阿里巴巴": "BABA", "百度": "BIDU", "京东": "JD", "拼多多": "PDD",
            "腾讯音乐": "TME", "网易": "NTES", "携程": "TCOM", "唯品会": "VIPS",
            "理想汽车": "LI", "蔚来": "NIO", "小鹏汽车": "XPEV", "哔哩哔哩": "BILI",
            "新东方": "EDU", "好未来": "TAL", "中芯国际美股": "SIUIF", "富途控股": "FUTU",
            # 其他美股明星行业
            "伯克希尔": "BRK-B", "可口可乐": "KO", "百事可乐": "PEP", "麦当劳": "MCD",
            "星巴克": "SBUX", "耐克": "NKE", "迪士尼": "DIS", "宝洁": "PG",
            "沃尔玛": "WMT", "好市多": "COST", "埃克森美孚": "XOM", "雪佛龙": "CVX",
            "摩根大通": "JPM", "高盛": "GS", "美国运通": "AXP", "辉瑞": "PFE"
        }

    def _create_unverified_context(self):
        """强行穿透 Mac 底层 SSL 证书验证，最大化网络连通率"""
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def _fetch_from_sina(self, keyword):
        """L2 云端通道 A：新浪财经"""
        try:
            encoded_kw = urllib.parse.quote(keyword.encode('gbk'))
            url = f"http://suggest3.sinajs.cn/suggest/type=&key={encoded_kw}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            
            with urllib.request.urlopen(req, timeout=3, context=self._create_unverified_context()) as response:
                html = response.read().decode('gbk')
                
            if '="' in html:
                data = html.split('="')[1].split('"')[0]
                if data:
                    first_item = data.split(';')[0]
                    parts = first_item.split(',')
                    if len(parts) >= 5:
                        market_code = parts[0]
                        stock_name = parts[4]
                        
                        m = re.match(r'^(sh|sz|hk|us)(.*)$', market_code, re.IGNORECASE)
                        if m:
                            market = m.group(1).lower()
                            code = m.group(2)
                            if market == 'sh': return f"{code}.SS", stock_name
                            elif market == 'sz': return f"{code}.SZ", stock_name
                            elif market == 'hk': return f"{code}.HK", stock_name
                            elif market == 'us': return code.upper(), stock_name
        except Exception as e:
            print(f"[新浪通道] 检索受阻: {e}")
        return None, None

    def _fetch_from_tencent(self, keyword):
        """L2 云端通道 B：腾讯财经"""
        try:
            encoded_kw = urllib.parse.quote(keyword)
            url = f"http://smartbox.gtimg.cn/s3/?q={encoded_kw}&t=all"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            
            with urllib.request.urlopen(req, timeout=3, context=self._create_unverified_context()) as response:
                html = response.read().decode('utf-8')
                
            if 'v_hint="' in html:
                raw_data = html.split('v_hint="')[1].split('"')[0]
                if raw_data:
                    first_result = raw_data.split('^')[0]
                    parts = [p.strip() for p in first_result.split('~') if p.strip()]
                    
                    yf_code = None
                    stock_name = keyword
                    
                    for part in parts:
                        m = re.match(r'^(sh|sz|hk)(\d{5,6})$', part, re.IGNORECASE)
                        if m:
                            market = m.group(1).lower()
                            num_code = m.group(2)
                            if market == 'sh': yf_code = f"{num_code}.SS"
                            elif market == 'sz': yf_code = f"{num_code}.SZ"
                            elif market == 'hk': yf_code = f"{num_code}.HK"
                            break
                        elif part.startswith('us') and len(part) > 2 and part[2:].isalpha():
                            yf_code = part[2:].upper()
                            break

                    for part in parts:
                        if re.search(r'[\u4e00-\u9fa5]', part) and "股" not in part:
                            stock_name = part
                            break
                    if yf_code:
                        return yf_code, stock_name
        except Exception as e:
            print(f"[腾讯通道] 检索受阻: {e}")
        return None, None

    def resolve_stock_code(self, keyword):
        """核心智能路由控制层"""
        keyword = str(keyword).strip()
        if not keyword:
            return None, None

        # 1. 历史记录完美闭环（直接提取括号内代码）
        parentheses_match = re.search(r'[（\(]([A-Za-z0-9\.]+)[）\)]', keyword)
        if parentheses_match:
            extracted_code = parentheses_match.group(1).upper()
            name_part = re.split(r'[（\(]', keyword)[0].strip()
            if extracted_code.isdigit() and len(extracted_code) == 6:
                extracted_code = f"{extracted_code}.SS" if extracted_code.startswith(('6', '688', '900')) else f"{extracted_code}.SZ"
            return extracted_code, name_part

        # 2. 💡 [L1 极速命中] 优先检查 100只常驻核心大字典，断网直接秒杀！
        if keyword in self.stock_map:
            return self.stock_map[keyword], keyword

        # 3. 纯英文(美股代码如 AAPL) 或带有标准后缀的代码直接放行
        if (keyword.isascii() and keyword.isalpha()) or keyword.endswith((".SS", ".SZ", ".HK", ".US")):
            return keyword.upper(), keyword.upper()

        # 4. 💡 [L2 云端联想] 如果是非高频的生僻股，调用双通道动态匹配
        yf_code, stock_name = self._fetch_from_sina(keyword)
        if yf_code:
            print(f"[云端联想-新浪] {keyword} -> {stock_name}({yf_code})")
            return yf_code, stock_name
            
        yf_code, stock_name = self._fetch_from_tencent(keyword)
        if yf_code:
            print(f"[云端联想-腾讯] {keyword} -> {stock_name}({yf_code})")
            return yf_code, stock_name
            
        # 5. 最终底线防火墙拦截
        if re.search(r'[\u4e00-\u9fa5]', keyword):
            return None, None 
        return keyword, keyword

    def download_data(self, code, start=None, end=None):
        # 1. 明确区间策略：如果不传 start，默认拉取最近 5 年（这通常能覆盖上市至今且雅虎最稳定）
        if start is None:
            # 这里的 period="5y" 既是全量历史的替代品，也是 yfinance 最稳定的区间
            print(f"[量化引擎] 检测到全量请求，采用 5 年稳定区间: {code}")
            df = yf.download(code, period="5y", progress=False, ignore_tz=True)
        else:
            # 用户指定了特定日期
            print(f"[量化引擎] 正在拉取 {code} 真实数据... ({start} 至 {end})")
            df = yf.download(code, start=start, end=end, progress=False, ignore_tz=True)
            
        # 2. 只有在真的没数据时，才进行最后的“半年数据”保底降级
        if df.empty:
            print(f"[量化引擎] ⚠️ 原始区间未获取到数据，触发降级至半年数据...")
            df = yf.download(code, period="6mo", progress=False, ignore_tz=True)
            
            if df.empty:
                raise ValueError(f"未检索到 {code} 的数据。")
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        return Stock(code, df)

    def save_to_history(self, display_name, price, currency="CNY"):
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "code": display_name,
            "price": float(price),
            "currency": currency
        }
        history = self.load_history()
        history.append(record)
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def load_history(self):
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []