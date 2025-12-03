import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import load_workbook

def extract_items_from_page(name):
    """
    从指定的 PRTS 页面中提取符合条件的 <div> 标签内容。
    
    参数:
        url (str): PRTS 页面的 URL。
    
    返回:
        list: 包含 (title, span_text) 元组的列表。
    """
    base_url = "https://prts.wiki/w/"
    url = f"{base_url}{name}"
    # 发送 HTTP 请求
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return []

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有符合条件的 <div> 标签
    items = soup.find_all('div', style="display:inline-block;position:relative")

    # 提取数据
    results = []
    for item in items:
        # 查找 <a> 标签
        a_tag = item.find('a')
        if a_tag:
            title = a_tag.get('title')  # 获取 title 属性
            # 查找 <span> 标签
            span_tag = item.find('span')
            if span_tag:
                span_text = span_tag.get_text(strip=True)  # 获取 span 标签的文本内容
                results.append((title, span_text))
    
    return results

def find_effective_reason(title: str, df: pd.DataFrame):
    """
    根据 title 在 DataFrame 中查找对应的等效理智。
    
    参数:
        title (str): 物品名称。
        df (pd.DataFrame): 包含物品名称和等效理智的 DataFrame。
    
    返回:
        str: 对应的等效理智，如果未找到则返回 "未找到"。
    """
    # 在 DataFrame 中查找 title 对应的行
    row = df[df['物品名称'] == title]
    if not row.empty:
        # 返回等效理智
        return str(row['等效理智'].values[0])
    else:
        return "未找到"
    
    

    
def convert_to_number(value: str) -> int:

    value = value.strip()  # 去除首尾空格
    if value.endswith('w') or value.endswith('万'):
        # 如果以 'w' 或 '万' 结尾，去掉后缀并乘以 10000
        return int(float(value[:-1]) * 10000)
    else:
        # 否则直接转换为整数
        return int(value)
    
    
    
def calculate_total_effective_reason(result: list, df: pd.DataFrame):
    """
    根据结果列表计算每个物品的等效理智总和。
    
    参数:
        result (list): 包含 (title, span_text) 的列表。
        df (pd.DataFrame): 包含物品名称和等效理智的 DataFrame。
    
    返回:
        list: 包含 (title, 等效理智总和) 的列表。
    """
    total_reasons = []
    for title, span_text in result:
        # 查找等效理智
        effective_reason = find_effective_reason(title, df)
        if effective_reason == "未找到":
            print(f"未找到物品 '{title}' 的等效理智")
            continue
        
        # 将等效理智转换为数字
        effective_reason = float(effective_reason)
        
        # 将 span_text 转换为数字
        try:
            quantity = convert_to_number(span_text)
        except ValueError:
            print(f"无法解析数量 '{span_text}'")
            continue
        
        # 计算等效理智总和
        total_reason = effective_reason * quantity
        total_reasons.append((title, total_reason))
    
    return total_reasons








