import datetime
import datetime as dt

from crispy_forms.bootstrap import InlineField, FormActions, StrictButton
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div
from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import SelectDateWidget

from assessment.models import Employee, Desg, Unit, appointment_choices, termination_choices, Section, Year
from budget_app import settings

EDIT_ENABLED = getattr(settings, "EDIT_ENABLED", False)

class EmployeeListFormHelper(FormHelper):
    form_id = 'customer-search-form'
    form_class = 'form-inline'
    field_template = 'bootstrap3/layout/inline_field.html'
    field_class = 'col-xs-3'
    label_class = 'col-xs-3'
    form_show_errors = True
    help_text_inline = False
    html5_required = True

    layout = Layout(
        Fieldset(
            '<i class="fa fa-search"></i> Search Employee Records',
            InlineField('e_gender'),
            InlineField('e_desg__d_discp'),
            InlineField('e_desg__d_code'),
        ),
        FormActions(
            StrictButton(
                '<i class="fa fa-search"></i> Search',
                type='submit',
                css_class='btn-primary',
                style='margin-top:10px;')
        )
    )


class EmployeeFormHelper(FormHelper):
    form_method = 'GET'
    layout = Layout(
        Div(
            Div('e_desg__d_discp', css_class='col-md-3'),
            Div('e_desg__d_id', css_class='col-md-3'),
            Div('e_unit_roll__u_id', css_class='col-md-3'),
            Div('e_unit_work__u_id', css_class='col-md-3'), css_class='row'
        ),
        Div(
            Div('e_regsno', css_class='col-md-3'),
            Div('e_eis', css_class='col-md-3'),
            Div('e_name', css_class='col-md-3'),
            Div('e_gender', css_class='col-md-3'), css_class='row'
        ),
        Div(
            Div('e_status', css_class='col-md-3'),
            # Div('e_doj' , css_class='col-md-3'),
            # Div('e_join', css_class='col-md-3'),
            # Div('e_termi', css_class='col-md-3'),
            Div(Submit('submit', 'Apply Filter'), css_class='col-md-3'), css_class='row'
        ),

        # Div(
        #     Div(Submit('submit', 'Apply Filter'), css_class='col-md-12'), css_class='row'
        # )
    )


class MySelectDateWidget(SelectDateWidget):

    def create_select(self, *args, **kwargs):
        old_state = self.is_required
        self.is_required = False
        result = super(MySelectDateWidget, self).create_select(*args, **kwargs)
        self.is_required = old_state
        return result


class EmpEditForm(forms.ModelForm):
    empty_dt_label = ("Year", "Month", "Day"),
    e_eis = forms.CharField(label="EIS/NEIS:", disabled=True)
    e_dob = forms.DateField(required=False, label="Date of Retirement:", widget=MySelectDateWidget(
        years=range(dt.date.today().year - 1, dt.date.today().year + 65),
        empty_label=("Year", "Month", "Day"),
    ), )
    e_id = forms.CharField(disabled=True)
    # e_id = forms.CharField()
    e_year = forms.ModelChoiceField(label="Budget Year:",
                                    queryset=Year.objects.all().order_by('y_code'),
                                    # widget=autocomplete.ModelSelect2(url='desg-autocomplete')
                                    )
    e_desg = forms.ModelChoiceField(label="Designation:",
                                    queryset=Desg.objects.all().order_by('d_discp', 'd_gdesig', 'd_rank'),
                                    # widget=autocomplete.ModelSelect2(url='desg-autocomplete')
                                    )
    e_sect = forms.ModelChoiceField(label="Section:",
                                    queryset=Section.objects.all().order_by('s_rank'),
                                    # widget=autocomplete.ModelSelect2(url='desg-autocomplete')
                                    )
    e_unit_roll = forms.ModelChoiceField(label="On-Roll Unit:",
                                         queryset=Unit.objects.order_by('u_area',
                                                                        'u_type',
                                                                        'u_name'),
                                         # widget=autocomplete.ModelSelect2(url='unit-autocomplete',attrs={'data-minimum-input-length': 3,})
                                         )
    e_unit_work = forms.ModelChoiceField(label="Working Unit:",
                                         queryset=Unit.objects.order_by('u_area',
                                                                        'u_type',
                                                                        'u_name'),
                                         # widget=autocomplete.ModelSelect2(url='unit-autocomplete')
                                         )

    class Meta:
        model = Employee
        fields = ['e_year', 'e_id', 'e_eis', 'e_name', 'e_regsno',
                  'e_sect',
                  'e_gender', 'e_desg', 'e_unit_roll', 'e_unit_work', 'e_dob', ]

    def __init__(self, *args, **kwargs):
        super(EmpEditForm, self).__init__(*args, **kwargs)

        # import ipdb; ipdb.set_trace()
        self.helper = FormHelper()
        self.helper.form_id = 'id_intake_form'
        self.helper.form_method = 'POST'
        self.helper.form_tag = True
        # self.helper.form_action = '.'
        self.helper.layout = Layout(
            Div(
                Div('e_year', 'e_eis', 'e_name', 'e_desg', css_class='col-md-4'),
                Div('e_sect', 'e_unit_roll', 'e_unit_work', InlineRadios('e_gender'), css_class='col-md-4'),
                Div('e_dob', 'e_id', css_class='col-md-4'), css_class='row'
            ),
            Div(
                Div(Submit('save', 'Save'), css_class='col-md-12'), css_class='row'
            )
        )
    # def delete(self, *args, **kw):
    #     print(kw)
    #     instance = super(EmpCreateForm, self).delete()
    #     Employee.objects.get(id=self.e_id).delete()
    #     print(instance)


