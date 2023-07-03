from fastapi import FastAPI, Request, Depends, HTTPException, status
from datetime import datetime
import uvicorn
import pyrebase
import pymongo

app = FastAPI()
config = {
    "apiKey": "AIzaSyCgJjNDVlYeOuEoUzlLJe9lulrzO1rRceY",
    "authDomain": "adminconsole-updated.firebaseapp.com",
    "databaseURL": "https://adminconsole-updated-default-rtdb.firebaseio.com",
    "storageBucket": "adminconsole-updated.appspot.com",
}

firebase = pyrebase.initialize_app(config=config)
auth = firebase.auth()
database = firebase.database()
email = "a@a.in"
password = "password"
user = auth.sign_in_with_email_and_password(email, password)
id_token = user['idToken']
alldata = database.get(token=id_token).val()
# myclient = pymongo.MongoClient("mongodb+srv://koushik:koushik@cluste111.bq7qcte.mongodb.net/")
# mydb = myclient["testdb"]
# mycol = mydb["test coll"]
# mm = mycol.find()
# alldata = next(mm)

@app.get("/")
def home():
    return {"msg": "Welcome"}

@app.get("/login/{email}/{password}")
async def login(request: Request,email:str,password:str):
    """This is to check login user
    :param request:
    :return:
    Enter email with password
    """
    # print(f"the username is{email} password is{password}")
    # response = await request.json()
    # print(f"Response is {response}")
    # email = response["email"]
    # password = response["password"]
    try:
        user = auth.sign_in_with_email_and_password(email=email, password=password)
        userid = user["localId"]
        return {"user id":userid}
    except Exception as error:
        error_message = str(error)
        # print(f'Error is {error_message}')
        if "EMAIL_NOT_FOUND" in error_message:
            error = {"Error": "Email Not Found"}
        if "INVALID_PASSWORD" in error_message:
            error = {"Error": "Invalid Password"}
        else:
            pass
            # print('some other error')
    # print(f"User is {user}")
        return error


@app.get("/staffdetails/name/{uid}")
async def staff_name(request: Request,uid:str):
    """This is for getting staff name
    By their UID
    """
    try:
        staffname=alldata["office_staffs"]["staff_details"][uid]["name"]
    except:
        staffname="Not found"
    return staffname

@app.get("/staffdetails/department/{uid}")
async def staff_department(request: Request,uid:str):
    """This is for getting staff department
    By their UID
    """
    try:
        staffdepartment=alldata["office_staffs"]["staff_details"][uid]["department"]
    except:
        staffdepartment="Not found"
    return staffdepartment

@app.get("/staffdetails/email/{uid}")
async def staff_email(request: Request,uid:str):
    """This is for getting staff email
    By their UID
    """ 
    try:
        staffdemail=alldata["office_staffs"]["staff_details"][uid]["email"]
    except:
        staffdemail="Not found" 
    return staffdemail

@app.get("/staffdetails/{uid}")
async def staff_details_uid(request: Request,uid:str):
    """This is for getting staff name,email and department
    By their UID
    """
    try:
        staffname = alldata["office_staffs"]["staff_details"][uid]["name"]
    except:
        staffname = "Not found"
    try:     
        staffemail = alldata["office_staffs"]["staff_details"][uid]["department"]
    except:
        staffemail = "Not found"
    try:        
        staffdepartment = alldata["office_staffs"]["staff_details"][uid]["email"]
    except:
        staffdepartment = "Not found"
    return staffname,staffemail,staffdepartment

@app.get("/absentees")
def absentees():
    """This is getting the today absentees only
    """
    todays_date = datetime.now().strftime("%Y-%m-%d")
    currentmonth = datetime.now().strftime("%m")
    currentyear = datetime.now().strftime("%Y")
    absenteesList = []
    virtualdattendance = alldata["attendance_logs"]["virtual_attendance"]
    punch_data = alldata["attendance_logs"]["fingerprint"]
    try:
        for staffuid in punch_data:
            try:
                punch_data[staffuid][todays_date]
            except:
                try:
                    virtualdattendance[staffuid][currentyear][currentmonth][todays_date]
                except:
                    absenteesList.append(punch_data[staffuid]["name"])
        return {"absentees_list": absenteesList,"absenteesCount":len(absenteesList)}         
    except:
        return "Not Found"
    


