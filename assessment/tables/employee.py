# tutorial/tables.py
import django_filters
import django_tables2 as tables
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django_filters import FilterSet, DateFromToRangeFilter
from django_tables2.utils import A

from assessment.models import Employee


class EmployeeFilter(FilterSet):
    # author = ModelChoiceFilter(queryset=Author.objects.all())
    # e_desg__d_name = django_filters.CharFilter(lookup_expr='icontains')
    e_doj = DateFromToRangeFilter()
    e_dob = DateFromToRangeFilter()
    e_dot = DateFromToRangeFilter()

    class Meta:
        model = Employee
        fields = ['e_gender', 'e_desg__d_discp', 'e_desg__d_id', 'e_dob',
                  'e_unit_roll__u_id', 'e_unit_work__u_id', 'e_regsno', 'e_doj',
                  'e_eis', 'e_name', 'e_status',
                  'e_dot']  # 'e_desg.d_grade','e_unit.u_areacode','e_unit.u_name','e_join','e_termi',
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }

    # @classmethod
    # def filter_for_lookup(cls, f, lookup_type):
    #     # override date range lookups
    #     if isinstance(f, models.DateField) and lookup_type == 'range':
    #         return django_filters.DateRangeFilter, {}

    #     # use default behavior otherwise
    #     return super(EmployeeFilter, cls).filter_for_lookup(f, lookup_type)


# import itertools
# class CounterColumn(tables.Column):
#     def __init__(self, *args, **kwargs):
#         self.counter = itertools.count()
#         kwargs.update({
#             'empty_values': (),
#             'orderable': False
#         })
#         super(CounterColumn, self).__init__(*args, **kwargs)
#     def render(self):
#         return next(self.counter)

class EmployeeTable(tables.Table):
    # a': {'style': 'color: red;', 'next':'{% request.path %}'}
    eis = tables.Column(
        verbose_name='Employe_No', accessor='e_eis')
    # delete_link = tables.LinkColumn('bug_delete', args=[A('pk')],
    #             verbose_name='Delete',accessor='pk', attrs={'class':'delete_link'})
    x_edit = tables.Column(accessor='e_eis', verbose_name='Edit', exclude_from_export=True)
    # x_transfer = tables.Column(accessor='e_eis', verbose_name='l2', exclude_from_export=True)
    # x_promote = tables.Column(accessor='e_eis', verbose_name='l3', exclude_from_export=True)
    # x_terminate = tables.Column(accessor='e_eis', verbose_name='Delete', exclude_from_export=True)
    x_terminate = tables.Column(accessor='e_eis', verbose_name='Delete', exclude_from_export=True)
    # eis_x = tables.Column(accessor='e_eis', verbose_name='Links_for_edit',)
    # regsno = tables.Column(accessor='e_regsno')
    name = tables.Column(accessor='e_name')
    dob = tables.DateColumn(accessor='e_dob', short=True, verbose_name='Retirement Date')
    gender = tables.Column(accessor='e_gender')
    dscd = tables.Column(accessor='e_desg.d_code', verbose_name='Desg Code')
    gdesig = tables.Column(accessor='e_desg.d_gdesig', verbose_name='Grp Desig')
    # desg1 = tables.LinkColumn('e_desg.d_name', args=[A('e_desg.d_name')])
    desg = tables.Column(accessor='e_desg.d_name', verbose_name='Grade Desig')
    grade = tables.Column(accessor='e_desg.d_grade', verbose_name='Grade/ Category')
    # cadre = tables.Column(accessor='e_unit_roll.u_name')
    discp = tables.Column(accessor='e_desg.d_discp', verbose_name='Discipline')
    unit_roll_code = tables.Column(accessor='e_unit_roll.u_code', verbose_name='On-Roll Unit Code')
    unit_roll = tables.Column(accessor='e_unit_roll.u_name', verbose_name='On-Roll Unit Name')
    unit_work = tables.Column(accessor='e_unit_work.u_name', verbose_name='Working Unit Name')

    # doj = tables.DateColumn(accessor='e_doj', verbose_name='Join Date')
    # join_type = tables.Column(accessor='e_join', verbose_name='Join. Type')
    # dot = tables.DateColumn(accessor='e_dot',verbose_name='Termination Date')
    # termination = tables.Column(accessor='e_termi', verbose_name='Termi. Type')
    # dop = tables.DateColumn(accessor='e_dop')
    # status = tables.Column(accessor='e_status')

    class Meta:
        model = Employee
        attrs = {"class": "rwd-table"}
        fields = ('x_edit', 'x_terminate', 'eis', 'name', 'dob', 'gender', 'dscd', 'gdesig', 'desg', 'grade', 'discp',
                  'unit_roll_code', 'unit_roll', 'unit_work', 'dop')
        sequence = ('x_edit', 'x_terminate', 'eis', 'name', 'dob', 'gender', 'dscd', 'gdesig', 'desg', 'grade', 'discp',
                    'unit_roll_code', 'unit_roll', 'unit_work', 'dop')

        # attrs = {"class": "table-striped table-bordered"}
        empty_text = "There are no employees matching the search criteria..."
        # add class="paleblue" to <table> tag

    # def render_eis(self,record):
    #     url = reverse('emp_detail',kwargs={'pk':record.e_eis})
    #     return format_html('''
    #         <a title="Employee Detail" next:"./", class=" convert_link linkcolumn" href="{}">{}</a>
    #         ''', url,record.e_eis)
    #
    def render_x_edit(self, record):
        url = reverse('emp_update', kwargs={'pk': record.e_id})
        return format_html('''
            <a title="Edit Employee" target="_blank"  next:"./", class="convert_link edit_icon_16" href="{}"></a>
            ''', url)

    def render_x_terminate(self, record):
        url = reverse('emp_terminate', kwargs={'pk': record.e_id})
        return format_html('''
            <a title="Terminate Employee" next:"./", class="convert_link terminate_icon_16" href="{}"></a>
            ''', url)

    # def render_x_transfer(self,record):
    #     url = reverse('emp_transfer',kwargs={'pk':record.e_eis})
    #     return format_html('''
    #         <a title="Transfer Employee" next:"./", class="convert_link transfer_icon_16" href="{}"></a>
    #         ''', url)
    # def render_x_promote(self,record):
    #     url = reverse('emp_promote',kwargs={'pk':record.e_eis})
    #     return format_html('''
    #         <a title="Promote Employee" next:"./", class="convert_link promote_icon_16" href="{}"></a>
    #         ''', url)
    # def render_x_terminate(self,record):
    #     url = reverse('emp_terminate',kwargs={'pk':record.e_eis})
    #     return format_html('''
    #         <a title="Terminate Employee" next:"./", class="convert_link terminate_icon_16" href="{}"></a>
    #         ''', url)
    def value_eis(self, record):
        return record.e_eis

    def value_name(self, record):
        return record.e_name

    # def render_eis_x(self, record):
    #     url = reverse('emp_update')
    #     return format_html('''
    #         <div class"edit_link">
    #         <a title="Edit Employee" next:"./", class="convert_link iconFriends edit_icon_16" href="{}{}"></a>
    #         <span class"link_col_summ">|</span>
    #         <a title="Terminate" next:"./", class="convert_link iconFriends terminate_icon_16"></a>
    #         <span class"link_col_summ">|</span>
    #         <a title="Tranfer to other Unit/Area" next:"./", class="convert_link iconFriends transfer_icon_16"></a>
    #         <span class"link_col_summ">|</span>
    #         <a title="Promote" next:"./", class="convert_link iconFriends promote_icon_16"></a>
    #         </div>''', url, record.e_eis,  record.e_eis)


