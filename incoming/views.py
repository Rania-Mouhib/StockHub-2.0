from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Article
from inventory.models import Type, Model
from django.http import JsonResponse

@login_required
def incoming(request):
    items = Article.objects.all().order_by('id')
    return render(request, 'incoming/index.html', {'incoming_stock': items})

@login_required
def new(request):
    if request.method == 'POST':
        type_id = request.POST.get('type')
        model_id = request.POST.get('model')
        quantity = request.POST.get('quantity')
        serial_number = request.POST.get('serial_number', None)
        description = request.POST.get('description', None)
        vnc = request.POST.get('vnc')
        vnc = int(vnc) if vnc else None
        bci = request.POST.get('bci', None)
        plant = request.POST.get('plant')
        date_in = request.POST.get('date_in')
        rack = request.POST.get('rack')
        pilot = request.POST.get('pilot', None)
        comment = request.POST.get('comment', None)

        # Validation
        errors = {}
        if not type_id or not model_id or not quantity or not rack:
            errors['required'] = 'Please fill out all required fields.'

        if errors:
            return render(request, 'incoming/new.html', {'errors': errors, 'form_data': request.POST})

        # Fetch related type and model
        try:
            article_type = Type.objects.get(id=type_id)
        except Type.DoesNotExist:
            errors['type'] = 'Invalid type selected.'
            return render(request, 'incoming/new.html', {'errors': errors, 'form_data': request.POST})

        try:
            article_model = Model.objects.get(id=model_id)
        except Model.DoesNotExist:
            errors['model'] = 'Invalid model selected.'
            return render(request, 'incoming/new.html', {'errors': errors, 'form_data': request.POST})

        # Create and save new Article instance
        article = Article(
            type=article_type,
            model=article_model,
            quantity=quantity,
            serial_number=serial_number,
            description=description,
            vnc=vnc,
            bci=bci,
            plant=plant,
            date_in=timezone.now(),
            pilot=pilot,
            rack=rack,
            comment=comment
        )
        article.save()
        return redirect('incoming:incoming')

    # Fetching types and models for the form
    types = Type.objects.all()
    models = Model.objects.all()
    return render(request, 'incoming/new.html', {'types': types, 'models': models})


@login_required
def update_models(request):
    type_id = request.GET.get('type_id')
    models = Model.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse({'models': list(models)})


@login_required
def graph(request):
    # Récupérer tous les articles de stock
    items = Article.objects.all().order_by('date_in')
    
    # Préparer les données pour le graphique
    labels = [item.model.name for item in items]  # Utiliser le modèle au lieu du type pour les labels
    quantities = [item.quantity for item in items]  # Quantités des articles

    context = {
        'labels': labels,
        'quantities': quantities,
    }

    return render(request, 'incoming/graph.html', context)


@login_required
def edit_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        type_id = request.POST.get('type')
        model_id = request.POST.get('model')
        quantity = request.POST.get('quantity')
        serial_number = request.POST.get('serial_number', None)
        description = request.POST.get('description', None)
        vnc = request.POST.get('vnc')
        vnc = int(vnc) if vnc else None
        bci = request.POST.get('bci', None)
        plant = request.POST.get('plant')
        date_in = request.POST.get('date_in')
        pilot = request.POST.get('pilot', None)
        rack = request.POST.get('rack')
        comment = request.POST.get('comment', None)

        # Validation
        errors = {}
        if not type_id or not model_id or not quantity or not rack:
            errors['required'] = 'Please fill out all required fields.'

        if errors:
            return render(request, 'incoming/edit_article.html', {'article': article, 'errors': errors})

        # Fetch related type and model
        article_type = get_object_or_404(Type, id=type_id)
        article_model = get_object_or_404(Model, id=model_id)

        # Update and save the article
        article.type = article_type
        article.model = article_model
        article.quantity = quantity
        article.serial_number = serial_number
        article.description = description
        article.vnc = vnc
        article.bci = bci
        article.plant = plant
        article.date_in = timezone.now()
        article.pilot = pilot
        article.rack = rack
        article.comment = comment
        article.save()
        return redirect('incoming:incoming')

    types = Type.objects.all()
    models = Model.objects.all()
    return render(request, 'incoming/edit_article.html', {'article': article, 'types': types, 'models': models})

@login_required
def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        article.delete()
        return redirect('incoming:incoming')
    return render(request, 'incoming/delete_confirm.html', {'article': article})
