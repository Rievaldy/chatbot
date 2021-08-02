from action_process import *
import requests

import json
from corebot import *
from helper_func import *

class telegram_bot():
    def __init__(self):
        self.token = "1853317583:AAG08Gk-6Y6RtPNXW2V8L8x6cPW7Z72ai5w"    #write your token here!
        self.url = f"https://api.telegram.org/bot{self.token}"
    def get_updates(self,offset=None):
            url = self.url+"/getUpdates?timeout=100"    # In 100 seconds if user input query then process that, use it as the read timeout from the server
            if offset:
                url = url+f"&offset={offset+1}"
            url_info = requests.get(url)
            return json.loads(url_info.content)
    def send_message(self,msg,chat_id):
            url = self.url + f"/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=markdown"
            if msg is not None:
                requests.get(url)
    def grab_token(self):
            return self.tokens

tbot = telegram_bot()

update_id = None

chat_history = None
user_status = None


while True:
    print("...")
    updates = tbot.get_updates(offset=update_id)
    print(updates)
    updates = updates['result']

    id_user = ""

    reply = ""

    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = item["message"]["text"]
            except:
                message = None
            from_ = item["message"]["from"]["id"]
            id_user = from_

        user_status, chat_history = open_user_dialog_file(id_user)
        

        if message == "/start" and user_status['isGoingThroughStep'] == False:
             reply = "hello im bpt protect bot :) \n\n i can help you on :\n *-register an account :* if you want to request something you need to register first \n *-showing our list of brand :* if you need information about brand that available on us\n *-showing detail of brand* : if you need information about profil of brand\n *-showing our list of product :* if you need information about product that available on us\n *-showing detail of product* : if you need information about the benefit of product\n *-showing your subscribed company product* : you can see detail of your company product \n -*request product* : if you interest in one of our product you can request it \n *-request maintenance* : if you have trouble with your product, *-maintenance history* : if you need your maintenance history\n\n if you need this information again, say show your feature :)"
             tbot.send_message(reply, from_)
        elif message != "/start" and user_status['isGoingThroughStep'] == False :
            ints = predict_classes(message)
            if ints == None : tbot.send_message("im sory i dont understand what are you trying to say", from_)
            elif len(ints) > 1  and ints !=None:
                reply = "im confused, do you want to  "
                for i in range(len(ints)) :
                    response, desc_tag, permission,action, context = lookOnSpecificTag(ints[i])
                    reply += desc_tag
                    if i != len(ints)-1 : reply += " or "
                reply+= " ?"
                tbot.send_message(reply,from_)
            else :
                response, desc_tag, permission, action, context = lookOnSpecificTag(ints[0])
                user, message, for_user = performAction(process = "getUserInformation", action_step=None, id_user=id_user)
                if permission == "Member" and  user == None:       
                        reply = "unable to do this command, need to register first"
                        tbot.send_message(reply,from_)
                elif ints[0] == "register_account" and user != None:
                    reply = "you already registered "
                    tbot.send_message(reply,from_)
                else :
                    reply = response
                    tbot.send_message(reply,from_)
                    if action != "" :
                        process, actionstep_template = gettingStepInput(action)
                        if len(actionstep_template) > 0 :
                            change_user_status(id_user=id_user, isGoingThroughStep=True, for_desc_tag= desc_tag, waiting_for_input=actionstep_template[0]['desc'])
                            # if len(trackValueNumber(id_user, actionstep_template[0]['desc'])) == 0 : 
                            #     result, message, for_user = performAction(process = actionstep_template[0]['helper_information'], action_step = None, id_user = id_user)
                            #     actionstep_template[0]['helper_information'] = result
                            #     tbot.send_message(for_user, from_)
                            #     add_user_chat_history(id_user=id_user, context=context, desc_tag=desc_tag, user_input=actionstep_template, result=None)
                            #     chat_history.append({'context' : context, 'desc_tag' : desc_tag, 'user_input' : actionstep_template, 'result' : None})
                            #     writeJson(template_json, path)
                            add_user_chat_history(id_user=id_user,context=context, desc_tag=desc_tag,user_input=actionstep_template,result=None)
                            tbot.send_message(actionstep_template[0]['response'], from_)
                        else :
                            result, message,for_user = performAction(process = process, action_step = None, id_user=id_user)
                            add_user_chat_history(id_user=id_user,context=context, desc_tag=desc_tag,user_input=actionstep_template,result=result)
                            tbot.send_message(for_user, from_)
        else :
            selected_chathistory = None
            for i in reversed(range(len(chat_history)-1)) :
                if chat_history[i]['desc_tag'] ==  user_status['for_desc_tag']: 
                    selected_chathistory = chat_history[i]
                    for j in range(0,len(selected_chathistory['user_input'])):
                        if selected_chathistory['user_input'][j]['desc'] ==  user_status['waiting_for_input']: 
                            isRightInput, value, erMessage = validation(selected_chathistory['user_input'][j]['input_validation'], message, id_user, selected_chathistory['user_input'][j]['desc'])
                            if isRightInput == True :
                                selected_chathistory['user_input'][j]['value'] = value
                                if j+1 != len(selected_chathistory['user_input']) :
                                    change_user_status(id_user=id_user, isGoingThroughStep="",for_desc_tag="", waiting_for_input=selected_chathistory['user_input'][j+1]['desc'],process="")
                                    tbot.send_message(selected_chathistory['user_input'][j+1]['response'], from_)
                                    break
                                else:  
                                    change_user_status(id_user=id_user,isGoingThroughStep=False, for_desc_tag="", waiting_for_input=None,process="")    
                                    break
                            else : tbot.send_message(erMessage, from_)
                    break

            if user_status['isGoingThroughStep'] == False :
                process = user_status['process']
                result, message, for_user = performAction(process= process, action_step = selected_chathistory['user_input'], id_user=id_user)
                selected_chathistory['result'] = result
                user_status['process'] = None
                user_status['for_desc_tag'] = None
                tbot.send_message(for_user,from_)
            