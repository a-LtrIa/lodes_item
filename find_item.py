import requests
from bs4 import BeautifulSoup

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
    
    for result in results:
        print(result)

    return results




# extract_items_from_page("调香师")