class EmpCreateForm(forms.ModelForm):
    empty_dt_label = ("Year", "Month", "Day"),
    e_eis = forms.CharField(label="EIS/NEIS:", )
    # e_name = forms.CharField()
    e_regsno = forms.CharField(label="Token no:", required=False)
    # e_status = forms.CharField(label = "Service Status:")
    e_termi = forms.ChoiceField(label="Service Termination Type:", required=False, choices=termination_choices)
    e_join = forms.ChoiceField(label="Service Join Type:", required=False, choices=appointment_choices)
    e_doj = forms.DateField(label="Service Join Date:", required=False,
                            widget=MySelectDateWidget(
                                years=range(datetime.date.today().year - 65, datetime.date.today().year),
                                empty_label=("Year", "Month", "Day"),
                            ), )
    e_dot = forms.DateField(label="Service Termination Date:", required=False, widget=MySelectDateWidget(
        years=range(datetime.date.today().year - 65, datetime.date.today().year + 1),
        empty_label=("Year", "Month", "Day"),
    ), )
    e_dob = forms.DateField(label="Date of Birth:", widget=MySelectDateWidget(
        years=range(datetime.date.today().year - 65, datetime.date.today().year),
        empty_label=("Year", "Month", "Day"),
    ), )
    # e_gender = forms.CharField(label = "Gender:",)

    e_desg = forms.ModelChoiceField(label="Designation:",
                                    queryset=Desg.objects.all().order_by('d_discp', 'd_gdesig', 'd_rank'),
                                    # widget=autocomplete.ModelSelect2(url='desg-autocomplete')
                                    )
    e_unit_roll = forms.ModelChoiceField(label="On-Roll Unit:",
                                         queryset=Unit.objects.filter(u_status__isnull=True).order_by('u_area',
                                                                                                      'u_type',
                                                                                                      'u_name'),
                                         # widget=autocomplete.ModelSelect2(url='unit-autocomplete',attrs={'data-minimum-input-length': 3,})
                                         )
    e_unit_work = forms.ModelChoiceField(label="Working Unit:",
                                         queryset=Unit.objects.filter(u_status__isnull=True).order_by('u_area',
                                                                                                      'u_type',
                                                                                                      'u_name'),
                                         # widget=autocomplete.ModelSelect2(url='unit-autocomplete')
                                         )

    class Meta:
        model = Employee
        fields = ['e_eis', 'e_name', 'e_regsno', 'e_status', 'e_termi',
                  'e_gender', 'e_desg', 'e_unit_roll', 'e_unit_work', 'e_doj',
                  'e_dot', 'e_join', 'e_dob', 'e_gender']

    def clean(self):
        if not EDIT_ENABLED:
            raise ValidationError("Cannot edit; edit feature locked")
        cleaned_data = super(EmpCreateForm, self).clean()
        if cleaned_data.get("e_unit_roll"):
            e_unit_roll = cleaned_data.get("e_unit_roll").u_code
            if e_unit_roll[1:3] != self.req_username[0:2] and e_unit_roll[1:3] != '99' and self.req_username not in [
                'iedstaff', 'iedhq']:
                raise ValidationError("You dont have permission to edit other Area records.")

    def __init__(self, *args, **kwargs):
        self.req_username = kwargs.pop('req_username', None)
        super(EmpCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_intake_form'
        self.helper.form_method = 'POST'
        self.helper.form_tag = True
        # self.helper.form_action = '.'
        self.helper.layout = Layout(
            Div(
                Div('e_eis', 'e_desg', 'e_unit_roll', 'e_unit_work', css_class='col-md-4'),
                Div('e_name', 'e_dob', InlineRadios('e_gender'), InlineRadios('e_status'), css_class='col-md-4'),
                Div('e_regsno', 'e_join', 'e_doj', 'e_termi', 'e_dot', css_class='col-md-4'), css_class='row'
            ),
            Div(
                Div(Submit('save', 'Save'), css_class='col-md-12'), css_class='row'
            )
        )

    def save(self, *args, **kw):
        print(kw)
        instance = super(EmpCreateForm, self).save(commit=False)
        instance.save()
        return instance

    def delete(self, *args, **kw):
        print(kw)
        instance = super(EmpCreateForm, self).save(commit=False)
        print(instance)
        # instance.save()
        # return instance
        # redirect('.')


class EmpTerminateForm(forms.ModelForm):
    empty_dt_label = ("Year", "Month", "Day"),
    e_eis = forms.CharField(label="EIS/NEIS:", disabled=True)
    e_name = forms.CharField(disabled=True)
    e_regsno = forms.CharField(label="Token no:", disabled=True, required=False)
    # e_gender = forms.CharField(label = "Gender:",)
    form_action = './?next={{ redirect_to }}'
    e_desg = forms.ModelChoiceField(label="Designation:",
                                    queryset=Desg.objects.all().order_by('d_discp', 'd_gdesig', 'd_rank'),
                                    # widget=autocomplete.ModelSelect2(url='desg-autocomplete')
                                    disabled=True)
    e_unit_roll = forms.ModelChoiceField(label="Current On-Roll Unit:",
                                         queryset=Unit.objects.filter(u_status__isnull=True).order_by('u_area',
                                                                                                      'u_type',
                                                                                                      'u_name'),
                                         # widget=autocomplete.ModelSelect2(url='unit-autocomplete',attrs={'data-minimum-input-length': 3,})
                                         disabled=True)
    # t_reason = forms.ModelChoiceField(label="Reason/Category:", queryset=TerminationCat.objects.all(),
    # widget=autocomplete.ModelSelect2(url='desg-autocomplete')
    # disabled=False)
    t_date = forms.DateField(label="Date of Transfer:", widget=SelectDateWidget(
        years=range(1990, dt.date.today().year + 1),
        empty_label=("Year", "Month", "Day"),
    ), )

    class Meta:
        model = Employee
        fields = ['e_eis', 'e_name', 'e_regsno', 'e_desg', 'e_unit_roll', 't_date']

    def __init__(self, *args, **kwargs):
        self.req_username = kwargs.pop('req_username', None)
        self.curr_user = kwargs.pop('curr_user', None)
        super(EmpTerminateForm, self).__init__(*args, **kwargs)

        # import ipdb; ipdb.set_trace()
        self.helper = FormHelper()
        self.helper.form_id = 'id_intake_form'
        self.helper.form_method = 'POST'
        self.helper.form_tag = True
        # self.helper.form_action = '.'
        self.helper.layout = Layout(
            Div(
                Div('t_reason', 't_date', css_class='col-md-4'),
                Div('e_eis', 'e_name', 'e_regsno', css_class='col-md-4'),
                Div('e_desg', 'e_unit_roll', css_class='col-md-4'), css_class='row'
            ),
            Div(
                Div(Submit('save', 'Save'), css_class='col-md-12'), css_class='row'
            )
        )

    def clean(self):
        if not EDIT_ENABLED:
            raise ValidationError("Cannot edit; edit feature locked")
        cleaned_data = super(EmpTerminateForm, self).clean()

        if cleaned_data.get("e_termi"):
            t_reason = cleaned_data.get("t_reason").tc_value
            e_termi = cleaned_data.get("e_termi").tc_value
            if t_reason == e_termi:
                raise ValidationError("Current Reason is same as prev reason")

    def save(self, *args, **kw):
        print(kw)
        dt = self.cleaned_data
        # import ipdb; ipdb.set_trace()
        instance = super(EmpTerminateForm, self).save(commit=False)
        instance.e_termi = dt['t_reason']
        instance.e_dot = dt['t_date']
        instance.e_status = 'Not_in_service'
        instance.save()
        # Termination.objects.create(t_eis=instance, t_unit=instance.e_unit_roll, t_date=dt['t_date'],
        #                            t_reason=dt['t_reason'], t_edit_by=self.curr_user, t_edit_on=timezone.now())
        return instance


class EmpAddForm(forms.ModelForm):
    empty_dt_label = ("Year", "Month", "Day"),
    e_eis = forms.CharField(label="EIS/NEIS:", )
    e_dob = forms.DateField(required=False, label="Date of Retirement:", widget=MySelectDateWidget(
        years=range(dt.date.today().year - 1, dt.date.today().year + 65),
        empty_label=("Year", "Month", "Day"),
    ), )
    e_id = forms.CharField(widget=forms.HiddenInput())
    # e_id = forms.CharField()
    e_year = forms.ModelChoiceField(label="Budget Year:",
                                    queryset=Year.objects.all().order_by('y_code'),
                                    # widget=autocomplete.ModelSelect2(url='desg-autocomplete')
                                    )
    e_desg = forms.ModelChoiceField(label="Designation:",
                                    queryset=Desg.objects.all().order_by('d_discp', 'd_gdesig', 'd_rank'),
                                    # widget=autocomplete.ModelSelect2(url='desg-autocomplete')
                                    )
    e_sect = forms.ModelChoiceField(label="Section:",
                                    queryset=Section.objects.all().order_by('s_rank'),
                                    # widget=autocomplete.ModelSelect2(url='desg-autocomplete')
                                    )
    e_unit_roll = forms.ModelChoiceField(label="On-Roll Unit:",
                                         queryset=Unit.objects.order_by('u_area',
                                                                        'u_type',
                                                                        'u_name'),
                                         # widget=autocomplete.ModelSelect2(url='unit-autocomplete',attrs={'data-minimum-input-length': 3,})
                                         )
    e_unit_work = forms.ModelChoiceField(label="Working Unit:",
                                         queryset=Unit.objects.order_by('u_area',
                                                                        'u_type',
                                                                        'u_name'),
                                         # widget=autocomplete.ModelSelect2(url='unit-autocomplete')
                                         )

    class Meta:
        model = Employee
        fields = ['e_year', 'e_id', 'e_eis', 'e_name', 'e_regsno',
                  'e_sect',
                  'e_gender', 'e_desg', 'e_unit_roll', 'e_unit_work', 'e_dob', ]

    def clean(self):
        cleaned_data = super(EmpAddForm, self).clean()
        #     # cleaned_data = self.cleaned_data
        yr = cleaned_data.get("e_year")
        eis = cleaned_data.get("e_eis")
        print(yr, eis, cleaned_data)
        #     # cleaned_data['e_id'] = yr.y_name+"_"+eis
        #     # cleaned_data['e_id'] = yr + "_" + eis
        #     # cleaned_data['e_year_id'] = yr
        #     # cleaned_data.pop("e_id_yr")
        #     # delattr(cleaned_data,"e_id_yr")
        #     self.cleaned_data = cleaned_data
        #     # self.instance.e_id = cleaned_data['e_id']
        #     print(self.cleaned_data)
        # obj = Employee.objects.create(e_id=cleaned_data.get('e_id'))
        # obj.e_year_id=cleaned_data.get('e_year_id')
        # obj.e_id=cleaned_data.get('e_id')
        # obj.e_eis=cleaned_data.get('e_eis')
        # obj.e_name=cleaned_data.get('e_name')
        # obj.e_regsno=cleaned_data.get('e_regsno')
        # obj.e_sect_id=cleaned_data.get('e_sect').s_id
        # obj.e_gender=cleaned_data.get('e_gender')
        # obj.e_desg_id=cleaned_data.get('e_desg').d_id
        # obj.e_unit_roll_id=cleaned_data.get('e_unit_roll').u_id
        # obj.e_unit_work_id=cleaned_data.get('e_unit_work').u_id
        # obj.e_dob=cleaned_data.get('e_dob')
        # obj.e_gender=cleaned_data.get('e_gender')
        #
        # obj.save()
        if not EDIT_ENABLED:
            raise ValidationError("Cannot edit; edit feature locked")
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        # self.req_username = kwargs.pop('req_username', None)
        # self.curr_user = kwargs.pop('curr_user', None)
        super(EmpAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_intake_form'
        self.helper.form_method = 'POST'
        self.helper.form_tag = True
        # self.helper.form_action = '.'
        # InlineRadios('e_status'),
        self.helper.layout = Layout(
            Div(
                Div('e_year', 'e_eis', 'e_name', 'e_desg', css_class='col-md-4'),
                Div('e_sect', 'e_unit_roll', 'e_unit_work', InlineRadios('e_gender'), css_class='col-md-4'),
                Div('e_dob', 'e_id', css_class='col-md-4'), css_class='row'
            ),
            Div(
                Div(Submit('save', 'Save'), css_class='col-md-12'), css_class='row'
            )
        )

    def save(self, *args, **kw):
        print("In Save method")
        # print(kw)
        # import ipdb; ipdb.set_trace()
        dt = self.cleaned_data
        instance = super(EmpAddForm, self).save(commit=False)
        instance.e_id = str((dt['e_year']).y_code) + "_" + dt['e_eis']
        instance.save()
        # instance
        print("-->", instance)
        # dt = self.cleaned_data
        # Addition.objects.create(a_eis=instance, a_unit=instance.e_unit_roll, a_reason=dt['e_join'], a_date=dt['e_doj'],
        #                         a_edit_by=self.curr_user, a_edit_on=timezone.now())
        return instance
        # redirect('.')
