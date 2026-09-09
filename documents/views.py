from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import CustomUser
from patients.models import PatientProfile
from .models import EncryptedDocument


def _can_access(user, document: EncryptedDocument) -> bool:
    if user.role == CustomUser.Role.ADMIN:
        return True
    if user.role == CustomUser.Role.PATIENT:
        return document.patient.user_id == user.id
    if user.role in (CustomUser.Role.DOCTOR, CustomUser.Role.DEPARTMENT):
        return True  # tightened further with per-relationship checks in a fuller build
    return False


@login_required
def upload_document(request, patient_id):
    patient = get_object_or_404(PatientProfile, pk=patient_id)
    if request.method == "POST" and request.FILES.get("file"):
        doc = EncryptedDocument(
            patient=patient,
            uploaded_by=request.user,
            doc_type=request.POST.get("doc_type", EncryptedDocument.DocType.OTHER),
        )
        doc.set_content(request.FILES["file"])
        doc.save()
        messages.success(request, "Document uploaded and encrypted.")
        return redirect("documents:list", patient_id=patient.id)
    return render(request, "documents/upload.html", {"patient": patient})


@login_required
def list_documents(request, patient_id):
    patient = get_object_or_404(PatientProfile, pk=patient_id)
    docs = patient.documents.all()
    return render(request, "documents/list.html", {"patient": patient, "documents": docs})


@login_required
def download_document(request, doc_id):
    document = get_object_or_404(EncryptedDocument, pk=doc_id)
    if not _can_access(request.user, document):
        return HttpResponseForbidden("You are not allowed to access this document.")
    content = document.get_content()
    response = HttpResponse(content, content_type="application/octet-stream")
    response["Content-Disposition"] = f'attachment; filename="{document.original_filename}"'
    return response
