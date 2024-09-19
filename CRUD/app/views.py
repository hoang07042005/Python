from django.shortcuts import redirect, render, get_object_or_404
from .models import Member

def index(request):
    mem = Member.objects.all()
    return render(request, 'index.html', {'mem': mem})

# def add(request):
#     return render(request, 'add.html')

def addrec(request):
    if request.method == 'POST':
        x = request.POST.get('first')
        y = request.POST.get('last')
        mem = Member(firstname=x, lastname=y)
        
        if 'image' in request.FILES:
            mem.image = request.FILES['image']
        
        mem.save()
        return redirect("/")

def delete(request, id):
    mem = get_object_or_404(Member, id=id)
    mem.delete()
    return redirect("/")

def update(request, id):
    mem = get_object_or_404(Member, id=id)
    return render(request, 'update.html', {'mem': mem})

def uprec(request, id):
    if request.method == 'POST':
        x = request.POST.get('first')
        y = request.POST.get('last')
        mem = get_object_or_404(Member, id=id)
        mem.firstname = x
        mem.lastname = y
        
        if 'image' in request.FILES:
            mem.image = request.FILES['image']
        
        mem.save()
        return redirect("/")
