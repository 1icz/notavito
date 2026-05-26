from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Ad, Category
from .forms import AdForm

def index(request):
    return render(request, 'index.html')

def ad_list(request):
    category_slug = request.GET.get('category')
    query = request.GET.get('q')
    ads = Ad.objects.filter(is_active=True).select_related('category', 'author')
    categories = Category.objects.all()

    if category_slug:
        ads = ads.filter(category__slug=category_slug)
    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(text__icontains=query))

    return render(request, 'ads/ad_list.html', {
        'ads': ads,
        'categories': categories,
        'selected_category': category_slug,
        'query': query,
    })

def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk, is_active=True)
    ad.views_count += 1
    ad.save()
    return render(request, 'ads/ad_detail.html', {'ad': ad})

@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            messages.success(request, 'Объявление создано!')
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form, 'title': 'Создать объявление'})

@login_required
def ad_edit(request, pk):
    ad = get_object_or_404(Ad, pk=pk, author=request.user)
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление обновлено!')
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form, 'title': 'Редактировать объявление'})

@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk, author=request.user)
    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Объявление удалено')
        return redirect('my_ads')
    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})

@login_required
def my_ads(request):
    ads = Ad.objects.filter(author=request.user)
    return render(request, 'ads/my_ads.html', {'ads': ads})