from django.shortcuts import render, redirect
from .models import Note


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        # TAREFA: Utilize o title e content para criar um novo Note no banco de dados

        Note.objects.create(title = title, content = content)

        return redirect('index')
    else:
        all_notes = Note.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes})

def delete(request, id):
    note = Note.objects.get(id=id)
    note.delete()
    return redirect('index')

def update(request, id):
    note = Note.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST.get('titulo').strip()
        content = request.POST.get('detalhes').strip()
        note.title = title
        note.content = content
        if not title or not content:
            return render(request, 'notes/update.html', {
                                "note": note,
                                "error": "Preencha o título e o conteúdo da anotação."
            })
        else:
            note.save()
            return redirect('index')
    else:
        return render(request, 'notes/update.html', {'note': note})