def suma_footer(table):
    try:
        s = sum(x['tot'] for x in table.data)
        print('total:', s)
    except Exception(e):
        print(str(e))
        raise
    return s


class EmpSummAreaTable(tables.Table):
    # ln_unit = tables.LinkColumn('emp_unit_summ', kwargs={'area_code':A('e_unit_roll__u_area__a_code')},
    #             verbose_name='area code', accessor='e_unit_roll__u_area__a_name',footer='Total:', attrs={'class':'edit_link', 'a': {'next':'./', 'class':'convert_link'}})

    # ln_add = tables.LinkColumn('emp_unit_addi_redu', kwargs={'code':A('d2_code')},
    #             verbose_name='link: add/ red', accessor='e_unit_roll__u_area__a_code', attrs={'class':'convert_link edit_icon_16', 'a': {'next':'./', 'class':'convert_link'}})
    # ln_desg = tables.LinkColumn('emp_desg_area_summ', kwargs={'area_code':A('e_unit_roll__u_area__a_code')},
    #             verbose_name='link: desg summ', accessor='e_unit_roll__u_area__a_code', attrs={'class':'edit_link', 'a': {'next':'./', 'class':'convert_link'}})
    # area_code = tables.LinkColumn('emp_unit_summ', kwargs={'area_code':A('e_unit_roll__u_area__a_code')},
    #             verbose_name='link: unit summ', accessor='d2_code',footer='Total:', attrs={'class':'edit_link', 'a': {'next':'./', 'class':'convert_link'}})
    area_id = tables.Column(accessor='area_id', visible=False)
    area_name = tables.Column(accessor='area_name', footer='Total:')
    total = tables.Column(accessor='tot', footer=suma_footer)
    male = tables.Column(accessor='male', footer=lambda table: sum(x['male'] for x in table.data))
    female = tables.Column(accessor='female', footer=lambda table: sum(x['female'] for x in table.data))

    C6 = tables.Column(accessor='C6', footer=lambda table: sum(x['C6'] for x in table.data), empty_values=(0,))
    C5 = tables.Column(accessor='C5', footer=lambda table: sum(x['C5'] for x in table.data), empty_values=(0,))
    C4 = tables.Column(accessor='C4', footer=lambda table: sum(x['C4'] for x in table.data), empty_values=(0,))
    C3 = tables.Column(accessor='C3', footer=lambda table: sum(x['C3'] for x in table.data), empty_values=(0,))
    C2 = tables.Column(accessor='C2', footer=lambda table: sum(x['C2'] for x in table.data), empty_values=(0,))
    C1 = tables.Column(accessor='C1', footer=lambda table: sum(x['C1'] for x in table.data), empty_values=(0,))

    T1 = tables.Column(accessor='T1', footer=lambda table: sum(x['T1'] for x in table.data), empty_values=(0,))
    TA = tables.Column(accessor='TA', footer=lambda table: sum(x['TA'] for x in table.data), empty_values=(0,))
    TB = tables.Column(accessor='TB', footer=lambda table: sum(x['TB'] for x in table.data), empty_values=(0,))
    TC = tables.Column(accessor='TC', footer=lambda table: sum(x['TC'] for x in table.data), empty_values=(0,))
    TD = tables.Column(accessor='TD', footer=lambda table: sum(x['TD'] for x in table.data), empty_values=(0,))
    TE = tables.Column(accessor='TE', footer=lambda table: sum(x['TE'] for x in table.data), empty_values=(0,))
    TF = tables.Column(accessor='TF', footer=lambda table: sum(x['TF'] for x in table.data), empty_values=(0,))
    TG = tables.Column(accessor='TG', footer=lambda table: sum(x['TG'] for x in table.data), empty_values=(0,))
    TH = tables.Column(accessor='TH', footer=lambda table: sum(x['TH'] for x in table.data), empty_values=(0,))
    GS = tables.Column(accessor='GS', footer=lambda table: sum(x['GS'] for x in table.data), empty_values=(0,))
    G1 = tables.Column(accessor='G1', footer=lambda table: sum(x['G1'] for x in table.data), empty_values=(0,))
    G2 = tables.Column(accessor='G2', footer=lambda table: sum(x['G2'] for x in table.data), empty_values=(0,))
    G3 = tables.Column(accessor='G3', footer=lambda table: sum(x['G3'] for x in table.data), empty_values=(0,))
    XS = tables.Column(accessor='XS', footer=lambda table: sum(x['XS'] for x in table.data), empty_values=(0,))
    XA = tables.Column(accessor='XA', footer=lambda table: sum(x['XA'] for x in table.data), empty_values=(0,))
    XB = tables.Column(accessor='XB', footer=lambda table: sum(x['XB'] for x in table.data), empty_values=(0,))
    XC = tables.Column(accessor='XC', footer=lambda table: sum(x['XC'] for x in table.data), empty_values=(0,))
    XD = tables.Column(accessor='XD', footer=lambda table: sum(x['XD'] for x in table.data), empty_values=(0,))
    XE = tables.Column(accessor='XE', footer=lambda table: sum(x['XE'] for x in table.data), empty_values=(0,))
    PR = tables.Column(accessor='PR', footer=lambda table: sum(x['PR'] for x in table.data), empty_values=(0,))
    ZZ = tables.Column(accessor='ZZ', footer=lambda table: sum(x['ZZ'] for x in table.data), empty_values=(0,))

    # suma = tables.Column(footer=suma_footer)

    def render_area_name(self, record, ):
        # print(record)
        url = reverse('emp_unit_summ', kwargs={'a_id': record['area_id']})
        return format_html('''<a class="link_col_summ" 
                    href="{}">{}</a>''',
                           url, record['area_name'])

    class Meta:
        attrs = {"class": "fixed_headers rwd-table", id: "my_table"}


