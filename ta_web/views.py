from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from .models import Document, Profile
from .forms import CreateUserForm, AddDocumentForm


def homepage(request):
    return render(request, 'ta_web/home.html')


@login_required
def show_entries(request):

    documents = Document.objects.all().filter(
        user=request.user
    ).order_by(
        'date_submitted'
    )

    return render(request, 'ta_web/show_documents.html', {'documents': documents})


@login_required
def entry_detail(request, pk):

    # try:
    #     document = Document.objects.get(pk=pk)
    # except Document.DoesNotExist:
    #     raise Http404('Document DOES NOT EXIST')

    document = get_object_or_404(Document, pk=pk)

    return render(request, 'ta_web/document_detail.html', {'document': document})


def add_document(request):

    if request.method == 'POST':

        form = AddDocumentForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data
            doc = Document.objects.create(user = request.user)
            doc.title = data['title']
            doc.text = data['text']
            doc.submit()
            doc.save()

            return redirect('ta_web:entry_detail', pk=doc.pk)

    else:

        form = AddDocumentForm()

    return render(request, 'ta_web/add_document.html', {'form': form})


##################################################################
#
# User views...
#
# - user registration
# - logout redirect
#
##################################################################

def register(request):

    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():

            user = form.save()
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password1']
            )
            login(request, user)

            return redirect('ta_web:homepage')

        else:

            return render(request, 'registration/register.html', {'form': form})

    else:

        form = CreateUserForm()

        return render(request, 'registration/register.html', {'form': form})


def logout_message(request):

    return render(request, 'ta_web/logout_message.html')

def about(request):

    return render(request, 'ta_web/about.html')
