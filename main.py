from fastapi import FastAPI, Request
import uvicorn
import pyrebase
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from pydantic import BaseModel
from datetime import datetime
import pymongo

app = FastAPI()
config = {
  "apiKey": "AIzaSyCgJjNDVlYeOuEoUzlLJe9lulrzO1rRceY",
  "authDomain": "adminconsole-updated.firebaseapp.com",
  "databaseURL": "https://adminconsole-updated-default-rtdb.firebaseio.com",
  "storageBucket": "adminconsole-updated.appspot.com",
}

firebase = pyrebase.initialize_app(config=config)
database = firebase.database()
authentication = firebase.auth()

myclient = pymongo.MongoClient("mongodb+srv://koushik:koushik@cluste111.bq7qcte.mongodb.net/")
mydb = myclient["testdb"]
mycol = mydb["test coll"]
mm = mycol.find()
a = next(mm)

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
    print(f"the username is{email} password is{password}")
    # response = await request.json()
    # print(f"Response is {response}")
    # email = response["email"]
    # password = response["password"]
    try:
        user = authentication.sign_in_with_email_and_password(email=email, password=password)
        userid = user["localId"]
        return {"user id":userid}
    except Exception as error:
        error_message = str(error)
        print(f'Error is {error_message}')
        if "EMAIL_NOT_FOUND" in error_message:
            error = {"Error": "Email Not Found"}
        if "INVALID_PASSWORD" in error_message:
            error = {"Error": "Invalid Password"}
        else:
            print('some other error')
    # print(f"User is {user}")
        return error


@app.get("/staffdetails/name/{uid}")
async def staff_name(request: Request,uid:str):
    """This is for getting staff name
    By UID
    """
    try:
        staffname=a["staff_details"][uid]["name"]
    except:
        staffname="Not found"    
    return staffname

@app.get("/staffdetails/department/{uid}")
async def staff_department(request: Request,uid:str):
    """This is for getting staff department
    By UID
    """
    try:
        staffdepartment=a["staff_details"][uid]["department"]
    except:
        staffdepartment="Not found"
    return staffdepartment

@app.get("/staffdetails/email/{uid}")
async def staff_email(request: Request,uid:str):
    """This is for getting staff email
    By UID
    """ 
    try:
        staffdemail=a["staff_details"][uid]["email"]
    except:
        staffdemail="Not found" 
    return staffdemail

@app.get("/staffdetails/{uid}")
async def staff_details(request: Request,uid:str):
    """This is for getting staff name,email and department
    By UID
    """
    try:
        staffname = a["staff_details"][uid]["name"]
    except:
        staffname = "Not found"
    try:     
        staffemail = a["staff_details"][uid]["department"]
    except:
        staffemail = "Not found"
    try:        
        staffdepartment = a["staff_details"][uid]["email"]
    except:
        staffdepartment = "Not found"
    return staffname,staffemail,staffdepartment

@app.get("/absentees")
def absentees():
    """This is a tetingasdfasdf
    """
    todays_date = datetime.now().strftime("%Y-%m-%d")
    currentmonth = datetime.now().strftime("%m")
    currentyear = datetime.now().strftime("%Y")
    absenteesList = []
    virtualdattendance = a["virtualAttendance"]
    punch_data = a["fingerPrint"]
    for staffuid in punch_data:
        print(staffuid)
        try:
            punch_data[staffuid][todays_date]
        except:
           try:
               virtualdattendance[staffuid][currentyear][currentmonth][todays_date]
           except:
               absenteesList.append(punch_data[staffuid]["name"])   
    return {"absentees_list": absenteesList,"absenteesCount":len(absenteesList)}


@app.get("/absentees/{date}")
async def absentees_fordate(request: Request,date:str):
    """This i sa docstring for absentees for date
    FORMAT DATE = 2023-02-01
    """
    todays_date = timestampcovert(date)
    currentmonth = datetime.now().strftime("%m")
    currentyear = datetime.now().strftime("%Y")
    absenteesList = []
    virtualdattendance = database.child("attendance_logs").child("virtual_attendance").get().val()
    punch_data = database.child("attendance_logs").child("fingerprint").get().val()

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
    inventory_data = database.child('general_office').child("inventory_management").get().val()
    for id in inventory_data:
        inventoryList.append(inventory_data[id])
    return inventoryList

@app.get("/inventory/{inventory_id}")
async def inventory_id(request: Request,inventory_id:str):
    """This is getting inventory details by id
    """
    inventory_data = database.child('general_office').child("inventory_management").get().val()
    try:
        for id in inventory_data:
            if id == inventory_id:
                inventoryid_data = inventory_data[id]
        return inventoryid_data         
    except:
        inventoryid_data = "Not found"  
        return inventoryid_data

@app.get("/customer")
def customer():
    """This is getting all the inventory details
    """
    customer_data = a["customer"]
    return customer_data

@app.get("/customer/{customer_number}")
async def customer_number(request: Request,customer_number:str):
    """This is getting customer details by phone number
    FORMAT ATLEAST 10 NUMBERS
    """
    try:
        customer = a["customer"][customer_number]
    except:
        customer = "Not found"
    return customer

