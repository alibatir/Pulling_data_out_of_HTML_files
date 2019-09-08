#!/usr/bin/env python3
import requests
import bs4
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import csv
import sys

txt = (sys.argv)[1] + " " + (sys.argv)[2] #input is received.
startSemester = [None] * 6
endSemester = [None] * 6 #the variables to hold the semester names are created.
length = len(txt)

for i in range(0,length):
    if txt[i] == " ":
        startSemester[4] = "-"
        endSemester[4] = "-"
        for j in range(0,4):
            startSemester[j] = txt[j]    #checking whether the first semester is fall or spring or summer
            if txt[5] == "F" or "f":
                startSemester[5] = "1"
            if txt[5] == ("S" or "s") and txt[6] == ("p"):
                startSemester[5] = "2"
            if txt[5] == ("S" or "s") and txt[6] == ("u"):
                startSemester[5] = "3"
        for j in range(i+1,i+5):
            endSemester[j-i-1] = txt[j]  #checking whether the first semester is fall or spring or summer
            if txt[i+6] == "F" or "f":
                endSemester[5] = "1"
            if txt[i+6] == ("S" or "s") and txt[i+7] == ("p"):
                endSemester[5] = "2"
            if txt[i+6] == ("S" or "s") and txt[i+7] == ("u"):
                endSemester[5] = "3"
firstSemester = ""
lastSemester = ""
firstYear = ""
lastYear = ""

firstSemester = startSemester[0] + startSemester[1] + startSemester[2] + startSemester[3] + startSemester[4] + startSemester[5]
lastSemester = endSemester[0] + endSemester[1] + endSemester[2] + endSemester[3] + endSemester[4] + endSemester[5]
firstYear = startSemester[0] + startSemester[1] + startSemester[2] + startSemester[3]
lastYear = endSemester[0] + endSemester[1] + endSemester[2] + endSemester[3]
intFirstYear = int(firstYear)
intLastYear = int(lastYear)

#semester codes and integer values of first and last year of the termspan are constructed.

currentYear = intFirstYear
currentSemester = int(firstSemester[5])
numOfSemesters = 1
while 1:  #number of semesters is calculated.
    if currentYear == intLastYear and currentSemester == int(lastSemester[5]) :
        break
    if currentSemester == 2:
        currentSemester = 3
        numOfSemesters = numOfSemesters + 1
    elif currentSemester == 1:
        currentSemester = 2
        currentYear = currentYear + 1
        numOfSemesters = numOfSemesters + 1
    elif currentSemester == 3:
        currentSemester = 1
        numOfSemesters = numOfSemesters + 1

semesters = []
firstLink = ""
if firstSemester[5] == "1":
    firstLink = firstYear + "/" + str(intFirstYear+1) + "-" + "1"
elif firstSemester[5] == "2":
    firstLink = str(intFirstYear-1) + "/" + firstYear +  "-" + "2"
elif firstSemester[5] == "3":
    firstLink = str(intFirstYear-1) + "/" + firstYear +  "-" + "3"
#first semester link to use in html links is created.


myCurrentLink = firstLink
myYear = intFirstYear
iii = 0
while iii < numOfSemesters:
    if myCurrentLink[10] == "1":
        myCurrentLink = str(myYear) + "/" + str(myYear+1) + "-" +"1"
        semesters.append(myCurrentLink)
        myYear = myYear + 1
        myCurrentLink = str(myYear-1) + "/" + str(myYear) + "-" + "2"
        iii = iii + 1
    elif myCurrentLink[10] == "2":
        myCurrentLink = str(myYear-1) + "/" + str(myYear) + "-" +"2"
        semesters.append(myCurrentLink)
        myCurrentLink = str(myYear-1) + "/" + str(myYear) + "-" +"3"
        iii = iii + 1
    elif myCurrentLink[10] == "3":
        myCurrentLink = str(myYear-1) + "/" + str(myYear) + "-" +"3"
        semesters.append(myCurrentLink)
        myCurrentLink = str(myYear) + "/" + str(myYear+1) + "-" +"1"
        iii = iii + 1
