# # script.py

# import argparse
# import pyexcel as pe
# import configparser 
# import os
# import sys
# import sqlite3
# import datetime
# import my_connection as connection

# from insert import sanction as insert_sanc

# DB_URL = None
# global conn
# conn = None
# sheet = None

# desg_ls=None
# gdesg_ls=None
# unit_ls=None
# sect_ls=None

# def load_tables():
#     # conn.row_factory = sqlite3.Row
#     c = conn.cursor()
#     c.execute("select dscd from desg")
#     global desg_ls
#     desg_ls = [ x[0] for x in c.fetchall()]

#     c.execute("select code from unit")
#     global unit_ls
#     unit_ls = [ x[0] for x in c.fetchall()]

#     c.execute("select code from section")
#     global sect_ls
#     sect_ls = [ x[0] for x in c.fetchall()]

#     c.execute("select eis from employee")
#     global eis_ls
#     eis_ls = [ x[0] for x in c.fetchall()]

#     c.execute("select substr(dscd,3,5) gdesg from desg group by substr(dscd,3,5)")
#     global gdesg_ls
#     gdesg_ls = [ x[0] for x in c.fetchall() ]

# eis_list = []
# working_unit = []
# not_first_row = False
# qualification_ls=[0,80,100,120,130,140,141,150,160]

# def validate_date(date_text):
#     # print(type_of(date_text))
#     try:
#         if not date_text.strftime('%Y-%m-%d'):
#             raise ValueError
#         return True
#     except ValueError:
#         return False

# def validate_row(row, ignore_multi_unit):
#     # hold all error list
#     err = []

#    # print(row)

#     # check wrong codes
#     if row['DSCD'] not in desg_ls:
#         err.append(" dscd("+row['DSCD']+")")
#     if row['SECTION_CD'] not in sect_ls:
#         err.append(" sect("+row['SECTION_CD']+")")
#     if row['WORKING UNIT'] not in unit_ls:
#         err.append(" unit("+row['WORKING UNIT']+")")
#     if row['ONROLL_UNIT'] not in unit_ls:
#         err.append(" roll_unit("+row['ONROLL_UNIT']+")")
#     # if  row['WORKING_AS'] and row['WORKING_AS'] not in gdesg_ls:
#     #     err.append(" working_as("+row['WORKING_AS']+")")
#     # if  row['WORKING_SINCE']  and not validate_date(row['WORKING_SINCE']) :
#     #     err.append(" date_format("+row['WORKING_SINCE'].strftime('%Y-%m-%d')+")")
#     # if  row['QUALIFICATION']  and row['QUALIFICATION'] not in qualification_ls :
#     #     err.append(" qualification("+row['QUALIFICATION']+")")

#     # check duplicate eis in file
#     global eis_list
#     if str(row['EIS']) in eis_list:
#         err.append(" eis_repeat("+str(row['EIS'])+")")
#     else:
#         eis_list.append(str(row['EIS']))

#     # check duplicate eis in db
#     try:
#         if int(row['EIS']) in eis_ls:
#             err.append(" eis_dup_db("+str(row['EIS'])+")")
#     except ValueError as e:
#         err.append(" eis_err("+str(row['EIS'])+")")

#     # check if multiple working_unit present in file
#     global working_unit
#     global not_first_row
#     if not ignore_multi_unit:
#         if not_first_row:
#             if str(row['WORKING UNIT']) not in working_unit:
#                 err.append(" multiple_work_unit("+str(row['WORKING UNIT'])+")")
#         else:
#             working_unit.append(str(row['WORKING UNIT']))
#             not_first_row = True

#     # return err list
#     if not err:
#         return None
#     else:
#         return err

# def read_file(xls_path, sheet_name, upload, ignore_multi_unit):
#     # book = pe.get_book(file_name=os.path.normpath(xls_path))
#     # sheets = book.to_dict()
#     # for name in sheets.keys():
#     #     print(name)
#     # self.wb.sheetnames
#     print(sheet_name)

#     try:
#         sheet = pe.get_sheet(file_name=os.path.normpath(xls_path), sheet_name=sheet_name, name_columns_by_row=0)

#     except ValueError as e:
#         print(e)
#         print("Error ValueError: {0}".format(e))
#         sys.exit()
#     except AttributeError as e:
#         print(e)
#         print("Error AttributeError: {0}".format(e))
#         sys.exit()
#         #raise e
#     except NotImplementedError as e:
#         print(e)
#         print("File not found or File not in proper format: {0}".format(e))
#         sys.exit()
#         #raise e

#     records = sheet.get_records()
#     count = 0
#     error_ls = []

