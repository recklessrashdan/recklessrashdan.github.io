import time
marks1=int(input("Enter yout 1st mark"))
marks2=int(input("Enter yout 2nd mark"))
marks3=int(input("Enter yout 3rd mark"))

def total():
    total2=(marks1+marks2+marks3)
    return(total2)

def multiply():
    multiply2=(marks1+marks2+marks3/3)
    return(multiply2)

time.sleep(2)

print("Student Mark Report")
print("Total Marks-",total())
print("Average Marks-",multiply())

time.sleep(5)
