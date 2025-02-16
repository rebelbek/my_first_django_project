from weasyprint import HTML
import csv
import openpyxl


class ReportsMaker:
    def __init__(self, values: list, content_field: list, model: str, format_file: str,
                 reports_path: str, additional: dict = None):
        self.values = values
        self.content_fields = content_field
        self.model = model
        self.format_file = format_file
        self.reports_path = reports_path
        self.additional = additional

    def get_html_fields(self):
        result = []
        for count, field in enumerate(self.values, start=1):
            html = ''
            html += f"<td><b>{count}</b></td>"
            for i in field:
                html += f"<td><b>{i}</b></td>"
            html = "<tr>" + html + "</tr>"
            result.append(html)
        return result

    def get_content_html_fields(self):
        result = []
        for item in self.content_fields:
            result.append(f"<td><b>{item}</b></td>")
        return f"<tr> {' '.join(result)} </tr>"

    def write_to_html_or_pdf(self):
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
            result.write_pdf(self.reports_path)
        else:
            with open(self.reports_path, "w") as file:
                file.write(html)

    def write_to_csv(self):
        with open(self.reports_path, "w", newline="") as file:
            filewriter = csv.writer(file)
            filewriter.writerow(self.content_fields[1:])
            for field in self.values:
                filewriter.writerow(field)
            if self.additional:
                filewriter.writerow(['Потрачено', 'Стоимость', 'Прибыль'])
                filewriter.writerow([round(i, 2) for i in self.additional.values()])

    def write_to_xlsx(self):
        file = openpyxl.Workbook()
        sheet = file.active
        sheet.append(self.content_fields[1:])
        for field in self.values:
            sheet.append(field)
        if self.additional:
            sheet.append(['Потрачено', 'Стоимость', 'Прибыль'])
            sheet.append([round(i, 2) for i in self.additional.values()])
        file.save(self.reports_path)

    def write_to_file(self):
        if self.format_file == 'pdf' or 'html':
            self.write_to_html_or_pdf()
        if self.format_file == 'csv':
            self.write_to_csv()
        if self.format_file == 'xlsx':
            self.write_to_xlsx()


if __name__ == '__main__':
    pass