class EmpSummUnitTable(tables.Table):
    # ln_add = tables.LinkColumn('emp_unit_addi_redu', kwargs={'code':A('e_unit_roll')},
    #             verbose_name='link: add/ red', accessor='e_unit_roll', attrs={'class':'convert_link edit_icon_16', 'a': {'next':'./', 'class':'convert_link'}})
    # ln_desg = tables.LinkColumn('emp_desg_unit_summ', kwargs={'unit_code':A('e_unit_roll')},
    #             verbose_name='link: desg summ', accessor='e_unit_roll', attrs={'class':'edit_link', 'a': {'next':'./', 'class':'convert_link'}})

    # unit_name = tables.LinkColumn('empl_list', kwargs={'e_unit_roll__u_code':A('e_unit_roll'),'_export':'csv'},
    # verbose_name='link: download', accessor='e_unit_roll__u_name', attrs={'class':'edit_link', 'a': {'next':'./', 'class':'convert_link'}})
    unit_name = tables.Column(verbose_name='Unit', accessor='u_name', footer='Total:')
    unit_id = tables.Column(accessor='u_id', visible=False)
    total = tables.Column(accessor='tot', footer=suma_footer)
    male = tables.Column(accessor='male', footer=lambda table: sum(x['male'] for x in table.data))
    female = tables.Column(accessor='female', footer=lambda table: sum(x['female'] for x in table.data))
    C6 = tables.Column(accessor='C6', footer=lambda table: sum(x['C6'] for x in table.data), empty_values=(0,))
    C5 = tables.Column(accessor='C5', footer=lambda table: sum(x['C5'] for x in table.data), empty_values=(0,))
    C4 = tables.Column(accessor='C4', footer=lambda table: sum(x['C4'] for x in table.data), empty_values=(0,))
    C3 = tables.Column(accessor='C3', footer=lambda table: sum(x['C3'] for x in table.data), empty_values=(0,))
    C2 = tables.Column(accessor='C2', footer=lambda table: sum(x['C2'] for x in table.data), empty_values=(0,))
    C1 = tables.Column(accessor='C1', footer=lambda table: sum(x['C1'] for x in table.data), empty_values=(0,))

    T1 = tables.Column(accessor='T1', footer=lambda table: sum(x['T1'] for x in table.data), empty_values=(0,))
    TA = tables.Column(accessor='TA', footer=lambda table: sum(x['TA'] for x in table.data), empty_values=(0,))
    TB = tables.Column(accessor='TB', footer=lambda table: sum(x['TB'] for x in table.data), empty_values=(0,))
    TC = tables.Column(accessor='TC', footer=lambda table: sum(x['TC'] for x in table.data), empty_values=(0,))
    TD = tables.Column(accessor='TD', footer=lambda table: sum(x['TD'] for x in table.data), empty_values=(0,))
    TE = tables.Column(accessor='TE', footer=lambda table: sum(x['TE'] for x in table.data), empty_values=(0,))
    TF = tables.Column(accessor='TF', footer=lambda table: sum(x['TF'] for x in table.data), empty_values=(0,))
    TG = tables.Column(accessor='TG', footer=lambda table: sum(x['TG'] for x in table.data), empty_values=(0,))
    TH = tables.Column(accessor='TH', footer=lambda table: sum(x['TH'] for x in table.data), empty_values=(0,))
    GS = tables.Column(accessor='GS', footer=lambda table: sum(x['GS'] for x in table.data), empty_values=(0,))
    G1 = tables.Column(accessor='G1', footer=lambda table: sum(x['G1'] for x in table.data), empty_values=(0,))
    G2 = tables.Column(accessor='G2', footer=lambda table: sum(x['G2'] for x in table.data), empty_values=(0,))
    G3 = tables.Column(accessor='G3', footer=lambda table: sum(x['G3'] for x in table.data), empty_values=(0,))
    XS = tables.Column(accessor='XS', footer=lambda table: sum(x['XS'] for x in table.data), empty_values=(0,))
    XA = tables.Column(accessor='XA', footer=lambda table: sum(x['XA'] for x in table.data), empty_values=(0,))
    XB = tables.Column(accessor='XB', footer=lambda table: sum(x['XB'] for x in table.data), empty_values=(0,))
    XC = tables.Column(accessor='XC', footer=lambda table: sum(x['XC'] for x in table.data), empty_values=(0,))
    XD = tables.Column(accessor='XD', footer=lambda table: sum(x['XD'] for x in table.data), empty_values=(0,))
    XE = tables.Column(accessor='XE', footer=lambda table: sum(x['XE'] for x in table.data), empty_values=(0,))
    PR = tables.Column(accessor='PR', footer=lambda table: sum(x['PR'] for x in table.data), empty_values=(0,))
    ZZ = tables.Column(accessor='ZZ', footer=lambda table: sum(x['ZZ'] for x in table.data), empty_values=(0,))

    def return_url(self, record, column_id):
        url = reverse('empl_list')
        return format_html('''<a class="link_col_summ" 
            href="{}?e_unit_roll__u_id={}
            &e_desg__d_id={}">{}</a>''',
                           url, record['e_unit_roll'], column_id, record[column_id])

    def render_unit_name(self, record, ):
        # print(record)
        url = reverse('emp_desg_unit_summ', kwargs={'unit_code': record['u_id']})
        return format_html('''<a class="link_col_summ" 
                      href="{}">{}</a>''',
                           url, record['u_name'])

    # def render_unit_name(self, record):
    #     # print(record)
    #     url = reverse('empl_list')
    #     return format_html('<a class="download_link" href="{}?e_unit_roll__u_code={}&_export=csv">{}</a>', url, record['e_unit_roll'],record['e_unit_roll__u_name'])

    # def render_male(self, record):
    #     url = reverse('empl_list')
    #     return format_html('<a class="link_col_summ" href="{}?e_desg__d_id={}&e_unit_roll__u_code={}&e_gender=Male">{}</a>', url, record['d5_code'],record['e_unit_roll'],record['male'])

    def render_C6(self, record): return self.return_url(record, 'C6')

    def render_C5(self, record): return self.return_url(record, 'C5')

    def render_C4(self, record): return self.return_url(record, 'C4')

    def render_C3(self, record): return self.return_url(record, 'C3')

    def render_C2(self, record): return self.return_url(record, 'C2')

    def render_C1(self, record): return self.return_url(record, 'C1')

    def render_T1(self, record): return self.return_url(record, 'T1')

    def render_TA(self, record): return self.return_url(record, 'TA')

    def render_TB(self, record): return self.return_url(record, 'TB')

    def render_TC(self, record): return self.return_url(record, 'TC')

    def render_TD(self, record): return self.return_url(record, 'TD')

    def render_TE(self, record): return self.return_url(record, 'TE')

    def render_TF(self, record): return self.return_url(record, 'TF')

    def render_TG(self, record): return self.return_url(record, 'TG')

    def render_TH(self, record): return self.return_url(record, 'TH')

    def render_GS(self, record): return self.return_url(record, 'GS')

    def render_G1(self, record): return self.return_url(record, 'G1')

    def render_G2(self, record): return self.return_url(record, 'G2')

    def render_G3(self, record): return self.return_url(record, 'G3')

    def render_XS(self, record): return self.return_url(record, 'XS')

    def render_XA(self, record): return self.return_url(record, 'XA')

    def render_XB(self, record): return self.return_url(record, 'XB')

    def render_XC(self, record): return self.return_url(record, 'XC')

    def render_XD(self, record): return self.return_url(record, 'XD')

    def render_XE(self, record): return self.return_url(record, 'XE')

    def render_PR(self, record): return self.return_url(record, 'PR')

    def render_ZZ(self, record): return self.return_url(record, 'ZZ')

    # suma = tables.Column(footer=suma_footer)

    class Meta:
        attrs = {"class": "fixed_headers rwd-table", id: "my_table"}


