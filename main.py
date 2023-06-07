from fastapi import FastAPI, Request
import uvicorn
import pyrebase
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime

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
    staff_details = database.child('office_staffs').child("staff_details").get().val()
    try:
        staffname = staff_details[uid]["name"]
    except:
        staffname="Not found"
    return staffname

@app.get("/staffdetails/department/{uid}")
async def staff_department(request: Request,uid:str):
    """This is for getting staff department
    By UID
    """
    staff_details = database.child('office_staffs').child("staff_details").get().val()
    try:
        staffdepartment = staff_details[uid]["department"]
    except:
        staffdepartment="Not found"
    return staffdepartment

@app.get("/staffdetails/email/{uid}")
async def staff_email(request: Request,uid:str):
    """This is for getting staff email
    By UID
    """ 
    staff_details = database.child('office_staffs').child("staff_details").get().val()
    try:
        staffdemail = staff_details[uid]["email"]
    except:
        staffdemail="Not found"    
    return staffdemail

@app.get("/staffdetails/{uid}")
async def staff_details(request: Request,uid:str):
    """This is for getting staff name,email and department
    By UID
    """
    staff_details = database.child('office_staffs').child("staff_details").get().val()
    try:
        staffname = staff_details[uid]["name"]
    except:
        staffname = "Not found"
    try:     
        staffemail = staff_details[uid]["email"]
    except:
        staffemail = "Not found"
    try:        
        staffdepartment = staff_details[uid]["department"]
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


@app.get("/absentees/{date}")
async def absentees_fordate(request: Request,date:str):
    """This i sa docstring for absentees for date
    FORMAT DATE = 2023-02-01
    """
    todays_date = date
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
    customer_data = database.child('customer_data').child("customer_details").get().val()
    return customer_data

@app.get("/customer/{customer_number}")
async def customer_number(request: Request,customer_number:str):
    """This is getting customer details by phone number
    FORMAT ATLEAST 10 NUMBERS
    """
    customer_data = database.child('customer_data').child("customer_details").get().val()
    try:
        customer = customer_data[customer_number]
    except:
        customer = "Not found"
    return customer

@app.get("/staff/{staff_uid}/{month}")
async def staff_month(request: Request,staff_uid:str,month:str):
    """This is getting staff workmanager details by month
    FORMAT MONTH = 02
    """
    currentyear = datetime.now().strftime("%Y")
    staff_data = database.child('staff').get().val()
    try:
        staff_work = staff_data[staff_uid]["workManager"]["timeSheet"][currentyear][month]
    except:
        staff_work="Not found"
    return staff_work

@app.get("/staff/{staff_id}/{date}")
async def staff_date(request: Request,staff_id:str,date:str):
    """This is getting staff workmanager details by date
    FORMAT DATE = 2023-02-01
    """
    staff_data = database.child('staff').get().val()
    try:
        staff_date_data = staff_data[staff_id]["workManager"]["timeSheet"]
        for year in staff_date_data:
            for month in staff_date_data[year]:
                for dat in staff_date_data[year][month]:
                    if dat == date:
                        staff_work = staff_date_data[year][month][dat]
                    else:
                        pass
        return staff_work            
    except:
        staff_work = "Not found"               
        return staff_work

@app.get("/financialanalyzing/expense/{month}")
async def expense_month(request: Request,month:str):
    """This is getting all the Expense details by month
    FORMAT MONTH = 02
    """
    currentyear = datetime.now().strftime("%Y")
    expense_data = database.child('FinancialAnalyzing').get().val()
    try:
        expensemonth_data = expense_data["Expense"][currentyear][month]
    except:
         expensemonth_data = "Not found"   
    return expensemonth_data

@app.get("/financialanalyzing/expense/{date}")
async def expense_date(request: Request,date:str):
    """This is getting all the Expense details by date
    FORMAT DATE = 2023-02-01
    """
    expensedate_data = database.child('FinancialAnalyzing').get().val()
    expense_details=[]
    try:
        for year in expensedate_data["Expense"]:
            for month in expensedate_data[year]:
                for dat in expensedate_data[year][month]:
                        if expensedate_data[year][month][dat]["EnteredDate"] == date:
                            expense_details.append(expensedate_data[year][month][dat])
    except:
         expense_details = "Not found"
    return expense_details

