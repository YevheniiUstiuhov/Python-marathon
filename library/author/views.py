from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .models import Author


def author_list(request):
    authors = Author.objects.all()
    context = {'authors': authors}
    return render(request, 'author/author_list.html', context)


@login_required(login_url='login/')
@staff_member_required
def author_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        if not name:
            messages.error(request, 'Name is required.')
        else:
            author = Author.objects.create(name=name, surname=surname)
            messages.success(request, f'{author.name} has been created.')
            return redirect('author_list')
    return render(request, 'author/author_create.html')


@login_required(login_url='login/')
@staff_member_required
def author_delete(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    if author.books.exists():
        messages.error(request, f"{author.name} cannot be deleted because they're associated with books.")
        return redirect('author_list')
    author.delete()
    messages.success(request, f"{author.name} has been deleted.")
    return redirect('author_list')
