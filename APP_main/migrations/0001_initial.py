# Generated by Django 4.2.4 on 2023-08-13 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('App_auth', '0002_alter_doctorprofilemodel_full_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckupModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eye_vision', models.FileField(upload_to='eye_vision/')),
                ('predicted_result', models.CharField(max_length=500)),
                ('doc_comment', models.TextField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('assigned_doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='assigned_doc', to='App_auth.doctorprofilemodel')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checked_patient', to='App_auth.patientprofilemodel')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]