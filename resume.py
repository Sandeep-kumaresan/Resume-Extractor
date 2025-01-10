import pdfplumber
import re
from flask import Flask,request

app = Flask(__name__)
def extract_pdf_text(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def description(resumetext):
    start_words = ['About Me','Objective','Description','Profile Summary']
    stop_words = ['Experience','Education','Projects','Skills','Certificates','Languages','Technical Skills']
    about_me=[]
    capture = False
    for i in resumetext:
        if any(word in i for word in start_words):
            capture = True
            continue
        if any(words in i for words in stop_words):
            capture = False
        if capture:
            about_me.append(i+" ")
    return "".join(about_me)

@app.get('/find')
def find():
    path = request.get_json()
    file_path = path["path"]
    resume_text = extract_pdf_text(file_path)
    # print(resume_text)

    separated = resume_text.split()
    lines = resume_text.split("\n")
    desc = description(lines)
    # print(separated)
    phone = ""
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    valid_emails = re.findall(email_regex, resume_text)
    # print(valid_emails)
    email = valid_emails[0]
    for i in range(len(separated)):
        if ("+91" in separated[i] and len(separated[i + 1]) == 10) :
            phone = separated[i + 1]
        elif("+91" in separated[i] and len(separated[i])>=5):
            check = ord(separated[i][3])
            if check>=48 and check<=57:
                num = separated[i][3:]
                if len(num)!=10:
                    phone=num+separated[i+1]
            elif ord(separated[i][4])>=48 and ord(separated[i][3]) <=57:
                num = separated[i][4:]
                if len(num) != 10:
                    phone = num + separated[i + 1]
        elif len(separated[i]) == 10 and separated[i].isdigit() :
            phone = separated[i]
    name = separated[0]+" "+separated[1]
    total_details = {"name":name,"email":email,"phone":phone,"description":desc}
    return total_details

if __name__ == "__main__":
    app.run(port=3000,debug=True)