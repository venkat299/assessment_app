# Create your models here.

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Year(models.Model):
    y_code = models.IntegerField(primary_key=True, null=False)
    y_name = models.CharField(max_length=7)

    def __str__(self):
        return self.y_name


class Area(models.Model):
    a_id = models.CharField(primary_key=True, null=False, max_length=8)
    a_name = models.CharField(max_length=20)
    a_order = models.IntegerField()
    a_code = models.CharField(max_length=4, default='', null=True)
    a_year = models.ForeignKey(Year, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('a_code', 'a_year'),)

    def __str__(self):
        return self.a_name + '__' + str(self.a_code)


class Unit(models.Model):
    # status_choices = (("NOT_ACTIVE", "NOT_ACTIVE"), ("ACTIVE", "Not_in_service"))
    u_id = models.CharField(verbose_name="Unit Id", primary_key=True, null=False, max_length=12)
    u_area = models.ForeignKey(Area, on_delete=models.CASCADE)
    u_name = models.CharField(max_length=20)
    u_type = models.CharField(max_length=2)
    u_code = models.CharField(max_length=7)
    u_status = models.CharField(max_length=20, null=True)

    # u_year = models.ForeignKey(Year, on_delete=models.CASCADE)

    # class Meta:
    #     unique_together = (('u_code', 'u_year'),)

    def __str__(self):
        return self.u_area.a_code + '__' + self.u_code + '__' + self.u_name


class Desg(models.Model):
    cadre_choices = (("CD", "CD"), ("XCD", "XCD"))
    d_id = models.CharField(verbose_name="Desg Code", primary_key=True, null=False, max_length=12)
    d_code = models.CharField(verbose_name="DSCD", max_length=7)
    d_name = models.CharField(max_length=40)
    d_grade = models.CharField(max_length=10)
    d_gdesig = models.CharField(max_length=40)
    d_gcode = models.IntegerField()
    d_rank = models.IntegerField()
    d_cadre = models.CharField(choices=cadre_choices, default="CD", max_length=10)
    d_discp = models.CharField(verbose_name="Discpline", max_length=20)
    d_promo = models.CharField(max_length=2, null=True)
    d_year = models.ForeignKey(Year, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('d_code', 'd_year'),)

    def __str__(self):
        return self.d_code + '__' + self.d_name
        # return self.d_code+'__'+self.d_discp+'__'+self.d_name + '__'+ self.d_grade


appointment_choices = (("A_NA", "NA"),
                       ("A_Land_Losers", "Appt of Land Losers"),
                       ("A_Fresh_Recruitment", "Fresh Recruitment"),
                       ("A_Death", "In lieu of Death"),
                       ("A_Disability", "In lieu of perm Disability"),
                       ("A_Female_VRS", "Female VRS"),
                       ("A_Reinstt_Rejoin", "Reinstt/Rejoin"),
                       ("A_Other_tranfer", "Other reason(Inter Co transfer)"))
termination_choices = (("T_NA", "NA"),
                       ("T_Retirement", "Retirement"),
                       ("T_Resignation", "Resignation"),
                       ("T_Unfit", "Medically Unfit"),
                       ("T_Death", "Death"),
                       ("T_Female_VRS", "Female VRS"),
                       ("T_VRS_BPE", "VRS BPE"),
                       ("T_Dismissal", "Dismissal/Termination"),
                       ("T_Other_reason", "Other reason(Inter Co transfer)"))
status_choices = (("In_service", "In_service"), ("Not_in_service", "Not_in_service"))
gender_choices = (("M", "M"), ("F", "F"))


class Section(models.Model):
    location_choices = (("Underground", "Underground"), ("Surface", "Surface"))
    type_choices = (("OC", "OC"), ("UG", "UG"), ("CU", "CU"))
    s_id = models.CharField(primary_key=True, null=False, max_length=12)
    s_code = models.CharField(verbose_name="Code", max_length=7)
    s_name = models.CharField(max_length=40)
    s_type = models.CharField(max_length=2, choices=type_choices)
    s_location = models.CharField(max_length=15, choices=location_choices)
    s_rank = models.IntegerField()
    s_year = models.ForeignKey(Year, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('s_code', 's_year'),)

    def __str__(self):
        return self.s_code + '__' + self.s_name