@app.get("/financialanalyzing/income/{month}")
async def income_month(request: Request,month:str):
    """This is getting all the Income details by month
    FORMAT MONTH = 02
    """
    currentyear = datetime.now().strftime("%Y")
    expense_data = database.child('FinancialAnalyzing').get().val()
    try:
        expensemonth_data = expense_data["Income"][currentyear][month]
    except:
         expensemonth_data = "Not found"   
    return expensemonth_data

@app.get("/financialanalyzing/income/{date}")
async def income_date(request: Request,date:str):
    """This is getting all the Income details by date
    FORMAT DATE = 2023-02-01
    """
    response = await request.json()
    date = response["date"]
    incomedate_data = database.child('FinancialAnalyzing').get().val()
    expense_details=[]
    try:
        for year in incomedate_data["Income"]:
            for month in incomedate_data["Income"][year]:
                for dat in incomedate_data["Income"][year][month]:
                        if incomedate_data["Income"][year][month][dat]["EnteredDate"] == date:
                            expense_details.append(incomedate_data["Income"][year][month][dat])
        return expense_details                    
    except:
         expense_details = "Not found"
    return expense_details

@app.post("/quotationandinvoice/quotation/year")
async def quotation_year(request: Request):
    """This is getting all the quotation details by year
    FORMAT YEAR = 2023
    """
    response = await request.json()
    year = response["year"]
    quotation_data = database.child('QuotationAndInvoice').get().val()
    try:
        quotation_details = quotation_data["QUOTATION"][year]
    except:
        quotation_details = "Not found"
    return quotation_details

@app.post("/quotationandinvoice/quotation/month")
async def quotation_month(request: Request):
    """This is getting all the quotation details by month
    FORMAT MONTH = 02
    """
    response = await request.json()
    month = response["month"]
    currentyear = datetime.now().strftime("%Y")
    quotation_data = database.child('QuotationAndInvoice').get().val()
    try:
        quotationmonth_data = quotation_data["QUOTATION"][currentyear][month]     
    except:
        quotationmonth_data = "Not found"
    return quotationmonth_data

@app.post("/quotationandinvoice/invoice/year")
async def invoice_year(request: Request):
    """This is getting all the invoice details by year
    FORMAT YEAR = 2023
    """
    response = await request.json()
    year = response["year"]
    invoice_data = database.child('QuotationAndInvoice').get().val()
    try:
        invoice_details=invoice_data["INVOICE"][year]

    except:
        invoice_details = "Not found"
    return invoice_details

@app.post("/quotationandinvoice/invoice/month")
async def invoice_month(request: Request):
    """This is getting all the invoice details by month
    FORMAT MONTH = 02
    """
    response = await request.json()
    month = response["month"]
    currentyear = datetime.now().strftime("%Y")
    invoice_data = database.child('QuotationAndInvoice').get().val()
    try:
        invoicemonth_data = invoice_data["INVOICE"][currentyear][month]     
    except:
        invoicemonth_data = "Not found"
    return invoicemonth_data

@app.get("/suggestion")
def suggestion():
    """This is a getting all suggestion details
    """
    suggestion_data = database.child('suggestion').get().val()
    return suggestion_data

@app.post("/suggestion/date")
async def suggestion_date(request: Request):
    """This is getting all the suggestion details by date
    FORMAT DATE = 2023-01-01
    """
    response = await request.json()
    date = response["date"]
    suggestion_data = database.child('suggestion').get().val()
    suggestiondate_data=[]
    for timedata in suggestion_data:
        for dat in suggestion_data[timedata]:
            try:
                if suggestion_data[timedata]["date"] == date:
                    print(suggestion_data[timedata]["date"])
                    suggestiondate_data.append(suggestion_data[timedata][dat])
                else:
                    pass
            except:
                suggestiondate_data = "Not found"
    return suggestiondate_data