@app.get("/customer/date/{created_date}")
async def customer_number(request: Request,created_date:str):
    """This is getting customer details by phone number
    FORMAT ATLEAST 10 NUMBERS
    """
    customer_data = a["customer"]
    customerlist=[]
    try:
        for customer_number in customer_data:
            timestamp = customer_data[customer_number]["created_date"]
            if timestamp == created_date:
                print(customer_data[customer_number])
                customerlist.append(customer_data[customer_number])
    except:
        pass
    return customerlist

@app.get("/customer/date/{created_name}")
async def customer_number(request: Request,created_name:str):
    """This is getting customer details by phone number
    FORMAT ATLEAST 10 NUMBERS
    """
    customer_data = a["customer"]
    customerlist=[]
    try:
        for customer_number in customer_data:
            createdperson = customer_data[customer_number]["created_by"]
            if createdperson == created_name:
                print(customer_data[customer_number])
                customerlist.append(customer_data[customer_number])
    except:
        pass
    return customerlist

@app.get("/staffworkmonth/{staff_uid}/{month}")
async def staff_month(request: Request,staff_uid:str,month:str):
    """This is getting staff workmanager details by month
    FORMAT MONTH = 02
    """
    currentyear = datetime.now().strftime("%Y")
    staff_data = database.child('office_staffs').child("workdone").get().val()
    try:
        staff_work = staff_data[staff_uid]["workManager"]["timeSheet"][currentyear][month]
    except:
        staff_work="Not found"
    return staff_work

@app.get("/staffworkdate/{staff_id}/{date}")
async def staff_date(request: Request,staff_id:str,date:str):
    """This is getting staff workmanager details by date
    FORMAT DATE = 2023-02-01
    """
    datedata = timestampcovert(date)
    staff_data = database.child('office_staffs').child("workdone").get().val()
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
    FORMAT MONTH = 02
    """
    currentyear = datetime.now().strftime("%Y")
    expense_data = database.child("general_office").child("financial_analyzer").get().val()
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
    expensedate_data = database.child("general_office").child("financial_analyzer").get().val()
    expense_details=[]
    try:
        for year in expensedate_data["Expense"]:
            for month in expensedate_data["Expense"][year]:
                for dat in expensedate_data["Expense"][year][month]:
                    try:
                        timedata = expensedate_data["Expense"][year][month][dat]['enteredtimestamp']
                        enetereddate=timestampcovert(timedata)
                        if date == str(enetereddate):
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
    FORMAT MONTH = 02
    """
    currentyear = datetime.now().strftime("%Y")
    expense_data = database.child("general_office").child("financial_analyzer").get().val()
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
    incomedate_data = database.child("general_office").child("financial_analyzer").get().val()
    income_details=[]
    try:
        for year in incomedate_data["Income"]:
            for month in incomedate_data["Income"][year]:
                for dat in incomedate_data["Income"][year][month]:
                    try:
                        timedata = incomedate_data["Income"][year][month][dat]['enteredtimestamp']
                        enetereddate=timestampcovert(timedata)
                        if date == enetereddate:
                            income_details.append(incomedate_data["Income"][year][month][dat])
                        else:
                            pass    
                    except:
                        pass  
        return income_details                    
    except:
        income_details = "Not found"
    return income_details

@app.get("/quotationandinvoice/quotation/{year}")
async def quotation_year(request: Request,year:str):
    """This is getting all the quotation details by year
    FORMAT YEAR = 2023
    """
    quotation_data = database.child('customer_data').child("quotation_and_invoice").get().val()
    try:
        quotation_details = quotation_data["QUOTATION"][year]
    except:
        quotation_details = "Not found"
    return quotation_details

@app.get("/quotationandinvoice/quotation/{month}")
async def quotation_month(request: Request,month:str):
    """This is getting all the quotation details by month
    FORMAT MONTH = 02
    """
    currentyear = datetime.now().strftime("%Y")
    quotation_data = database.child('customer_data').child("quotation_and_invoice").get().val()
    try:
        quotationmonth_data = quotation_data["QUOTATION"][currentyear][month]     
    except:
        quotationmonth_data = "Not found"
    return quotationmonth_data

@app.get("/quotationandinvoice/invoice/{year}")
async def invoice_year(request: Request,year:str):
    """This is getting all the invoice details by year
    FORMAT YEAR = 2023
    """
    invoice_data = database.child('customer_data').child('quotation_and_invoice').get().val()
    try:
        invoice_details=invoice_data["INVOICE"][year]
    except:
        invoice_details = "Not found"
    return invoice_details

@app.get("/quotationandinvoice/invoice/{month}")
async def invoice_month(request: Request,month:str):
    """This is getting all the invoice details by month
    FORMAT MONTH = 02
    """
    currentyear = datetime.now().strftime("%Y")
    invoice_data = database.child('customer_data').child('quotation_and_invoice').get().val()
    try:
        invoicemonth_data = invoice_data["INVOICE"][currentyear][month]     
    except:
        invoicemonth_data = "Not found"
    return invoicemonth_data