@app.get("/absentees/{date}")
async def absentees_fordate(request: Request,date:str):
    """This getting absentees by the date
    FORMAT DATE = 2023-02-01
    """
    
    dtNow = datetime.strptime(date, "%Y-%m-%d")
    todays_date = dtNow.strftime("%Y-%m-%d")
    currentmonth = dtNow.strftime("%m")
    currentyear = dtNow.strftime("%Y")
    absenteesList = []
    virtualdattendance = alldata["attendance_logs"]["virtual_attendance"]
    punch_data = alldata["attendance_logs"]["fingerprint"]
    for staffuid in punch_data:
        try:
            punch_data[staffuid][todays_date]
        except:
           try:
            virtualdattendance[staffuid][currentyear][currentmonth][todays_date]
           except:
            absenteesList.append(punch_data[staffuid]["name"])   
    return {"absentees_list": absenteesList,"absenteesCount":len(absenteesList)}

@app.get("/inventory")
def inventory():
    """This is getting all the inventory details
    """
    inventoryList = []
    inventory_data = alldata["general_office"]["inventory_management"]
    for id in inventory_data:
        inventoryList.append(inventory_data[id])
    return inventoryList

@app.get("/inventory/{inventory_id}")
async def inventory_id(request: Request,inventory_id:str):
    """This is getting inventory details by inventory_id
    """
    inventory_data = alldata["general_office"]["inventory_management"]
    try:
        inventoryid_data = inventory_data[inventory_id]
        return inventoryid_data         
    except:
        inventoryid_data = "Not found"  
        return inventoryid_data

@app.get("/customer")
def customer():
    """This is getting all the customer details
    """
    customer_data = alldata["customer_data"]["customer_details"]
    return customer_data

@app.get("/customer/{customer_number}")
async def customer_by_number(request: Request,customer_number:str):
    """This is getting customer details by customer phone number
    """
    try:
        customer = alldata["customer_data"]["customer_details"][customer_number]
    except:
        customer = "Not found"
    return customer

@app.get("/customer/date/{created_date}")
async def customer_by_date(request: Request,created_date:str):
    """This is getting customer details by created date
    FORMAT 2023-01-16
    """
    customer_data = alldata["customer_data"]["customer_details"]
    customerlist=[]
    try:
        for customer_number in customer_data:
            timestamp = customer_data[customer_number]["created_date"]
            if timestamp == created_date:
                customerlist.append(customer_data[customer_number])
    except:
        pass
    return customerlist

@app.get("/customer/created_name/{created_by}")
async def customer_by_name(request: Request,created_name:str):
    """This is getting customer details by created person name
    FORMAT Jeeva S include space
    """
    customer_data = alldata["customer_data"]["customer_details"]
    customerlist=[]
    try:
        for customer_number in customer_data:
            createdperson = customer_data[customer_number]["created_by"]
            if createdperson == created_name:
                customerlist.append(customer_data[customer_number])
            else:
                pass
    except:
        pass        
    return customerlist

@app.get("/staffworkmonth/{staff_uid}/{month}")
async def staffworkdone_month(request: Request,staff_uid:str,month:str):
    """This is getting staff workmanager details by staff uid and month
    FORMAT MONTH = 02 MUST TWO DIGITS
    """
    currentyear = datetime.now().strftime("%Y")
    staff_data = alldata["office_staffs"]["workdone"]
    try:
        staff_work = staff_data[staff_uid]["workManager"]["timeSheet"][currentyear][month]
    except:
        staff_work="Not found"
    return staff_work

@app.get("/staffworkdate/{staff_id}/{date}")
async def staffworkdone_date(request: Request,staff_id:str,date:str):
    """This is getting staff workmanager details by staff uid and date
    FORMAT DATE = 2023-02-01
    """
    datedata = date
    staff_data = alldata["office_staffs"]["workdone"]
    staff_date_data = staff_data[staff_id]["workManager"]["timeSheet"]
    try:
        for year in staff_date_data:
            for month in staff_date_data[year]:
                for dat in staff_date_data[year][month]:
                    if dat == datedata:
                        staff_work = staff_date_data[year][month][datedata]
                    else:
                        pass
        return staff_work            
    except:
        staff_work = "Not found"               
    return staff_work

