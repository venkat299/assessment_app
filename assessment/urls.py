from django.conf.urls import url
from django.views.generic import RedirectView

from assessment.models import Employee
from assessment.tables.employee import EmployeeTable, EmployeeFilter
from assessment.views import main_view, table_views, class_views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('<int:question_id>/', views.detail, name='detail')
    # url(r'^$', RedirectView.as_view(url='emp/list/')),
    url(r'^$', RedirectView.as_view(url='budget_summary_unit/')),

    url(r'^upload_files/$', main_view.upload_files, name='upload_files'),
    url(r'^upload_req/$', main_view.upload_req, name='upload_req'),
    url(r'^upload_ext/$', main_view.upload_ext, name='upload_ext'),
    url(r'^bulk_delete_unit/$', main_view.bulk_delete_unit, name='bulk_delete_unit'),

    url(r'^report_download/$', main_view.report_download, name='report_download'),

    url(r'^budget_summary_unit/$', main_view.budget_summary_unit, name='budget_summary_unit'),

    url(r'^unit_req/$', main_view.unit_req, name='unit_req'),
    url(r'^unit_req_filtered/$', main_view.unit_req_filtered, name='unit_req_filtered'),
    url(r'^get_req_unit_gdesg/$', main_view.get_req_unit_gdesg, name='get_req_unit_gdesg'),

    url(r'^get_filter_unit_gdesg_list/$', main_view.get_filter_unit_gdesg_list, name='get_filter_unit_gdesg_list'),
    url(r'^get_desg_summary_company/$', main_view.get_desg_summary_company, name='get_desg_summary_company'),
    url(r'^get_desg_summary_area/$', main_view.get_desg_summary_area, name='get_desg_summary_area'),

    url(r'^get_stat_for_gdesg_list/$', main_view.get_stat_for_gdesg_list, name='get_stat_for_gdesg_list'),

    url(r'^get_req_unit_desg/$', main_view.get_req_unit_desg, name='get_req_unit_desg'),
    url(r'^set_req_unit_desg/$', main_view.set_req_unit_desg, name='set_req_unit_desg'),
    url(r'^get_req_unit_sect/$', main_view.get_req_unit_sect, name='get_req_unit_sect'),
    url(r'^set_req_unit_sect/$', main_view.set_req_unit_sect, name='set_req_unit_sect'),

    url(r'^get_all_desg/$', main_view.get_all_desg, name='get_all_desg'),
    url(r'^get_all_gdesg/$', main_view.get_all_gdesg, name='get_all_gdesg'),
    url(r'^get_all_sect/$', main_view.get_all_sect, name='get_all_sect'),
    url(r'^get_unit_detail/$', main_view.get_unit_detail, name='get_unit_detail'),

    # ======================= class based views ==============================
    url(r'^emp/update/(?P<pk>\w+)/$', class_views.EditEmpView.as_view(), name='emp_update'),
    url(r'^emp/add/$', class_views.AddEmpView.as_view(), name="emp_add"),
    url(r'^emp/terminate/(?P<pk>\w+)/$', class_views.EditTerminateView.as_view(), name='emp_terminate'),
    url(r'^emp/terminate_confirm/(?P<pk>\w+)/$', class_views.EditTerminateView.as_view(), name='emp_terminate_confirm'),
    # url(r'^emp/terminate/(?P<pk>\w+)/$', main_view.EditTerminateView.as_view(), name='emp_terminate'),

    # ======================= table based views ==============================
    url(r'^emp/list/area/$', table_views.emp_area_summ, name='emp_area_summ'),
    url(r'^emp/list/unit/(?P<a_id>\w+)$', table_views.emp_unit_summ, name='emp_unit_summ'),
    url(r'^emp/list/desg/unit/(?P<unit_code>\w+)$', table_views.emp_desg_unit_summ, name='emp_desg_unit_summ'),
    url(r'^emp/list/$', table_views.EmployeeListView.as_view(
        model=Employee,
        table_class=EmployeeTable,
        template_name='employee_new.html',
        filter_class=EmployeeFilter,
    ), name='empl_list'),
    # url(r'^emp/list/desg/$', main_view.emp_desg_summ, name='emp_desg_summ'),
    # url(r'^emp/list/desg/(?P<area_code>\w+)$', main_view.emp_desg_area_summ, name='emp_desg_area_summ'),

    url(
        r'^desg-autocomplete/$',
        main_view.DesgAutocomplete.as_view(),
        name='desg-autocomplete',
    ),
    url(
        r'^unit-autocomplete/$',
        main_view.UnitAutocomplete.as_view(),
        name='unit-autocomplete',
    ),
]
