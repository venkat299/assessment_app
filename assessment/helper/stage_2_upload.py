import functools
import os

import pyexcel as pe

from assessment.models import Unit, Desg, Section, Sanction

dscd_column = 'DSCD'
ext_column = 'TOT'
req_column = 'REQ'  # 'TOT REQT 20-21'
san_column = 'SAN'  # 'SANC 20-21'
comment_column = 'COMMENTS'  # 'COMMENTS, IF ANY'


def validate_row(row, desg_ls, desg_dup_ls):
    err = []
    if row[dscd_column] not in desg_ls:
        err.append(" dscd(" + row[dscd_column] + ")")
    # if row['SECTION_CD'] not in sect_ls:
    # 	err.append(" sect("+row['SECTION_CD']+")")
    # if row['WORKING UNIT'] not in unit_ls:
    # 	err.append(" unit("+row['WORKING UNIT']+")")
    # if row['ONROLL_UNIT'] not in unit_ls:
    # 	err.append(" roll_unit("+row['ONROLL_UNIT']+")")

    if str(row[dscd_column]) in desg_dup_ls:
        err.append(" DSCD_repeat(" + str(row[dscd_column]) + ")")
    else:
        desg_dup_ls.append(str(row[dscd_column]))

    # try:
    # 	if int(row['EIS']) in eis_ls:
    # 		err.append(" eis_dup_db("+str(row['EIS'])+")")
    # except ValueError as e:
    # 	err.append(" eis_err("+str(row['EIS'])+")")

    if not err:
        return None, desg_dup_ls
    else:
        return err, desg_dup_ls


def filter_records(row, unit_code, unit_ls, desg_ls, discp_ls, sect_ls):
    if row[dscd_column] in desg_ls or (
            (len(row[dscd_column]) == 7 and row[dscd_column] not in discp_ls) and row[dscd_column] not in sect_ls) or \
            row['IDX'] == unit_code + '_g':
        return True
    else:
        return False


def sum_acc_tot(result, row):
    try:
        data = row[ext_column]
        if data != '' and data is not None:
            return result + int(data)
        else:
            return result
    except ValueError:
        return result + 0


def sum_acc_req(result, row):
    try:
        data = row[req_column]
        if data != '' and data is not None:
            return result + int(data)
        else:
            return result
    except ValueError:
        return result + 0


def sum_acc_sanc(result, row):
    try:
        data = row[san_column]
        if data != '' and data is not None:
            return result + int(data)
        else:
            return result
    except ValueError:
        return result + 0


def upload_stage_2(content, extension, u_code, year, column_upload):
    response_message = []

    unit_ls = Unit.objects.values_list('u_code', flat=True)
    desg_ls = Desg.objects.values_list('d_code', flat=True)
    discp_ls = Desg.objects.values_list('d_discp', flat=True)
    sect_ls = Section.objects.values_list('s_code', flat=True)

    desg_dup_ls = []

    # book = pe.get_book(file_name=os.path.normpath(xls_path))
    # sheets = book.to_dict()
    # for name in sheets.keys():
    # 	print(name)
    # unit_code = (os.path.basename(xls_path)).split('.')[0]

    if u_code not in unit_ls:
        # raise ValueError('Err: Unit code mentioned in file_name is wrong')
        response_message.append('Unit code mentioned in file_name is wrong')
        return "error", response_message

    # print("uploading for unit:{0}".format(unit_code))
    try:
        sheet = pe.get_sheet(file_type=extension, file_content=content)
        sheet.row[0] = ['IDX', 'CADRE', 'DSCD', 'DESIG', 'GRADE', 'TOT', 'REQ', 'SAN', 'COMMENTS']
        sheet.save_as("./temp/" + u_code + ".xls")
        sheet = pe.get_sheet(file_name=os.path.normpath("./temp/" + u_code + ".xls"), name_columns_by_row=0)
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
    error_ls = []
    filtered_rec = []

    for idx, record in enumerate(records):
        if filter_records(record, u_code, unit_ls, desg_ls, discp_ls, sect_ls):
            filtered_rec.append(record)
            err_row, desg_dup_ls = validate_row(record, desg_ls, desg_dup_ls)
            # print(record)

            if err_row:
                error_ls.append(err_row)
                response_message.append('ERR @ ROW {} => {}'.format(idx + 2, err_row))

    length = len(filtered_rec)
    if error_ls:
        response_message.append('correct the above error and upload')
        return 'error', response_message
    else:
        sum_req = functools.reduce(sum_acc_req, filtered_rec, 0)
        response_message.append("REQT total: {0}".format(sum_req))
        sum_sanc = functools.reduce(sum_acc_sanc, filtered_rec, 0)
        response_message.append("SANC total: {0}".format(sum_sanc))

        response_message.append('{0} rows will be inserted'.format(length))

        ls = []
        ls_alt = []
        for idx, r in enumerate(filtered_rec):
            # unit, dscd, req, sanc remark
            # sno	AREA	UNIT	MINE_TYPE	ONROLL_UNIT	WORKING UNIT	SECTION_TYPE	CADRE	SECTION	SECTION_CD	DESIG	DSCD	EIS	NAME	GENDER	DOB	Comments

            req_val = r[req_column]
            san_val = r[san_column]

            if req_val == '' or req_val == "" or req_val is None:
                req_val = 0
            if san_val == '' or san_val == "" or san_val is None:
                san_val = 0
            # print(req_val, san_val)
            ls.append(Sanction(sn_id=year + "_" + u_code + "_" + year + "_" + r[dscd_column],
                               sn_unit_id=year + "_" + u_code,
                               sn_dscd_id=year + "_" + r[dscd_column],
                               sn_req=req_val,
                               sn_san=san_val,
                               sn_comment=r[comment_column]))

            sn_obj = {'sn_id': year + "_" + u_code + "_" + year + "_" + r[dscd_column],
                      'sn_unit_id': year + "_" + u_code,
                      'sn_dscd_id': year + "_" + r[dscd_column],
                      'sn_comment': r[comment_column]}

            if column_upload == 'r':
                sn_obj['sn_req'] = req_val
            if column_upload == 's':
                sn_obj['sn_san'] = san_val
            if column_upload == 's+r':
                sn_obj['sn_req'] = req_val
                sn_obj['sn_san'] = san_val


            ls_alt.append(sn_obj)

        # c = conn.cursor()
        # #print(ls)
        # c.execute('delete from sanc where unit = ?',(unit_code,))
        # print('deleting rows for unit : {0}'.format(unit_code))
        # c.executemany('''insert into sanc (unit, dscd, req, san, remark) values(?,?,?,?,?)''',ls)
        # conn.commit()
        # if column_upload == "s+r":
        #     Sanction.objects.filter(sn_unit_id=year + '_' + u_code).delete()
        #     batch_size = len(ls)
        #     if batch_size <= 0:
        #         response_message.append("no data found")
        #         return 'error', response_message
        #     Sanction.objects.bulk_create(ls, batch_size)
        #     response_message.append('--->{0} records inserted sucessfully'.format(len(ls)))

        # if column_upload != "s+r":
        created_count = 0
        updated_count = 0

        for item in ls_alt:
            sanction, created = Sanction.objects.update_or_create(sn_id=item['sn_id'], defaults=item)
            sanction.save()
            if created:
                created_count = created_count + 1
            else:
                updated_count = updated_count + 1

        response_message.append(
            '--->{0} records added and  {1} records updated sucessfully'.format(created_count, updated_count))

        

    return "success", response_message

# if __name__ == '__main__':
# 	read_file("./temp/U08SAR.xls", "1", False)