#     # validate each row
#     for idx, record in enumerate(records):
#         err_row = validate_row(record, ignore_multi_unit)

#         if err_row:
#             error_ls.append(err_row)
#             print('ERR @ ROW {} => {}'.format(idx+2, err_row))
#         else:
#             count=count+1

#     if error_ls:
#         print('correct the above errors and upload')
#     else:
#         print('{0} rows will be inserted. add "-u" to upload'.format(count))
#         if upload:
#             ls=[]
#             records = sheet.get_records()  
#             for idx, r in enumerate(records):
#                 #sno    AREA    UNIT    MINE_TYPE    ONROLL_UNIT    WORKING UNIT    SECTION_TYPE    CADRE    SECTION    SECTION_CD    DESIG    DSCD    EIS    NAME    GENDER    DOB    Comments
#                 ls.append(('N','W',None,r['SECTION_CD'],r['WORKING UNIT'],r['ONROLL_UNIT'],r['DSCD'],r['GENDER'],r['DOR'],r['NAME'],r['EIS'],r['Comments']
#                     #,r['WORKING_AS'],r['WORKING_SINCE'],r['QUALIFICATION']
#                     ))
#             c = conn.cursor()
#             c.executemany('''insert into employee (emp_type,working,o_dcd,sect,ucde,roll_ucde,desg,gend,dob,name,eis,comments

#                 )
#                 values(?,?,?,?,?,  ?,?,?,?,?, ?,?
#                 )''',ls)
#             #,NULL,NULL, NULL
#             #,working_as, working_since,qualification
#                 # , ?,?,?)''',ls)
#             conn.commit()
#             print('--->{0} records inserted sucessfully'.format(len(ls)))

# def upload_desg(xls_path, sheet_name, upload, ignore_multi_unit):
#     try:
#         sheet = pe.get_sheet(file_name=os.path.normpath(xls_path), sheet_name=sheet_name, name_columns_by_row=0)

#     except ValueError as e:
#         print("Sheet name not in excel file: {0}".format(e))
#         sys.exit()
#     except AttributeError as e:
#         print("Sheet name not in excel file: {0}".format(e))
#         sys.exit()
#         #raise e
#     except NotImplementedError as e:
#         print("File not found or File not in proper format: {0}".format(e))
#         sys.exit()
#         #raise e

#     records = sheet.get_records()
#     error_ls = []

#     if error_ls:
#         print('correct the above errors and upload')
#     else:
#         print('{0} rows will be inserted. add "-u" to upload'.format(len(records)))
#         if upload:
#             ls=[]
#             for idx, r in enumerate(records):
#                 #sno    AREA    UNIT    MINE_TYPE    ONROLL_UNIT    WORKING UNIT    SECTION_TYPE    CADRE    SECTION    SECTION_CD    DESIG    DSCD    EIS    NAME    GENDER    DOB    Comments
#                 #cadre    gcd    dscd    desig    discp    grade    gdesig    promo
#                 print(r)
#                 ls.append((r['cadre'],r['gcd'],r['dscd'],r['desig'],r['discp'],r['grade'],r['gdesig'],r['promo']))
#             c = conn.cursor()
#             c.execute('delete from desg')
#             c.executemany('''insert into desg
#                 values(?,?,?,?,?,?,?,?)''',ls)
#             conn.commit()
#             print('--->{0} records inserted sucessfully'.format(len(ls)))


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     # parser.add_argument(
#     #     'filename', metavar='int', type=int, choices=range(10),
#     #      nargs='+', help='give a file name')
#     parser.add_argument('filename',  help='give file name')
#     parser.add_argument('table',  help='e for inserting employee; s for inserting sanction')
#     parser.add_argument("-sh",'--sheetname',  help='give sheet name; type * to include all sheets')
#     parser.add_argument("-u", "--upload", action="store_true", help="to update/commit changes into database")
#     parser.add_argument("-im", "--ignore_multi_unit", action="store_true", help="to upload file with multiple units and suppress its errors")#default=max,

#     args = parser.parse_args()
#     print(args)
#     #read_config()
#     conn = connection.get_connection()

#     if args.table == 'e':
#         load_tables()
#         read_file(args.filename, args.sheetname, args.upload, args.ignore_multi_unit)
#     elif args.table == 's':
#         insert_sanc.load_tables()
#         insert_sanc.read_file(args.filename, args.sheetname, args.upload)
#     elif args.table == 'd':
#         upload_desg(args.filename, args.sheetname, args.upload, args.ignore_multi_unit)
#     else:
#         print('supplied argument is wrong or the order of argument is wrong')
#         sys.exit()
