from fastapi import FastAPI, Request
import uvicorn
import pyrebase
from datetime import datetime


app = FastAPI()
config = {
    "apiKey": "AIzaSyCCTeiCYTB_npcWKKxl-Oj0StQLTmaFOaE",
    "authDomain": "marketing-data-d141d.firebaseapp.com",
    "databaseURL": "https://marketing-data-d141d-default-rtdb.firebaseio.com/",
    "storageBucket": "marketing-data-d141d.appspot.com",
}

firebase = pyrebase.initialize_app(config=config)
database = firebase.database()
authentication = firebase.auth()


@app.get("/")
def home():
    return {"msg": "Welcome"}


@app.post("/asdf")
def asdf(request: Request):
    print('aaa', request.url)
    return {"msg": "This is a post request"}

@app.get("/absentees")
def absentees():
    """This is a tetingasdfasdf
    """
    todays_date = datetime.now().strftime("%Y-%m-%d")
    absenteesList = []
    staff_data = database.child('staff').get().val()
    punch_data = database.child('fingerPrint').get().val()
    for staff in staff_data:
        try:
            punch_data[staff]
            try:
                punch_data[staff][todays_date]
            except:
                absenteesList.append(staff_data[staff]['name'])
        except:
            pass

    return {"absentees_list": absenteesList}

@app.post("/absentees/fordate")
async def absentees_fordate(request: Request):
    """This i sa docstring for absentees for date
    """
    response = await request.json()
    todays_date = response["date"]
    absenteesList = []
    staff_data = database.child('staff').get().val()
    punch_data = database.child('fingerPrint').get().val()
    for staff in staff_data:
        try:
            punch_data[staff]
            try:
                punch_data[staff][todays_date]
            except:
                absenteesList.append(staff_data[staff]['name'])
        except:
            pass

    return {"absentees_list": absenteesList, "absentees_count": len(absenteesList)}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8118 , reload=True)

