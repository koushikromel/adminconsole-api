import firebase_admin
from firebase_admin import auth, credentials

cred = credentials.Certificate('')
# Create a Firebase project and download your credentials.
firebase_admin.initialize_app(cred)


users = auth.get_users()

print(users)





# Create a new user.
# user = auth.create_user(email="example@gmail.com", password="password")

# Sign in the user.
# user = auth.sign_in_with_email_and_password(email="example@gmail.com", password="password")
# email="example@gmail.com"
# user = auth.get_user_by_email(email=email)
# print(user)

# email="example@gmail.com"
# password="password"
# user = auth.get_user_by_email(email)
# try:
#     # auth.verify_password(user.uid, 'password123')
#     decoded_token = auth.verify_id_token(id_token)
#     print('User authenticated successfully.')
# except Exception as e:
#     print('eeee', e)

# try:
#     user = auth.get_user_by_email(email)
#     print(dir(user))
#     # auth.verify_password(user.uid, password)
#     # print('User authenticated successfully')
# except auth.AuthError as e:
#     print('User authentication failed:', e)