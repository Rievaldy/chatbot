
import json
from chatbotapi.data_model.db_func.db_user_func import *
from chatbotapi.data_model.db_func.db_company_func import *
from chatbotapi.data_model.db_func.db_brand_func import *
from chatbotapi.data_model.db_func.db_product_func import *
from chatbotapi.data_model.db_func.db_subscribe_product_func import *
from chatbotapi.data_model.db_func.db_maintenance_func import *

action_map = json.load(open("chatbot\\test_siemese_network\\action_step.json"))

def gettingStepInput(act_name, id_user):
    action_step = []
    
    process = ""
    
    for action in action_map['actions'] :
        if action['tag'] == act_name :
            process = action['process']
            if len(action['step']) > 0 :
                for step in action['step'] :
                    desc_name = step['desc']       
                    response_step = step['response']
                    validation_step = step['input_validation']
                    helper_information = step['helper_information']
                    helper_template = ""
                    value_step = None
                    if helper_information != "" :
                        helper_result, helper_for_user = performAction(process=helper_information, action_step=None, id_user=id_user)
                        if len(helper_result) > 1 :
                            helper_template = {'helper_result' : helper_result, 'helper_for_user' : helper_for_user}
                        elif len(helper_result) == 1 :
                            value_step = helper_result[0][desc_name]
                        else :
                            helper_template = None
                            action_step = helper_for_user
                            return process,action_step
                    if desc_name == 'id_company' : 
                        user_information = getUserInformation(id_user)
                        value_step = user_information['id_company'] if user_information != None else None
                    action_step.append({"response" : response_step, "desc" : desc_name, "value": value_step, "input_validation" : validation_step, 'helper_information' : helper_template})

    return process,action_step


def performAction(process,action_step,id_user):
    action_result = []
    for_user = ""

    if process == "getUserInformation" :action_result = getUserInformation(id_user)
    elif process == "create_account" : action_result,for_user = createAccont(id_user, action_step)
    elif process == "retrive_list_brand" : action_result,for_user = retriveListBrand()
    elif process == "retrive_desc_brand" : action_result,for_user = retriveDescBrand(action_step)
    elif process == "retrive_list_product" : action_result,for_user = retriveListProduct()
    elif process == "retrive_desc_product" : action_result,for_user = retriveDescProduct(action_step)
    elif process == "retrive_list_company_product" : action_result, for_user = retriveListCompanyProduct(id_user,action_step)
    elif process == "request_product" : action_result, for_user = requestProduct(id_user,action_step)
    elif process == "request_maintenance" : action_result, for_user = requestMaintenance(id_user,action_step)
    elif process == "retrive_history_maintenance" : action_result, for_user = retriveHistoryMaintenance(action_step)
            
    return action_result,for_user

def getUserInformation(id_user) :
    user = getUserData(id_user)
    template_user = { 
        "name_user" : user.name_user, 
        "email_user" : user.email_user, 
        "phone_number" : user.phone_number,
        "address_user" : user.address_user,
        "id_company" : user.id_company } if user != None else None
    return template_user

def createAccont(id_user,step_values):
    name_user = step_values[0]['value']
    email_user = step_values[1]['value']
    phone_number = step_values[2]['value']
    address_user = step_values[3]['value'] 
    id_company = step_values[4]['value']
    newUser = insertUserData(id_user, name_user, email_user, phone_number, address_user, id_company)
    print(newUser != None)
    template_user = []
    for_user = "register Failed"
    if newUser != None :
        for_user = "*Register Success* \n\n" 
        for_user +="Name : "+ newUser.name_user+"\n" 
        for_user += "email : "+ newUser.email_user+"\n" 
        for_user += "phone number : "+ newUser.phone_number+ "\n"
        for_user += "adress : "+ newUser.address_user+"\n" 
        for_user +=  "company : "+ str(newUser.id_company)+"\n" 
        template_user = {
            "id_user" : newUser.id_user, 
            "name_user" : newUser.name_user, 
            "email_user" : newUser.email_user, 
            "phone_number" : newUser.phone_number,
            "address_user" : newUser.address_user,
            "id_company" : newUser.id_company}
    return template_user,for_user

def retriveListBrand():
    brand_list = getAllBrand()
    template_brand = []
    for_user = ""
    for i in range (len(brand_list)):
        template_brand.append({
        "number" : i+1,
        "id_brand" : brand_list[i].id_brand, 
        "name_brand" : brand_list[i].name_brand}) 

        for_user+="*"+str((i+1))+"."+brand_list[i].name_brand+"*\n"
    return template_brand,for_user

