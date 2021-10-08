from flask import Flask, render_template , request,redirect
import pandas as pd
import os
# from werkzeug.utils import secure_filename
UPLOAD_FOLDER ='static'

# 200001071 Saurabh Kumar Singh
# 200001068 Rishi Parsai
# 200001053 Nilay Jayantibhai Ganvit
# 200001069 Sanskar Verma



app=Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.secret_key='sfasgawifwhga'

#fuction to check
def check_name(s1 , s2):
   m, n = len(s1), len(s2)
   prev, cur = [0]*(n+1), [0]*(n+1)
   for i in range(1, m+1):
       for j in range(1, n+1):
           if s1[i-1] == s2[j-1]:
               cur[j] = 1 + prev[j-1]
           else:
               if cur[j-1] > prev[j]:
                   cur[j] = cur[j-1]
               else:
                   cur[j] = prev[j]
       cur, prev = prev, cur
   if min(n,m)-prev[n]<3:
        return True
   else:
        return False


@app.route('/',methods=["GET","POST"])
def main():
    msg=""
    if request.method=="POST":

        #taking attendance file
        file1=request.files['Attendance']
        if file1.filename=='':
            return redirect(request.url)
        filename1="Attendance"
        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

        #taking reference file
        file2 = request.files['Reference']
        if file2.filename == '':
            return redirect(request.url)
        filename2 ="Reference"
        file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
        filepath2 = 'static/Reference'
        data = pd.read_csv(filepath2)

        dicNR={}
        dicRN={}

        for row in data.iterrows():

            dicRN[row[1]['RollNo.']]=row[1]['Name'].lower()
            dicNR[row[1]['Name'].lower()] = row[1]['RollNo.']




        filepath1="static/Attendance"
        fi1 = open(filepath1, "r")
        contents = fi1.readlines()
        # code for reading attendance
        st = ""
        proxy=[]
        proRN={}
        dict = {}
        st=""
        #to check
        cnt=0

        for line in contents:
            if line[0] <= '9' and line[0] >= '0':
                st1 = ""
                for j in line:
                    if j <= '9' and j >= '0':
                        st1 += j
                    else:
                        break
                roll = int(st1)
                if roll not in dicRN:

                    continue
                str3=dicRN[roll]
                str3=str3.lower()
                st=st.lower()


                if check_name(str3,st):
                    dict[roll]=st

                else:

                    #checking of proxy
                    if st in dicNR:
                        list6=[dicNR[st],st.upper()]
                        proxy.append(list6)
                        proRN[dicNR[st]]=st
            else:
                st2 = ""
                for j in line:
                    if j <= '9' and j >= '0':
                        break
                    st2 += j
                st = st2


        list = []
        absent=0
        absent_list=[]
        list5=["RollNo.","Name"]
        absent_list.append(list5)
        #iterating through the reference file
        for row in data.iterrows():
            list2 = []
            list2.append(row[0])
            list2.append(row[1]['RollNo.'])
            list2.append(row[1]['Name'])

            if row[1]['RollNo.'] in dict:
                if row[1]['RollNo.'] not in proRN:
                    list2.append(1)
                else:
                    list2.append(0)
            else:
                list4=[]
                str3=str(row[1]['RollNo.'])
                list4.append(str3)
                list4.append(row[1]['Name'])
                absent_list.append(list4)
                list2.append(0)
            list.append(list2)

        list3=data.columns.values.tolist()

        df=pd.DataFrame(columns=list3, data=list)
        df.to_csv("static/final-reference.csv")


        msg4=""
        msg5=""
        msg3=""

        if len(absent_list)!=1:
            if len(proxy)==0:
                return render_template('Download.html',msg="DOWNLOAD",msg3="ABSENT STUDENTS",mylist=absent_list,msg7="HONEST STUDENTS")
            else:   
                return render_template('Download.html',msg="DOWNLOAD",msg3="ABSENT STUDENTS",mylist=absent_list,msg7="STUDENTS, WHO DID PROXY",mylist2=proxy)
        else:
            if len(proxy)==0:
                return render_template('Download.html',msg="DOWNLOAD",msg3="HURRAY 100% ATTENDANCE",msg7="HONEST STUDENTS")
            else:
                return render_template('Download.html', msg="DOWNLOAD", msg3="HURRAY 100% ATTENDANCE",msg7="STUDENTS, WHO DID PROXY",mylist2=proxy)
    return render_template('home.html')

if __name__=='__main__':
    app.run(debug=True)





