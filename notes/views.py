from django.shortcuts import render, redirect
from .models import Note, Tag


def index(request):
    if request.method == 'POST':
        title = (request.POST.get('titulo') or '').strip()
        content = (request.POST.get('detalhes') or '').strip()
        tag_name = (request.POST.get('tag') or '').strip().lower()

        if not title or not content:
            all_notes = Note.objects.all()

            return render(
                request,
                'notes/index.html',
                {
                    'notes': all_notes,
                    'error': 'Preencha o título e o conteúdo da anotação.',
                    'title': title,
                    'content': content,
                    'tag_name': tag_name,
                }
            )

        tag = None

        if tag_name:
            tag = Tag.objects.filter(name__iexact=tag_name).first()

            if tag is None:
                tag = Tag.objects.create(name=tag_name)

        Note.objects.create(
            title=title,
            content=content,
            tag=tag
        )

        return redirect('index')

    all_notes = Note.objects.all()

    return render(
        request,
        'notes/index.html',
        {'notes': all_notes}
    )


def delete(request, id):
    note = Note.objects.get(id=id)
    note.delete()

    return redirect('index')


def update(request, id):
    note = Note.objects.get(id=id)

    if request.method == 'POST':
        title = (request.POST.get('titulo') or '').strip()
        content = (request.POST.get('detalhes') or '').strip()
        tag_name = (request.POST.get('tag') or '').strip().lower()

        if not title or not content:
            note.title = title
            note.content = content

            return render(
                request,
                'notes/update.html',
                {
                    'note': note,
                    'tag_value': tag_name,
                    'error': 'Preencha o título e o conteúdo da anotação.',
                }
            )

        if tag_name:
            tag = Tag.objects.filter(name__iexact=tag_name).first()

            if tag is None:
                tag = Tag.objects.create(name=tag_name)

            note.tag = tag
        else:
            note.tag = None

        note.title = title
        note.content = content
        note.save()

        return redirect('index')

    tag_value = note.tag.name if note.tag else ''

    return render(
        request,
        'notes/update.html',
        {
            'note': note,
            'tag_value': tag_value,
        }
    )


def tags(request):
    all_tags = Tag.objects.all().order_by('name')

    return render(
        request,
        'notes/tags.html',
        {'tags': all_tags}
    )


def tag(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    notes = Note.objects.filter(tag=tag)

    return render(
        request,
        'notes/tag.html',
        {
            'tag': tag,
            'notes': notes,
        }
    )