def retriveDescBrand(step_values):
    id_brand = step_values[0]['value']
    message,brand = searchSpecificBrand(id_brand)
    template_brand = {
        "id_brand" : brand.id_brand, 
        "name_brand" : brand.name_brand, 
        "desc_brand" : brand.desc_brand } if brand != None else ""
    
    for_user = "*"+ brand.name_brand +"*\n" + brand.desc_brand + "\n" if brand != None else ""

    return template_brand,for_user

def retriveListProduct():
    product = getAllProduct()
    template_product = []
    header = product[0][1].name_brand
    for_user = "*"+header+"*\n"
    if product != None :
        for i in range(len(product)):
            template_product.append({
                "number" : i+1,
                "id_product" : product[i][0].id_product,
                "id_brand" : product[i][0].id_brand, 
                "name_product" : product[i][0].name_product, 
                "desc_product" : product[i][0].desc_product})
            
            if header != product[i][1].name_brand:
                header = product[i][1].name_brand
                for_user+= "\n*"+header+"*\n" 
                
            for_user+= str(i+1) +". "+product[i][0].name_product +"\n"
        
    return template_product,for_user

#belom
def retriveListProductByBrand(step_values):
    id_brand = step_values[0]['value']
    product = getAllProductByBrand(id_brand)
    template_product = []
    for_user = ""
    if product != None :
        for i in range(len(product)):
            template_product.append({
                "id_product" : product[i].id_product,
                "id_brand" : product[i].id_brand, 
                "name_product" : product[i].name_product, 
                "desc_product" : product[i].desc_product})
            
            for_user+= "*"+str(i+1)+". "+product[i].name_product+"*\n" 
            for_user+= product[i].desc_product +"\n\n"
        
    return template_product,for_user

def retriveDescProduct(step_values):
    id_product = step_values[0]['value']
    product = getDetailProduct(id_product)
    template_product = {
        "id_brand" : product.id_product, 
        "name_brand" : product.name_product, 
        "desc_brand" : product.desc_product } if product != None else ""
    
    for_user = "*"+ product.name_product +"*\n" + product.desc_product + "\n" if product != None else ""
        
    return template_product,for_user

def retriveListCompanyProduct(id_user, step_values):
    print("masuk")
    user_information = getUserData(id_user)
    print(user_information.id_company)
    id_company = user_information.id_company if step_values == None else step_values[0]['value']
    subscribe_products = getAlSubscribeProductByCompany(id_company)
    print(subscribe_products)
    template_subscribe_products = []
    for_user = ""

    if subscribe_products != None :
        for i in range (len(subscribe_products)) :
            template_subscribe_products.append({
                'number' : i+1,
                'id_subscribe_product' : subscribe_products[i][0].id_subcribe_product,
                'id_user' : subscribe_products[i][0].id_user,
                'id_product' : subscribe_products[i][0].id_product,
                'id_company' : subscribe_products[i][0].id_company,
                'maintenance_ticket' : subscribe_products[i][0].maintenance_ticket,
                'request_date' : subscribe_products[i][0].request_date,
                'start_date' : subscribe_products[i][0].start_date,
                'end_date' : subscribe_products[i][0].end_date,
                'status_code' : subscribe_products[i][0].status_code })

            for_user+= "*"+ str(i+1) +". "+ subscribe_products[i][3].name_product+"*\n" 
            for_user+= "Maintenance Ticket : " + str(subscribe_products[i][0].maintenance_ticket) +"\n" 
            for_user+= "Request Date : " + str(subscribe_products[i][0].request_date) +"\n" 
            for_user+= "Start Date : " + str(subscribe_products[i][0].start_date) +"\n" 
            for_user+= "End Date : " + str(subscribe_products[i][0].end_date) +"\n" 
            for_user+= "Requested By : " + subscribe_products[i][1].name_user +"\n\n"

        return template_subscribe_products, for_user

    else:return  template_subscribe_products,"your company dont have any subscribed product please request 1 if u interested" 

