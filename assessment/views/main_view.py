# Create your views here.
import json

from dal import autocomplete
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.db.models import Sum, FloatField
from django.db.models.functions import Cast
from django.http import FileResponse, Http404
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from assessment.helper.stage_1_upload import upload_stage_1
from assessment.helper.stage_2_upload import upload_stage_2
from assessment.models import Employee, Desg, Unit, Sanction, SanctionSection, UnitSancDesg, UnitSancSect
from assessment.models import Section
from assessment.reports.report import ReportGenerator

EDIT_ENABLED = getattr(settings, "EDIT_ENABLED", False)

# def index(request):
#     employee_list = Employee.objects.order_by('-e_dob')[:5]
#     context = {'employee_list': employee_list}
#     return render(request, 'assessment/index.html', context)


# from mpm_app.utils import PagedFilteredTableView

def in_ied_execs_grp(user):
    # print(user.groups.all())
    # print(u'area_apms')
    return user.groups.filter(name='ied_execs').exists()
    # return True

def index(request):
    return render(request, 'base.html')

# @user_passes_test(in_ied_execs_grp)
def upload_files(request):
    unit_ls = Unit.objects.values('u_id', 'u_name', 'u_type', 'u_area__a_name')
    context = {'display': False, 'unit_list': unit_ls}
    return render(request, 'upload_files.html', context)


def upload_req(request):
    unit_ls = Unit.objects.values('u_id', 'u_name', 'u_type', 'u_area__a_name')
    context = {'display': False, 'status': 'error', 'unit_list': unit_ls}

    if request.method == 'POST' and request.FILES:
        file = request.FILES['file']
        if file:
            filename = file.name
            u_code = filename.split(".")[0]
            content = file.read()
            column_upload = request.POST['column_select']
            # print(content)
            # u_code = "U08SAR"
            if filename and filename.split(".")[-1] == "xls":
                # todo -  get 'year' dynamically from user input
                status, response_msg = upload_stage_2(content, 'xls', u_code, '2020', column_upload)
                context['display'] = True
                context['status'] = status
                context['response_msg'] = response_msg
                # print(context)

    return render(request, 'upload_files.html', context)


def upload_ext(request):
    unit_ls = Unit.objects.values('u_id', 'u_name', 'u_type', 'u_area__a_name')
    context = {'display': False, 'status': 'error', 'unit_list': unit_ls}

    if request.method == 'POST' and request.FILES:
        file = request.FILES['file']
        if file:
            filename = file.name
            ignore_multiple_unit = request.POST["ignore_multiple_unit"]
            sheet_name = request.POST["sheet_name"]
            # extension = filename.split(".")[-1]
            content = file.read()
            # print(content)
            # u_code = "U08SAR"
            if filename and filename.split(".")[-1] == "xls":
                # todo -  get 'year' dynamically from user input
                status, response_msg = upload_stage_1(content, 'xls', ignore_multiple_unit, sheet_name, '2020')
                context['display'] = True
                context['status'] = status
                context['response_msg'] = response_msg
                # print(context)
            # return render(request, 'upload_files.html', context)
    return render(request, 'upload_files.html', context)


def bulk_delete_unit(request):
    unit_ls = Unit.objects.values('u_id', 'u_name', 'u_type', 'u_area__a_name')
    context = {'display': False, 'status': 'error', 'unit_list': unit_ls}

    if request.POST["unit_select"] and request.POST["table_select"]:
        unit_val = request.POST["unit_select"]
        table_select = request.POST["table_select"]
        response_msg = []
        msg = ""
        count = 0
        if table_select == "employee":
            count, msg = Employee.objects.filter(e_unit_roll_id=unit_val).delete()
        elif table_select == "sanction":
            count, msg = Sanction.objects.filter(sn_unit=unit_val).delete()
        response_msg.append("deleted {0} rows".format(count))
        response_msg.append(json.dumps(msg, cls=DjangoJSONEncoder))
        context['display'] = True
        context['status'] = 'success'
        context['response_msg'] = response_msg
        # print(context)
        # return render(request, 'upload_files.html', context)
    return render(request, 'upload_files.html', context)


