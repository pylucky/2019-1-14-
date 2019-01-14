

def fun1():
    list1=[]
    x=5
    y=6
    result=x+y
    list1.append(result)
    return  list1

def fun2(list1):


    list2=list(range(1,20))
    print(list2)
    res=sum(list1+list2)

    return res

if __name__=="__main__":
    f1=fun1()
    f2=fun2(f1)
    print(f2)