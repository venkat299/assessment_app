# Create your views here.

# def index(request):
#     employee_list = Employee.objects.order_by('-e_dob')[:5]
#     context = {'employee_list': employee_list}
#     return render(request, 'assessment/index.html', context)

import datetime

from braces.views import GroupRequiredMixin
from django.db.models import Case, When, IntegerField
from django.db.models import Count
from django.db.models.functions import Upper, Substr
from django.shortcuts import render
from django_tables2 import RequestConfig, SingleTableView
from django_tables2.export import ExportMixin

from assessment.forms.employee import EmployeeFormHelper
from assessment.models import Employee
from assessment.tables.employee import EmpSummAreaTable, EmpSummUnitTable, \
    EmpSummDesgTable, EmployeeTable, EmployeeFilter
from assessment.tables.employee import EmpSummDesgAreaTable


# EmpAddRedTable, EmpSummDesgAreaTable

class PagedFilteredTableView(ExportMixin, SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'
    exclude_column = ('x_edit', 'x_transfer', 'x_promote', 'x_terminate')

    def get_queryset(self, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        # context['total_rows'] = 33
        # print(context['total_rows'])
        return context


class EmployeeListView(GroupRequiredMixin, PagedFilteredTableView):
    model = Employee
    template_name = 'employee_new.html'
    context_object_name = 'customer'
    ordering = ['e_name']
    group_required = u'ied_execs'
    table_class = EmployeeTable
    filter_class = EmployeeFilter
    formhelper_class = EmployeeFormHelper

    def get_queryset(self):
        qs = super(EmployeeListView, self).get_queryset()
        # try:
        #   print(qs.query)
        # except Exception as e:
        #   print(e)

        return qs

    def post(self, request, *args, **kwargs):
        return PagedFilteredTableView.as_view()(request)

    def get_context_data(self, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        context['nav_customer'] = True
        search_query = self.get_queryset()
        # print(search_query.query)
        table = EmployeeTable(search_query)
        RequestConfig(self.request, paginate={'per_page': 20}).configure(table)
        context['table'] = table
        context['total_rows'] = search_query.count()
        print(context['total_rows'])
        return context


T1 = Count(Case(When(e_desg__d_code__startswith='T1', then=1), output_field=IntegerField))
TA = Count(Case(When(e_desg__d_code__startswith='TA', then=1), output_field=IntegerField))
TB = Count(Case(When(e_desg__d_code__startswith='TB', then=1), output_field=IntegerField))
TC = Count(Case(When(e_desg__d_code__startswith='TC', then=1), output_field=IntegerField))
TD = Count(Case(When(e_desg__d_code__startswith='TD', then=1), output_field=IntegerField))
TE = Count(Case(When(e_desg__d_code__startswith='TE', then=1), output_field=IntegerField))
TF = Count(Case(When(e_desg__d_code__startswith='TF', then=1), output_field=IntegerField))
TG = Count(Case(When(e_desg__d_code__startswith='TG', then=1), output_field=IntegerField))
TH = Count(Case(When(e_desg__d_code__startswith='TH', then=1), output_field=IntegerField))
GS = Count(Case(When(e_desg__d_code__startswith='GS', then=1), output_field=IntegerField))
G1 = Count(Case(When(e_desg__d_code__startswith='G1', then=1), output_field=IntegerField))
G2 = Count(Case(When(e_desg__d_code__startswith='G2', then=1), output_field=IntegerField))
G3 = Count(Case(When(e_desg__d_code__startswith='G3', then=1), output_field=IntegerField))
XS = Count(Case(When(e_desg__d_code__startswith='XS', then=1), output_field=IntegerField))
XA = Count(Case(When(e_desg__d_code__startswith='XA', then=1), output_field=IntegerField))
XB = Count(Case(When(e_desg__d_code__startswith='XB', then=1), output_field=IntegerField))
XC = Count(Case(When(e_desg__d_code__startswith='XC', then=1), output_field=IntegerField))
XD = Count(Case(When(e_desg__d_code__startswith='XD', then=1), output_field=IntegerField))
XE = Count(Case(When(e_desg__d_code__startswith='XE', then=1), output_field=IntegerField))
C6 = Count(Case(When(e_desg__d_code__startswith='C6', then=1), output_field=IntegerField))
C5 = Count(Case(When(e_desg__d_code__startswith='C5', then=1), output_field=IntegerField))
C4 = Count(Case(When(e_desg__d_code__startswith='C4', then=1), output_field=IntegerField))
C3 = Count(Case(When(e_desg__d_code__startswith='C3', then=1), output_field=IntegerField))
C2 = Count(Case(When(e_desg__d_code__startswith='C2', then=1), output_field=IntegerField))
C1 = Count(Case(When(e_desg__d_code__startswith='C1', then=1), output_field=IntegerField))
PR = Count(Case(When(e_desg__d_code__startswith='PR', then=1), output_field=IntegerField))
ZZ = Count(Case(When(e_desg__d_code__startswith='ZZ', then=1), output_field=IntegerField))


# @user_passes_test(in_apm_group)
def emp_area_summ(request):
    # 'e_unit_roll__u_area__a_code', 'e_unit_roll__u_area__a_name'
    qs = Employee.objects.values('e_unit_roll__u_area__a_code').order_by(
        'e_unit_roll__u_area__a_order').annotate(tot=Count('e_unit_roll'),
                                                 area_id=Upper('e_unit_roll__u_area__a_id'),
                                                 area_name=Substr('e_unit_roll__u_area__a_name', 1, 20),
                                                 male=Count(Case(
                                                     When(e_gender__iexact='Male', then=1),
                                                     output_field=IntegerField)),
                                                 female=Count(Case(
                                                     When(e_gender__iexact='Female',
                                                          then=1),
                                                     output_field=IntegerField)),
                                                 T1=T1, TA=TA, TB=TB, TC=TC, TD=TD, TE=TE,
                                                 TF=TF, TG=TG, TH=TH, GS=GS, G1=G1, G2=G2,
                                                 G3=G3, XS=XS, XA=XA, XB=XB, XC=XC, XD=XD,
                                                 XE=XE, C6=C6, C5=C5, C4=C4, C3=C3, C2=C2,
                                                 C1=C1, PR=PR, ZZ=ZZ,
                                                 )
    # # print(qs.query)
    table = EmpSummAreaTable(qs)
    # context = {'area_summary':  json.dumps(list(qs), cls=DjangoJSONEncoder)}
    # # print(unit_ls)
    # return render_to_response('emp_summ.html', context)
    return render(request, 'emp_summ_new.html', {
        'table': table
    })


# views.py
def emp_unit_summ(request, a_id):
    qs = Employee.objects.values('e_unit_roll', 'e_unit_roll__u_name').filter(e_unit_roll__u_area__a_id=a_id).annotate(
        u_id=Upper('e_unit_roll__u_id'),
        u_name=Upper('e_unit_roll__u_name'),
        tot=Count('e_unit_roll'),
        male=Count(Case(When(e_gender__iexact='Male', then=1), output_field=IntegerField)),
        female=Count(Case(When(e_gender__iexact='Female', then=1), output_field=IntegerField)),
        T1=T1, TA=TA, TB=TB, TC=TC, TD=TD, TE=TE, TF=TF, TG=TG, TH=TH, GS=GS, G1=G1, G2=G2, G3=G3, XS=XS, XA=XA, XB=XB,
        XC=XC, XD=XD, XE=XE, C6=C6, C5=C5, C4=C4, C3=C3, C2=C2, C1=C1, PR=PR, ZZ=ZZ,
    )
    # print(qs.query)
    table = EmpSummUnitTable(qs)

    return render(request, 'emp_summ_new.html', {
        'table': table
    })


def emp_desg_unit_summ(request, unit_code):
    qs = Employee.objects.values('e_unit_roll', 'e_desg__d_gdesig').filter(e_unit_roll__u_id=unit_code).annotate(
        d5_code=Substr('e_desg__d_code', 3, 5),
        gdesig=Substr('e_desg__d_gdesig', 1, 20),
        # unit = '',(
        tot=Count('e_unit_roll'),
        male=Count(Case(When(e_gender__iexact='Male', then=1), output_field=IntegerField)),
        female=Count(Case(When(e_gender__iexact='Female', then=1), output_field=IntegerField)),
        T1=T1, TA=TA, TB=TB, TC=TC, TD=TD, TE=TE, TF=TF, TG=TG, TH=TH, GS=GS, G1=G1, G2=G2, G3=G3, XS=XS, XA=XA, XB=XB,
        XC=XC, XD=XD, XE=XE, C6=C6, C5=C5, C4=C4, C3=C3, C2=C2, C1=C1, PR=PR, ZZ=ZZ,
    ).order_by(
        'd5_code')
    # print(qs.query)
    table = EmpSummDesgTable(qs)

    return render(request, 'emp_summ_new.html', {
        'table': table
    })


def emp_desg_area_summ(request, area_code):
    qs = Employee.objects.values('e_desg__d_gcode', 'e_unit_roll__u_area__a_code', 'e_desg__d_gdesig').filter(
        e_unit_roll__u_area__a_code=area_code, e_status='In_service').annotate(
        # d2_code = Substr('e_desg__d_code',3,2),
        # unit = '',
        tot=Count('e_unit_roll'),
        male=Count(Case(When(e_gender__iexact='Male', then=1), output_field=IntegerField)),
        female=Count(Case(When(e_gender__iexact='Female', then=1), output_field=IntegerField)),
        T1=T1, TA=TA, TB=TB, TC=TC, TD=TD, TE=TE, TF=TF, TG=TG, TH=TH, GS=GS, G1=G1, G2=G2, G3=G3, XS=XS, XA=XA, XB=XB,
        XC=XC, XD=XD, XE=XE, C6=C6, C5=C5, C4=C4, C3=C3, C2=C2, C1=C1, PR=PR, ZZ=ZZ,
    )
    # print(qs.query)
    table = EmpSummDesgAreaTable(qs)

    return render(request, 'emp_summ.html', {
        'table': table
    })


def emp_desg_summ(request):
    qs = Employee.objects.values('e_unit_roll', 'e_desg__d_gdesig').filter(e_status='In_service').order_by(
        'e_desg__d_gcode').annotate(
        d5_code=Substr('e_desg__d_code', 3, 5),
        # unit = '',
        tot=Count('e_unit_roll'),
        male=Count(Case(When(e_gender__iexact='Male', then=1), output_field=IntegerField)),
        female=Count(Case(When(e_gender__iexact='Female', then=1), output_field=IntegerField)),
        T1=T1, TA=TA, TB=TB, TC=TC, TD=TD, TE=TE, TF=TF, TG=TG, TH=TH, GS=GS, G1=G1, G2=G2, G3=G3, XS=XS, XA=XA, XB=XB,
        XC=XC, XD=XD, XE=XE, C6=C6, C5=C5, C4=C4, C3=C3, C2=C2, C1=C1, PR=PR, ZZ=ZZ,
    )
    # print(qs.query)
    table = EmpSummDesgTable(qs)

    return render(request, 'emp_summ.html', {
        'table': table
    })


present = datetime.date.today()
fiscal_yr = present.year
if present.month < 4:
    fiscal_yr = present.year - 1
fiscal_st = datetime.date(fiscal_yr, 4, 1)
fiscal_end = datetime.date(fiscal_yr + 1, 3, 30)
prev_fiscal_st = datetime.date(fiscal_yr - 1, 4, 1)
prev_fiscal_end = datetime.date(fiscal_yr, 3, 30)
