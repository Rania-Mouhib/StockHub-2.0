from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Type, Model
from .forms import TypeForm, ModelForm
from django.http import JsonResponse

@login_required
def type_list(request):
    types = Type.objects.all()
    return render(request, 'inventory/type_list.html', {'types': types})

@login_required
def add_type(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:type_list')
    else:
        form = TypeForm()
    return render(request, 'inventory/add_type.html', {'form': form})

@login_required
def edit_type(request, pk):
    type_instance = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        form = TypeForm(request.POST, instance=type_instance)
        if form.is_valid():
            form.save()
            return redirect('inventory:type_list')
    else:
        form = TypeForm(instance=type_instance)
    return render(request, 'inventory/edit_type.html', {'form': form})

@login_required
def delete_type(request, pk):
    type_instance = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        type_instance.delete()
        return redirect('inventory:type_list')
    return render(request, 'inventory/confirm_delete.html', {'type': type_instance})

@login_required
def model_list(request):
    models = Model.objects.all()
    return render(request, 'inventory/model_list.html', {'models': models})

@login_required
def add_model(request):
    if request.method == 'POST':
        form = ModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:model_list')
    else:
        form = ModelForm()
    return render(request, 'inventory/add_model.html', {'form': form})

@login_required
def edit_model(request, pk):
    model = get_object_or_404(Model, pk=pk)
    if request.method == 'POST':
        form = ModelForm(request.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect('inventory:model_list')
    else:
        form = ModelForm(instance=model)
    return render(request, 'inventory/edit_model.html', {'form': form, 'model': model})

@login_required
def delete_model(request, pk):
    model = get_object_or_404(Model, pk=pk)
    if request.method == 'POST':
        model.delete()
        return redirect('inventory:model_list')
    return render(request, 'inventory/delete_model.html', {'model': model})


