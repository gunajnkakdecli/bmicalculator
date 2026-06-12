def bmi_calculator( weight, height):
    bmi=weight/(height **2)
    if bmi<18.5:
      category = "underweight"
    elif bmi<2530:
       category="Normal weight"
    elif bmi>30:
       category="over weight" 
    else:
       category ="obese" 

    return bmi, category
    
name=input("enter the name:")
weight= float(input("enter the weight(kg):"))
height=float(input("enter the height(cm):"))
height=height/100

bmi, category = bmi_calculator(weight,height)

print("\n----BMI report----")
print("name:" ,name)
print(f"\n your BMI is: {bmi:.2f}")
print("category:",category)