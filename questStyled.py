import os
from datetime import datetime
from prompt_toolkit.document import Document
from questionary import Validator, ValidationError
import questionary


class IntegerValidator(Validator):
    def __init__(self, min=None, max=None, default=None) -> None:
        self.min = min
        self.max = max
        self.default = default

    def validate(self, document: Document) -> None:
        value = document.text.strip()
        try:
            value = int(value)
            if (self.min and value < self.min) and (self.max and value > self.max):
                raise ValidationError('range error')
        except:
            if self.default is not None or len(value) > 0:
                raise ValidationError('not number')

class Filter:
    def __init__(self) -> None:
        pass

    @staticmethod
    def _integer(answer:str, min:int=None, max:int=None, default:int=None) -> int:
        value = answer.strip()
        try:
            value = int(value)
            if (min and value < min) and (max and value > max):
                raise Exception('range error')
        except:
            if len(value) == 0 and default is not None:
                value = default
            else:
                raise Exception('not number')

        return value



class Question:
    def __selectFile():
        return questionary.prompt([
            {
                "type": "path",
                "name": "file_path",
                "message": "엑셀 파일 선택"
            }
        ])
    
    def __getMethod():
        quests = questionary.prompt([
            {
                "type": "checkbox",
                "name": "method",
                "message": "리턴 값",
                "choices": [
                    "return_csv: csv 파일 변환",
                    "split_file: 파일 분리"
                ]
            }
        ])

        quests['method'] = list(map(lambda v: v.split(":")[0], quests['method']))
        return quests

    def __getOutputPath(options):
        quest_list = []
        if 'return_csv' in options['method']:
            quest_list.append({
                "type": "path",
                "name": "output_path_csv",
                "message": "CSV 출력 위치",
                "default": f'''./{options['file_name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv'''
            })
        if 'split_file' in options['method']:
            quest_list.append({
                "type": "path",
                "name": "output_path_splitted",
                "message": "분리엑셀 출력 폴더 위치",
                "default": f'''./{options['file_name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}/'''
            })

        return questionary.prompt(quest_list)
    
    @staticmethod
    def getOption():
        options = {}
        options.update(Question.__selectFile())
        file_name = os.path.splitext(os.path.basename(options['file_path']))[0]
        options.update({ "file_name": file_name })
        options.update(Question.__getMethod())
        options.update(Question.__getOutputPath(options))

        return options