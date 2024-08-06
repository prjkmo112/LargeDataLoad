import os
import sys
import re
import click
from clint import textui
from clint.arguments import Args
import pandas as pd
from bs4 import BeautifulSoup

import questStyled


def getFile():
    textui.puts(textui.colored.blue('>> 작업 시작 << '))
    response = questStyled.Question.selectFile()
    file = response['file_path']

    if os.path.exists(file) and re.match(r'^.+\.xlsx?$', file):
        return file
    else:
        return None

def readDataFrame(option):
    pre_filecont = ''
    with open(option['file_path'], mode='rb') as f:
        for i in range(10):
            line = f.readline()
            if not line:
                break
            pre_filecont += str(line) + '\n'

    if (
        'PK\\x03\\x04' in pre_filecont or 'pk\\x03\\x04' in pre_filecont or
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in pre_filecont
    ):
        # xlsx
        print("file detected as 'xlsx'")
        df = pd.read_excel(option['file_path'])
    elif (
        '\\xd0\\xcf\\x11\\xe0\\xa1\\xb1\\x1a\\xe1' in pre_filecont or '\\xD0\\xCF\\x11\\xE0\\xA1\\xB1\\x1A\\xE1' in pre_filecont or
        'application/vnd.ms-excel' in pre_filecont
    ):
        # xls
        encoding = re.search(r'; charset=([a-zA-Z-]+)[;>]', pre_filecont)
        if encoding:
            encoding = encoding.group(1).lower()
            print(f"file detected as 'xls' (encoding: {encoding})")

            if encoding == 'utf-8':
                df = pd.read_html(option['file_path'], header=0)[0]
            else:
                # pandas 인코딩오류(euc-kr)로 인해 bs4로 태그 수집해서 df 변환
                with open(option['file_path'], 'rb') as f:
                    content = f.read()

                soup = BeautifulSoup(content.decode(encoding, 'ignore'), 'html.parser')
                table = soup.find('table')
                
                headers = [th.text.strip() for th in table.find_all('tr')[0].find_all('td')]
                data = []

                for row in table.find_all('tr')[1:]:
                    row_data = [td.text.strip() for td in row.find_all('td')]
                    if len(row_data) < len(headers):
                        row_data.extend([''] * (len(headers) - len(row_data)))
                    data.append(row_data)

                df = pd.DataFrame(data, columns=headers)
        else:
            raise Exception(f'ENCODING ERROR\n{pre_filecont}')

    return df



@click.command()
def main():
    try:
        OPTION = questStyled.Question.getOption()

        if OPTION['file_path'] is not None:
            print("Work Start")
            
            df = readDataFrame(OPTION)

            if 'return_csv' in OPTION['method']:
                print("make csv")
                df.to_csv(OPTION['output_path_csv'], encoding='euc-kr')
            if 'split_file' in OPTION['method']:
                print('split_file')

    except Exception as e:
        print(e)

    sys.exit()


if __name__ == "__main__":
    main()