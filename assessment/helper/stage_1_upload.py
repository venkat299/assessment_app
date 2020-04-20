import pyexcel as pe
from django.db import transaction

from assessment.models import Unit, Desg, Section, Employee

eis_col = 'EIS'
dscd_col = 'DSCD'
sect_col = 'SECTION_CD'
work_unit_col = 'WORKING UNIT'
roll_unit_col = 'ONROLL_UNIT'
dob_col = 'DOR'
comments_col = 'Comments'
gender_col = 'GENDER'
name_col = 'NAME'


def validate_row(year, not_first_row, row, ignore_multiple_unit, unit_ls, desg_ls, sect_ls, eis_ls, eis_local_list,
                 working_unit):
    err_ls = []
    try:
        if year + "_" + row[dscd_col] not in desg_ls:
            err_ls.append(" dscd(" + row[dscd_col] + ")")
        if year + "_" + row[sect_col] not in sect_ls:
            err_ls.append(" sect(" + row[sect_col] + ")")
        if year + "_" + row[work_unit_col] not in unit_ls:
            err_ls.append(" unit(" + row[work_unit_col] + ")")
        if year + "_" + row[roll_unit_col] not in unit_ls:
            err_ls.append(" roll_unit(" + row[roll_unit_col] + ")")
        # if  row['WORKING_AS'] and row['WORKING_AS'] not in gdesg_ls:
        #     err.append(" working_as("+row['WORKING_AS']+")")
        # if  row['WORKING_SINCE']  and not validate_date(row['WORKING_SINCE']) :
        #     err.append(" date_format("+row['WORKING_SINCE'].strftime('%Y-%m-%d')+")")
        # if  row['QUALIFICATION']  and row['QUALIFICATION'] not in qualification_ls :
        #     err.append(" qualification("+row['QUALIFICATION']+")")

        # check duplicate eis in file
        if str(row[eis_col]) in eis_local_list:
            err_ls.append(" eis_repeat(" + str(row[eis_col]) + ")")
        else:
            eis_local_list.append(str(row[eis_col]))

        # check duplicate eis in db
        try:
            if str(year) + "_" + str(row[eis_col]) in eis_ls:
                err_ls.append(" eis_dup_db(" + str(row[eis_col]) + ")")
        except ValueError as e:
            err_ls.append(" eis_err(" + str(row[eis_col]) + ")")

        # check if multiple working_unit present in file
        if not ignore_multiple_unit:
            if not_first_row:
                if str(row[work_unit_col]) not in working_unit:
                    err_ls.append(" multiple_work_unit(" + str(row[work_unit_col]) + ")")
            else:
                working_unit.append(str(row[work_unit_col]))
                not_first_row = True
    except KeyError as e:
        err_ls.append("Couldn't find required columns".format(e))
    # return err list
    if not err_ls:
        return None, eis_local_list, working_unit, not_first_row
    else:
        return err_ls, eis_local_list, working_unit, not_first_row


@transaction.atomic
def upload_stage_1(content, extension, ignore_multiple_unit, sheet_name, year):
    response_message = []

    unit_ls = Unit.objects.values_list('u_id', flat=True)
    desg_ls = Desg.objects.values_list('d_id', flat=True)
    sect_ls = Section.objects.values_list('s_id', flat=True)
    eis_ls = Employee.objects.values_list('e_id', flat=True)

    desg_dup_ls = []
    eis_local_list = []
    working_unit = []
    not_first_row = False

    if sheet_name == "":
        sheet_name = None

    try:
        sheet = pe.get_sheet(file_type=extension, file_content=content, sheet_name=sheet_name,
                             name_columns_by_row=3)  # row_limit=10
        sheet.delete_rows([0, 1, 2, 3])
        print(sheet)
        # sheet.row[0] = ['IDX',	'CADRE',	dscd_col,	'DESIG', 'GRADE',	'TOT',	'REQ',	'SAN',	'COMMENTS']
        # sheet.save_as("./temp/"+u_code+".xls")
        # sheet = pe.get_sheet(file_name=os.path.normpath("./temp/"+u_code+".xls"), name_columns_by_row=0)
        # sheet = pe.get_sheet(file_type=extension, file_content=content, name_columns_by_row=0,sheet_name=sheet_name)
    except ValueError as e:
        response_message.append("Sheet name not in excel file: {0}".format(e))
        return "error", response_message
    except AttributeError as e:
        response_message.append("Sheet name not in excel file: {0}".format(e))
        return "error", response_message
    except NotImplementedError as e:
        response_message.append("File not found or File not in proper format: {0}".format(e))
        return "error", response_message

    records = sheet.get_records()
    count = 0

    # validate each row
    for idx, record in enumerate(records):
        error_ls, eis_local_list, working_unit, not_first_row = validate_row(year,
                                                                             not_first_row,
                                                                             record,
                                                                             ignore_multiple_unit,
                                                                             unit_ls,
                                                                             desg_ls,
                                                                             sect_ls,
                                                                             eis_ls,
                                                                             eis_local_list,
                                                                             working_unit)

        if error_ls:
            # response_message.join(error_ls)
            response_message.append('ERR @ ROW {} => {}'.format(idx + 6, error_ls))
        else:
            count = count + 1

    ls = []
    if response_message:
        response_message.append('correct the errors and upload')
        return "error", response_message
    else:
        records = sheet.get_records()
        for idx, r in enumerate(records):
            # ls.append(('N','W',None,r['SECTION_CD'],r[work_unit_col],r['ONROLL_UNIT'],r[dscd_col],r['GENDER'],r['DOR'],r['NAME'],r[eis_col],r['Comments']
            #         #,r['WORKING_AS'],r['WORKING_SINCE'],r['QUALIFICATION']
            #         ))
            # ls.append(Employee(e_id=year + "_" + str(r[eis_col]),
            #                    e_eis=r[eis_col],
            #                    e_name=r[name_col],
            #                    e_desg_id=year + "_" + r[dscd_col],
            #                    e_sect_id=year + "_" + r[sect_col],
            #                    e_unit_roll_id=year + "_" + r[roll_unit_col],
            #                    e_unit_work_id=year + "_" + r[work_unit_col],
            #                    # e_year_id=year,
            #                    e_dob=r[dob_col],
            #                    e_gender=r[gender_col],
            #                    e_comments=r[comments_col]
            #                    ))
            emp, created = Employee.objects.update_or_create(e_id=year + "_" + str(r[eis_col]),
                                                             e_eis=r[eis_col],
                                                             e_name=r[name_col],
                                                             e_desg_id=year + "_" + r[dscd_col],
                                                             e_sect_id=year + "_" + r[sect_col],
                                                             e_unit_roll_id=year + "_" + r[roll_unit_col],
                                                             e_unit_work_id=year + "_" + r[work_unit_col],
                                                             e_year_id=year,
                                                             # e_dob=r[dob_col],
                                                             e_gender=r[gender_col],
                                                             e_comments=r[comments_col])
            emp.save()
            ls.append(created)

        batch_size = len(ls)
        print(batch_size)
        # if batch_size <= 0:
        #     response_message.append("no data found")
        #     return 'error', response_message
        # Employee.objects.bulk_create(ls, batch_size)
        response_message.append('--->{0} records inserted sucessfully'.format(batch_size))

    return "success", response_message

# if __name__ == '__main__':
# 	read_file("./temp/U08SAR.xls", "1", False)
