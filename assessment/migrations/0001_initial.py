# Generated by Django 3.0.4 on 2020-03-06 07:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UnitSancDesg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=12)),
                ('d5', models.CharField(max_length=12)),
                ('idx', models.CharField(max_length=12)),
                ('u_id', models.CharField(max_length=12)),
                ('u_name', models.CharField(max_length=12)),
                ('u_type', models.CharField(max_length=12)),
                ('u_code', models.CharField(max_length=12)),
                ('u_status', models.CharField(max_length=12)),
                ('u_area_id', models.CharField(max_length=12)),
                ('d_id', models.CharField(max_length=12)),
                ('d_code', models.CharField(max_length=12)),
                ('d_name', models.CharField(max_length=40)),
                ('d_grade', models.CharField(max_length=12)),
                ('d_gdesig', models.CharField(max_length=12)),
                ('d_gcode', models.IntegerField()),
                ('d_rank', models.IntegerField()),
                ('d_cadre', models.CharField(max_length=12)),
                ('d_discp', models.CharField(max_length=40)),
                ('d_promo', models.CharField(max_length=12)),
                ('d_year_id', models.CharField(max_length=12)),
                ('e_unit', models.CharField(max_length=12)),
                ('e_dscd', models.CharField(max_length=12)),
                ('e_dcd5', models.CharField(max_length=12)),
                ('male', models.IntegerField()),
                ('female', models.IntegerField()),
                ('tot', models.IntegerField()),
                ('retr1', models.IntegerField()),
                ('retr2', models.IntegerField()),
                ('req', models.IntegerField()),
                ('san', models.IntegerField()),
                ('acde', models.CharField(max_length=12)),
                ('a_name', models.CharField(max_length=12)),
                ('a_order', models.IntegerField()),
                ('comment', models.TextField(blank=True, max_length=200, verbose_name='Comments')),
            ],
            options={
                'db_table': 'unit_sanc_desg',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UnitSancSect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=12)),
                ('d5', models.CharField(max_length=12)),
                ('sect', models.CharField(max_length=12)),
                ('s_id', models.CharField(max_length=12)),
                ('s_code', models.CharField(max_length=12)),
                ('s_name', models.CharField(max_length=40)),
                ('s_type', models.CharField(max_length=12)),
                ('s_location', models.CharField(max_length=12)),
                ('s_rank', models.IntegerField()),
                ('s_year_id', models.CharField(max_length=12)),
                ('tot', models.IntegerField()),
                ('req', models.IntegerField()),
                ('san', models.IntegerField()),
                ('sns_comment', models.TextField(blank=True, max_length=200, verbose_name='Comments')),
            ],
            options={
                'db_table': 'unit_sanc_sect',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('a_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('a_name', models.CharField(max_length=20)),
                ('a_order', models.IntegerField()),
                ('a_code', models.CharField(default='', max_length=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Desg',
            fields=[
                ('d_id', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='Desg Code')),
                ('d_code', models.CharField(max_length=7, verbose_name='DSCD')),
                ('d_name', models.CharField(max_length=40)),
                ('d_grade', models.CharField(max_length=10)),
                ('d_gdesig', models.CharField(max_length=40)),
                ('d_gcode', models.IntegerField()),
                ('d_rank', models.IntegerField()),
                ('d_cadre', models.CharField(choices=[('CD', 'CD'), ('XCD', 'XCD')], default='CD', max_length=10)),
                ('d_discp', models.CharField(max_length=20, verbose_name='Discpline')),
                ('d_promo', models.CharField(max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('y_code', models.IntegerField(primary_key=True, serialize=False)),
                ('y_name', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('u_id', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='Unit Code')),
                ('u_name', models.CharField(max_length=20)),
                ('u_type', models.CharField(max_length=2)),
                ('u_code', models.CharField(max_length=7)),
                ('u_status', models.CharField(max_length=20, null=True)),
                ('u_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessment.Area')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('s_id', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('s_code', models.CharField(max_length=7, verbose_name='Code')),
                ('s_name', models.CharField(max_length=40)),
                ('s_type', models.CharField(choices=[('OC', 'OC'), ('UG', 'UG'), ('CU', 'CU')], max_length=2)),
                ('s_location',
                 models.CharField(choices=[('Underground', 'Underground'), ('Surface', 'Surface')], max_length=15)),
                ('s_rank', models.IntegerField()),
                ('s_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessment.Year')),
            ],
            options={
                'unique_together': {('s_code', 's_year')},
            },
        ),
        migrations.CreateModel(
            name='SanctionSection',
            fields=[
                ('sns_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('sns_d5', models.CharField(max_length=5)),
                ('sns_req', models.IntegerField()),
                ('sns_san', models.IntegerField()),
                ('sns_comment', models.TextField(blank=True, max_length=200, verbose_name='Comments')),
                ('sns_sect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessment.Section')),
                ('sns_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessment.Unit')),
            ],
        ),
        migrations.CreateModel(
            name='Sanction',
            fields=[
                ('sn_id', models.CharField(max_length=24, primary_key=True, serialize=False)),
                ('sn_req', models.IntegerField()),
                ('sn_san', models.IntegerField()),
                ('sn_comment', models.TextField(blank=True, max_length=200, verbose_name='Comments')),
                ('sn_dscd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessment.Desg')),
                ('sn_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessment.Unit')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('e_id', models.CharField(max_length=13, primary_key=True, serialize=False, verbose_name='EIS No/ID')),
                ('e_eis', models.CharField(max_length=8, verbose_name='EIS No')),
                ('e_regsno', models.CharField(blank=True, max_length=15, null=True, verbose_name='Token No')),
                ('e_name', models.CharField(max_length=40, verbose_name='Full Name')),
                ('e_dob', models.DateField(blank=True, null=True, verbose_name='Date of Retirement')),
                ('e_gender',
                 models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=10,
                                  verbose_name='Gender')),
                ('e_doj', models.DateField(blank=True, null=True, verbose_name='Service Join Date')),
                ('e_dot', models.DateField(blank=True, null=True, verbose_name='Service Termination Date')),
                ('e_status',
                 models.CharField(choices=[('In_service', 'In_service'), ('Not_in_service', 'Not_in_service')],
                                  default='In_service', max_length=20, verbose_name='Service Status')),
                ('e_dop', models.DateField(blank=True, null=True, verbose_name='Last promo. Date')),
                ('e_comments', models.TextField(blank=True, max_length=200, null=True, verbose_name='Comments')),
                ('e_desg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='desg_code',
                                             to='assessment.Desg', verbose_name='Designation')),
                ('e_sect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessment.Section')),
                ('e_unit_roll',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='e_unit_roll',
                                   to='assessment.Unit', verbose_name='On-Roll Unit')),
                ('e_unit_work',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='e_unit_work',
                                   to='assessment.Unit', verbose_name='Working Unit')),
                ('e_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessment.Year')),
            ],
        ),
        migrations.AddField(
            model_name='desg',
            name='d_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessment.Year'),
        ),
        migrations.AddField(
            model_name='area',
            name='a_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessment.Year'),
        ),
        migrations.AlterUniqueTogether(
            name='desg',
            unique_together={('d_code', 'd_year')},
        ),
        migrations.AlterUniqueTogether(
            name='area',
            unique_together={('a_code', 'a_year')},
        ),
    ]