class Employee(models.Model):
    e_id = models.CharField(verbose_name="EIS No/ID", primary_key=True, null=False, max_length=13)
    e_eis = models.CharField(verbose_name="EIS No", max_length=8, )
    e_regsno = models.CharField(verbose_name="Token No", max_length=15, null=True, blank=True)
    e_name = models.CharField(verbose_name="Full Name", max_length=40)
    e_dob = models.DateField(verbose_name="Date of Retirement", null=True, blank=True)
    e_gender = models.CharField(verbose_name="Gender", choices=gender_choices, default="M", max_length=10)
    e_desg = models.ForeignKey(Desg, verbose_name="Designation", related_name='desg_code', on_delete=models.CASCADE)
    e_unit_roll = models.ForeignKey(Unit, verbose_name="On-Roll Unit", on_delete=models.CASCADE,
                                    related_name='e_unit_roll')
    e_unit_work = models.ForeignKey(Unit, verbose_name="Working Unit", on_delete=models.CASCADE,
                                    related_name='e_unit_work')

    e_doj = models.DateField(verbose_name="Service Join Date", null=True, blank=True)
    e_dot = models.DateField(verbose_name="Service Termination Date", null=True, blank=True)
    # e_join = models.ForeignKey(AdditionCat, verbose_name="Service Join Type", default="A_NA", max_length=20)
    # e_termi = models.ForeignKey(TerminationCat, verbose_name="Service Termination Type", default="T_NA", max_length=20)
    e_status = models.CharField(verbose_name="Service Status", choices=status_choices, default="In_service",
                                max_length=20)
    e_dop = models.DateField(verbose_name="Last promo. Date", null=True, blank=True)  # date of last promotion
    e_year = models.ForeignKey(Year, on_delete=models.CASCADE)
    e_sect = models.ForeignKey(Section, on_delete=models.CASCADE)
    e_comments = models.TextField(verbose_name="Comments", max_length=200, null=True, blank=True)

    #
    # class Meta:
    #     unique_together = (('e_eis', 'e_year'),)

    def __str__(self):
        return str(self.e_eis) + '__' + self.e_name

    # def clean_e_name(self):
    #     return self.cleaned_data['e_name'].capitalize()

    def clean(self):
        # if self.e_doj is not None and self.e_dot is not None and self.e_dot < self.e_doj:
        #     raise ValidationError(_('Termination Date is earlier than Join Date'))
        #
        # if self.e_doj is not None and self.e_dob is not None and self.e_doj < self.e_dob:
        #     raise ValidationError(_('Join Date is earlier than Birth Date'))
        #
        # if self.e_dot is not None and self.e_dob is not None and self.e_dot < self.e_dob:
        #     raise ValidationError(_('Termination Date is earlier than Birth Date'))

        # import ipdb; ipdb.set_trace()
        # if self.e_unit_roll_id is not None and self.e_unit_work_id is not None and self.e_unit_roll.u_code[
        #                                                                            1:3] != self.e_unit_work.u_code[1:3]:
        #     raise ValidationError(_('Working Unit should match area of On-roll unit'))
        #
        # if not (self.e_eis.isdigit() or (len(self.e_eis.split('T')) == 2
        #                                  and (self.e_eis.split('T')[1]).isdigit()
        #                                  and self.e_eis.split('T')[0] is ''
        # )):
        #     raise ValidationError(
        #         _('EIS should be a Number or Temporary EIS is should be a number prefixed by a letter "T"'))

        self.e_name = self.e_name.upper()
        if not (all(x.isalpha() or x.isspace() or x == "." for x in self.e_name)):
            raise ValidationError(_('Name Should be alphabet or space Only'))

        # import ipdb; ipdb.set_trace()


