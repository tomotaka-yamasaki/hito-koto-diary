import datetime
import locale
import os.path

import click
from config.config import Config
from lib.google.spreadsheets import GoogleSpreadSheet

COLUMN_LIST = {
    "PRIVATE": {"alpha": "B", "index": 1},
    "WORK": {"alpha": "C", "index": 2},
    "MEMO": {"alpha": "D", "index": 3},
}


def get_spreadsheet():
    cred_dir = os.path.join(os.path.dirname(__file__), Config.SA_KEY_PATH)
    return GoogleSpreadSheet(Config.SPREADSHEET_ID, cred_dir)


def write_diary(date, text, column, force):
    year, month, day = to_yyyymmdd_element(date)
    target = to_formatdate_for_diary(year, month, day)

    spreadsheet = get_spreadsheet()
    diary = spreadsheet.read_table(year, "A", "1", "E", "367")
    target_index, target_row = [(index, row) for index, row in enumerate(diary) if row[0] == target][0]

    col_index = COLUMN_LIST.get(column).get("index")
    is_writable = col_index >= len(target_row) or not target_row[col_index]

    response = f"{target}  {column}  に対して\n  {text}\nを書き込みます\n\n"
    if is_writable or force:
        updated_range = spreadsheet.write_value(text, year, COLUMN_LIST.get(column).get("alpha"), target_index + 1)
        response += f"...... {updated_range}  に正常に書き込まれました"
    else:
        response += "...... 書き込みに失敗しました\n書き込み対象のセルにはすでに値が入力されています"
    return response


def read_diary(date):
    year, month, day = to_yyyymmdd_element(date)
    target = to_formatdate_for_diary(year, month, day)

    spreadsheet = get_spreadsheet()
    diary = spreadsheet.read_table(year, "A", "1", "E", "367")

    target_index = [index for index, row in enumerate(diary) if row[0] == target][0]
    days, *contents = diary[target_index]

    response = f"{days}\n"
    for index, item in enumerate(contents):
        response += f"  {diary[0][index + 1]}: {item}\n"

    return response


def to_yyyymmdd_element(date):
    year, month, day = [int(v) for v in date.split("-")]
    return [year, month, day]


def to_formatdate_for_diary(year, month, day):
    return datetime.datetime(year, month, day).strftime("%Y/%m/%d (%a)")


@click.command()
@click.option("--text", "-t", type=str, default="", help="書き込むテキスト")
@click.option(
    "--date",
    "-d",
    type=click.DateTime(["%Y-%m-%d", "%Y/%m/%d"]),
    default=datetime.datetime.today().strftime("%Y-%m-%d"),
    help="予定の取得日 (yyyy-mm-dd or yyyy/mm/dd) default:Today",
)
@click.option("--column", "-c", type=click.Choice(["PRIVATE", "WORK", "MEMO"]), default="PRIVATE", help="書き込むカラムを指定する")
@click.option("-force", "-f", is_flag=True, default=False, help="書き込み操作実行時に値の上書きを強制する")
def main(text, date, column, force):
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
    formated_date = date.strftime("%Y-%m-%d")
    if not text:
        response = read_diary(formated_date)
        print(response)
    else:
        response = write_diary(formated_date, text, column, force)
        print(response)


if __name__ == "__main__":
    main()