@app.get("/financialanalyzing/expensemonth/{month}")
async def expense_month(request: Request,month:str):
    """This is getting all the Expense details by month
    FORMAT MONTH = 02 MUST TWO DIGITS
    """
    currentyear = datetime.now().strftime("%Y")
    expense_data = alldata["general_office"]["financial_analyzer"]
    try:
        expensemonth_data = expense_data["Expense"][currentyear][month]
    except:
         expensemonth_data = "Not found"   
    return expensemonth_data

@app.get("/financialanalyzing/expensedate/{date}")
async def expense_date(request: Request,date:str):
    """This is getting all the Expense details by date
    FORMAT DATE = 2023-02-01
    """
    expensedate_data = alldata["general_office"]["financial_analyzer"]
    expense_details=[]
    try:
        for year in expensedate_data["Expense"]:
            for month in expensedate_data["Expense"][year]:
                for dat in expensedate_data["Expense"][year][month]:
                    try:
                        timedata = expensedate_data["Expense"][year][month][dat]['EnteredDate']
                        if date == timedata:
                            expense_details.append(expensedate_data["Expense"][year][month][dat])
                        else:
                            pass    
                    except:
                        pass   
                    # expense_details.append(expensedate_data[year][month][dat]['timestamp'])
    except:
         expense_details = "Not found"
    return expense_details

@app.get("/financialanalyzing/income/{month}")
async def income_month(request: Request,month:str):
    """This is getting all the Income details by month
    FORMAT MONTH = 02 MUST TWO DIGITS
    """
    currentyear = datetime.now().strftime("%Y")
    expense_data = alldata["general_office"]["financial_analyzer"]
    try:
        expensemonth_data = expense_data["Income"][currentyear][month]
    except:
         expensemonth_data = "Not found"   
    return expensemonth_data

@app.get("/financialanalyzing/incomedate/{date}")
async def income_date(request: Request,date:str):
    """This is getting all the Income details by date
    FORMAT DATE = 2023-02-01
    """
    incomedate_data = alldata["general_office"]["financial_analyzer"]
    income_details=[]
    try:
        for year in incomedate_data["Income"]:
            for month in incomedate_data["Income"][year]:
                for dat in incomedate_data["Income"][year][month]:
                    try:
                        timedata = incomedate_data["Income"][year][month][dat]['EnteredDate']
                        # enetereddate=timestampcovert(timedata)
                        if date == timedata:
                            income_details.append(incomedate_data["Income"][year][month][dat])
                        else:
                            pass    
                    except:
                        pass  
        return income_details                    
    except:
        income_details = "Not found"
    return income_details

@app.get("/quotationandinvoice/quotationyear/{year}")
async def quotation_year(request: Request,year:str):
    """This is getting all the quotation details by year
    FORMAT YEAR = 2023
    """
    quotation_data = alldata["customer_data"]["quotation_and_invoice"]
    try:
        quotation_details = quotation_data["QUOTATION"][year]
    except:
        quotation_details = "Not found"
    return quotation_details

@app.get("/quotationandinvoice/quotationmonth/{month}")
async def quotation_month(request: Request,month:str):
    """This is getting all the quotation details by month
    FORMAT MONTH = 02
    """
    currentyear = datetime.now().strftime("%Y")
    quotation_data = alldata["customer_data"]["quotation_and_invoice"]
    try:
        quotationmonth_data = quotation_data["QUOTATION"][currentyear][month]     
    except:
        quotationmonth_data = "Not found"
    return quotationmonth_data

@app.get("/quotationandinvoice/quotationdate/{date}")
async def quatation_date(request: Request,date:str):
    """This is getting all the quotation details by month
    FORMAT MONTH = 02
    """
    currentyear = datetime.now().strftime("%Y")
    quatation_data = alldata["customer_data"]["quotation_and_invoice"]
    quatationlist=[]
    try:
        for invoiceyear in quatation_data["QUOTATION"]:
            for invoicemonth in quatation_data["QUOTATION"][invoiceyear]:
                for invoiceid in quatation_data["QUOTATION"][invoiceyear][invoicemonth]:
                    timestamp = quatation_data["QUOTATION"][invoiceyear][invoicemonth][invoiceid]['TimeStamp']
                    timedata = timestampcovert(timestamp)
                    if date == timedata:
                        quatationlist.append(quatation_data["QUOTATION"][invoiceyear][invoicemonth][invoiceid])
    except:
        quatationlist = "Not found"
    return quatationlist

