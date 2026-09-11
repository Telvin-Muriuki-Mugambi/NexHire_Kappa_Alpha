from Models.User import User

user1 = User("Telvin", "telvin@gmail.com", "2345432", "dcdceee")
print (user1._hash_password())
print (user1.verify_password())