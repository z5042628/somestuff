# From COMP4920 group project - flow (2017)
# Written by: Irvin Deddy Yonowiharjo

# Note: I totally forgot to write comments
# Summary: - makeDic        : creates a dictionary for Flask and Django by providing course code and the title
#          - scrapeCourses  : grabs all courses offered in the handbook (from 2017) and return them in a list
#          - courseInfo     : grabs relevant information from a course code from the handbook
#          - checkGened     : checks if a course is a gened from a program
#          - fill_course_database : init the database will all courses information (this is a slow process, should be run once)

import sys, re, requests
from flow.translate import *
from flow.models import Course

def makeDic(courseCode, courseTitle):
    courseDic = {'CourseCode' : "", 'CourseTitle' : ""}
    courseDic['CourseCode'] = courseCode
    courseDic['CourseTitle'] = courseTitle

    return courseDic


def scrapeCourses():
    handbook = "http://www.handbook.unsw.edu.au/vbook2018/brCoursesByAtoZ.jsp?StudyLevel=Undergraduate&descr=All"

    requestUrl = requests.get(handbook)
    content = requestUrl.text

    overallList = []
    tempCode = ""
    #courseDic = {'CourseCode' : "", 'CourseTitle' : ""}
    for line in content.splitlines():

        courseCode = re.search(r'align=\"left\"\>([A-Z]{4}[0-9]{4})\<\/TD\>', line)
        if courseCode:
            tempCode = courseCode.group(1)
            #courseDic['CourseCode'] = courseCode.group(1)
            #overallList.append([courseCode.group(1)])

        courseName = re.search(r'\.html\"\>(.*)\<\/A\>\<\/TD\>', line)
        if courseName:
            #courseDic['CourseTitle'] = courseName.group(1)
            overallList.append(makeDic(tempCode, courseName.group(1)))

            #overallList[len(overallList) -1 ].append(courseName.group(1))

    return overallList


def courseInfo(course):
    if course == "BIOS6692":
        url = "http://www.handbook.unsw.edu.au/undergraduate/courses/2018/BEES6692.html"
    else:
        url = "".join(["http://www.handbook.unsw.edu.au/undergraduate/courses/2018/", course, ".html"])

    requestUrl = requests.get(url)
    content = requestUrl.text

    content = re.sub(r'<p>', '\n', content)

    infoDic = {'Prerequisite' : [], 'Corequisite' : [], 'Excluded' : [], 'Prerequisite_raw' : [], 'Corequisite_raw' : [], 'Excluded_raw' : [], 'UOC' : "", 'Faculty': [], 'Gen' : False, 'Semester' : []}

    for line in content.splitlines():
        preReq = re.search(r'[Pp]re[ \-]?[Rr]equisite[s]?.*:\s*(.*)\s*\<\/p\>', line)
        preReq1 = re.search(r'[Pp]re[Rr]eq[\s:]\s*(.*)\s*\<\/p\>', line)
        preReq2 = re.search(r'[Pp]re[\s:]\s*(.*)\s*\<\/p\>', line)
        preReq3 = re.search(r'[Pp]re[ \-]?[Rr]eq.*:\s*(.*)\s*\<\/p\>', line)
        preReq4 = re.search(r'[Pp]re[Rr]eq.*:\s*(.*)\s*\<\/p\>', line)
        preReq5 = re.search(r'[Pp]?re[ \-]?[Rr]equisite[s]?.*:\s*(.*)\s*\<\/p\>', line)
        preReq6 = re.search(r'[Pp]re[ \-]?[Rr]equisite[s]?[:]?\s*(.*)\s*\<\/p\>', line)
        uoc = re.search(r'<meta name=\"DC\.Subject\.UOC\"\s*CONTENT=\"\s*(.*)\s*\">', line)
        faculty = re.search(r'<meta name=\"DC\.Subject\.Faculty\"\s*CONTENT=\"\s*(.*)\s*\">', line)
        isGen = re.search(r'<meta name=\"DC\.Subject\.GenED\"\s*CONTENT=\"\s*(.*)\s*\">', line)

        if preReq or preReq1 or preReq2 or preReq3 or preReq4 or preReq5:
            if preReq:
                output = re.sub(r'<[/]?strong>', '', preReq.group(1))

            elif preReq1:
                output = re.sub(r'<[/]?strong>', '', preReq1.group(1))

            elif preReq3:
                output = re.sub(r'<[/]?strong>', '', preReq3.group(1))

            elif preReq2:
                output = re.sub(r'<[/]?strong>', '', preReq2.group(1))

            elif preReq4:
                output = re.sub(r'<[/]?strong>', '', preReq4.group(1))

            elif preReq5:
                output = re.sub(r'<[/]?strong>', '', preReq5.group(1))

            elif preReq6:
                output = re.sub(r'<[/]?strong>', '', preReq6.group(1))

            output = re.sub(r'\&nbsp\;', '', output)
            infoDic['Prerequisite_raw'].append(output)
            #courseList.append("".join(["Prerequisite: ", output]))

        coReq = re.search(r'[Cc]o[ \-]?[Rr]equisite[s]?.*:\s*(.*)\s*\<\/p\>', line)
        if coReq:
            output = re.sub(r'<[/]?strong>', '', coReq.group(1))
            output = re.sub(r'\&nbsp\;', '', output)
            infoDic['Corequisite_raw'].append(output)

            #courseList.append("".join(["Corequisite: ", output]))


        exclude = re.search(r'[Ee]xcluded:\s*(.*)\s*</p>', line)
        if exclude:
            output = re.sub(r'<[/]?strong>', '', exclude.group(1))
            output = re.sub(r'\&nbsp\;', '', output)
            infoDic['Excluded_raw'].append(output)

            #courseList.append("".join(["Excluded: ", output]))

        equ = re.search(r'[Ee]quivalent:\s*(.*)\s*</p>', line)
        if equ:
            output = re.sub(r'<[/]?strong>', '', equ.group(1))
            output = re.sub(r'\&nbsp\;', '', output)
            infoDic['Excluded_raw'].append(output)

            #courseList.append("".join(["Equivalent: ", output]))

        exclusion = re.search(r'[Ee]xclusion:\s*(.*)\s*</p>', line)
        if exclusion:
            output = re.sub(r'<[/]?strong>', '', exclusion.group(1))
            output = re.sub(r'\&nbsp\;', '', output)
            infoDic['Excluded_raw'].append(output)

            #courseList.append("".join(["Exclusion: ", output]))

        if uoc:
            infoDic['UOC'] = int(uoc.group(1))

        if faculty:
            infoDic['Faculty'] = faculty.group(1)

        if isGen:
            if isGen.group(1) == 'Y':
                infoDic['Gen'] = True

    url2 = "".join(["http://timetable.unsw.edu.au/2018/", course, ".html"])
    requestUrl = requests.get(url2)
    content = requestUrl.text

    for line in content.splitlines():
        # <td class="data" colspan="5"><a href="#X1S">SUMMER TERM</a></td>
        semester = re.search(r'<td class=\"data\">([A-Z]{1}[0-9]{1})</td>', line)
        if semester:
            infoDic['Semester'].append(semester.group(1))

    infoDic['Prerequisite'] = query_to_list(''.join(infoDic['Prerequisite_raw']))
    infoDic['Corequisite'] = query_to_list(''.join(infoDic['Corequisite_raw']))
    infoDic['Excluded'] = query_to_list(''.join(infoDic['Excluded_raw']))

    return infoDic

