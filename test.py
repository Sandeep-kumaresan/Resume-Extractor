from flask import Flask,jsonify,request
import os
import pymupdf

global phone
global email
app = Flask(__name__)
def extract(path):

    document = pymupdf.open(path)
# document = pymupdf.open('D:\\Adra\\prepy_ai_source\\prepy_ai_source\\diabetic-cardiology.pdf')
# print(document.page_count)
    page = document.load_page(0)
    content = page.get_text()
    separated = content.split()
    print(separated)
# page = document.load_page(1)
# for i in range(n,31):
#
#     page = document.load_page(i)
#     print(page.get_text())

    for i in range(len(separated)):
        if "@gmail.com" in separated[i]:
            email = separated[i]
        if "+91" in separated[i] and len(separated[i+1]) == 10:
            phone = separated[i+1]
    arr=[email,phone]
    return arr

@app.get('/details')
def details():
    content= request.get_json()
    path = content["path"]
    extract(path)
    return jsonify({"email":email,"phone":phone})

if __name__ == "__main__":
    app.run(debug=True,port=3000)