import bs4
import csv

RARITY_COLORS = {
    '#313131': '普通',
    '#1f999c': '蓝色',
    '#7d0022': '红色'
}

with open('source_mizuki.html', encoding='utf8') as f:
    html = f.read()

html = bs4.BeautifulSoup(html, 'html.parser')
items = html.select('.logo > tbody')
item_info = []

for item in items[:]:
    dom_rows = list(filter(lambda x: not isinstance(
            x, bs4.element.NavigableString), item.children))
    dom_name_row, dom_img_row, dom_desc_row, *dom_others_row = dom_rows

    # ========== Name row ==========
    dom_num = dom_name_row.th
    dom_name = dom_num.fetchNextSiblings()[0]

    num = dom_num.string.strip()[3:]
    name = dom_name.contents[0].strip()
    is_not_changable = len(dom_name.contents) > 1
    rarity = RARITY_COLORS[dom_num['style'][-8:-1]]

    # ========== Image row ==========
    img_srcset = dom_img_row.img['data-srcset']

    # ========== Desc row ==========
    dom_desc_tds = dom_desc_row.findAll('td')
    if len(dom_desc_tds) > 1:
        dom_price, dom_desc = dom_desc_tds
    else:
        dom_price, dom_desc = None, dom_desc_tds[0]
    price = dom_price.span.string if dom_price else None
    effect = dom_desc.b.text.strip()
    desc = dom_desc.i.text.strip()

    print(f'{num}  [{rarity}]  {name} ', f'(售价：{price}源石锭)' if price is not None else '(无法购买)')
    print('  藏品效果:', effect)
    print('  藏品描述:', desc)

    # ========== Other rows [Unlock, Obtain, Note] ==========
    unlock = ''
    obtain = ''
    note = ''
    for row in dom_others_row:
        th = row.th.text.strip()
        td = row.td.text.strip()
        if th == '解锁条件':
            unlock = td
        elif th == '获取方式':
            obtain = td
        elif th == '备注':
            note = td
        else:
            raise RuntimeError(f'Unknown key "{th}"')
        print(f'  {th}: {td}')
    
    item_info.append(dict(
        编号=num,
        名称=name,
        品质=rarity,
        价格=price if price else '',
        效果=effect,
        描述=desc,
        交换='不可交换' if is_not_changable else '可交换',
        解锁条件=unlock,
        获取方式=obtain,
        图片集=img_srcset,
        备注=note
    ))

with open('output_mizuki.csv', 'w', encoding='gbk', newline='\n') as f:
    writer = csv.DictWriter(f, list(item_info[0].keys()))
    writer.writeheader()
    writer.writerows(item_info)
