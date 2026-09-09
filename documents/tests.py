import os
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from cryptography.fernet import Fernet
from accounts.models import CustomUser
from patients.models import PatientProfile
from .models import EncryptedDocument

TEST_KEY = Fernet.generate_key().decode()


@override_settings()
class EncryptedDocumentTests(TestCase):
    def setUp(self):
        os.environ["DOCUMENT_ENCRYPTION_KEY"] = TEST_KEY
        self.patient_user = CustomUser.objects.create_user(
            username="pat4", password="pw12345", role=CustomUser.Role.PATIENT, is_approved=True
        )
        self.profile = PatientProfile.objects.create(user=self.patient_user)

    def test_document_is_encrypted_on_disk_and_decrypts_correctly(self):
        original = b"sensitive scan result content"
        doc = EncryptedDocument(patient=self.profile, uploaded_by=self.patient_user, doc_type="LAB_REPORT")
        doc.set_content(SimpleUploadedFile("result.txt", original))
        doc.save()

        stored_bytes = doc.encrypted_file.read()
        self.assertNotEqual(stored_bytes, original, "File must not be stored in plaintext")

        decrypted = doc.get_content()
        self.assertEqual(decrypted, original)
