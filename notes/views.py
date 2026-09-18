from django.shortcuts import render, redirect
from .models import Note, Tag

def get_tags_from_text(tags_text):
    tag_names = [
        name.strip().lower()
        for name in tags_text.split(',')
        if name.strip()
    ]

    tag_objects = []

    for tag_name in tag_names:
        tag, created = Tag.objects.get_or_create(
            name=tag_name
        )
        tag_objects.append(tag)

    return tag_objects

def index(request):
    if request.method == 'POST':
        title = (request.POST.get('titulo') or '').strip()
        content = (request.POST.get('detalhes') or '').strip()
        tags_text = (request.POST.get('tags') or '').strip()

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
                    'tags_text': tags_text,
                }
            )

        note = Note.objects.create(
            title=title,
            content=content
        )

        tag_objects = get_tags_from_text(tags_text)

        note.tags.set(tag_objects)

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
        tags_text = (request.POST.get('tags') or '').strip()

        if not title or not content:
            return render(
                request,
                'notes/update.html',
                {
                    'note': note,
                    'tags_text': tags_text,
                    'error': 'Preencha o título e o conteúdo da anotação.',
                }
            )

        note.title = title
        note.content = content
        note.save()

        tag_objects = get_tags_from_text(tags_text)

        note.tags.set(tag_objects)

        return redirect('index')

    tags_text = ', '.join(
        tag.name
        for tag in note.tags.all()
    )

    return render(
        request,
        'notes/update.html',
        {
            'note': note,
            'tags_text': tags_text,
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
    notes = Note.objects.filter(tags=tag)

    return render(
        request,
        'notes/tag.html',
        {
            'tag': tag,
            'notes': notes,
        }
    )