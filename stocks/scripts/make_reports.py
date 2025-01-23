from weasyprint import HTML
from datetime import datetime

date_today = datetime.today().strftime('%d-%m-%Y')

stocks_content_fields = ['№', 'тикер', 'полное название', 'количество акций',
                         'размер лота', 'цена 1 акции']
deals_content_fields = ['№', 'пользователь', 'тикер', 'количество акций',
                        'стоимость', 'потрачено', 'прибыль']

def get_stocks_fields(dict_values: list[dict]) -> list[str]:
    result = []
    for stock in dict_values:
        tmp_lst = []
        tmp_lst.append(stock['secid'])
        tmp_lst.append(stock['secname'])
        tmp_lst.append(stock['issuesize'])
        tmp_lst.append(stock['lotsize'])
        tmp_lst.append(stock['last'])
        result.append(tmp_lst)
    return result


def get_deals_fields(dict_values: list[dict]) -> list[str]:
    result = []
    for deal in dict_values:
        tmp_lst = []
        tmp_lst.append(deal['username'])
        tmp_lst.append(deal['secid'])
        tmp_lst.append(deal['quantity'])
        tmp_lst.append(round(deal['cost'], 2))
        tmp_lst.append(round(deal['value'], 2))
        tmp_lst.append(round(deal['profit'], 2))
        result.append(tmp_lst)
    return result


def get_html_fields(fields: list[str]) -> list[str]:
    result = []
    for count, stock in enumerate(fields, start=1):
        html = ''
        html += f"<td><b>{count}</b></td>"
        for i in stock:
            html += f"<td><b>{i}</b></td>"
        html = "<tr>" + html + "</tr>"
        result.append(html)
    return result


def get_content_html_fields(content_fields: list) -> str:
    fields_lst = []
    for item in content_fields:
        fields_lst.append(f"<td><b>{item.capitalize()}</b></td>")
    return f"<tr> {' '.join(fields_lst)} </tr>"


def write_to_pdf(dict_values: dict, model: str):
    if model == 'stocks':
        content_fields = get_content_html_fields(stocks_content_fields)
        stocks_fields = get_html_fields(get_stocks_fields(dict_values))
        filename = f'stocks_{date_today}.pdf'
    else:
        content_fields = get_content_html_fields(deals_content_fields)
        stocks_fields = get_html_fields(get_deals_fields(dict_values))
        filename = f'deals_{date_today}.pdf'
    html = HTML(string=f'''<table> {content_fields} {' '.join(stocks_fields)} </table>''')
    file = html.write_pdf(f'reports/pdf/{filename}')
    result = (file, filename)
    return result


if __name__ == '__main__':
    pass