class Sanction(models.Model):
    sn_id = models.CharField(primary_key=True, null=False, max_length=24)
    sn_dscd = models.ForeignKey(Desg, on_delete=models.CASCADE)
    sn_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    sn_req = models.IntegerField(default=0)
    sn_san = models.IntegerField(default=0)
    sn_comment = models.TextField(verbose_name="Comments", max_length=200, blank=True)

    def __str__(self):
        return self.sn_unit.u_name + '__' + self.sn_dscd.d_code + '__' + str(self.sn_req) + '__' + str(self.sn_san)


class PrevSanction(models.Model):
    ps_id = models.CharField(primary_key=True, null=False, max_length=24)
    ps_dscd = models.ForeignKey(Desg, on_delete=models.CASCADE)
    ps_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    ps_req = models.IntegerField(default=0)
    ps_san = models.IntegerField(default=0)
    ps_comment = models.TextField(verbose_name="Comments", max_length=200, blank=True)

    def __str__(self):
        return self.ps_unit.u_name + '__' + self.ps_dscd.d_code + '__' + str(self.ps_req) + '__' + str(self.ps_san)


class SanctionSection(models.Model):
    sns_id = models.CharField(primary_key=True, null=False, max_length=30)
    sns_sect = models.ForeignKey(Section, on_delete=models.CASCADE)
    sns_d5 = models.CharField(max_length=5)
    sns_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    sns_req = models.IntegerField()
    sns_san = models.IntegerField()
    sns_comment = models.TextField(verbose_name="Comments", max_length=200, blank=True)

    def __str__(self):
        return self.sns_unit.u_name + '__' + self.sns_sect.s_name + '__' + str(self.sns_req) + '__' + str(self.sns_san)


class UnitSancDesg(models.Model):
    pkey = models.CharField(primary_key=True, max_length=20)
    unit = models.CharField(max_length=12)
    d5 = models.CharField(max_length=12)
    idx = models.CharField(max_length=12)
    u_id = models.CharField(max_length=12)
    u_name = models.CharField(max_length=12)
    u_type = models.CharField(max_length=12)
    u_code = models.CharField(max_length=12)
    u_status = models.CharField(max_length=12)
    u_area_id = models.CharField(max_length=12)
    d_id = models.CharField(max_length=12)
    d_code = models.CharField(max_length=12)
    d_name = models.CharField(max_length=40)
    d_grade = models.CharField(max_length=12)
    d_gdesig = models.CharField(max_length=12)
    d_gcode = models.IntegerField()
    d_rank = models.IntegerField()
    d_cadre = models.CharField(max_length=12)
    d_discp = models.CharField(max_length=40)
    d_promo = models.CharField(max_length=12)
    d_year_id = models.CharField(max_length=12)
    e_unit = models.CharField(max_length=12)
    e_dscd = models.CharField(max_length=12)
    e_dcd5 = models.CharField(max_length=12)
    male = models.IntegerField()
    female = models.IntegerField()
    tot = models.IntegerField()
    retr1 = models.IntegerField()
    retr2 = models.IntegerField()
    req = models.IntegerField()
    san = models.IntegerField()
    acde = models.CharField(max_length=12)
    a_name = models.CharField(max_length=12)
    a_order = models.IntegerField()
    comment = models.TextField(verbose_name="Comments", max_length=200, blank=True)
    retr0 = models.IntegerField()
    prev_req = models.IntegerField()
    prev_san = models.IntegerField()

    class Meta:
        managed = False
        db_table = "unit_sanc_desg"



class UnitSancSect(models.Model):
    unit = models.CharField(max_length=12)
    d5 = models.CharField(max_length=12)
    sect = models.CharField(max_length=12)
    s_id = models.CharField(max_length=12)
    s_code = models.CharField(max_length=12)
    s_name = models.CharField(max_length=40)
    s_type = models.CharField(max_length=12)
    s_location = models.CharField(max_length=12)
    s_rank = models.IntegerField()
    s_year_id = models.CharField(max_length=12)
    tot = models.IntegerField()
    req = models.IntegerField()
    san = models.IntegerField()
    sns_comment = models.TextField(verbose_name="Comments", max_length=200, blank=True)

    class Meta:
        managed = False
        db_table = "unit_sanc_sect"

