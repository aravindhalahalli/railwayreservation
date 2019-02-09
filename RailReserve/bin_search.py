def bin(arr , l, r, x):
    if r >= l:
        mid = (l+r)//2
        #print(type(arr[mid][0]))
        if int(arr[mid][0]) == int(x):
            return mid
        elif int(arr[mid][0]) > int(x):
            return bin(arr, l, mid-1, x)
        else:
            return bin(arr, mid+1, r, x)
    else:
        return -1            

def delete(pn):
    f= open("index1.txt")
    t = f.read().split("\n")[:-1]
    x = list()
    #print(type(pn))
    for i in t :
        s = i.split('|')[:-1]
        x.append(s)
    r = bin(x, 0 , len(x)-1,pn)
    print(r)
    f.seek(0 , 0)
    l = 0
    for j in range(r):
        temp = f.readline()
        l = l + len(temp)
    print(l)    
    f.close()
    f= open("index1.txt","r+")
    f.seek(l,0)
    d = f.read()
    print("goto",d)
    f.seek(0,0)
    t = f.read().split('\n')[:-1]
    f.seek(0,0)
    res = ''
    for i in range(len(t)):
        a = t[i].split('|')[0]
        b = d.split('|')[0]
        if int(a) != int(b) :    
            f.write(t[i])
            f.write('\n')
        else:
            res = d.split('|')[1]
            print("gugu",t[i])
    f.truncate()
    f.close()
    print("nerd hallu")
    return res

