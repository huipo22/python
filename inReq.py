import os
file = open("req.txt")
 
while 1:
    line = file.readline()
    if not line:
        break
    else:
        try:
            os.system('sudo pip install '+line)
        except:
            continue        
