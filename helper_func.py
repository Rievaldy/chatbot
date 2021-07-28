import json
import re

def loadJson(path):
    try :
        action_map = json.load(open(path))
    except FileNotFoundError as e:
        return None
    else:
        return action_map

def writeJson(data, path):
    json_object = json.dumps(data, indent = 4, default=str)
    with open(path,'w') as outfile :
        outfile.write(json_object)

def trackValueNumber(id_user, finding_for):
    print(finding_for)
    path = "chatbot\\test_siemese_network\\dialog\\"+str(id_user)+".json"
    userJson = loadJson(path)
    chat_history = userJson['chat_history']
    removeId = re.sub(re.compile('id_'), '', finding_for)
    result = re.sub(re.compile('_'), ' ', removeId)
    isFound = False
    size_chat_history = len(chat_history)

    data_number = []
    if size_chat_history == 0 : return data_number
    for i in range (chat_history[len(chat_history)-1]['user_input']) :
        if chat_history[len(chat_history)-1]['user_input'][i]['desc'] == finding_for and chat_history[len(chat_history)-1]['user_input'][i]['helper_information'] != None:
            isFound = True
            data_number =  chat_history[len(chat_history)-1]['user_input'][i]['helper_information']

    if size_chat_history > 4 and isFound == False:
        for i in range(len(chat_history)-1,len(chat_history)-4,-1 ) :
            if chat_history[i]['context'] == "list "+ result :
                data_number = chat_history[i]['result']
                break
    elif size_chat_history < 4 and isFound == False: 
        for i in range(len(chat_history)-1, -1,-1 ) :
            if chat_history[i]['context'] == "list "+ result :
                data_number = chat_history[i]['result']
                break
    
    return data_number

def validation(type, data, id_user, desc_input):
    print("type = ",type)
    print("data = ",data)
    print("id_user = ",id_user)
    print("desc_input = ",desc_input)

    if type == "name" :
        regexname = re.compile('[a-zA-Z][a-zA-Z ]{2,}')
        if re.fullmatch(regexname, data) : return True, data, ""
        else: return False, data, "this name doesnt looks valid to me"
    elif type == "email":
        regexemail = re.compile('^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$')
        if re.fullmatch(regexemail, data) : return True, data, ""
        else: return False, data, "this email doesnt looks valid to me"
    elif type == "phone number":
        regexphone = re.compile('\+62\s\d{3}[-\.\s]??\d{3}[-\.\s]??\d{3,4}|\(0\d{2,3}\)\s?\d+|0\d{2,3}\s?\d{6,7}|\+62\s?361\s?\d+|\+62\d+|\+62\s?(?:\d{3,}-)*\d{3,5}')
        if re.match(regexphone, data) : return True, data, ""
        else: return False, data, "this phone number doesnt looks valid to me"
    elif type == "company":
        regexcompanyId = re.compile('[1-9]{4}')
        if re.fullmatch(regexcompanyId, data) : return True, data, ""
        else: return False, data, "this id company doesnt looks valid to me"
    elif type == "available number option":
        regex_number = re.compile('^[\+\-]?\d*\.?\d+(?:[Ee][\+\-]?\d+)?$')
        data_number = trackValueNumber(id_user, desc_input)
        print("data number = ", data_number)

        
        if re.fullmatch(regex_number, str(data)):
            if int(data) < len(data_number) :
                for i in range(len(data_number)) :
                    print(data_number[i]['number'])
                    print(int(data))
                    if data_number[i]['number'] == int(data) : return True, data_number[i][desc_input], ""
            else :return False, data, "please input valid number" 
        else : return False, data, "please input valid number"
    else: return True, data, ""

def open_user_dialog_file(id_user):
    path = "chatbot\\test_siemese_network\\dialog\\"+str(id_user)+".json"
    user_json = None

    if loadJson(path) != None:
        template_json = loadJson(path)
        chat_history = template_json['chat_history']
        user_status = template_json['user_status']
    else:
        user_status = { 'isGoingThroughStep' : False,
                    'for_desc_tag' : None,
                    'waiting_for_input' : None,
                    'process': None }
        chat_history = []
        user_json = {"user_status" : user_status,
                    "chat_history": chat_history}
        writeJson(user_json,path)
        
    return user_json['user_status'] , user_json['chat_history']

def add_user_chat_history(id_user, context, desc_tag, user_input, result):
    path = "chatbot\\test_siemese_network\\dialog\\"+str(id_user)+".json"
    user_json = loadJson(path)
    recent_chat_history = user_json['chat_history']
    recent_chat_history.append(context, desc_tag, user_input, result)
    writeJson(user_json,path)

def edit_user_chat_history(id_user, context, desc_tag, user_input, result):
    path = "chatbot\\test_siemese_network\\dialog\\"+str(id_user)+".json"
    user_json = loadJson(path)
    size_chat_history = user_json['chat_history']
    recent_chat_history = user_json['chat_history'][size_chat_history-1]
    if context != "" :
        recent_chat_history['context'] = context
    elif desc_tag != "" :
        recent_chat_history['desc_tag'] = desc_tag
    elif user_input != "" :
        recent_chat_history['user_input'] = user_input
    elif result != "" :
        recent_chat_history['result'] = result  

    writeJson(user_json,path)


def change_user_status(id_user, isGoingThroughStep, for_desc_tag, waiting_for_input, process):
    path = "chatbot\\test_siemese_network\\dialog\\"+str(id_user)+".json"
    user_json = loadJson(path)
    if isGoingThroughStep != "" :
        user_json['user_status']['isGoingThroughStep'] = isGoingThroughStep
    elif for_desc_tag != "" :
        user_json['user_status']['for_desc_tag'] = for_desc_tag
    elif waiting_for_input != "" :
        user_json['user_status']['waiting_for_input'] = waiting_for_input
    elif process != "" :
        user_json['user_status']['process'] = process

    writeJson(user_json,path)

def change_chat_history_input_value(id_user,target_desc,value):
    path = "chatbot\\test_siemese_network\\dialog\\"+str(id_user)+".json"
    user_json = loadJson(path)
    size_chat_history = user_json['chat_history']
    recent_chat_history = user_json['chat_history'][size_chat_history-1]
    for i in range(recent_chat_history['user_input']) :
        if recent_chat_history['user_input']['desc'] == target_desc :
            recent_chat_history['user_input']['desc'] = value
            break
    writeJson(user_json,path)

