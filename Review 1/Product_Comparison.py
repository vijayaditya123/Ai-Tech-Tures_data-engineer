class Product :
    def __init__(self,device,price):
        self.device=device
        self.price=price


    def __str__(self):
        return f"device : {self.device} ,Price: {self.price}"
    def __eq__(self,self1):
        return self.price== self1.price
    
    def __gt__(self,self1):
        return  self.price<self1.price 
     
p1= Product("Phone",30000)
p2= Product("laptop",60000)

print(p1)
print(p1==p2)
print(p1>p2)
