from database import add_user

username = input("Enter username: ")
password = input("Enter password: ")

add_user(username, password)
print("User created successfully.")
