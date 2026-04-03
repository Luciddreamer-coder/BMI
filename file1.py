
weight = float(input("Enter your weight in kg: "))
height = float(input("Enter your height in cm: "))
print(weight)
print(height)
bmi = (weight *10000)/ (height*height)
print("Your bmi is " , bmi)
if bmi < 18.5:
    print("Under")
elif bmi >18.5 and bmi <24.9:
    print("Normal")
elif bmi>25 and bmi<30:
    print("over")
elif bmi>30 and bmi<34.9:
    print("obsese")
else:
    print("extreme obsese")
    