@app.get("/quotationandinvoice/invoiceyear/{year}")
async def invoice_year(request: Request,year:str):
    """This is getting all the invoice details by year
    FORMAT YEAR = 2023
    """
    invoice_data = alldata["customer_data"]["quotation_and_invoice"]
    try:
        invoice_details=invoice_data["INVOICE"][year]
    except:
        invoice_details = "Not found"
    return invoice_details

@app.get("/quotationandinvoice/invoicemonth/{month}")
async def invoice_month(request: Request,month:str):
    """This is getting all the invoice details by month
    FORMAT MONTH = 02
    """
    currentyear = datetime.now().strftime("%Y")
    invoice_data = alldata["customer_data"]["quotation_and_invoice"]
    try:
        invoicemonth_data = invoice_data["INVOICE"][currentyear][month]     
    except:
        invoicemonth_data = "Not found"
    return invoicemonth_data

@app.get("/quotationandinvoice/invoicedate/{date}")
async def invoice_date(request: Request,date:str):
    """This is getting all the invoice details by month
    FORMAT MONTH = 02
    """
    currentyear = datetime.now().strftime("%Y")
    invoice_data = alldata["customer_data"]["quotation_and_invoice"]
    invoicelist=[]
    try:
        for invoiceyear in invoice_data["INVOICE"]:
            for invoicemonth in invoice_data["INVOICE"][invoiceyear]:
                for invoiceid in invoice_data["INVOICE"][invoiceyear][invoicemonth]:
                    timestamp = invoice_data["INVOICE"][invoiceyear][invoicemonth][invoiceid]['TimeStamp']
                    timedata = timestampcovert(timestamp)
                    if date == timedata:
                        invoicelist.append(invoice_data["INVOICE"][invoiceyear][invoicemonth][invoiceid])
                    else:
                        pass    
    except:         
        invoicelist = "Not found"
    return invoicelist

@app.get("/suggestion")
def suggestion():
    """This is a getting all suggestion details
    """
    suggestion_data = alldata["others"]["suggestion"]
    return suggestion_data

@app.get("/suggestion/{date}")
async def suggestion_date(request: Request,date:str):
    """This is getting all the suggestion details by date
    FORMAT DATE = 2023-01-01
    """
    suggestion_data = alldata["others"]["suggestion"]
    suggestiondate_data=[]
    for timedate in suggestion_data:
        try:
            timestamp = suggestion_data[timedate]["date"]
            if timestamp == date:
                suggestiondate_data.append(suggestion_data[timedate])
        except:
            pass
    return suggestiondate_data

@app.get("/refreshments")
def refreshments():
    """This is a getting currentday refreshment details
    """
    currentdate = datetime.now().strftime("%Y-%m-%d")
    refreshments_data = alldata["general_office"]["refreshments"]
    try:
        for dat in refreshments_data:
                if dat == currentdate:
                    refreshmentsdate_data = refreshments_data[dat]
                else:
                    pass
        return refreshmentsdate_data        
    except:
        refreshmentsdate_data = "Not found"  
        return refreshmentsdate_data

@app.get("/refreshments/{date}")
async def refreshment_date(request: Request,date:str):
    """This is getting all the refreshment details by date 
       FORMAT DATE = 2023-02-01
    """
    refreshments_data = alldata["general_office"]["refreshments"]
    try:
        for dat in refreshments_data:
                if dat == date:
                    refreshmentsdate_data = refreshments_data[dat]
                else:
                    pass
        return refreshmentsdate_data     
    except:
        refreshmentsdate_data = "Not found"  
        return refreshmentsdate_data

@app.get("/test/{uid}")
async def test_date(uid:str):
    """This is a getting all suggestion details
    """
    return uid

@app.get("/prpoints")
def prpoints():
    """This is a getting all prpoints details
    """
    prpointsalldata=[]
    prpoints_data = alldata["general_office"]["pr_dashboard"]["pr_points"]
    for uid in prpoints_data:
        prpointsalldata.append(prpoints_data[uid])
    return prpointsalldata

