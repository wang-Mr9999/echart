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
        ##  create data
        with open("data.json",'rb')as f:
            data=json.load(f)
            f.close()
        data['data'].append(create['data'])
        with open("data.json",'w')as f:
            f.write(json.dumps(data,indent=4))
            f.close()
        for i, data1 in enumerate(data['data']):
            if str(data1['name'])==str(create['link']["source"]):
                link1=i
        for i, data1 in enumerate(data['data']):
            if str(data1['name'])==str(create['link']["target"]):
                link2=i
        with open("link.json",'rb')as f:
            data=json.load(f)
            f.close()
        data['link'].append({"source": link1, "target": link2})
        with open("link.json",'w')as f:
            f.write(json.dumps(data,indent=4))
            f.close()


@app.route('/del',methods=['POST'])
def delete():
    if request.method == 'POST':
        del_data = json.loads(request.get_data(as_text=True))
        ###处理data.json文件
        with open("data.json", 'rb')as f:
            data = json.load(f)
            f.close()
        dn=[]
        for i, data1 in enumerate(data['data']):
            if data1['name'] == del_data['data']['name']:
                dn.append(i)
        del data['data'][int(dn[0])]
        with open("data.json", 'w')as f:
            f.write(json.dumps(data, indent=4))
            f.close()
        ####处理link.json文件
        ln = []
        with open("link.json", 'rb')as f:
            data = json.load(f)
            f.close()
        ##  寻找相同的index，这个index也可以是data的
        for i, data1 in enumerate(data['link']):
            if int(data1['source']) == int(dn[0]):
                ln.append(i)
            if int(data1['target']) == int(dn[0]):
                ln.append(i)

        ### 删除相同的link index标签
        ln.reverse()
        for i in range(0, len(ln)):
            del data['link'][int(ln[i])]
        print(data)
        ### 处理大于index的，处理小于index的
        for data3 in data['link']:
            if int(data3['source']) > int(dn[0]):
                data3['source'] = int(data3['source']) - 1
            if int(data3['target']) > int(dn[0]):
                data3['target'] = int(data3['target']) - 1

        print(data)
        ###  写文件
        with open("link.json", 'w')as f:
            f.write(json.dumps(data, indent=4))
            f.close()

if __name__ == '__main__':
    app.run(debug=True)
