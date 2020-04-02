from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, make_response
import json


app = Flask(__name__)

@app.route('/',methods=['POST','Get'])
def my_echart():
    data,link=readfile("data.json","link.json")
    return render_template('echart.html', data=json.dumps(data),link=json.dumps(link))
def readfile(data_path,link_path):
    with open (data_path,'rb')as f:
        data = f.read()
        data = json.loads(data)
    with open (link_path,'rb')as f1:
        link = f1.read()
        link = json.loads(link)
    return(data,link)

@app.route('/create',methods=['POST'])
def create():
    if request.method == 'POST':
        create = json.loads(request.get_data(as_text=True))
        with open("link.json",'rb')as f:
            data=json.load(f)
            f.close()
        data['link'].append(create['link'])
        with open("link.json",'w')as f:
            f.write(json.dumps(data,indent=4))
            f.close()
        ##  create data
        with open("data.json",'rb')as f:
            data=json.load(f)
            f.close()
        data['data'].append(create['data'])
        with open("data.json",'w')as f:
            f.write(json.dumps(data,indent=4))
            f.close()

@app.route('/del',methods=['POST'])
def delete():
    if request.method == 'POST':
        del_data = json.loads(request.get_data(as_text=True))
        print(del_data['data']['name'])
        with open("data.json", 'rb')as f:
            data = json.load(f)
            f.close()
        n=[]
        for i, data1 in enumerate(data['data']):
            print(i, data1)
            print(type(data1['name'] ))
            print(type(del_data['data']['name']))
            if data1['name'] == int(del_data['data']['name']):
                print(type(i))
                n.append(i)
        n.reverse()
        print(n)
        for i in range(0, len(n)):
            del data['data'][int(n[i])]
        print(data)
        with open("data.json", 'w')as f:
            f.write(json.dumps(data, indent=4))
            f.close()

if __name__ == '__main__':
    app.run(debug=True)
