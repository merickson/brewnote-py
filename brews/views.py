from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Batch, Fermentation

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
    return render(request, 'brews/addbatch.html', {})

def newbatch(request):
    batch = Batch.objects.create(
        name=request.POST['batch-name'],
        num=request.POST['batch-num'],
    )

    return HttpResponseRedirect(reverse('brewdetail', args=(batch.id,)))

