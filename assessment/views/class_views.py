from braces.views import GroupRequiredMixin
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# EmpAddRedTable, EmpSummDesgAreaTable
from assessment.forms.employee import EmpEditForm, EmpTerminateForm, EmpAddForm
from assessment.models import Employee


class AddEmpView(CreateView):
    """A create view for Foo model"""
    template_name = "transaction/add_employee.html"
    form_class = EmpAddForm  # the change is over here
    model = Employee
    # group_required = u'area_apms'
    success_url = '.'

    def get_form_kwargs(self):
        kw = super(AddEmpView, self).get_form_kwargs()
        # kw['req_username'] = self.request.user.username # the trick!
        # kw['curr_user'] = self.request.user
        # import ipdb; ipdb.set_trace()
        return kw


# class CreateEmpView(GroupRequiredMixin, CreateView):
#     """A create view for Foo model"""
#     template_name = "emp_create.html"
#     form_class = EmpCreateForm  # the change is over here
#     model = Employee
#     group_required = u'area_apms'
#     success_url = '.'
#
#     def get_form_kwargs(self):
#         kw = super(CreateEmpView, self).get_form_kwargs()
#         kw['req_username'] = self.request.user.username  # the trick!
#         # import ipdb; ipdb.set_trace()
#         return kw


class EmployeeUpdate(GroupRequiredMixin, UpdateView):
    model = Employee
    # fields = '__all__'
    group_required = u'area_apms'
    form_class = EmpEditForm
    template_name = 'emp_update.html'

    def get_success_url(self):
        print('success_url=' + self.request.GET.get('next'))
        return self.request.GET.get('next')

    def dispatch(self, request, *args, **kwargs):
        handler = super(EmployeeUpdate, self).dispatch(request, *args, **kwargs)
        # Only allow editing if current user is owner
        # import ipdb; ipdb.set_trace()
        # if self.object.e_unit_roll.u_code[1:3] != request.user.username[0:2] and self.object.e_unit_roll.u_code[1:3] != '99' and request.user.username not in [
        #     'iedstaff', 'iedhq']:
        #     # return HttpResponseForbidden(u"You dont have permission to edit other Area records.")
        #     return HttpResponseForbidden(index_403(request))
        return handler


# class EditEmpView(GroupRequiredMixin, UpdateView):
class EditEmpView(UpdateView):
    model = Employee
    # fields = '__all__'
    # group_required = u'area_apms'
    form_class = EmpEditForm
    template_name = 'transaction/edit_employee.html'

    def get_success_url(self):
        print('success_url=' + self.request.GET.get('next'))
        return self.request.GET.get('next')

    def dispatch(self, request, *args, **kwargs):
        handler = super(EditEmpView, self).dispatch(request, *args, **kwargs)
        # Only allow editing if current user is owner
        # import ipdb; ipdb.set_trace()
        # if self.object.e_unit_roll.u_code[1:3] != request.user.username[0:2] and self.object.e_unit_roll.u_code[
        #                                                                          1:3] != '99' and request.user.username not in [
        #     'iedstaff', 'iedhq']:
        #     # return HttpResponseForbidden(u"You dont have permission to edit other Area records.")
        #     return HttpResponseForbidden(index_403(request))
        return handler

    def get_context_data(self, **kwargs):
        context = super(EditEmpView, self).get_context_data(**kwargs)
        context['panel_header'] = 'Edit Employee Details'
        return context


class EmployeeDelete(DeleteView):
    model = Employee

    def get_success_url(self):
        print('success_url=' + self.request.GET.get('next'))
        return self.request.GET.get('next')


class EditTerminateView(DeleteView):
    model = Employee
    # fields = '__all__'
    # group_required = u'area_apms'
    form_class = EmpTerminateForm
    template_name = 'deleteConfirm.html'

    def get_success_url(self):
        print('success_url=' + self.request.GET.get('next'))
        return self.request.GET.get('next')

    def dispatch(self, request, *args, **kwargs):
        # Only allow editing if current user is owner
        # import ipdb; ipdb.set_trace()
        # if check_user_permission(self.kwargs['pk'], request.user.username):
        #     return HttpResponseForbidden(index_403(request))
        handler = super(EditTerminateView, self).dispatch(request, *args, **kwargs)
        return handler

    def get_form_kwargs(self):
        kw = super(EditTerminateView, self).get_form_kwargs()
        kw['req_username'] = self.request.user.username  # the trick!
        kw['curr_user'] = self.request.user
        # import ipdb; ipdb.set_trace()
        return kw

    def get_context_data(self, **kwargs):
        context = super(EditTerminateView, self).get_context_data(**kwargs)
        context['panel_header'] = 'Delete a record'
        context['success_url'] = reverse('emp_terminate_confirm', kwargs={'pk': self.object.e_id})
        return context
