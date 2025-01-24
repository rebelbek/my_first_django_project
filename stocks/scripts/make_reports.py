from weasyprint import HTML
import csv
import openpyxl
from datetime import datetime

date_today = datetime.today().strftime('%d-%m-%Y')

stocks_content_fields = ['№', 'Тикер', 'Полное название', 'Кол-во акций',
                         'Размер лота', 'Цена 1 акции']
deals_content_fields = ['№', 'Тикер', 'Кол-во акций', 'Цена покупки',
                        'Потрачено', 'Стоимость', 'Прибыль']


def get_stocks_fields(dict_values):
    result = []
    for stock in dict_values:
        result.append([stock['secid'], stock['secname'], stock['issuesize'], stock['lotsize'], stock['last']])
    return result


def get_deals_fields(dict_values):
    result = []
    for deal in dict_values:
        result.append([deal['secid'], deal['quantity'], deal['buy_price'],
                   round(deal['cost'], 2), round(deal['value'], 2), round(deal['profit'], 2)])
    return result


def get_html_fields(fields):
    result = []
    for count, stock in enumerate(fields, start=1):
        html = ''
        html += f"<td><b>{count}</b></td>"
        for i in stock:
            html += f"<td><b>{i}</b></td>"
        html = "<tr>" + html + "</tr>"
        result.append(html)
    return result


def get_content_html_fields(content_fields):
    fields_lst = []
    for item in content_fields:
        fields_lst.append(f"<td><b>{item}</b></td>")
    return f"<tr> {' '.join(fields_lst)} </tr>"


def get_html_or_pdf_file(dict_values: dict, model: str, format_file: str, additional: dict):
    filename = f'{model}_{date_today}.{format_file}'
    if model == 'stocks':
        content_fields = get_content_html_fields(stocks_content_fields)
        stocks_fields = get_html_fields(get_stocks_fields(dict_values))
    else:
        content_fields = get_content_html_fields(deals_content_fields)
        stocks_fields = get_html_fields(get_deals_fields(dict_values))
    if additional:
        add_html = f'''<ul>
        <li><p>Всего потрачено: {additional['cost__sum']}</p></li>
        <li><p>Стоимость всех акций: {round(additional['value__sum'], 2)}</p></li>
        <li><p>Прибыль: {round(additional['profit__sum'], 2)}</p></li>
        </ul>'''
        html = f'''<table> {content_fields} {' '.join(stocks_fields)} </table> <br> {add_html}'''
    else:
        html = f'''<table> {content_fields} {' '.join(stocks_fields)} </table>'''
    if format_file == 'pdf':
        result = HTML(string=html)
        file = result.write_pdf(f'reports/{format_file}/{filename}')
    else:
        with open(f'reports/{format_file}/{filename}', "w") as file:
            file.write(html)
    return file


def get_csv_file(dict_values: dict, model: str, format_file: str, additional: dict):
    filename = f'{model}_{date_today}.{format_file}'
    with open(f'reports/{format_file}/{filename}', "w", newline="") as file:
        filewriter = csv.writer(file)
        if model == 'stocks':
            filewriter.writerow(stocks_content_fields[1:])
            for stock in get_stocks_fields(dict_values):
                filewriter.writerow(stock)
        else:
            filewriter.writerow(deals_content_fields[1:])
            for deal in get_deals_fields(dict_values):
                filewriter.writerow(deal)
            filewriter.writerow(['Потрачено', 'Стоимость', 'Прибыль'])
            filewriter.writerow([round(i, 2) for i in additional.values()])
    return file


def get_xlsx_file(dict_values: dict, model: str, format_file: str, additional: dict):
    filename = f'{model}_{date_today}.{format_file}'
    file = openpyxl.Workbook()
    sheet = file.active
    if model == 'stocks':
        sheet.append(stocks_content_fields[1:])
        for stock in get_stocks_fields(dict_values):
            sheet.append(stock)
    else:
        sheet.append(deals_content_fields[1:])
        for deal in get_deals_fields(dict_values):
            sheet.append(deal)
        sheet.append(['Потрачено', 'Стоимость', 'Прибыль'])
        sheet.append([round(i, 2) for i in additional.values()])
    file.save(f'reports/{format_file}/{filename}')
    return file


def write_to_file(dict_values: dict, model: str, format_file: str, additional: dict = {}):
    filename = f'{model}_{date_today}.{format_file}'
    if format_file == 'pdf' or 'html':
        file = get_html_or_pdf_file(dict_values, model, format_file, additional)
    if format_file == 'csv':
        file = get_csv_file(dict_values, model, format_file, additional)
    if format_file == 'xlsx':
        file = get_xlsx_file(dict_values, model, format_file, additional)
    result = (file, filename)
    return result


if __name__ == '__main__':
    pass