#belom
def requestProduct(id_user,step_values):
    user_information = getUserData(id_user)
    id_company = user_information.id_company
    id_brand = step_values[0]['value']
    subscribe_product = insertSubscribeProduct(id_user,id_company, id_brand, 0)
    if subscribe_product != None :
        complete_information_subscribe_product = getSubscribeProductByIdSubscribe(subscribe_product.id_subcribe_product) 
        for_user = "*Sumary Report :*\n" 
        for_user +="Brand Name : "+ complete_information_subscribe_product[4].name_brand+"\n"
        for_user +="Produk Name : "+ complete_information_subscribe_product[3].name_product+"\n" 
        for_user += "Company Name : "+ complete_information_subscribe_product[2].name_company+"\n" 
        for_user += "Request Date : "+ str(complete_information_subscribe_product[0].request_date)+"\n"
        for_user += "Request By : "+ complete_information_subscribe_product[1].name_user+"\n"
        for_user += "We will contact you as soon as posible please wait \n"

        template_subscribe_product = {
            "id_subcribe_product" : subscribe_product.id_subcribe_product, 
            "id_product" : subscribe_product.id_product, 
            "id_user" : subscribe_product.id_user, 
            "id_company" : subscribe_product.id_company,
            "maintenance_ticket" : subscribe_product.maintenance_ticket,
            "request_date" : subscribe_product.request_date,
            "start_date" : subscribe_product.start_date,
            "end_date" : subscribe_product.end_date,
            "status_code" : subscribe_product.status_code }
        return template_subscribe_product, for_user
    
    else : return "", "your company already has this product"

def requestMaintenance(id_user, step_values):
    id_subscribe_product = step_values[0]['value']
    desc_maintenance = step_values[1]['value']
    severity_level = step_values[2]['value']
    maintenance = insertMaintenance(id_user, id_subscribe_product, desc_maintenance, severity_level,  0)
    if maintenance != None :
        complete_information_subscribe_product = getSubscribeProductByIdSubscribe(id_subscribe_product)
        complete_information_maintenance = getSpecificMaintenance(maintenance.id_subcribe_product, maintenance.request_date)
        for_user = "*Sumary Report :*\n" 
        for_user +="Brand Name : "+ complete_information_subscribe_product[4].name_brand+"\n"
        for_user +="Produk Name : "+ complete_information_subscribe_product[3].name_product+"\n" 
        for_user += "Company Name : "+ complete_information_subscribe_product[2].name_company+"\n" 
        for_user += "Symptom : "+ complete_information_maintenance[0].desc_maintenance+"\n" 
        for_user += "Severity Level : "+ str(complete_information_maintenance[0].severity_level )+"\n" 
        for_user += "Request Date : "+ str(complete_information_maintenance[0].request_date)+"\n"
        for_user += "Request By : "+ complete_information_maintenance[1].name_user+"\n"
        for_user += "We will notify you when the problem is solved we will try our best to solve it as soon as posible \n"

        template_subscribe_product = {
            "id_user" : maintenance.id_user, 
            "id_subcribe_product" : maintenance.id_subcribe_product, 
            "request_date" : maintenance.request_date,
            "finish_date" : maintenance.finish_date,
            "severity_level" : maintenance.severity_level,
            "status_code" : maintenance.status_code }
        return template_subscribe_product, for_user
    else : return "", "your company already request maintenance for this product today"

def retriveHistoryMaintenance(step_values):
    id_subscribe_product = step_values[0]['value']
    maintenance = getAllMaintenanceByIdSubscribe(id_subscribe_product)
    template_subscribe_product = []
    if len(maintenance) > 0 :
        complete_information_subscribe_product = getSubscribeProductByIdSubscribe(id_subscribe_product)
        for_user = "*Maintenance History For Product " + complete_information_subscribe_product[3].name_product+ " and Brand " + complete_information_subscribe_product[4].name_brand +" :*\n\n" 
        for i in range (len(maintenance)) :
            complete_information_maintenance = getSpecificMaintenance(maintenance[i].id_subcribe_product, maintenance[i].request_date)
            for_user += "Symptom : "+ complete_information_maintenance[0].desc_maintenance+"\n" 
            for_user += "Severity Level : "+ str(complete_information_maintenance[0].severity_level )+"\n" 
            for_user += "Request Date : "+ str(complete_information_maintenance[0].request_date)+"\n"
            for_user += "Finish Date : "+ str(complete_information_maintenance[0].finish_date)+"\n"
            for_user += "Request By : "+ complete_information_maintenance[1].name_user+"\n\n"

            template_subscribe_product.append({
                "id_user" : maintenance[i].id_user, 
                "id_subcribe_product" : maintenance[i].id_subcribe_product, 
                "request_date" : maintenance[i].request_date,
                "finish_date" : maintenance[i].finish_date,
                "severity_level" : maintenance[i].severity_level,
                "status_code" : maintenance[i].status_code })
        return template_subscribe_product, for_user
    else : return template_subscribe_product, "your company dont have any maintenance history for now"