@app.get("/prpoints/cycle")
def prpoints_cycle():
    """This is a getting current cycle details
    """
    currentyear = datetime.now().strftime("%Y")
    current_week = datetime.now().strftime("%W")
    prpoints=[]
    prpointstotal=[]
    prname=[]
    prpoints_data = alldata["general_office"]["pr_dashboard"]["pr_points"]
    for uid in prpoints_data:
            try:
                prpoints.append(prpoints_data[uid][currentyear][current_week]["weekly_points"])
            except:
                prpoints.append(0)
            try:
                prpointstotal.append(prpoints_data[uid][currentyear][current_week]["weekly_total_points"])
            except:
                prpointstotal.append(0)
            prname.append(prpoints_data[uid]["name"])
    total_data = zip(prname,prpoints,prpointstotal)

    final_data = []
    for name,points,totalpoints in total_data:
        final_data.append({"name":name,"points":points,"totalpoints":totalpoints})
    return final_data

@app.get("/prpoints/{current_week}")
async def prpoints_month(request: Request,current_week:str):
    """This is getting all the prpoints details by week
    FORMAT week = 22 MUST BE TWO DIGITS
    """
    currentyear = datetime.now().strftime("%Y")
    prpoints_data = alldata["general_office"]["pr_dashboard"]["pr_points"]
    prpointsdata=[]
    prname=[]
    for uid in prpoints_data:
        try:
            prpointsdata.append(prpoints_data[uid][currentyear][current_week])
        except:
            prpointsdata.append(0)
        prname.append(prpoints_data[uid]["name"])
    total_data = zip(prname,prpointsdata)

    final_data = []
    for name,points in total_data:
        final_data.append({"name":name,"data":points})
    return final_data

@app.get("/leavedetails")
def leavedetails():
    """This is a getting all leavedetails
    """
    leaveDetails_data = alldata["office_staffs"]["leaveDetails"]
    leavedetailsall = []
    try:
        for uid in leaveDetails_data:
            leavedetailsall.append(leaveDetails_data[uid]['leaveApplied'])
    except:
        pass        
    return leavedetailsall

@app.get("/leavedetails/currentmonth")
def currentmonth_leavedetails():
    """This is a getting current month leavedetails
    """
    leaveDetails_data = alldata["office_staffs"]["leaveDetails"]
    currentyear = datetime.now().strftime("%Y")
    currentmonth = datetime.now().strftime("%m")
    leavedetailsall = []
    for uid in leaveDetails_data:
        try:
            leavedetailsall.append(leaveDetails_data[uid]["leaveApplied"][currentyear][currentmonth])
        except:
            pass
    return leavedetailsall

@app.get("/deletedcustomer/")
def deletedcustomer():
    """This is a getting all deleted customer
    """
    deletedcustomer = alldata["customer_data"]["deleted_customers"]
    deletedcustomerlist=[]
    try:
        for customernumber in deletedcustomer:
            deletedcustomerlist.append(deletedcustomer[customernumber])
    except:
        pass
    return deletedcustomerlist

@app.get("/deletedcustomer/{customer_number}")
async def deleted_customer(request: Request,customer_number:str):
    """This is a getting the particular deleted customer
    """
    deleted_customer = alldata["customer_data"]["deleted_customers"]
    try:
        deleted_customer = deleted_customer[customer_number]
    except:
        deleted_customer = "Not Found"    

@app.get("/visits/")
def visit():
    """This is a getting the all visit data
    """
    all_visit=alldata["customer_data"]["visit_details"]
    visits_list=[]
    try:
        for data in all_visit:
            visits_list.append(all_visit[data])
    except:
        pass
    return visits_list
@app.get("/visites/{month}/")
async def visitmonth(request:Request,month:str):
    """This is a getting the particular visit
    FORMAT= 1 to 12 WITHOUT zero Like this 01,02
    """
    currentyear = datetime.now().strftime("%Y")
    all_visit=alldata["customer_data"]["visit_details"]
    visit_list=[]
    try:
        for visitmonth in all_visit[currentyear]:
            if visitmonth == month:
                visit_list.append(visit_list[currentyear])
            else:
                pass
    except:
        pass         
 
def timestampcovert(date):
    try:
        date_obj = datetime.fromtimestamp(date)
    except:
        date_obj = datetime.fromtimestamp(date / 1000)    
    timestampdate = date_obj.strftime("%Y-%m-%d")
    return timestampdate

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8118 , reload=True)