if __name__ == "__main__":
    # 读取物品价值表
    excel_path = '物品价值表.xlsx'
    df = pd.read_excel(excel_path)
    
    # 读取干员名单
    people_path = '干员名单.xlsx'
    pe = pd.read_excel(people_path, engine='openpyxl')
    
    star6 = ['推进之王', '风笛', '嵯峨', '琴柳', '焰尾', '伺夜', '伊内丝', '缪尔赛思', '忍冬', '凛冬', '银灰', '斯卡蒂', '陈', '赫拉格', '煌', '棘刺', '史尔特尔', '山', '帕拉斯', '耀骑士临光', '艾丽妮', '百炼嘉维尔', '玛恩纳', '重岳', '仇白', '圣约送葬人', '赫德雷', '止颂', '薇薇安娜', '锏', '左乐', '乌尔比安', '佩佩', '维娜·维多利亚', '隐德来希', '星熊', '塞雷娅', '年', '森蚺', '瑕光', '泥岩', '号角', '斥罪', '涤火杰西卡', '黍', '余', '伊芙利特', '艾雅法拉', '莫斯提马', '刻俄柏', '夕', '异客', '卡涅利安', '澄闪', '黑键', '林', '霍尔海雅', '逻各斯', '妮芙', '玛露西尔', '荒芜拉普兰德', '烛煌', '能天使', '黑', 'W', '早露', '迷迭香', '空弦', '灰烬', '假日威龙陈', '远牙', '菲亚梅塔', '鸿雪', '提丰', '莱伊', '维什戴尔', '娜仁图亚', '闪灵', '夜莺', '凯尔希', '流明', '焰影苇草', '纯烬艾雅法拉', '安洁莉娜', '麦哲伦', '铃兰', '浊心斯卡蒂', '灵知', '令', '白铁', '淬羽赫默', '塑心', '魔王', '阿', '傀影', '温蒂', '歌蕾蒂娅', '水月', '老鲤', '归溟幽灵鲨', '多萝西', '缄默德克萨斯', '麒麟R夜刀', '琳琅诗怀雅', '艾拉', '阿斯卡纶', '弑君者', '引星棘刺']
    star5 = ['德克萨斯', '格拉尼', '苇草', '极境', '贾维', '野鬃', '夜半', '晓歌', '谜图', '青枳', '万顷', '红隼', '历阵锐枪芬', '渡桥', '齐尔查克', '寻澜', '芙兰卡', '因陀罗', '拉普兰德', '幽灵鲨', '暴行', '诗怀雅', '星极', '炎客', '布洛卡', '柏喙', '铸铁', '断崖', '燧石', '鞭刃', '阿米娅(近卫)', '战车', '赤冬', '龙舌兰', '羽毛笔', '海沫', '达格达', '铎铃', '火龙S黑角', '摩根', '苍苔', '烈夏', '导火索', '医生', '奥达', '莱欧斯', '临光', '雷蛇', '可颂', '火神', '拜松', '吽', '石棉', '闪击', '暴雨', '灰毫', '极光', '暮落', '车尔尼', '火哨', '洋灰', '深律', '深巡', '森西', '菲莱', '阿米娅', '天火', '夜魔', '惊蛰', '苦艾', '莱恩哈特', '蜜蜡', '特米米', '薄绿', '爱丽丝', '炎狱炎熔', '蚀清', '耶拉', '洛洛', '星源', '至简', '雪绒', '和弦', '寒檀', '戴菲恩', '折光', '温米', '阿罗玛', '特克诺', '蓝毒', '白金', '陨星', '普罗旺斯', '守林人', '送葬人', '灰喉', '慑砂', '安哲拉', '四月', '奥斯塔', '熔泉', '寒芒克洛丝', '埃拉托', '承曦格雷伊', '子月', '截云', '玫拉', '隐现', '冰酿', '白面鸮', '赫默', '华法琳', '锡兰', '微风', '亚叶', '絮雨', '图耶', '桑葚', '蜜莓', '濯尘芙蓉', '明椒', '刺玫', '哈洛德', '阿米娅( 医疗)', '莎草', '瑰盐', '诺威尔', '梅尔', '初雪', '真理', '空', '格劳克斯', '巫恋', '月禾', '稀音', '九色鹿', '夏栎', ' 海蒂', '掠风', '但书', '凛视', '小满', '海霓', '衡沙', '凯瑟琳', '波卜', '行箸', '红', '崖心', '狮蝎', '食铁兽', '槐琥', '雪雉', '罗宾', '卡夫卡', '乌有', '霜华', '贝娜', '绮良', '见行者', '风丸', '空构', '杏仁', '双月', '锡人', '裁度']
    star4 = ['讯使', '清道夫', '红豆', '桃金娘', '豆苗', '杜宾', '缠丸', '霜叶', '艾丝黛尔', '慕斯', '猎蜂', '宴', '断罪者', '刻刀', '芳汀', '杰克', '罗小黑', '石英', '休谟斯', '角峰', '蛇屠箱', '古米', '坚雷', '泡泡', '露托', '杰西卡', '流星', '白雪', '红云', '梅', '安比尔', '酸糖', '松果', '铅踝', '跃跃', '夜烟', '远山', '格雷伊', '卡达', '深靛', '布丁', '末药', '嘉维尔', '调香师', '苏苏洛', '清流', '褐果', '深海色', '地灵', '波登可', '罗比菈塔', '砾', '暗索', '阿消', '伊桑', '孑', '维荻', '云迹',]
    star3 = ['芬', '香草', '翎羽', '玫兰莎', '月见夜', '泡普卡', '卡缇', '米格鲁', '斑点', '克洛丝', '安德切尔', '空爆', '炎熔', '史都华德', '芙蓉', '安赛尔', '梓兰']
    star1 = ['夜刀', 'Castle-3', '黑角', 'Friston-3', '巡林者', '正义骑士号', '泰拉大陆调查团', '杜林', '12F', 'Lancet-2', 'U-Official', 'PhonoR-0', 'THRM-EX']
    
    pe0ple = [star6, star5, star4, star3, star1]
    count = 0
    output_data = []
    total = 0
    for names in pe0ple:
        # 遍历每个干员
        for name in names:
            per_people = 0
            match count:
                case 0:
                    per_people = 6480.68
                case 1:
                    per_people = 3995.6
                case 2:
                    per_people = 2265.4
                case 3:
                    per_people = 588.68
                case 4:
                    per_people = 43.16
            
            # 提取干员对应的物品信息
            result = extract_items_from_page(name)
            
            # 计算等效理智总和
            total_reasons = calculate_total_effective_reason(result, df)
            

            
            # 遍历每个物品及其等效理智
            for title, total_reason in total_reasons:
                per_people += total_reason
            
            # 打印当前干员的总等效理智
            print(f"{name} 的总等效理智总和: {per_people}")
            
            # 将当前干员的结果添加到输出数据中
            output_data.append({
                "干员名称": name,
                "总等效理智": per_people
            })
            
            # 累加到总等效理智
            total += per_people
        count += 1
    
    
    # 打印总等效理智总和
    print(f"总等效理智总和: {total}")
    
    # 将输出数据保存到 Excel 文件
    output_df = pd.DataFrame(output_data)
    output_df.to_excel("output.xlsx", index=False)
    print("结果已保存到 output.xlsx 文件中")