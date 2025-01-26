from weasyprint import HTML
import csv
import openpyxl
from datetime import datetime

date_today = datetime.today().strftime('%d-%m-%Y')

stocks_content_fields = ['№', 'Тикер', 'Полное название', 'Кол-во акций',
                         'Размер лота', 'Цена 1 акции']
deals_content_fields = ['№', 'Тикер', 'Кол-во акций', 'Цена покупки',
                        'Потрачено', 'Стоимость', 'Прибыль']


class ReportsMaker:
    def __init__(self, dict_values: list, model: str, format_file: str, additional: dict = {}):
        self.dict_values = dict_values
        self.model = model
        self.format_file = format_file
        self.additional = additional
        self.filename = f'{model}_{date_today}.{format_file}'
        self.path = f'reports/{format_file}/{self.filename}'
        if model == 'stocks':
            self.content_fields = stocks_content_fields
        else:
            self.content_fields = deals_content_fields

    def get_fields(self):
        result = []
        if self.model == 'stocks':
            for stock in self.dict_values:
                result.append([stock['secid'], stock['secname'], stock['issuesize'], stock['lotsize'], stock['last']])
        else:
            for deal in self.dict_values:
                result.append([deal['secid'], deal['quantity'], deal['buy_price'],
                               round(deal['cost'], 2), round(deal['value'], 2), round(deal['profit'], 2)])
        return result

    def get_html_fields(self):
        result = []
        for count, stock in enumerate(self.get_fields(), start=1):
            html = ''
            html += f"<td><b>{count}</b></td>"
            for i in stock:
                html += f"<td><b>{i}</b></td>"
            html = "<tr>" + html + "</tr>"
            result.append(html)
        return result

    def get_content_html_fields(self):
        fields_lst = []
        for item in self.content_fields:
            fields_lst.append(f"<td><b>{item}</b></td>")
        return f"<tr> {' '.join(fields_lst)} </tr>"

    def get_html_or_pdf_file(self):
        content_html_fields = self.get_content_html_fields()
        stocks_html_fields = self.get_html_fields()
        if self.additional:
            add_html = f'''<ul>
            <li><p>Всего потрачено: {self.additional['cost__sum']}</p></li>
            <li><p>Стоимость всех акций: {round(self.additional['value__sum'], 2)}</p></li>
            <li><p>Прибыль: {round(self.additional['profit__sum'], 2)}</p></li>
            </ul>'''
            html = f'''<table> {content_html_fields} {' '.join(stocks_html_fields)} </table> <br> {add_html}'''
        else:
            html = f'''<table> {content_html_fields} {' '.join(stocks_html_fields)} </table>'''
        if self.format_file == 'pdf':
            result = HTML(string=html)
            file = result.write_pdf(self.path)
        else:
            with open(self.path, "w") as file:
                file.write(html)
        return file

    def get_csv_file(self):
        with open(self.path, "w", newline="") as file:
            filewriter = csv.writer(file)
            filewriter.writerow(self.content_fields[1:])
            for stock in self.get_fields():
                filewriter.writerow(stock)
            if self.additional:
                filewriter.writerow(['Потрачено', 'Стоимость', 'Прибыль'])
                filewriter.writerow([round(i, 2) for i in self.additional.values()])
        return file

    def get_xlsx_file(self):
        file = openpyxl.Workbook()
        sheet = file.active
        sheet.append(self.content_fields[1:])
        for item in self.get_fields():
            sheet.append(item)
        if self.additional:
            sheet.append(['Потрачено', 'Стоимость', 'Прибыль'])
            sheet.append([round(i, 2) for i in self.additional.values()])
        file.save(self.path)
        return file

    def write_to_file(self):
        if self.format_file == 'pdf' or 'html':
            file = self.get_html_or_pdf_file()
        if self.format_file == 'csv':
            file = self.get_csv_file()
        if self.format_file == 'xlsx':
            file = self.get_xlsx_file()
        result = (file, self.filename)
        return result


if __name__ == '__main__':
    pass
