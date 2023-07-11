import pyrebase

config = {

    "apiKey": "AIzaSyDryxSRmMokvtUjwuHtlYQ2oQBv7rnSCtY",
    "authDomain": "testcheck-171c7.firebaseapp.com",
    "databaseURL": "https://testcheck-171c7-default-rtdb.firebaseio.com",
    "projectId": "testcheck-171c7",
    "storageBucket": "testcheck-171c7.appspot.com",
    "messagingSenderId": "434343854472",
    "appId": "1:434343854472:web:54c0acf8ca6ae1305cfa3d",
    "measurementId": "G-W213826CXE"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()


data={
    "location":"coimbatore"
}
db.child("staffall").child("UIDkjdnkqe").child("2023-07-11").update(data)