@app.get("/quotationandinvoice/invoicedate/{date}")
async def invoice_month(request: Request,date:str):
    """This is getting all the invoice details by month
    FORMAT MONTH = 02
    """
    currentyear = datetime.now().strftime("%Y")
    invoice_data = database.child('customer_data').child('quotation_and_invoice').get().val()
    invoicelist=[]
    try:
        for invoiceyear in invoice_data["INVOICE"]:
            for invoicemonth in invoice_data["INVOICE"][invoiceyear]:
                for invoiceid in invoice_data["INVOICE"][invoiceyear][invoicemonth]:
                    timestamp = invoice_data["INVOICE"][invoiceyear][invoicemonth][invoiceid]['TimeStamp']
                    timedata = timestampcovert(timestamp)
                    if date == timedata:
                        invoicelist.append(invoice_data["INVOICE"][invoiceyear][invoicemonth][invoiceid])
    except:
        invoicelist = "Not found"
    return invoicelist

@app.get("/suggestion")
def suggestion():
    """This is a getting all suggestion details
    """
    suggestion_data = database.child('suggestion').get().val()
    return suggestion_data

@app.get("/suggestion/{date}")
async def suggestion_date(request: Request,date:str):
    """This is getting all the suggestion details by date
    FORMAT DATE = 2023-01-01
    """
    suggestion_data = database.child('suggestion').get().val()
    suggestiondate_data=[]
    for timedate in suggestion_data:
        try:
            print(suggestion_data[timedate])
            timestamp = suggestion_data[timedate]["Timestamp"]
            timedata= timestampcovert(timestamp)
            if timedata == date:
                print("vjcjhchj")
                suggestiondate_data.append(suggestion_data[timedate])
        except:
            pass
    return suggestiondate_data

@app.get("/refreshments")
def refreshments():
    """This is a getting currentday refreshment details
    """
    currentdate = "2023-06-02"
    # currentdate = datetime.now().strftime("%Y-%m-%d")
    refreshments_data = database.child("general_office").child('refreshments').get().val()
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
    refreshments_data = database.child("general_office").child('refreshments').get().val()
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
    prpoints_data = database.child('general_office').child('pr_dashboard').child('pr_points').get().val()
    for uid in prpoints_data:
        prpointsalldata.append(prpoints_data[uid])
    return prpointsalldata

@app.get("/prpoints")
def prpoints():
    """This is a getting all prpoints details
    """
    prpointsalldata=[]
    prpoints_data = database.child('general_office').child('pr_dashboard').child('pr_points').get().val()
    for uid in prpoints_data:
        prpointsalldata.append(prpoints_data[uid])
    return prpointsalldata

@app.get("/prpoints/cycle")
def prpoints_cycle():
    """This is a getting current cycle details
    """
    # todaysDate = int(datetime.now().strftime("%d"))
    currentyear = datetime.now().strftime("%Y")
    # currentmonth = datetime.now().strftime("%m")
    current_week = datetime.now().strftime("%W")
    prpoints=[]
    prpointstotal=[]
    prname=[]
    prpoints_data = database.child('general_office').child('pr_dashboard').child('pr_points').get().val()
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
    """This is getting all the prpoints details by month
    FORMAT MONTH = 02
    """
    currentyear = datetime.now().strftime("%Y")
    prpoints_data = database.child('general_office').child('pr_dashboard').child('pr_points').get().val()
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
    leaveDetails_data = database.child('office_staffs').child('leave_details').get().val()
    leavedetailsall = []
    for uid in leaveDetails_data:
        leavedetailsall.append(leaveDetails_data[uid]['leaveApplied'])
    return leavedetailsall

@app.get("/leavedetails/currentmonth")
def leavedetails():
    """This is a getting all leavedetails
    """
    leaveDetails_data = database.child('office_staffs').child('leave_details').get().val()
    currentyear = datetime.now().strftime("%Y")
    currentmonth = datetime.now().strftime("%m")
    leavedetailsall = []
    for uid in leaveDetails_data:
        try:
            leavedetailsall.append(leaveDetails_data[uid]["leaveApplied"][currentyear][currentmonth])
        except:
            pass
    return leavedetailsall

def timestampcovert(date):
    try:
        date_obj = datetime.fromtimestamp(date)
    except:
        date_obj = datetime.fromtimestamp(date / 1000)    
    timestampdate = date_obj.strftime("%Y-%m-%d") 
    return timestampdate

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8118 , reload=True)

#     import pymongo

# myclient = pymongo.MongoClient("mongodb+srv://koushik:koushik@cluste111.bq7qcte.mongodb.net/")
# mydb = myclient["testdb"]
# mycol = mydb["newtest"]

# # mylist={'name':'create todo file'}
# # mycol.insert_one(mylist)
# mm = mycol.find()
# a = next(mm)
# print(a["staff_details"])
# print("=====================")
# print(a["all_staff"])