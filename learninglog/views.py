

from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
# Create your views here.
def index(request):
        """The home page for Learning Log."""
   
        return render(request, 'learninglog/index.html')
@login_required
def topics(request):
        """show all topics"""
        topics = Topic.objects.filter(owner=request.user).order_by('date_added')
        context = {'topics': topics}
        return render(request, 'learninglog/topics.html', context)
@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries"""
    topic = Topic.objects.get(id=topic_id)
    #make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learninglog/topic.html', context)
@login_required
def new_topic(request):
    """Add a new topic"""

    if request.method != 'POST':
        #No data submitted; create a blank page
        form = TopicForm()
    else:
        #POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form. is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            form.save()
            return redirect('learninglog:topics')

    #Display a blank or invalid form
    context = {'form': form}
    return render(request, 'learninglog/new_topic.html',context)
    
@login_required
def new_entry(request, topic_id):
    """Add a new entry"""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        #No data submitted; create a blank page
        form = TopicForm()
    else:
        #POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form. is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learninglog:topic', topic_id=topic_id )

    #Display a blank or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'learninglog/new_entry.html',context)
@login_required
def edit_entry(request, entry_id):

    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learninglog:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learninglog/edit_entry.html', context)