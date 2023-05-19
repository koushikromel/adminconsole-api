import pyrebase


firebaseConfig = {
  "apiKey": "AIzaSyAnTyor4wXJ2fKzkV4_YnQjPxMFf4pZqdg",
  "authDomain": "onw-test.firebaseapp.com",
  "projectId": "onw-test",
  "storageBucket": "onw-test.appspot.com",
  "messagingSenderId": "1089161279985",
  "databaseURL": "https://onw-test-default-rtdb.firebaseio.com/",
  "appId": "1:1089161279985:web:c57956d38d532287f7ac50",
  "measurementId": "G-NWZXYFYQHG"
}

fb = pyrebase.initialize_app(firebaseConfig)

db = fb.database()
authe = fb.auth()

# users = authe.list_users()

# for user in users:
#     print(user.email)

# data = db.get().val()
# a = authe.create_user_with_email_and_password('koushik', '123456')
# aa = authe.get_account_info("eyJhbGciOiJSUzI1NiIsImtpZCI6IjFiYjI2MzY4YTNkMWExNDg1YmNhNTJiNGY4M2JkYjQ5YjY0ZWM2MmYiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vb253LXRlc3QiLCJhdWQiOiJvbnctdGVzdCIsImF1dGhfdGltZSI6MTY4NDM5MzY0MSwidXNlcl9pZCI6IkszZEI2VUE5Z2diTUFobm9YaTd2aTZFZ2lFSjIiLCJzdWIiOiJLM2RCNlVBOWdnYk1BaG5vWGk3dmk2RWdpRUoyIiwiaWF0IjoxNjg0MzkzNjQxLCJleHAiOjE2ODQzOTcyNDEsImVtYWlsIjoidGVzdDJAdGVzdC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsidGVzdDJAdGVzdC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.GBjH0tvtpSZhPUCj8SBdElxVZ8aVkYW0EBu7TH34Z7nZiPhWp3NpzuGms0sxOKcLffadVSQtYGSJZIGheBHZkYbkFMB04iUm8_ulQTYgIIgBg2DRmcx-2sltrc9uqusrxPGLopcyhQ5XSapZCTbUJFLloit0R6p_GUMzL2G3pmUSF42vMWfc28Tupvua8uH5Gpp7sm_LILUVfGxwKQbkKU_7svw-3WWvS05U2utnNI-VCe6QROfeBxYL_Ayl-SK5jR-vt2oDFrYX9I1DLKMga7W1oHsKuXmRSAv-z7xfXdhDY3Vqb0buy7cl_CBwXQYxcGZQhVelTdc2ptf96UUdtQ")
# print(aa)
# print(a["localId"])



import firebase_admin

firebase_admin.initialize_app(
    {
      "apiKey": "AIzaSyAnTyor4wXJ2fKzkV4_YnQjPxMFf4pZqdg",
      "authDomain": "onw-test.firebaseapp.com",
      "projectId": "onw-test",
      "storageBucket": "onw-test.appspot.com",
      "messagingSenderId": "1089161279985",
      "databaseURL": "https://onw-test-default-rtdb.firebaseio.com/",
      "appId": "1:1089161279985:web:c57956d38d532287f7ac50",
      "measurementId": "G-NWZXYFYQHG"
    }
)

auth = firebase_admin.auth()

users = auth.list_users()

for user in users:
    print(user.email)