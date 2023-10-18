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
# user_message_template: text
# defects_json: JSON{"rule": text, "message": text, "startLine": int}
# function_json: JSON{"sourceCode": text, "startLine": int, "endLine": int}
def getAnswerFromGPT(system_message, user_message_template, defects_json, function_json):
    # openai api key setting
    openai.api_key = api_key

    # 함수에 해당하는 defect 추출하기
    defect_list = getDefectListFromJSON(defects_json, function_json)

    # User message 생성
    user_message = createUserMessage_v1(user_message_template, defect_list, function_json)

    # openai API 호출
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                'role': "system",
                'content': system_message
            },
            {
                'role': "user",
                'content': user_message
            }
        ],
        temperature=0
    )

    # Answer 추출
    answer = response['choices'][0]['message']['content']
    return answer

def getDefectListFromJSON(defects_json, function_json):
    defect_list = []  # defect list (JSON)
    for defect in defects_json:
        if defect['startLine'] >= function_json['startLine'] and defect['startLine'] <= function_json['endLine']:
            defect_list.append(defect)
    return defect_list

# User message 생성 version 1
# defect_positions 포함
# user_message_template: ${rule_name}, ${rule_description}, ${source_code}, ${defect_message}, ${defect_position} 포함 필수
def createUserMessage_v1(user_message_template, defect_list, function_json):
    # User message 구성 요소
    rule_names = ''
    rule_descriptions = ''
    defect_messages = ''
    defect_positions = ''

    # User message 구성 작업
    number = 1
    for defect in defect_list:
        rule_description = list(filter(lambda item: item['name'] == defect['ruleName'], description_list))  # defect에 해당하는 rule description 가져오기
        rule_names += str(number) + '. ' + defect['ruleName']
        rule_descriptions += str(number) + '. ' + rule_description[0]['title'] + rule_description[0]['description']
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

    # user_message_template으로부터 변수 치환하여 데이터 삽입
    user_message = ((user_message_template.replace('${rule_name}', rule_names)
               .replace('${rule_description}', rule_descriptions)
               .replace('${source_code}', function_json['sourceCode'])
               .replace('${defect_message}', defect_messages))
              .replace('${defect_position}', defect_positions))

    return user_message

# User message 생성 version 2
# defect_positions 비포함
# user_message_template: ${rule_name}, ${rule_description}, ${source_code}, ${defect_message} 포함 필수
def createUserMessage_v2(user_message_template, defect_list, function_json):
    # User message 구성 요소
    rule_names = ''
    rule_descriptions = ''
    defect_messages = ''

    number = 1
    for defect in defect_list:
        rule_description = list(filter(lambda item: item['name'] == defect['ruleName'], description_list))  # defect에 해당하는 rule description 가져오기
        rule_names += str(number) + '. ' + defect['ruleName'] + '\n'
        rule_description += str(number) + '. ' + rule_description[0]['title'] + rule_description[0]['description'] + '\n'
        defect_messages += str(number) + '. ' + defect['message'] + '\n'

        number += 1

    # user_message_template으로부터 변수 치환하여 데이터 삽입
    user_message = ((user_message_template.replace('${rule_name}', rule_names)
               .replace('${rule_description}', rule_descriptions)
               .replace('${source_code}', function_json['sourceCode'])
               .replace('${defect_message}', defect_messages)))

    return user_message


# User message 생성 아이디어 1
# 필요한 변수를 ${} 형태로 다 넣고, replace() 메서드로 필터링 (user_message_template에 기입하지 않은 변수는 자동으로 무시 됨)
#   ex) 함수에 replace(${rule_title}, rule_title)을 넣어 두고 USER가 user_message_template에 ${rule_title}을 넣지 않는다면
#       rule_title을 제외한 나머지 변수들로만 user_message를 구성
# 현재 user_message_template에 포함된 변수:
#   ${rule_name}, ${rule_description}, ${source_code}, ${defect_message}, ${defect_position}
# 이후에 변수 추가가 필요하면 replace('${var_name}') 추가
def createUserMessage_v0(user_message_template, defect_list, function_json):
    # User message 구성 요소
    rule_names = ''
    rule_descriptions = ''
    defect_messages = ''
    defect_positions = ''

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

    # user_message_template으로부터 변수 치환하여 데이터 삽입
    user_message = ((user_message_template.replace('${rule_name}', rule_names)
                     .replace('${rule_description}', rule_descriptions)
                     .replace('${source_code}', function_json['sourceCode'])
                     .replace('${defect_message}', defect_messages))
                    .replace('${defect_position}', defect_positions))

    return user_message