from flask import Flask, render_template, flash, request
import json
import uuid
from bin_search import *

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
  return render_template("index.html") 

@app.route("/home")
def home():
  return render_template("home.html") 

@app.route("/register",methods=['POST','GET'])
def register():
  data = json.loads(request.data.decode())
  fo = open("users.txt","a")
  fo.write(data['username'])
  fo.write('|')
  fo.write(data['password'])
  fo.write('|')
  fo.write("\n")
  fo.close()
  return json.dumps({ "res": "success" })

@app.route("/login",methods=['POST','GET'])
def login():
  data = json.loads(request.data.decode())
  username = data['username']
  password = data['password']
  fo = open("users.txt","r")
  t = fo.read().split("\n")
  x = list()
  for i in t:
      s = i.split('|')
      x.append(s)
  for i in x:
      if i[0] == username :
          if i[1] == password :
              return json.dumps({ "res": "success", "user": data['username'] })
  return json.dumps({ "res": "failed" })

@app.route("/trains",methods=['POST','GET'])
def showTrains():
    data = json.loads(request.data.decode())
    source = data['source']
    destination = data['destination']
    fo = open('train.txt')
    t = fo.read().split("\n")
    x = list()
    fo.close()
    for i in t:
        s = i.split("|")
        if s[1] == source and s[2] == destination :
            x.append(s)
    return json.dumps({"res": x})

def ticketIndex():
  print("yoyo")
  f = open('ticket.txt','r')
  x = list()
  l = list()
  f.seek( 0, 0)
  c=f.tell()
  while True :
      s = f.readline()
      print(s)
      if s == "":
          print("file end")
          break
      k = s.split('|')      
      z = [k[0],c]
      m = [k[3][:-1],c]
      x.append(z)
      l.append(m)
      c = f.tell()
  data = sorted(x, key=lambda y: y[0])
  data1 = sorted(l, key= lambda y : y[0])
  print(data)
  f.close()
  fo = open('index.txt','w')
  fo1 = open('index1.txt','w')
  for i in  data:
      for j in i :
          fo.write(str(j))
          fo.write('|')
      fo.write('\n')
  fo.close()
  for i in  data1:
      for j in i :
          fo1.write(str(j))
          fo1.write('|')
      fo1.write('\n')
  
  fo1.close()     

@app.route("/reserve",methods=['POST','GET'])
def reserve():
  #Indexing of Usename And PNR into index and index1 respec
  data = json.loads(request.data.decode()) 
  username = data['user']
  train = data['train']
  date = data['date']
  pnr = str(uuid.uuid4().fields[-1])[:5]
  ff = open("ticket.txt","a")
  pos = ff.tell()
  ff.write(username)
  ff.write('|')
  ff.write(train)
  ff.write('|')
  ff.write(date)
  ff.write('|')
  ff.write(pnr)
  ff.write('\n')
  ff.close()
  ticketIndex()
  return json.dumps({ "res": "done", "date": date, "train": train })

@app.route("/view",methods=['POST','GET'])
def view():
  data = json.loads(request.data.decode())
  username = data['username']
  fr = open("index.txt")
  t = fr.read().split("\n")
  x = list()
  for i in t:
      s = i.split('|')
      x.append(s)
  pos = list()
  for i in x:
      if i[0] == username :
          pos.append(i[1])
  fr.close()
  fr = open("ticket.txt","r")
  data= list()
  for i in pos:
      fr.seek(int(i),0)
      data.append(fr.readline().split("|"))
  return json.dumps({"res":data})
                
def binarySearch (arr, l, r, x):
    if r >= l:
        mid = (l+r)//2
        if arr[mid][0] == x:
            return mid
        elif arr[mid][0] > x:
            return binarySearch(arr, l, mid-1, x)
        else:
            return binarySearch(arr, mid+1, r, x)
    else:
        return -1            

@app.route("/cancel",methods=['POST','GET'])
def cancel():
    data = json.loads(request.data.decode()) 
    username = data['user']
    pnr = str(data['pnr'])
    print("\t",pnr)
    l = delete(pnr)
    print(l)
    fo = open("index.txt",'r+')
    t = fo.read().split('\n')[:-1]
    x = list()
    for i in t:
        s = i.split('|')[:-1]
        x.append(s)
    z = 0
    for i in x:
        if l == i[1]:
            break              
        z = z+1
    fo.seek(0,0)
    o = 0
    for i in range(z):
        temp = fo.readline()
        o = o + len(temp)
    fo.seek(o,0)
    d = fo.read()
    print(d)
    fo.seek(0,0)
    for i in t:
        a = i.split('|')[1]
        
        b = d.split('|')[1]
        if int(a) != int(b):
            fo.write(i)
            fo.write('\n')
    fo.truncate() 
    fo.close()
    '''fo = open('ticket.txt','r+')
    fo.seek(int(l),0)
    d = fo.read()
    print(d)
    fo.seek(0,0)
    t = fo.read().split('\n')[:-1]
    fo.seek(0,0)
    for i in t:
        a = i.split('|')[3]
        if int(a) != int(pnr):
            fo.write(i)
            fo.write('\n')
    fo.truncate()
    fo.close()'''         
    return json.dumps({"res":"record deleted successfully"})                    



if __name__ == "__main__" :
    app.run(host='0.0.0.0', debug=True, port=4000)