#all the semester links are created.

firstSectionOfLink = "http://registration.boun.edu.tr/scripts/sch.asp?donem="
secondSectionOfLink = "&kisaadi="
thirdSectionOfLink = "&bolum="
#constant sections of the link are stored.

#department names are stored.
departments2 = ["ASIAN STUDIES", "ASIAN STUDIES WITH THESIS","ATATURK INSTITUTE FOR MODERN TURKISH HISTORY","AUTOMOTIVE ENGINEERING","BIOMEDICAL ENGINEERING","BUSINESS INFORMATION SYSTEMS","CHEMICAL ENGINEERING","CHEMISTRY","CIVIL ENGINEERING","COGNITIVE SCIENCE","COMPUTATIONAL SCIENCE %26 ENGINEERING","COMPUTER EDUCATION %26 EDUCATIONAL TECHNOLOGY","COMPUTER ENGINEERING","CONFERENCE INTERPRETING","CONSTRUCTION ENGINEERING AND MANAGEMENT","CRITICAL AND CULTURAL STUDIES","EARTHQUAKE ENGINEERING","ECONOMICS","ECONOMICS AND FINANCE","EDUCATIONAL SCIENCES","EDUCATIONAL TECHNOLOGY","ELECTRICAL %26 ELECTRONICS ENGINEERING","ENGINEERING AND TECHNOLOGY MANAGEMENT","ENVIRONMENTAL SCIENCES","ENVIRONMENTAL TECHNOLOGY","EXECUTIVE MBA","FINANCIAL ENGINEERING","FINE ARTS","FOREIGN LANGUAGE EDUCATION","GEODESY","GEOPHYSICS","GUIDANCE %26 PSYCHOLOGICAL COUNSELING","HISTORY","HUMANITIES COURSES COORDINATOR","INDUSTRIAL ENGINEERING","INTERNATIONAL COMPETITION AND TRADE","INTERNATIONALRELATIONS%3aTURKEY%2cEUROPE AND THE MIDDLE EAST","INTERNATIONAL RELATIONS%3aTURKEY%2cEUROPE AND THE MIDDLE EAST WITH THESIS","INTERNATIONAL TRADE","INTERNATIONAL TRADE MANAGEMENT","LEARNING SCIENCES","LINGUISTICS","MANAGEMENT","MANAGEMENT INFORMATION SYSTEMS","MATHEMATICS","MATHEMATICS AND SCIENCE EDUCATION","MECHANICAL ENGINEERING","MECHATRONICS ENGINEERING","MOLECULAR BIOLOGY %26 GENETICS","PHILOSOPHY","PHYSICAL EDUCATION","PHYSICS","POLITICAL SCIENCE%26INTERNATIONAL RELATIONS","PRIMARY EDUCATION","PSYCHOLOGY","SCHOOL OF FOREIGN LANGUAGES","SECONDARY SCHOOL SCIENCE AND MATHEMATICS EDUCATION","SOCIAL POLICY WITH THESIS","SOCIOLOGY","SOFTWARE ENGINEERING","SOFTWARE ENGINEERING WITH THESIS","SUSTAINABLE TOURISM MANAGEMENT","SYSTEMS %26 CONTROL ENGINEERING","TOURISM ADMINISTRATION","TRANSLATION","TRANSLATION AND INTERPRETING STUDIES","TURKISH COURSES COORDINATOR", "TURKISH LANGUAGE %26 LITERATURE" ,"WESTERN LANGUAGES %26 LITERATURES"]


