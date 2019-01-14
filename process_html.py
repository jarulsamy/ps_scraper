from bs4 import BeautifulSoup
import xlsxwriter
import datetime
from selenium.webdriver.support.ui import WebDriverWait
import os
from os.path import isfile, join
import natsort

def gen_data(filename):
    f = open(filename, "r")
    soup = BeautifulSoup(f, features="lxml")

    spans_date = soup.find_all('td', {'class' : 'ng-binding'})
    spans_cat = soup.find_all('span', {'class' : 'psonly ng-binding'})
    spans_assign = soup.find_all('td', {'class' : 'assignmentcol'})
    spans_grades = soup.find_all('span', {'class' : 'ng-binding ng-scope'})
    spans_teacher = soup.find_all('tr', {'class' : 'center'})

    date_lines = [str(span.get_text()) for span in spans_date]
    date_lines = [x.rstrip().lstrip() for x in date_lines]
    final_date = []

    for date in date_lines:
        try:
            datetime.datetime.strptime(date, '%m/%d/%Y')
            final_date.append(date)
        except:
            pass

    # Category
    cat_lines = [str(span.get_text()) for span in spans_cat]
    final_cat = [x.rstrip().lstrip() for x in cat_lines]

    # Assignment name
    assign_lines = [str(span.get_text()) for span in spans_assign]
    final_assign = [x.rstrip().lstrip() for x in assign_lines]
    
    # Actual grade
    grade_lines = [str(span.get_text()) for span in spans_grades]
    grade_lines.remove(grade_lines[-1])
    if "Grades last updated on:" in grade_lines[0]:
        grade_lines.remove(grade_lines[0])


    # Process and Remove extra random *
    teacher_lines = [span.get_text() for span in spans_teacher]
    teacher_lines = teacher_lines[1].split("\n")
    teacher_lines = teacher_lines[1:4]
    teacher_lines = [str(about) for about in teacher_lines]
    teacher_lines[0] = teacher_lines[0][0:len(teacher_lines[0]) - 1]

    final_grade = []

    for grade in grade_lines:

        # Remove leading and trailing whitespace, basically cleanup
        grade = grade.rstrip()
        grade = grade.lstrip()

        # Handle not yet inputted grades
        if "--" in grade:
            # Find top and bottom of fraction
            grade_split = ["--", float(grade.split("/")[1])]
        else:
            # Find top and bottom of fraction
            grade_split = [float(x) for x in grade.split("/")]
        
        # Create final list of all grades
        final_grade.append(grade_split)
        
    return final_date, final_cat, final_assign, final_grade, teacher_lines


def gen_worksheets(worksheets):
    
    # Dictionary of worksheets
    worksheet_obj = {}
    
    # Create a workbook
    workbook = xlsxwriter.Workbook("grades.xlsx")

    percent_fmt = workbook.add_format({'num_format': '0.00%'})

    final_grade_format = workbook.add_format()
    final_grade_format.set_num_format('0.00')

    title_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})
    
    grade_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#00FFFF'
    })

    fail_format = workbook.add_format({
        'border': 1,
        'bg_color': '#FF0000',
        'font_color': '	#000000',
    })

    moderate_format = workbook.add_format({
        'border': 1,
        'bg_color': '#ff9900',
        'font_color': '	#000000',
    })

    pass_format = workbook.add_format({
        'border': 1,
        'bg_color': '#00ff00',
        'font_color': '	#000000',
    })

    # worksheet = workbook.add_worksheet(teacher_lines[2])
    
    for filename in worksheets:
        row, row_grades, col = 2, 2, 0
        worksheet_obj[filename] = workbook.add_worksheet(worksheets[filename][5])
        
        final_date = worksheets[filename][0]
        final_cat = worksheets[filename][1]
        final_assign = worksheets[filename][2]
        final_grade = worksheets[filename][3]
        teacher_lines = worksheets[filename][4]
        
        # print(worksheets[filename])

        for i in range(len(final_date)):
            worksheet_obj[filename].write(row, col, final_date[i])
            worksheet_obj[filename].write(row, col+1, final_cat[i])
            worksheet_obj[filename].write(row, col+2, final_assign[i])
            row += 1
                
        for grade, total in (final_grade):
            worksheet_obj[filename].write(row_grades, col+3, grade)
            worksheet_obj[filename].write(row_grades, col+4, total)
            worksheet_obj[filename].write(row_grades, col+5,
                            "=(D{}/E{})".format(row_grades+1, row_grades+1), percent_fmt)
            row_grades += 1

        worksheet_obj[filename].merge_range('A1:F1', teacher_lines[0], title_format)
        worksheet_obj[filename].merge_range('A2:D2', 'Final Grade', grade_format)

        # Calculate Final Percentage
        percentage = '=SUMIF(D3:D{0}, ">=0") / SUMIF(D3:D{0}, ">=0", E3:E36) * 100'.format(row_grades)
        worksheet_obj[filename].write_formula("E2", percentage, final_grade_format)#, percent_fmt)

        # Calculate Final Grade Letter
        letter = '=IF(E2 <= 69, "F", IF(AND(E2 >= 69.9, E2 <= 79.9), "C", IF(AND(E2 >= 80, E2 < 89.9), "B", IF(E2 >= 89.9, "A"))))'
        worksheet_obj[filename].write_formula("F2", letter)

        worksheet_obj[filename].conditional_format("E2:F2",
        {
            'type': 'formula',
            'criteria': '=$F$2="A"',
            'format': pass_format
        })
        
        worksheet_obj[filename].conditional_format("E2:F2",
        {
            'type': 'formula',
            'criteria': '=$F$2="B"',
            'format': moderate_format
        })
        
        worksheet_obj[filename].conditional_format("E2:F2",
        {
            'type': 'formula',
            'criteria': '=$F$2="C"',
            'format': moderate_format
        })

        worksheet_obj[filename].conditional_format("E2:F2",
        {
            'type': 'formula',
            'criteria': '=$F$2="F"',
            'format': fail_format
        })

    # Sort the worksheets -> Ascending
    workbook.worksheets_objs.sort(key=lambda x: x.name)
    workbook.close()
    
def gen_excel(path=None):
    worksheets = {}
    if path == None:
        path = "Downloads/"
        
    htmls = [f for f in os.listdir(path) if isfile(join(path, f))]
    htmls = natsort.natsorted(htmls)
    
    for filename in htmls:
        final_date, final_cat, final_assign, final_grade, teacher_lines = gen_data(path + filename)
        
        sheet_name = teacher_lines[2]
        worksheets[filename] = [final_date, final_cat, final_assign, final_grade, teacher_lines, sheet_name]
    
    gen_worksheets(worksheets)

    print("Writing to grades.xlsx...Done!")