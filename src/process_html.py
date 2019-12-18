from bs4 import BeautifulSoup
import xlsxwriter
import datetime


def scrap_data(html):
    soup = BeautifulSoup(html, features="lxml")

    spans_date = soup.find_all('td', {'class': 'ng-binding'})
    spans_cat = soup.find_all('span', {'class': 'psonly ng-binding'})
    spans_assign = soup.find_all('td', {'class': 'assignmentcol'})
    spans_grades = soup.find_all('span', {'class': 'ng-binding ng-scope'})
    spans_teacher = soup.find_all('tr', {'class': 'center'})

    date_lines = [str(span.get_text()) for span in spans_date]
    date_lines = [x.rstrip().lstrip() for x in date_lines]
    final_date = []

    for date in date_lines:
        try:
            datetime.datetime.strptime(date, '%m/%d/%Y')
            final_date.append(date)
        except ValueError:
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
            grade_split = ("--", float(grade.split("/")[1]))
        else:
            # Find top and bottom of fraction
            grade_split = (
                float(grade.split("/")[0]), float(grade.split("/")[1]))

        # Create final list of all grades
        final_grade.append(grade_split)

    return final_date, final_cat, final_assign, final_grade, teacher_lines


def gen_worksheets(worksheets, path):
    # Dictionary of worksheets
    worksheet_obj = {}

    # Create a workbook
    workbook = xlsxwriter.Workbook(path)

    # Define various cell formats
    percent_fmt = workbook.add_format({'num_format': '0.00%'})

    final_grade_format = workbook.add_format()
    final_grade_format.set_num_format('0.00')

    title_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})

    letter_grade_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'center',
    })

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

    for filename in worksheets:
        row, row_grades, col = 2, 2, 0
        worksheet_obj[filename] = workbook.add_worksheet(
            worksheets[filename][5])

        final_date = worksheets[filename][0]
        final_cat = worksheets[filename][1]
        final_assign = worksheets[filename][2]
        final_grade = worksheets[filename][3]
        teacher_lines = worksheets[filename][4]

        # Write all data to file
        for i, j, k in zip(final_date, final_cat, final_assign):
            worksheet_obj[filename].write(row, col, i)
            worksheet_obj[filename].write(row, col + 1, j)
            worksheet_obj[filename].write(row, col + 2, k)
            row += 1

        for grade, total in (final_grade):
            worksheet_obj[filename].write(row_grades, col + 3, grade)
            worksheet_obj[filename].write(row_grades, col + 4, total)
            worksheet_obj[filename].write(row_grades, col + 5,
                                          "=(D{}/E{})".format(row_grades + 1, row_grades + 1), percent_fmt)
            row_grades += 1

        worksheet_obj[filename].merge_range(
            'A1:F1', teacher_lines[0], title_format)
        worksheet_obj[filename].merge_range(
            'A2:D2', 'Final Grade', grade_format)

        # Calculate Final Percentage
        percentage = '=SUMIF(D3:D{0}, ">=0") / SUMIF(D3:D{0}, ">=0", E3:E{0}) * 100'.format(
            row_grades)
        worksheet_obj[filename].write_formula(
            "E2", percentage, final_grade_format)

        # Calculate Final Grade Letter
        letter = '=IF(E2 <= 69, "F", IF(AND(E2 >= 69.9, E2 <= 79.9), "C", IF(AND(E2 >= 80, E2 < 89.9), "B", IF(E2 >= 89.9, "A"))))'
        worksheet_obj[filename].write_formula(
            "F2", letter, letter_grade_format)

        # Conditional Formatting
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

        # Calculate and set column widths
        longest_date = len(max(final_date, key=len))
        longest_cat = len(max(final_cat, key=len))
        longest_assign = len(max(final_assign, key=len))
        longest_grade = len(str(max([x[1] for x in final_grade])))

        worksheet_obj[filename].set_column("A:A", longest_date)
        worksheet_obj[filename].set_column('B:B', longest_cat)
        worksheet_obj[filename].set_column('C:C', longest_assign)
        worksheet_obj[filename].set_column("D:E", longest_grade)
        worksheet_obj[filename].set_column("F:F", 10)

    # Sort the worksheets -> Ascending
    workbook.worksheets_objs.sort(key=lambda x: x.name)
    workbook.close()


def gen_excel(htmls, path):
    worksheets = {}

    for html in htmls:
        final_date, final_cat, final_assign, final_grade, teacher_lines = scrap_data(
            html)

        sheet_name = teacher_lines[2]
        worksheets[html] = [final_date, final_cat,
                            final_assign, final_grade, teacher_lines, sheet_name]

    gen_worksheets(worksheets, path)