kisadepartments2 = ["ASIA","ASIA","ATA","AUTO","BM","BIS","CHE","CHEM","CE","COGS","CSE","CET","CMPE","INT","CEM","CCS","EQE","EC","EF","ED","CET","EE","ETM","ENV","ENVT","XMBA","FE","PA","FLED","GED","GPH","GUID","HIST","HUM","IE","INCT","MIR","MIR","INTT","INTT","LS","LING","AD","MIS","MATH","SCED","ME","MECA","BIO","PHIL","PE","PHYS","POLS","PRED","PSY","YADYOK","SCED","SPL","SOC","SWE","SWE","TRM","SCO","TRM","WTR","TR","TK","TKL","LL"]

links = []
link = ""
for i in range(0,numOfSemesters):
    for j in range(0,len(departments2)):
        link = firstSectionOfLink + semesters[i] + secondSectionOfLink + kisadepartments2[j] + thirdSectionOfLink + departments2[j]
        links.append(link)
#all the links are stored in a list.


def remove_duplicates(l): #duplicate removing function is defined.
    return sorted(list(set(l)))

def my_function(url):

    print('Url:',url)
    try:
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")

        tbody = soup.find(width='1300px')
    #tables are received from the links
        codesecList=[]
        nameList=[]
        instrList=[]
        for tr in tbody.find_all("tr"):
            codesec = tr.find_all('td')[0].text
            name=tr.find_all('td')[2].text
            instr=tr.find_all('td')[5].text
        #info of the courses are appended to lists from the columns of the table.
            if len(codesec)!=2:
                codesecList.append(codesec)
                nameList.append(name)
                instrList.append(instr)

         #first elements of the columns are deleted.
        codesecList=codesecList[1:]
        nameList=nameList[1:]

        #deleting section number from the course code.
        for i in range(0,len(codesecList)):
            codesecList[i] = codesecList[i][:-4]
        #finding the course code number from the course code name.
        codeList=[]
        for i in range(0,len(codesecList)):
            int_list = [int(s) for s in re.findall('\\d+', codesecList[i])]
            codeList.append(int_list[0])

        count_Undergraduate=0
        count_Graduate=0

        #converting list elements to int
        codeList = [ int(x) for x in codeList ]
        for i in range(0,len(codeList)):
            if codeList[i] > 99 and codeList[i] < 500 : #(1xx – 4xx courses).
                count_Undergraduate+=1
            elif codeList[i] > 499 and codeList[i] < 800 : #(5xx – 7xx courses).
                count_Graduate+=1
            elif codeList[i] < 100:
                count_Graduate+=1
        #number of graduate and undergraduate courses are stored.

        #first elements of the columns are deleted.
        instrList=instrList[1:]

        #finding the number of distinct instructors.
        count_Instructor=len(set(instrList))

        #STAFF are deleted from the instructors list.
        isthisstaf=False
        for i in range(0,len(instrList)):
            if instrList[i]=='STAFF STAFF':
                isthisstaf=True
        if isthisstaf==True:
            count_Instructor-=1

        courses = [[0] * 4 for i in range(0,len(codeList))]
        for i in range(0,len(codeList)):
            for j in range(0,4):
                if j==0: #course code
                    courses[i][j]=codesecList[i]
                if j==1: #course name
                    courses[i][j]=nameList[i]
                if j==2: #instructor
                    courses[i][j]=instrList[i]
                if j==3:
                    if codeList[i] > 99 and codeList[i] < 500 : #(1xx – 4xx courses).
                        courses[i][j]=0
                    elif codeList[i] > 499 and codeList[i] < 800 : #(5xx – 7xx courses).
                        courses[i][j]=1
                    elif codeList[i] < 100 and codeList[i] > 49:
                        courses[i][j]=1
                    elif codeList[i] > 9 and codeList[i] < 50:
                        courses[i][j]=0
                    else:
                        courses[i][j]=1
        #all data is transferred to a two-dimensional list.

        instrList2 = remove_duplicates(instrList)
        count_Instructor2=len(instrList2)
        isthisstaf2=False
        for i in range(0,count_Instructor2):
            if instrList2[i] =='STAFF STAFF':
                isthisstaf2= True
        if isthisstaf2 == True:
            count_Instructor2 -= 1

        return count_Undergraduate,count_Graduate,count_Instructor,courses,len(codeList),len(instrList2)
    except: #different return values for non-existent course in a semester.
        print('ERROR')
        courses=[]
        return 0,0,0,courses,0,0
    #***************************************************************end function

