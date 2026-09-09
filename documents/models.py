from django.conf import settings
from django.db import models
from patients.models import PatientProfile
from .crypto_utils import encrypt_bytes, decrypt_bytes


def encrypted_upload_path(instance, filename):
    return f"encrypted_documents/{instance.patient_id}/{filename}.enc"


class EncryptedDocument(models.Model):
    """
    Any document (doctor report attachment, scan result, patient-uploaded
    file). Content is encrypted before it touches disk/S3; it is only
    decrypted in memory when explicitly requested by an authorized user.
    """

    class DocType(models.TextChoices):
        SCAN_RESULT = "SCAN_RESULT", "Scan Result"
        LAB_REPORT = "LAB_REPORT", "Lab Report"
        PRESCRIPTION = "PRESCRIPTION", "Prescription"
        OTHER = "OTHER", "Other"

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="documents")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    doc_type = models.CharField(max_length=32, choices=DocType.choices, default=DocType.OTHER)
    original_filename = models.CharField(max_length=255)
    encrypted_file = models.FileField(upload_to=encrypted_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def set_content(self, django_file):
        """Encrypt an incoming UploadedFile and attach it to this instance."""
        from django.core.files.base import ContentFile

        raw = django_file.read()
        encrypted = encrypt_bytes(raw)
        self.original_filename = django_file.name
        self.encrypted_file.save(django_file.name, ContentFile(encrypted), save=False)

    def get_content(self) -> bytes:
        """Decrypt and return the original file bytes. Caller must check permissions first."""
        self.encrypted_file.open("rb")
        try:
            return decrypt_bytes(self.encrypted_file.read())
        finally:
            self.encrypted_file.close()

    def __str__(self):
        return f"{self.doc_type} for {self.patient.user.username}"
