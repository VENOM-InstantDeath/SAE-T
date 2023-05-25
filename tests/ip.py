import os
x=os.popen("ip a | grep 192").read()
x=x.split()[1][:-3]
print(x)