count_Instructor = [[0] * 69 for i in range(0,len(semesters))]
count_Graduate = [[0] * 69 for i in range(0,len(semesters))]
count_Undergraduate = [[0] * 69 for i in range(0,len(semesters))]
courses = [[[[[""] for i in range(0,4)] for i in range(0,300)] for i in range(0,69)] for i in range(0,len(semesters))]
instructorsForSemesters = [[0] * 69 for i in range(0,len(semesters))]
for i in range(0,len(links)): #function is called for every link and data of every semester of every department is stored in courses list.
    my_function(links[i])
    count_Undergraduate[i//69][i%69],count_Graduate[i//69][i%69],count_Instructor[i//69][i%69],get_courses,count_course,instructorsForSemesters[i//69][i%69]=my_function(links[i])
    for j in range(0,count_course):
        for k in range(0,4):
            #courses[semester][department][course][course info]
            courses[i//69][i%69][j][k] = get_courses[j][k]

numOfInstructorsInSemesters = [[0] * len(semesters) for i in range(0,69)]

#total number of undergraduate and graduate courses for every departemt in every semester are stored.
#total course data and which semesters they are available are stored in totalData.
#names of all instructors are stored for every department.
#number of instructors are stored in a list.

totalData = [[[[""] for i in range(0,len(semesters)+4)] for i in range(0,300)] for i in range(0,69)]
totalUnderGraduate = [[0] * 69 for i in range(0,len(semesters))]
totalGraduate = [[0] * 69 for i in range(0,len(semesters))]
nameOfInstructors = [[""] * 150 for i in range(0,69)]
numOfInstructors = [0] * 69

for i in range(0,len(semesters)):
    for j in range(0,69):
        for k in range(0,300):
            if courses[i][j][k][0] != "": #repeating lessons are removed.
                a = 0
                for l in range(0,300):
                    if totalData[j][l][len(semesters)] == courses[i][j][k][0]:
                        a = 1
                        break
            if a != 1:   #course data from different semesters are merged to a new list.
                totalData[j][k][len(semesters)] = courses[i][j][k][0]
                totalData[j][k][len(semesters)+1] = courses[i][j][k][1]
                totalData[j][k][len(semesters)+2] = courses[i][j][k][3]
            for m in range(0,len(semesters)):
                for n in range(0,300):
                    if courses[m][j][n][0] == totalData[j][k][len(semesters)]:
                        totalData[j][k][m] = "X"
                        break
                    else:
                        totalData[j][k][m] = "0"
            for n in range(0,300):
                countIfInSemester = 0
                for m in range(0,len(semesters)):
                    if totalData[j][n][m] == "X":
                        countIfInSemester +=1
                totalData[j][n][len(semesters)+3] = str(countIfInSemester)

            if len(totalData[j][k][len(semesters)]) != 1: #total undergraduate and graduate lessons are calculated.
                courseNumber =[int(s) for s in re.findall('\\d+', totalData[j][k][len(semesters)])]
                if (courseNumber[0] > 99 and courseNumber[0] < 500) or (courseNumber[0] > 9 and courseNumber[0] < 50):
                    if (totalData[j][k][len(semesters)+2] == 0) and (totalData[j][k][i] == "X"):
                        totalUnderGraduate[i][j] += 1 #total number of undergraduate and graduate courses for every semester is calculated.
                elif (totalData[j][k][len(semesters)+2] == 1) and (totalData[j][k][i] == "X"):
                    totalGraduate[i][j] += 1

            if courses[i][j][k][2] != "" and courses[i][j][k][2] !='STAFF STAFF' and courses[i][j][k][2] !='STAFF STAFF\xa0':
                b = 0 #repeating instructors are removed.
                for o in range(0,150):
                    if nameOfInstructors[j][o] == courses[i][j][k][2]:
                        b = 1
                if b!= 1:
                    for p in range(0,150):
                        if nameOfInstructors[j][p] == "": #names and total number of instructors for every department and every semester are stored.
                            nameOfInstructors[j][p] = courses[i][j][k][2]
                            numOfInstructorsInSemesters[j][i] += 1
                            break

for i in range(0,len(departments2)): #link problems are solved.
    departments2[i] = departments2[i].replace("%26","&")
    departments2[i] = departments2[i].replace("%3a",":")
    departments2[i] = departments2[i].replace("%2c",",")

numOfInstructors = [0] * 69

for i in range(0,69):
    for j in range(0,150):
        if len(nameOfInstructors[i][j]) != 1 and nameOfInstructors[i][j] != "STAFF STAFF" and len(nameOfInstructors[i][j]) != 0:
            print(len(nameOfInstructors[i][j]))
            numOfInstructors[i] += 1 #total number of instructors (all semesters are summed)

print(totalData)
numberOfUnderGraduate = [0] * 69
numberOfGraduate = [0] * 69
sumOfUnderGraduate = [0] * 69
sumOfGraduate = [0] * 69
newTotalData = totalData
numOfColumns = 4 + len(semesters)
tableArr = [] #the array that will be converted to csv format is created.
firstRow = ["Dept./Prog.(name)","Course Code","Course Name"]
for i in range(0,len(semesters)):
    firstRow.append(semesters[i])
firstRow.append("Total Offerings")
tableArr.append(firstRow) #first row of the table is inserted.
for i in range(0,69):
    for course in totalData[i]: #number of graduate and undergraduate courses for a department is calculated.
        if len(course[len(semesters)]) != 1 :
            if course[len(semesters)+2] == 0:
                numberOfUnderGraduate[i] += 1
            elif course[len(semesters)+2] == 1:
                numberOfGraduate[i] += 1
    foo = [None] * numOfColumns
    foo[0] = kisadepartments2[i] + " (" + departments2[i] + ")"#;curInd = len(tableArr) #name of the departments are printed.
    foo[1] = "U" + str(numberOfUnderGraduate[i]) + " " + "G" + str(numberOfGraduate[i]) #number of graduate and undergraduate courses for a department is printed.
    for j in range(3,len(semesters)+3):
        foo[j] = "U" + str(totalUnderGraduate[j-3][i]) + " " + "G" + str(totalGraduate[j-3][i]) + " " + "I" + str(numOfInstructorsInSemesters[i][j-3])
        sumOfUnderGraduate[i] += totalUnderGraduate[j-3][i]
        sumOfGraduate[i] += totalGraduate[j-3][i]
    foo[len(semesters)+3] = "U" + str(sumOfUnderGraduate[i]) + " " + "G" + str(sumOfGraduate[i]) + " " + "I" + str(numOfInstructors[i]) #sum of undergraduate and graduate courses offered is printed.
    tableArr.append(foo) #first row of the department is printed.
    for course in totalData[i]:
        if len(course[len(semesters)]) == 1: #name of the courses and whether they are offered is printed.
            continue
        foo = [None]*numOfColumns
        foo[1] = course[len(semesters)]
        foo[2] = course[(len(semesters)+1)]
        for j in range(0,len(semesters)):
            foo[j+3] = '' if course[j] == '0' else course[j]
        foo[(numOfColumns-1)] = course[len(semesters)+3] + "/" + course[len(semesters)+3]
        tableArr.append(foo)

with open("output.csv","w") as f: #csv file is created.
    writer = csv.writer(f)
    writer.writerows(tableArr)

tableArr = np.array(tableArr) #table is transferred to csv format.
df= pd.read_csv("output.csv")

df = df.replace(np.nan,'',regex=True)
