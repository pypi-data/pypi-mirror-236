import openai
import os
import json

# 시스템 환경 변수 ${OPENAI_API_KEY}: openai api key 입력
api_key = os.environ['OPENAI_API_KEY']

# 해당 디렉터리와 같은 계층에 "description_list_v3.json" 파일 두기
with open('description_list_v3.json', 'r', encoding='UTF8') as f:
    description_list = json.load(f)

# Prompt 생성 및 전송
# system_message: text
# user_message: text (${rule_name}, ${rule_description}, ${source_code}, ${defect_message}, ${defect_position} 포함 필수)
# defect_list: JSON{"rule": text, "message": text, "startLine": int}
# function: JSON{"sourceCode": text, "startLine": int, "endLinst": int}
def prompt_post(system_message, user_message, defect_json, function_json):
    # openai api key setting
    openai.api_key = api_key

    # prompt의 구성 요소
    rule_names = ''
    rule_descriptions = ''
    defect_messages = ''
    defect_positions = ''

    # 함수에 해당하는 defect 추출하기
    defect_list = []  # defect list (JSON)
    for defect in defect_json:
        if defect['startLine'] >= function_json['startLine'] and defect['startLine'] <= function_json['endLine']:
            defect_list.append(defect)


    number = 1
    for defect in defect_list:
        rule_description = list(filter(lambda item: item['name'] == defect['ruleName'], description_list))  # defect에 해당하는 rule description 가져오기
        rule_names += str(number) + '. ' + defect['ruleName']
        rule_description += str(number) + '. ' + rule_description[0]['title'] + rule_description[0]['description']
        defect_messages += str(number) + '. ' + defect['message']
        defect_positions += str(number) + '. '

        # Defect 위치 찾기
        line = 0
        index = 0
        for func_character in function_json['sourceCode']:
            if line + function_json['startLine'] == defect['startLine']:
                for c in function_json['sourceCode'][index:]:
                    if c == '\n':
                        break
                    defect_positions += c
                break
            elif func_character == '\n':
                line += 1
            index += 1
        rule_names += '\n'
        rule_descriptions += '\n'
        defect_messages += '\n'
        defect_positions += '\n'
        number += 1

    prompt = ((user_message.replace('${rule_name}', rule_names)
              .replace('${rule_description}', rule_descriptions)
              .replace('${source_code}', function_json['sourceCode'])
              .replace('${defect_message}', defect_messages))
              .replace('${defect_position}', defect_positions))

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                'role': "system",
                'content': system_message
            },
            {
                'role': "user",
                'content': prompt
            }
        ],
        temperature=0
    )
    answer = response['choices'][0]['message']['content']
    return answer