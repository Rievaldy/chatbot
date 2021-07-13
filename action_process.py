import json
from chatbotapi.data_model.db_func.db_user_func import *
from chatbotapi.data_model.db_func.db_company_func import *
from chatbotapi.data_model.db_func.db_brand_func import *
from chatbotapi.data_model.db_func.db_product_func import *
from chatbotapi.data_model.db_func.db_subscribe_product_func import *

action_map = json.load(open("chatbot\\test_siemese_network\\action_step.json"))

def performAction(id_user, act_name,entity_available):
    act_template = ""
    action_step = []
    action_process = ""
    
    for action in action_map['actions'] :
        if action['tag'] == act_name :
            response = action['response']
            action_process = action['process']
            if len(action['step']) != 0 :
                for step in action['step'] :
                    desc_name = step['desc']
                    if len(entity_available) > 0 : 
                        for i in range(len(entity_available)):
                            if entity_available[i]['desc'] == desc_name : value = entity_available[i]['value']
                    else :        
                        response_step = step['response']
                        print(response_step)
                        value = input("input something :")
                    action_step.append({"desc" : desc_name, "value" : value})
            print(response)

    if action_process == "create_account" : action_step = createAccont(action_step)
    elif action_process == "create_company" : action_step = createCompany(action_step)
    elif action_process == "login_account" : action_step =loginAccount(action_step)
    elif action_process == "retrive_list_product" : action_step = retriveListProduct()
    elif action_process == "retrive_desc_product" : retriveDescProduct(action_step)
    elif action_process == "retrive_benefit_product" : retriveBenefitProduct(action_step)
            
    return action_step

def createAccont(step_values):
    name_user = step_values[0]['value']
    email_user = step_values[1]['value']
    password_user = step_values[2]['value']
    phone_number = step_values[3]['value']
    address_user = step_values[4]['value'] 
    id_company = step_values[5]['value']
    message, newUser = insertUserData(name_user, email_user, password_user, phone_number, address_user, id_company)
    template_user = [
        {"desc" : "id_user", "value" : newUser.id_user}, 
        {"desc" : "name_user", "value" : newUser.name_user}, 
        {"desc" : "email_user", "value" : newUser.email_user}, 
        {"desc" : "phone_number", "value" : newUser.phone_number},
        {"desc" : "address_user", "value" : newUser.address_user},
        {"desc" : "id_company", "value" : newUser.id_company}] if newUser != None else ""
    return message, template_user

def createCompany(step_values):
    name_company = step_values[0]['value']
    address_company = step_values[1]['value']
    email_company = step_values[2]['value']
    message, newCompany = insertCompanyData(name_company,address_company,email_company)

    template_company = [
        {"desc" : "id_company", "value" : newCompany.id_company}, 
        {"desc" : "name_company", "value" : newCompany.name_company}, 
        {"desc" : "address_company", "value" : newCompany.address_company}, 
        {"desc" : "email_company", "value" : newCompany.email_company}] if newCompany != None else ""

    return message, template_company

    
def loginAccount(step_values):
    email_user = step_values[0]['value']
    password_user = step_values[1]['value']
    message, user = userLogin(email_user, password_user)

    template_user =  [
        {"desc" : "id_user", "value" : user.id_user}, 
        {"desc" : "name_user", "value" : user.name_user}, 
        {"desc" : "email_user", "value" : user.email_user}, 
        {"desc" : "phone_number", "value" : user.phone_number},
        {"desc" : "address_user", "value" : user.address_user},
        {"desc" : "id_company", "value" : user.id_company}] if user != None else ""

    return message, template_user

def retriveListProduct():
    brand_list = getAllBrand()
    template_brand = []
    for i in range (len(brand_list)):
        template_brand.append([
        {"desc" : "id_brand", "value" : brand_list[i].id_brand}, 
        {"desc" : "name_brand", "value" : brand_list[i].name_brand}, 
        {"desc" : "desc_brand", "value" : brand_list[i].desc_brand}, 
        {"desc" : "id_services", "value" : brand_list[i].id_services}]) 
    return template_brand

def retriveDescProduct(step_values):
    id_brand = step_values[0]['value']
    message,brand = searchSpecificBrand(id_brand)
    template_brand = [
        {"desc" : "id_brand", "value" : brand.id_brand}, 
        {"desc" : "name_brand", "value" : brand.name_brand}, 
        {"desc" : "desc_brand", "value" : brand.desc_brand}, 
        {"desc" : "id_services", "value" : brand.id_services}] if brand != None else ""
    return message, template_brand

def retriveBenefitProduct(step_values):
    id_brand = step_values[0]['value']
    message, product = getAllProductByBrand(id_brand)
    template_product = []
    for i in range(len(product)):
        template_product.append([{"desc" : "id_product", "value" : product.id_product},
        {"desc" : "id_brand", "value" : product.id_brand}, 
        {"desc" : "name_product", "value" : product.name_product}, 
        {"desc" : "desc_product", "value" : product.desc_product}])
        
    return template_product if product != None else message 

def retriveListCompanyProduct(id_company, step_values):
    return ""

def requestProduct(id_user,step_values):
    id_brand = step_values[0]
    message,subscribe_product = insertSubscribeProduct(id_user, id_brand, 0)    
    return ""

def requestMaintenance(step_values):
    return ""

def retriveHistoryMaintenance(step_values):
    return ""

def retriveListService(step_values):
    return ""

def retriveDescService(step_values):
    return ""

def retriveListProductByService(step_values):
    return ""
