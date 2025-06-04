# Problem 1
# Write a function, cabRide, which takes 2 integers (distance and time) as arguments.
# The function returns how much the cab ride would cost. 
# The pricing scale is as follows:
#
# Distance - every mile is $1.00 for the first 10 miles. 
# At the 11th+ mile, the price increases to $1.25 per mile for these miles only. 
# Ex. 10 mile trip = $10.00
#     11 mile trip = $11.25 (10*$1.00   + 1*$1.25) 
#
# Time - Every minute is $0.50.
# Ex. 10 minute trip = $5.00
#
# The cabRide total is both Distance and Time 

def cabRide(dist, time):
    if dist <= 10:
        return f'{dist + (time*0.5):.2f}'
    else:
        return f'{10 + ((dist-10)*1.25) + (time*0.5):.2f}'
print(cabRide(10,10)) # should return $15.00
print(cabRide(15,10)) # should return $21.25