def checkGened(course, program):
    url = "".join(["http://www.handbook.unsw.edu.au/undergraduate/programs/2018/", program, ".html"])
    urlGen = "http://www.handbook.unsw.edu.au/vbook2018/brGenEdByFaculty.jsp"

    requestUrl = requests.get(url)
    content = requestUrl.text

    content = re.sub(r'<p>', '\n', content)

    programFaculty = ""
    courseFaculty = ""

    for line in content.splitlines():
        faculty1 = re.search(r'<meta name=\"DC\.Subject\.Faculty\"\s*CONTENT=\"\s*(.*)\s*\">', line)
        if faculty1:
            programFaculty = faculty1.group(1)

    requestUrl = requests.get(urlGen)
    content = requestUrl.text

    content = re.sub(r'<p>', '\n', content)

    IsGen = False

    for line in content.splitlines():
        word = re.search(r'\.html\">([A-Z]{4}[0-9]{4})<\/TD>', line)
        if word:
            if word.group(1) == course:
                IsGen = True

    if IsGen:
        urlCheckGen = "".join(["http://www.handbook.unsw.edu.au/undergraduate/courses/2018/", course, ".html"])

        requestUrl = requests.get(urlCheckGen)
        content = requestUrl.text

        content = re.sub(r'<p>', '\n', content)
        for line in content.splitlines():
            faculty = re.search(r'<meta name=\"DC\.Subject\.Faculty\"\s*CONTENT=\"\s*(.*)\s*\">', line)
            if faculty:
                courseFaculty = faculty.group(1)

        if courseFaculty == programFaculty:
            IsGen = False

    #print(courseFaculty)
    #print(programFaculty)
    return IsGen

def fill_course_database():
    courses = scrapeCourses()
    for course in courses:
        c = Course(course['CourseCode'])
        c.title = course['CourseTitle']
        print(course['CourseCode'])
        course_info_dict = courseInfo(course['CourseCode'])

        c.prerequisites_raw = course_info_dict['Prerequisite_raw']
        c.corequisites_raw = course_info_dict['Corequisite_raw']
        c.excluded_raw = course_info_dict['Excluded_raw']
        c.uoc = course_info_dict['UOC']
        c.gened = course_info_dict['Gen']
        c.faculty = course_info_dict['Faculty']
        c.semester = course_info_dict['Semester']
        c.save()


#
# print(courseInfo("FINS4774"))
# print(courseInfo("MATH1231"))
#print(courseInfo("TELE3113"))

# print(" ".join(["ELEC2141", " ".join(courseInfo("ELEC2141"))]))
# print(" ".join(["FOOD3020", " ".join(courseInfo("FOOD3020"))]))
# print(" ".join(["FINS4774", " ".join(courseInfo("FINS4774"))]))
# print(" ".join(["CVEN4402", " ".join(courseInfo("CVEN4402"))]))
# print(" ".join(["COMP4906", " ".join(courseInfo("COMP4906"))]))
# print(" ".join(["ARTS3480", " ".join(courseInfo("ARTS3480"))]))
# print(" ".join(["SOLA5508", " ".join(courseInfo("SOLA5508"))]))


'''
test case
d = courseInfo("COMP2911")
assert d == ['Prerequisite: COMP1927 or COMP2521 or MTRN3500', 'Excluded: COMP2011, COMP2511']
e = courseInfo("COMP2121")
assert e == ['Prerequisite: COMP1917 or COMP1921 or COMP1511 or COMP1521, or (COMP1911 and MTRN2500)', 'Excluded: ELEC2142, MTRN3200']
f = courseInfo("ATSI0002")
assert f == []
a = checkGened("SOLA1070", "3778")
assert a == True
b = checkGened("COMP2521", "3778")
assert b == False
c = checkGened("ARTS1630", "3778")
assert c == True
g = checkGened("ATSI0002", "3778")
assert g = False
'''
