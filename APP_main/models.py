from django.db import models

# Create your models here.
from App_auth.models import PatientProfileModel, DoctorProfileModel


class CheckupModel(models.Model):
    patient = models.ForeignKey(PatientProfileModel, on_delete=models.CASCADE, related_name="checked_patient")
    assigned_doctor = models.ForeignKey(DoctorProfileModel, on_delete=models.DO_NOTHING, related_name="assigned_doc",
                                        blank=True, null=True)
    eye_vision = models.FileField(upload_to='eye_vision/')
    predicted_result = models.CharField(max_length=500)
    doc_comment = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Eye Checkup for {self.patient.full_name} - {self.date}'

    class Meta:
        ordering = ['-date']