def report_download(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    print(body)
    report = body['report']
    file_format = body['file_format']
    param = body['param']
    file_name = ReportGenerator(report, file_format, param).generate()
    try:
        return FileResponse(open(file_name, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()


def unit_req(request):
    unit_ls = Unit.objects.values('u_id', 'u_name', 'u_type', 'u_area__a_name')
    context = {'unit_list': unit_ls}

    u_id = request.GET.get('u_id')
    if u_id:
        u_obj = Unit.objects.get(u_id = u_id)
        context["selected_unit"] = u_obj


    # print(unit_ls)
    return render(request, 'unit_req.html', context)


def unit_req_filtered(request):
    unit_ls = Unit.objects.values('u_id', 'u_name', 'u_type', 'u_area__a_name').order_by('u_area__a_order', 'u_type',
                                                                                         'u_id')
    # dscd_ls = Desg.objects.values()
    context = {'unit_list': unit_ls}
    # print(unit_ls)
    return render(request, 'unit_req_filtered.html', context)

def budget_summary_unit(request):
    unit_summary = UnitSancDesg.objects.values('u_id', 'u_name', 'u_type', 'u_code', 'a_name', 'a_order', 'acde', ) \
        .annotate(ftot=Sum('tot'), fsan=Sum('san'), freq=Sum('req'), psan=Sum('prev_san'), preq=Sum('prev_req'),
                  retr0=Sum('retr0'),
                  order=Cast('a_order', FloatField())).order_by(
        'order', '-u_type', 'u_code')
    area_summary = UnitSancDesg.objects.values('a_name', 'a_order', 'acde', ) \
        .order_by('order', ) \
        .annotate(ftot=Sum('tot'), fsan=Sum('san'), freq=Sum('req'), psan=Sum('prev_san'), preq=Sum('prev_req'),
                  retr0=Sum('retr0'),
                  order=Cast('a_order', FloatField()))
    context = {'unit_summary': json.dumps(list(unit_summary), cls=DjangoJSONEncoder),
               'area_summary': json.dumps(list(area_summary), cls=DjangoJSONEncoder)
               }
    # print(unit_ls)
    return render(request, 'budget_summary_unit.html', context)


def get_all_desg(request):
    dscd_ls = Desg.objects.values()
    # response = json.dumps(dscd_ls, cls=DjangoJSONEncoder)
    return JsonResponse(list(dscd_ls), safe=False)
    # return HttpResponse(response, content_type='application/json')


def get_all_sect(request):
    sect_ls = Section.objects.values()
    return JsonResponse(list(sect_ls), safe=False)
    # response = json.dumps(sect_ls, cls=DjangoJSONEncoder)
    # return HttpResponse(response, content_type='application/json')


def get_unit_detail(request):
    u_id = request.GET.get('u_id')
    unit = Unit.objects.values('u_id', 'u_name', 'u_type', 'u_area__a_name', 'u_area__a_order').filter(u_id=u_id)[0]
    return JsonResponse(unit, safe=False)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_req_unit_gdesg(request):
    u_id = request.GET.get('u_id')
    # print(u_id)
    result1 = UnitSancDesg.objects.values('u_id', 'u_name', 'a_order', 'u_type', 'a_name', 'd5', 'd_gdesig', 'd_rank',
                                          'd_discp').filter(u_id=u_id).order_by(
        'd5').annotate(ftot=Sum('tot'), fsan=Sum('san'),
                       freq=Sum('req'), retr0=Sum('retr0'), psan=Sum('prev_san'))
    # print(result1.query)
    result2 = None
    with connection.cursor() as cursor:
        cursor.execute('''select substr(ad.d_code,-5) value ,d_year_id, d_discp, d_gdesig  as name 
            from assessment_desg ad 
            where ad.d_id not in (select as2.sn_dscd_id from assessment_sanction as2 where as2.sn_unit_id= %s) 
            group by value''', [u_id])
        result2 = dictfetchall(cursor)

    # print(result2.query)
    # print(result2)get_filter_unit_gdesg_list

    final_result = {'unit_sanc': list(result1), 'desg_list': list(result2)}
    response = json.dumps(final_result, cls=DjangoJSONEncoder)

    return HttpResponse(response, content_type='application/json')


def get_all_gdesg(request):
    with connection.cursor() as cursor:
        cursor.execute('''  SELECT substr(ad.d_code, -5)||"@"||group_concat(d_grade||":"||substr(ad.d_code,1,2))  value,
                            d_year_id,
                            d_discp,
                            d_gdesig AS name
                            FROM assessment_desg ad
                            GROUP BY substr(ad.d_code, -5) ''')
        result2 = dictfetchall(cursor)

    # print(result2.query)
    # print(result2)get_filter_unit_gdesg_list

    final_result = {'desg_list': list(result2)}
    response = json.dumps(final_result, cls=DjangoJSONEncoder)

    return HttpResponse(response, content_type='application/json')


# get_filter_unit_gdesg_list

def get_filter_unit_gdesg_list(request):
    filter = request.GET.get('filter')
    print("filter > ", filter)
    # d5 = request.GET.get('d5')
    # print(u_id, d5)
    # result1 = UnitSancDesg.objects.raw('SELECT pkey, a_name, a_order, u_id, d5, d_gdesig, d_id, d_rank, d_discp, d_name, d_grade, '
    #                                    'd_gcode, tot, san, req, comment, d_cadre, retr0, prev_san FROM Unit_Sanc_Desg where ' + filter + ' '
    #                                    'order by a_order, u_id, d_gcode')
    query_area = 'SELECT pkey, a_name, a_order, u_id, u_name, d5, d_gdesig, d_id, d_rank, d_discp, d_name, d_grade, u_type,' \
                 'd_gcode, sum(tot) ftot, sum(san) fsan, sum(req) freq, comment, d_cadre, sum(retr0) retr0, sum(prev_san) psan FROM Unit_Sanc_Desg where ' \
                 + filter + \
                 ' group by a_name, d5 order by a_order'
    with connection.cursor() as cursor:
        cursor.execute(query_area, )
        result_area = dictfetchall(cursor)

    query = 'SELECT pkey, a_name, a_order, u_id, u_name, d5, d_gdesig, d_id, d_rank, d_discp, d_name, d_grade, u_type,' \
            'd_gcode, sum(tot) ftot, sum(san) fsan, sum(req) freq, comment, d_cadre, sum(retr0) retr0, sum(prev_san) psan FROM Unit_Sanc_Desg where ' \
            + filter + \
            ' group by u_id, d5 order by a_order, u_id, d_gcode'
    with connection.cursor() as cursor:
        cursor.execute(query, )
        result_unit = dictfetchall(cursor)

    # print(result1)
    final_result = {'area_list': list(result_area), 'unit_list': list(result_unit), }
    response = json.dumps(final_result, cls=DjangoJSONEncoder)
    # print(response)
    return HttpResponse(response, content_type='application/json')


def get_desg_summary_company(request):
    filter = request.GET.get('filter')
    print(filter)
    query = ' select a_name, u_id, d5, d_gdesig, d_id, d_rank, d_discp, d_name, d_grade, d_gcode, d_cadre, ' \
            ' sum(tot) tot, sum(san) san, sum(req) req, sum(retr0) retr0, sum(prev_san)  prev_san FROM Unit_Sanc_Desg where ' \
            + filter + \
            ' group by d_gcode order by d_gcode'
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query, )
        desg_summary_company = dictfetchall(cursor)

    final_result = {'desg_summary_company': list(desg_summary_company)}
    response = json.dumps(final_result, cls=DjangoJSONEncoder)
    return HttpResponse(response, content_type='application/json')


def get_desg_summary_area(request):
    filter = request.GET.get('filter')
    a_order = request.GET.get('a_order')
    print(filter)
    # print(a_order)
    query = ' select a_name, u_id, d5, d_gdesig, d_id, d_rank, d_discp, d_name, d_grade, d_gcode, d_cadre, ' \
            ' sum(tot) tot, sum(san) san, sum(req) req, sum(retr0) retr0, sum(prev_san)  prev_san FROM Unit_Sanc_Desg where ' \
            + filter + \
            ' and a_order= ' \
            + str(a_order) + \
            ' group by d_gcode order by d_gcode'
    with connection.cursor() as cursor:
        cursor.execute(query, )
        desg_summary_area = dictfetchall(cursor)

    final_result = {'desg_summary_area': list(desg_summary_area)}
    response = json.dumps(final_result, cls=DjangoJSONEncoder)
    return HttpResponse(response, content_type='application/json')


def get_stat_for_gdesg_list(request):
    # filter = request.GET.get('filter')
    u_id = request.GET.get('u_id')
    d5 = request.GET.get('d5')
    a_order = request.GET.get('a_order')
    u_type = request.GET.get('u_type')

    result_area = UnitSancDesg.objects.values('a_name').filter(a_order=a_order, d5=d5) \
        .annotate(ftot=Sum('tot'), fsan=Sum('san'),
                  freq=Sum('req'), retr0=Sum('retr0'), psan=Sum('prev_san'))[0]
    result_area_unit_type = \
    UnitSancDesg.objects.values('a_name', 'u_type').filter(a_order=a_order, u_type=u_type, d5=d5) \
        .annotate(ftot=Sum('tot'), fsan=Sum('san'),
                  freq=Sum('req'), retr0=Sum('retr0'), psan=Sum('prev_san'))[0]
    result_company = UnitSancDesg.objects.values('d5').filter(d5=d5) \
        .annotate(ftot=Sum('tot'), fsan=Sum('san'),
                  freq=Sum('req'), retr0=Sum('retr0'), psan=Sum('prev_san'))[0]
    result_company_unit_type = UnitSancDesg.objects.values('d5', 'u_type').filter(u_type=u_type, d5=d5) \
        .annotate(ftot=Sum('tot'), fsan=Sum('san'),
                  freq=Sum('req'), retr0=Sum('retr0'), psan=Sum('prev_san'))[0]

    # print(result1)
    final_result = {'area_level': result_area, 'area_type_level': result_area_unit_type, 'wcl_level': result_company,
                    'wcl_type_level': result_company_unit_type}
    # response = json.dumps(final_result, cls=DjangoJSONEncoder)

    # response = jsonify('fetched_data', render_template('stat_desg.html', new_fetched_data=final_result))
    print(final_result)
    response = render_to_string('stat_desg.html', final_result)
    # response = jsonify('fetched_data', response)
    # print(response)
    return JsonResponse(response, safe=False)
    # return HttpResponse(response)


# get_stat_gdesg_list

def get_req_unit_desg(request):
    u_id = request.GET.get('u_id')
    d5 = request.GET.get('d5')
    # print(u_id, d5)
    result1 = UnitSancDesg.objects.values('u_id', 'd5', 'd_gdesig', 'd_id', 'd_rank', 'd_discp', 'd_name', 'd_grade',
                                          'd_gcode', 'tot', 'san', 'req', 'comment', 'd_cadre', 'retr0',
                                          'prev_san').filter(
        u_id=u_id,
        d5=d5).order_by(
        'd_gcode')
    # print(result1)
    response = json.dumps(list(result1), cls=DjangoJSONEncoder)
    # print(response)
    return HttpResponse(response, content_type='application/json')


def set_req_unit_desg(request):
    if not EDIT_ENABLED:
        print("Cannot edit; edit feature locked")
        msg = {'success': False, "msg": "Cannot edit; edit feature locked"}
        return HttpResponse(json.dumps(msg, cls=DjangoJSONEncoder), content_type='application/json')
    u_id = request.POST['u_id']
    d_id = request.POST['d_id']
    req = request.POST['req']
    san = request.POST['san']
    ext = request.POST['tot']
    comment = request.POST['comment']
    obj = Sanction(sn_id=u_id + '_' + d_id, sn_unit_id=u_id, sn_dscd_id=d_id, sn_req=req, sn_san=san,
                   sn_comment=comment, sn_ext = ext)
    obj.save()
    print(u_id, d_id, " ext=" ,ext, " req=", req, " sanc=", san, comment)
    result = {'success': True}
    # print(result)
    response = json.dumps(list(result), cls=DjangoJSONEncoder)
    return HttpResponse(response, content_type='application/json')


def get_req_unit_sect(request):
    u_id = request.GET.get('u_id')
    d5 = request.GET.get('d5')
    # print(u_id, d5)
    result = UnitSancSect.objects.values('s_name', 'unit', 'd5', 'sect', 's_location', 's_rank', 'tot', 'req', 'san',
                                         'sns_comment', 'retr0').filter(unit=u_id, d5=d5).order_by('s_rank')
    # print(result)
    response = json.dumps(list(result), cls=DjangoJSONEncoder)
    return HttpResponse(response, content_type='application/json')


def set_req_unit_sect(request):
    if not EDIT_ENABLED:
        print("Cannot edit; edit feature locked")
        msg = {'success': False, "msg": "Cannot edit; edit feature locked"}
        return HttpResponse(json.dumps(msg, cls=DjangoJSONEncoder), content_type='application/json')
    u_id = request.POST['unit']
    sect = request.POST['sect']
    d5 = request.POST['d5']
    req = request.POST['req']
    san = request.POST['san']
    comment = request.POST['sns_comment']
    obj = SanctionSection(sns_id=u_id + '_' + sect + '_' + d5, sns_sect_id=sect, sns_unit_id=u_id, sns_d5=d5,
                          sns_req=req, sns_san=san, sns_comment=comment )
    obj.save()
    # print(u_id, d5)
    result = {'success': True}
    # print(result)
    response = json.dumps(list(result), cls=DjangoJSONEncoder)
    return HttpResponse(response, content_type='application/json')


# check_user_permission(self.kwargs['pk'],request.user.username)
def check_user_permission(eis, username):
    # emp_obj = Employee.objects.get(pk=eis)
    # if emp_obj.e_unit_roll.u_code[1:3] !=username[0:2] and emp_obj.e_unit_roll.u_code[1:3]!='99' and username not in ['iedstaff','iedhq']:
    #     # return HttpResponseForbidden(u"You dont have permission to edit other Area records.")
    #     return True
    # else:
    #     return False
    return True


def index_403(request):
    return render(request, '403.html')


class DesgAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Desg.objects.none()

        qs = Desg.objects.order_by('d_discp', 'd_gdesig', 'd_rank').all()

        if self.q:
            qs = qs.filter(d_code__icontains=self.q)

        return qs


class UnitAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Unit.objects.none()

        qs = Unit.objects.filter(u_status__isnull=True).order_by('u_area', 'u_type', 'u_name').all()

        if self.q:
            qs = qs.filter(u_code__icontains=self.q)

        return qs

# class SectAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         # Don't forget to filter out results depending on the visitor !
#         if not self.request.user.is_authenticated():
#             return Section.objects.none()
#
#         qs = Section.objects.filter(u_status__isnull=True).order_by('s_rank').all()
#
#         if self.q:
#             qs = qs.filter(s_code__icontains=self.q)
#
#         return qs
