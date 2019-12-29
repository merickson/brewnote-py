from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Batch, Fermentation
from .forms import BatchForm, FermentationForm

def index(request):
    batches = Batch.objects.order_by('num')
    context = {
        'batch_list': batches,
    }
    return render(request, 'brews/index.html', context)

def brewdetail(request, brew_id):
    batch = get_object_or_404(Batch, pk=brew_id)
    fermentations = Fermentation.objects.filter(batch__exact=batch.pk).order_by('startdate')
    ctx = {
        'batch': batch,
        'fermentations': fermentations,
    }
    return render(request, 'brews/batchdetail.html', ctx)

def addbatch(request):
    if request.method == "POST":
        form = BatchForm(request.POST)
        if form.is_valid():
            batch = form.save()
                
            return HttpResponseRedirect(reverse('brewdetail', args=(batch.id,)))

    else:
        form = BatchForm()
        
    return render(request, 'brews/addbatch.html', {'form': form})

def addfermentation(request, brew_id):
    batch = get_object_or_404(Batch, pk=brew_id)
    if request.method == "POST":
        form = FermentationForm(request.POST)
        if form.is_valid():
            ferm = form.save(commit=False)
            ferm.batch = batch
            ferm.save()

            return HttpResponseRedirect(reverse('brewdetail', args=(batch.id,)))

    else:
        form = FermentationForm()

    return render(request, 'brews/addfermentation.html', {'batch': batch, 'form': form})
        
