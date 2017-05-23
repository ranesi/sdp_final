from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Document
from .forms import AddDocumentForm


@login_required
def show_documents(request):
    documents = Document.objects.filter(
        user=request.user
    ).order_by(
        'date_submitted'
    ).reverse()

    return render(request, 'ta_web/show_documents.html', dict(documents=documents))


@login_required
def document_detail(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)
    return render(request, 'ta_web/document_detail.html', dict(document=document))


@login_required
def add_document(request):
    if request.method == 'POST':

        form = AddDocumentForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            doc = Document.objects.create(user=request.user)
            doc.title = data['title']
            doc.text = data['text']
            doc.submit()  # function defined in models
            doc.save()

            return redirect('ta_web:document_detail', document_pk=doc.pk)

    else:
        form = AddDocumentForm()

    return render(request, 'ta_web/add_document.html', dict(form=form))
