def countup_str(end):
    out = ''
    for i in range(1, end + 1):
        out = out + str(i)
    return out

    
print(countup_str(5)) # '12345'
        