# url_attrs={ 'a': {'next':'./' , 'class':'convert_link'}}
class EmpSummDesgTable(tables.Table):
    desg_code = tables.Column(
        verbose_name='desg code', accessor='d5_code')
    desg_name = tables.Column(accessor='gdesig', footer='Total:')
    # total = tables.LinkColumn('empl_list',kwargs={'e_desg__d_code':A('e_desg__d_code'),}, accessor='tot',footer=suma_footer ,empty_values=(0,),attrs={'class':'edit_link', 'a': {'next':'./', 'class':'convert_link'}})
    # total = tables.Column(accessor='tot',footer=suma_footer ,empty_values=(0,))
    total = tables.LinkColumn('empl_list', accessor='tot', footer=lambda table: sum(x['tot'] for x in table.data),
                              empty_values=(0,))
    male = tables.LinkColumn('empl_list', accessor='male', footer=lambda table: sum(x['male'] for x in table.data),
                             empty_values=(0,))
    female = tables.LinkColumn('empl_list', accessor='female',
                               footer=lambda table: sum(x['female'] for x in table.data), empty_values=(0,))

    C6 = tables.Column(accessor='C6', footer=lambda table: sum(x['C6'] for x in table.data), empty_values=(0,))
    C5 = tables.Column(accessor='C5', footer=lambda table: sum(x['C5'] for x in table.data), empty_values=(0,))
    C4 = tables.Column(accessor='C4', footer=lambda table: sum(x['C4'] for x in table.data), empty_values=(0,))
    C3 = tables.Column(accessor='C3', footer=lambda table: sum(x['C3'] for x in table.data), empty_values=(0,))
    C2 = tables.Column(accessor='C2', footer=lambda table: sum(x['C2'] for x in table.data), empty_values=(0,))
    C1 = tables.Column(accessor='C1', footer=lambda table: sum(x['C1'] for x in table.data), empty_values=(0,))

    T1 = tables.Column(accessor='T1', footer=lambda table: sum(x['T1'] for x in table.data), empty_values=(0,))
    TA = tables.Column(accessor='TA', footer=lambda table: sum(x['TA'] for x in table.data), empty_values=(0,))
    TB = tables.Column(accessor='TB', footer=lambda table: sum(x['TB'] for x in table.data), empty_values=(0,))
    TC = tables.Column(accessor='TC', footer=lambda table: sum(x['TC'] for x in table.data), empty_values=(0,))
    TD = tables.Column(accessor='TD', footer=lambda table: sum(x['TD'] for x in table.data), empty_values=(0,))
    TE = tables.Column(accessor='TE', footer=lambda table: sum(x['TE'] for x in table.data), empty_values=(0,))
    TF = tables.Column(accessor='TF', footer=lambda table: sum(x['TF'] for x in table.data), empty_values=(0,))
    TG = tables.Column(accessor='TG', footer=lambda table: sum(x['TG'] for x in table.data), empty_values=(0,))
    TH = tables.Column(accessor='TH', footer=lambda table: sum(x['TH'] for x in table.data), empty_values=(0,))
    GS = tables.Column(accessor='GS', footer=lambda table: sum(x['GS'] for x in table.data), empty_values=(0,))
    G1 = tables.Column(accessor='G1', footer=lambda table: sum(x['G1'] for x in table.data), empty_values=(0,))
    G2 = tables.Column(accessor='G2', footer=lambda table: sum(x['G2'] for x in table.data), empty_values=(0,))
    G3 = tables.Column(accessor='G3', footer=lambda table: sum(x['G3'] for x in table.data), empty_values=(0,))
    XS = tables.Column(accessor='XS', footer=lambda table: sum(x['XS'] for x in table.data), empty_values=(0,))
    XA = tables.Column(accessor='XA', footer=lambda table: sum(x['XA'] for x in table.data), empty_values=(0,))
    XB = tables.Column(accessor='XB', footer=lambda table: sum(x['XB'] for x in table.data), empty_values=(0,))
    XC = tables.Column(accessor='XC', footer=lambda table: sum(x['XC'] for x in table.data), empty_values=(0,))
    XD = tables.Column(accessor='XD', footer=lambda table: sum(x['XD'] for x in table.data), empty_values=(0,))
    XE = tables.Column(accessor='XE', footer=lambda table: sum(x['XE'] for x in table.data), empty_values=(0,))
    PR = tables.Column(accessor='PR', footer=lambda table: sum(x['PR'] for x in table.data), empty_values=(0,))
    ZZ = tables.Column(accessor='ZZ', footer=lambda table: sum(x['ZZ'] for x in table.data), empty_values=(0,))

    # suma = tables.Column(footer=suma_footer)

    def return_url(self, record, column_id):
        url = reverse('empl_list')
        return format_html('''<a class="link_col_summ" 
            href="{}?e_unit_roll__u_id={}
            &e_desg__d_id={}{}">{}</a>''',
                           url, record['e_unit_roll'], column_id, record['d5_code'], record[column_id])

    # def render_desg_code(self, record):
    #     # print(record)
    #     url = reverse('empl_list')
    #     return format_html('<a href="{}?e_desg__d_id={}&e_unit_roll__u_code={}">{}</a>', url, record['d5_code'],record['e_unit_roll'],record['d5_code'])
    def render_total(self, record):
        url = reverse('empl_list')
        return format_html('<a  class="link_col_summ" href="{}?e_desg__d_id={}&e_unit_roll__u_id={}">{}</a>', url,
                           record['d5_code'], record['e_unit_roll'], record['tot'])

    def render_male(self, record):
        url = reverse('empl_list')
        return format_html(
            '<a class="link_col_summ" href="{}?e_desg__d_id={}&e_unit_roll__u_id={}&e_gender=Male">{}</a>', url,
            record['d5_code'], record['e_unit_roll'], record['male'])

    def render_female(self, record):
        url = reverse('empl_list')
        return format_html(
            '<a class="link_col_summ" href="{}?e_desg__d_id={}&e_unit_roll__u_id={}&e_gender=Female">{}</a>', url,
            record['d5_code'], record['e_unit_roll'], record['female'])

    def render_C6(self, record): return self.return_url(record, 'C6')

    def render_C5(self, record): return self.return_url(record, 'C5')

    def render_C4(self, record): return self.return_url(record, 'C4')

    def render_C3(self, record): return self.return_url(record, 'C3')

    def render_C2(self, record): return self.return_url(record, 'C2')

    def render_C1(self, record): return self.return_url(record, 'C1')

    def render_T1(self, record): return self.return_url(record, 'T1')

    def render_TA(self, record): return self.return_url(record, 'TA')

    def render_TB(self, record): return self.return_url(record, 'TB')

    def render_TC(self, record): return self.return_url(record, 'TC')

    def render_TD(self, record): return self.return_url(record, 'TD')

    def render_TE(self, record): return self.return_url(record, 'TE')

    def render_TF(self, record): return self.return_url(record, 'TF')

    def render_TG(self, record): return self.return_url(record, 'TG')

    def render_TH(self, record): return self.return_url(record, 'TH')

    def render_GS(self, record): return self.return_url(record, 'GS')

    def render_G1(self, record): return self.return_url(record, 'G1')

    def render_G2(self, record): return self.return_url(record, 'G2')

    def render_G3(self, record): return self.return_url(record, 'G3')

    def render_XS(self, record): return self.return_url(record, 'XS')

    def render_XA(self, record): return self.return_url(record, 'XA')

    def render_XB(self, record): return self.return_url(record, 'XB')

    def render_XC(self, record): return self.return_url(record, 'XC')

    def render_XD(self, record): return self.return_url(record, 'XD')

    def render_XE(self, record): return self.return_url(record, 'XE')

    def render_PR(self, record): return self.return_url(record, 'PR')

    def render_ZZ(self, record): return self.return_url(record, 'ZZ')

    class Meta:
        attrs = {"class": "fixed_headers rwd-table"}


