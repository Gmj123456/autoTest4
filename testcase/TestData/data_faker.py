import random
from faker import Faker
from faker.providers import BaseProvider

faker = Faker()
# faker = Faker('zh_CN') # 中文

email = faker.email()
username = faker.name()
country = faker.country()

print(email)
print(username)
print(country)


# 自定义数据范围
class MyProvider(BaseProvider):
    # 国家
    def country(self):
        data = {
            "香港特别行政区": "HK", "中国": "CN", "美国": "US", "英国": "GB", "印度": "IN", "泰国": "TH", "日本": "JP",
            "阿联酋": "AE", "阿富汗": "AF", "阿尔巴尼亚": "AL", "亚美尼亚": "AM", "安哥拉": "AO", "阿根廷": "AR",
            "奥地利": "AT", "澳大利亚": "AU", "阿塞拜疆": "AZ", "孟加拉": "BD", "比利时": "BE", "布基纳法索": "BF",
            "保加利亚": "BG", "巴林": "BH", "布隆迪": "BI", "贝宁": "BJ", "巴勒斯坦": "BL", "文莱": "BN",
            "玻利维亚": "BO", "巴西": "BR", "博茨瓦纳": "BW", "白俄罗斯": "BY", "加拿大": "CA", "中非": "CF",
            "刚果": "CG", "瑞士": "CH", "智利": "CL", "喀麦隆": "CM", "哥伦比亚": "CO", "哥斯达黎加": "CR",
            "捷克": "CS", "古巴": "CU", "塞浦路斯": "CY", "德国": "DE", "丹麦": "DK", "多米尼加共和国": "DO",
            "阿尔及利亚": "DZ", "厄瓜多尔": "EC", "爱沙尼亚": "EE", "埃及": "EG", "西班牙": "ES", "埃塞俄比亚": "ET",
            "芬兰": "FI", "斐济": "FJ", "法国": "FR", "加蓬": "GA", "格林纳达": "GD", "格鲁吉亚": "GE", "加纳": "GH",
            "几内亚": "GN", "希腊": "GR", "危地马拉": "GT", "洪都拉斯": "HN", "匈牙利": "HU", "印度尼西亚": "ID",
            "爱尔兰": "IE", "以色列": "IL", "伊拉克": "IQ", "伊朗": "IR", "冰岛": "IS", "意大利": "IT", "牙买加": "JM",
            "约旦": "JO", "吉尔吉斯坦": "KG", "柬埔寨": "KH", "北朝鲜": "KP", "韩国": "KR", "科特迪瓦共和国": "KT",
            "科威特": "KW", "哈萨克": "KZ", "老挝": "LA", "黎巴嫩": "LB", "圣卢西亚": "LC", "列支敦士登": "LI",
            "斯里兰卡": "LK", "利比里亚": "LR", "立陶宛": "LT", "卢森堡": "LU", "拉脱维亚": "LV", "利比亚": "LY",
            "摩洛哥": "MA", "摩纳哥": "MC", "摩尔多瓦": "MD", "马达加斯加": "MG", "马里": "ML", "缅甸": "MM", "蒙古": "MN",
            "澳门地区": "MO", "马耳他": "MT", "毛里求斯": "MU", "马拉维": "MW", "墨西哥": "MX", "马来西亚": "MY",
            "莫桑比克": "MZ", "纳米比亚": "NA", "尼日尔": "NE", "尼日利亚": "NG", "尼加拉瓜": "NI", "荷兰": "NL",
            "挪威": "NO", "尼泊尔": "NP", "新西兰": "NZ", "阿曼": "OM", "巴拿马": "PA", "秘鲁": "PE", "巴布亚新几内亚": "PG",
            "菲律宾": "PH", "巴基斯坦": "PK", "波兰": "PL", "葡萄牙": "PT", "巴拉圭": "PY", "卡塔尔": "QA", "罗马尼亚": "RO",
            "俄罗斯": "RU", "沙特阿拉伯": "SA", "塞舌尔": "SC", "苏丹": "SD", "瑞典": "SE", "新加坡": "SG", "斯洛文尼亚": "SI",
            "斯洛伐克": "SK", "圣马力诺": "SM", "塞内加尔": "SN", "索马里": "SO", "叙利亚": "SY", "斯威士兰": "SZ", "乍得": "TD",
            "多哥": "TG", "塔吉克斯坦": "TJ", "土库曼": "TM", "突尼斯": "TN", "土耳其": "TR", "台湾省": "TW", "坦桑尼亚": "TZ",
            "乌克兰": "UA", "乌干达": "UG", "乌拉圭": "UY", "乌兹别克": "UZ", "圣文森特岛": "VC", "委内瑞拉": "VE", "越南": "VN",
            "也门": "YE", "南斯拉夫联盟": "YU", "南非": "ZA", "赞比亚": "ZM", "扎伊尔": "ZR", "津巴布韦": "ZW"
        }
        return random.choice(list(data.keys()))
    # 性别
    def gender(self):
        return random.choice(['男','女'])
    # 内容
    def content(self):
        return random.choice(["TikTok视频", "IG Reel", "IG Story", "YT专题5-10min", "YT插播2-3min", "IG Post", "TK直播"])

    # 标签类型
    def label_type(self):
        return random.choice(["标签", "关键词", "种子视频", "种子账号", "关注列表"])
# 添加到Faker实例
faker.add_provider(MyProvider)

# 使用自定义提供者
print(faker.country())   # 随机国家名
print(faker.gender())
print(faker.content())
print(faker.label_type())