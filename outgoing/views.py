from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article

@login_required
def outgoing(request):
    # Fetch all articles (you can add filtering if needed)
    items = Article.objects.all().order_by('id')
    return render(request, 'outgoing/index.html', {'outgoing_stock': items})

@login_required
def new(request):
    if request.method == 'POST':
        # Handle form submission
        type = request.POST.get('type')
        model = request.POST.get('model')
        quantity = request.POST.get('quantity')
        serial_number = request.POST.get('serial_number')
        description = request.POST.get('description')
        vnc = request.POST.get('vnc')
        vnc = int(vnc) if vnc else None
        bci = request.POST.get('bci')
        plant = request.POST.get('plant')
        date_out = request.POST.get('date_out')  # Changed to date_out
        pilot = request.POST.get('pilot')
        rack = request.POST.get('rack')
        comment = request.POST.get('comment')

        # Simple validation
        errors = {}
        if not type or not model or not quantity or not date_out or not rack:
            errors['required'] = 'Please fill out all required fields.'

        if errors:
            return render(request, 'outgoing/new.html', {'errors': errors, 'form_data': request.POST})

        # Create a new Article instance
        article = Article(
            type=type,
            model=model,
            quantity=quantity,
            serial_number=serial_number,
            description=description,
            vnc=vnc,
            bci=bci,
            plant=plant,
            date_out=date_out,  # Changed to date_out
            pilot=pilot,
            rack=rack,
            comment=comment
        )
        article.save()
        return redirect('outgoing:outgoing')  # Redirect to the outgoing items list

    return render(request, 'outgoing/new.html')

@login_required
def graph(request):
    # Fetch all incoming stock items
    items = Article.objects.all().order_by('date_out')
    
    # Prepare data for the chart
    labels = [item.type for item in items]  # List of types for labels
    quantities = [item.quantity for item in items]  # List of quantities for data
    
    context = {
        'labels': labels,
        'quantities': quantities,
    }
    
    return render(request, 'outgoing/graph.html', context)

@login_required
def edit_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        # Handle form submission and update the article
        type = request.POST.get('type')
        model = request.POST.get('model')
        quantity = request.POST.get('quantity')
        serial_number = request.POST.get('serial_number', None)
        description = request.POST.get('description', None)
        vnc = request.POST.get('vnc')
        vnc = int(vnc) if vnc else None
        bci = request.POST.get('bci', None)
        plant = request.POST.get('plant')
        date_out = request.POST.get('date_out')  
        pilot = request.POST.get('pilot', None)
        rack = request.POST.get('rack')
        comment = request.POST.get('comment', None)

        # Simple validation
        errors = {}
        if not type or not model or not quantity or not date_out or not rack:
            errors['required'] = 'Please fill out all required fields.'

        if errors:
            return render(request, 'outgoing/edit_article.html', {'article': article, 'errors': errors})

        # Update the article
        article.type = type
        article.model = model
        article.quantity = quantity
        article.serial_number = serial_number
        article.description = description
        article.vnc = vnc
        article.bci = bci
        article.plant = plant
        article.date_out = date_out  
        article.pilot = pilot
        article.rack = rack
        article.comment = comment
        article.save()
        return redirect('outgoing:outgoing')  # Redirect to the outgoing items list

    return render(request, 'outgoing/edit_article.html', {'article': article})

@login_required
def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        article.delete()
        return redirect('outgoing:outgoing')  # Redirect to the outgoing list
    return render(request, 'outgoing/delete_confirm.html', {'article': article})