# url_attrs={ 'a': {'next':'./' , 'class':'convert_link'}}
class EmpSummDesgAreaTable(tables.Table):
    desg_code = tables.Column(
        verbose_name='link: download', accessor='e_desg__d_gcode')
    desg_name = tables.Column(accessor='e_desg__d_gdesig', footer='Total:')
    total = tables.LinkColumn('empl_list', kwargs={'e_desg__d_code': A('e_desg__d_code'), }, accessor='tot',
                              footer=suma_footer, empty_values=(0,),
                              attrs={'class': 'edit_link', 'a': {'next': './', 'class': 'convert_link'}})
    # total = tables.Column(accessor='tot',footer=suma_footer ,empty_values=(0,))
    total = tables.LinkColumn('empl_list', accessor='tot', footer=lambda table: sum(x['tot'] for x in table.data),
                              empty_values=(0,))
    male = tables.LinkColumn('empl_list', accessor='male', footer=lambda table: sum(x['male'] for x in table.data),
                             empty_values=(0,))
    female = tables.LinkColumn('empl_list', accessor='female',
                               footer=lambda table: sum(x['female'] for x in table.data), empty_values=(0,))

    C6 = tables.Column(accessor='C6', footer=lambda table: sum(x['C6'] for x in table.data), empty_values=(0,))
    C5 = tables.Column(accessor='C5', footer=lambda table: sum(x['C5'] for x in table.data), empty_values=(0,))
    C4 = tables.Column(accessor='C4', footer=lambda table: sum(x['C4'] for x in table.data), empty_values=(0,))
    C3 = tables.Column(accessor='C3', footer=lambda table: sum(x['C3'] for x in table.data), empty_values=(0,))
    C2 = tables.Column(accessor='C2', footer=lambda table: sum(x['C2'] for x in table.data), empty_values=(0,))
    C1 = tables.Column(accessor='C1', footer=lambda table: sum(x['C1'] for x in table.data), empty_values=(0,))

    T1 = tables.Column(accessor='T1', footer=lambda table: sum(x['T1'] for x in table.data), empty_values=(0,))
    TA = tables.Column(accessor='TA', footer=lambda table: sum(x['TA'] for x in table.data), empty_values=(0,))
    TB = tables.Column(accessor='TB', footer=lambda table: sum(x['TB'] for x in table.data), empty_values=(0,))
    TC = tables.Column(accessor='TC', footer=lambda table: sum(x['TC'] for x in table.data), empty_values=(0,))
    TD = tables.Column(accessor='TD', footer=lambda table: sum(x['TD'] for x in table.data), empty_values=(0,))
    TE = tables.Column(accessor='TE', footer=lambda table: sum(x['TE'] for x in table.data), empty_values=(0,))
    TF = tables.Column(accessor='TF', footer=lambda table: sum(x['TF'] for x in table.data), empty_values=(0,))
    TG = tables.Column(accessor='TG', footer=lambda table: sum(x['TG'] for x in table.data), empty_values=(0,))
    TH = tables.Column(accessor='TH', footer=lambda table: sum(x['TH'] for x in table.data), empty_values=(0,))
    GS = tables.Column(accessor='GS', footer=lambda table: sum(x['GS'] for x in table.data), empty_values=(0,))
    G1 = tables.Column(accessor='G1', footer=lambda table: sum(x['G1'] for x in table.data), empty_values=(0,))
    G2 = tables.Column(accessor='G2', footer=lambda table: sum(x['G2'] for x in table.data), empty_values=(0,))
    G3 = tables.Column(accessor='G3', footer=lambda table: sum(x['G3'] for x in table.data), empty_values=(0,))
    XS = tables.Column(accessor='XS', footer=lambda table: sum(x['XS'] for x in table.data), empty_values=(0,))
    XA = tables.Column(accessor='XA', footer=lambda table: sum(x['XA'] for x in table.data), empty_values=(0,))
    XB = tables.Column(accessor='XB', footer=lambda table: sum(x['XB'] for x in table.data), empty_values=(0,))
    XC = tables.Column(accessor='XC', footer=lambda table: sum(x['XC'] for x in table.data), empty_values=(0,))
    XD = tables.Column(accessor='XD', footer=lambda table: sum(x['XD'] for x in table.data), empty_values=(0,))
    XE = tables.Column(accessor='XE', footer=lambda table: sum(x['XE'] for x in table.data), empty_values=(0,))
    PR = tables.Column(accessor='PR', footer=lambda table: sum(x['PR'] for x in table.data), empty_values=(0,))
    ZZ = tables.Column(accessor='ZZ', footer=lambda table: sum(x['ZZ'] for x in table.data), empty_values=(0,))

    # suma = tables.Column(footer=suma_footer)

    def return_url(self, record, column_id):
        url = reverse('empl_list')
        return format_html('''<a class="link_col_summ" 
            href="{}?e_status=In_service&e_desg__d_id={}{}&e_unit_roll__u_id={}">{}</a>''',
                           url, column_id, record['e_desg__d_gcode'],
                           format(record['e_unit_roll__u_area__a_code'], '02d'), record[column_id])

    def render_desg_code(self, record):
        # print(record)
        url = reverse('empl_list')
        return format_html('<a class="download_link" href="{}?e_desg__d_id={}&e_unit_roll__u_id={}&_export=csv">{}</a>',
                           url, record['e_desg__d_gcode'], format(record['e_unit_roll__u_area__a_code'], '02d'),
                           record['e_desg__d_gcode'])

    def render_total(self, record):
        url = reverse('empl_list')
        return format_html('<a class="link_col_summ" href="{}?e_desg__d_id={}&e_unit_roll__u_id={}">{}</a>', url,
                           record['e_desg__d_gcode'], format(record['e_unit_roll__u_area__a_code'], '02d'),
                           record['tot'])

    def render_male(self, record):
        url = reverse('empl_list')
        return format_html(
            '<a class="link_col_summ" href="{}?e_desg__d_id={}&e_gender=Male&e_unit_roll__u_id={}">{}</a>', url,
            record['e_desg__d_gcode'], format(record['e_unit_roll__u_area__a_code'], '02d'), record['male'])

    def render_female(self, record):
        url = reverse('empl_list')
        return format_html(
            '<a class="link_col_summ" href="{}?e_desg__d_id={}&e_gender=Female&e_unit_roll__u_id={}">{}</a>', url,
            record['e_desg__d_gcode'], format(record['e_unit_roll__u_area__a_code'], '02d'), record['female'])

    def render_C6(self, record): return self.return_url(record, 'C6')

    def render_C5(self, record): return self.return_url(record, 'C5')

    def render_C4(self, record): return self.return_url(record, 'C4')

    def render_C3(self, record): return self.return_url(record, 'C3')

    def render_C2(self, record): return self.return_url(record, 'C2')

    def render_C1(self, record): return self.return_url(record, 'C1')

    def render_T1(self, record): return self.return_url(record, 'T1')

    def render_TA(self, record): return self.return_url(record, 'TA')

    def render_TB(self, record): return self.return_url(record, 'TB')

    def render_TC(self, record): return self.return_url(record, 'TC')

    def render_TD(self, record): return self.return_url(record, 'TD')

    def render_TE(self, record): return self.return_url(record, 'TE')

    def render_TF(self, record): return self.return_url(record, 'TF')

    def render_TG(self, record): return self.return_url(record, 'TG')

    def render_TH(self, record): return self.return_url(record, 'TH')

    def render_GS(self, record): return self.return_url(record, 'GS')

    def render_G1(self, record): return self.return_url(record, 'G1')

    def render_G2(self, record): return self.return_url(record, 'G2')

    def render_G3(self, record): return self.return_url(record, 'G3')

    def render_XS(self, record): return self.return_url(record, 'XS')

    def render_XA(self, record): return self.return_url(record, 'XA')

    def render_XB(self, record): return self.return_url(record, 'XB')

    def render_XC(self, record): return self.return_url(record, 'XC')

    def render_XD(self, record): return self.return_url(record, 'XD')

    def render_XE(self, record): return self.return_url(record, 'XE')

    def render_PR(self, record): return self.return_url(record, 'PR')

    def render_ZZ(self, record): return self.return_url(record, 'ZZ')

    class Meta:
        attrs = {"class": "fixed_headers rwd-table"}


month_map = {'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11',
             'dec': '12', 'jan': '01', 'feb': '02', 'mar': '03'}
import datetime

present = datetime.date.today()
fiscal_yr = present.year
if present.month < 4:
    fiscal_yr = present.year - 1