# class AdditionCat(models.Model):
#     ac_value = models.CharField(verbose_name="value", max_length=15, primary_key=True)
#     ac_name = models.CharField(verbose_name="name", max_length=40)
#
#     def __str__(self):
#         return self.ac_name
#
#
# class TerminationCat(models.Model):
#     tc_value = models.CharField(verbose_name="value", max_length=15, primary_key=True)
#     tc_name = models.CharField(verbose_name="name", max_length=40)
#
#     def __str__(self):
#         return self.tc_name


#
# class Addition(models.Model):
#     a_eis = models.OneToOneField(Employee, verbose_name="Employee", on_delete=models.CASCADE)
#     a_reason = models.ForeignKey(AdditionCat, verbose_name="Category", on_delete=models.CASCADE)
#     a_date = models.DateField(verbose_name="Addition Date")
#     a_edit_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Edited by")
#     a_edit_on = models.DateTimeField(verbose_name="Edit time")
#     a_unit = models.ForeignKey(Unit, verbose_name="On-Roll Unit", on_delete=models.CASCADE)
#
#
# class Termination(models.Model):
#     t_eis = models.OneToOneField(Employee, verbose_name="Employee", on_delete=models.CASCADE)
#     t_reason = models.ForeignKey(TerminationCat, verbose_name="Category", on_delete=models.CASCADE)
#     t_date = models.DateField(verbose_name="Termination Date")
#     t_edit_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Edited by")
#     t_edit_on = models.DateTimeField(verbose_name="Edit time")
#     t_unit = models.ForeignKey(Unit, verbose_name="On-Roll Unit", on_delete=models.CASCADE)
#
#
# transfer_choices = (("Transfer_In", "Transfer In"), ("Transfer_Out", "Transfer Out"))
#
#
# class TransferHistory(models.Model):
#     th_eis = models.ForeignKey(Employee, verbose_name="Employee", on_delete=models.CASCADE)
#     # th_old_unit = models.ForeignKey(Unit,verbose_name="Previous Unit", on_delete=models.CASCADE)
#     th_unit = models.ForeignKey(Unit, verbose_name="On-Roll Unit", related_name='th_unit', on_delete=models.CASCADE)
#     th_prev_unit = models.ForeignKey(Unit, verbose_name="On-Roll Unit", related_name='th_prev_unit',
#                                      on_delete=models.CASCADE)
#     # th_category = models.CharField(verbose_name="Category",choices=transfer_choices, default="Transfer_In", max_length=20)
#     th_date = models.DateField(verbose_name="Tranfer Date")
#     th_edit_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Edited by")
#     th_edit_on = models.DateTimeField(verbose_name="Edit time")
#
#     class Meta:
#         unique_together = ('th_eis', 'th_unit', 'th_prev_unit', 'th_date')
#
#
# class PromotionHistory(models.Model):
#     p_eis = models.ForeignKey(Employee, verbose_name="Employee", on_delete=models.CASCADE)
#     p_desg = models.ForeignKey(Desg, verbose_name="Designation", on_delete=models.CASCADE)
#     p_date = models.DateField(verbose_name="Promote Date")
#     p_edit_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Edited by")
#     p_edit_on = models.DateTimeField(verbose_name="Edit time")
#     p_unit = models.ForeignKey(Unit, verbose_name="On-Roll Unit", on_delete=models.CASCADE)
#
#     class Meta:
#         unique_together = ('p_eis', 'p_desg',)
#
#
# class Choices(models.Model):
#     c_value = models.CharField(verbose_name="value", max_length=15, primary_key=True)
#     c_name = models.CharField(verbose_name="name", max_length=40)
#     c_category = models.CharField(verbose_name="category", max_length=40)