@app.get("/refreshments")
def refreshments():
    """This is a getting currentday refreshment details
    """
    currentdate = datetime.now().strftime("%Y-%m-%d")
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

@app.post("/refreshments/date")
async def refreshment_date(request: Request):
    """This is getting all the refreshment details by date 
       FORMAT DATE = 2023-02-01
    """
    response = await request.json()
    date = response["date"]
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
    prpoints_data = database.child('PRDashboard').get().val()
    for uid in prpoints_data["pr_points"]:
        prpointsalldata.append(prpoints_data["pr_points"][uid])
    return prpointsalldata


@app.get("/prpoints/cycle")
def prpoints_cycle():
    """This is a getting current cycle details
    """
    todaysDate = int(datetime.now().strftime("%d"))
    currentyear = datetime.now().strftime("%Y")
    currentmonth = datetime.now().strftime("%m")
    prpoints_data = database.child('PRDashboard').get().val()
    prpoints=[]
    prpointstotal=[]
    prname=[]
    for uid in prpoints_data["pr_points"]:
        if  todaysDate <= 15:
            try:
                prpoints.append(prpoints_data["pr_points"][uid][currentyear][currentmonth]["first_cycle_points"])
            except:
                prpoints.append(0)
            try:
                prpointstotal.append(prpoints_data["pr_points"][uid][currentyear][currentmonth]["first_cycle_total_points"])
            except:
                prpointstotal.append(0)     
        else:
            try:
                prpoints.append(prpoints_data["pr_points"][uid][currentyear][currentmonth]["second_cycle_points"])
            except:
                prpoints.append(0)
            try:
                prpointstotal.append(prpoints_data["pr_points"][uid][currentyear][currentmonth]["second_cycle_total_points"])
            except:
                prpointstotal.append(0)           
        prname.append(prpoints_data["pr_points"][uid]["name"])
    total_data = zip(prname,prpoints,prpointstotal)

    final_data = []
    for name,points,totalpoints in total_data:
        final_data.append({"name":name,"points":points,"totalpoints":totalpoints})
    return final_data

@app.post("/prpoints/month")
async def prpoints_month(request: Request):
    """This is getting all the prpoints details by month
    FORMAT MONTH = 02
    """
    response = await request.json()
    month = response["month"]
    currentyear = datetime.now().strftime("%Y")
    prpoints_data = database.child('PRDashboard').get().val()
    prpointsdata=[]
    prname=[]
    for uid in prpoints_data["pr_points"]:
        try:
            prpointsdata.append(prpoints_data["pr_points"][uid][currentyear][month])
        except:
            prpointsdata.append("Not found")
        prname.append(prpoints_data["pr_points"][uid]["name"])
    total_data = zip(prname,prpointsdata)

    final_data = []
    for name,points in total_data:
        final_data.append({"name":name,"data":points})
    return final_data

@app.get("/prpoints/team")
def prpoints_team():
    """This is a getting all prpoints namelist
    """
    prnamelist=[]
    prpoints_data = database.child('PRDashboard').get().val()
    for team in prpoints_data["pr_team"]:
        for names in prpoints_data["pr_team"][team]:
            prnamelist.append(prpoints_data["pr_team"][team][names])
    return prnamelist

@app.get("/leavedetails")
def leavedetails():
    """This is a getting all leavedetails
    """
    leaveDetails_data = database.child('leaveDetails').get().val()
    leavedetailsall = []
    for uid in leaveDetails_data:
        leavedetailsall.append(leaveDetails_data[uid])
    return leavedetailsall

@app.get("/leavedetails/currentmonth")
def leavedetails():
    """This is a getting all leavedetails
    """
    leaveDetails_data = database.child('leaveDetails').get().val()
    currentyear = datetime.now().strftime("%Y")
    currentmonth = datetime.now().strftime("%m")
    print(currentmonth)
    leavedetailsall = []
    for uid in leaveDetails_data:
        try:
            leavedetailsall.append(leaveDetails_data[uid]["leaveApplied"][currentyear][currentmonth])
        except:
            pass    
    return leavedetailsall


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8118 , reload=True)