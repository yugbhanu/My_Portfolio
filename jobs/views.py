from django.db.models import fields
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment, Job
from django.views.generic import CreateView

from .forms import CommentForm

# Create your views here.

def homepage(request):
    jobs = Job.objects
    return render(request,'jobs/home.html', {'jobs':jobs})

def detail(request, job_id):
    job_detail = get_object_or_404(Job, pk=job_id)
    return render(request,'jobs/detail.html', {'job':job_detail})

# def comment(job_id, request):
#     comments = Comment.objects
#     return render(request,'jobs/<int:job_id>/comment.html', {'comments':comments})

def comment(request,job_id):
    job_detail = get_object_or_404(Job, id=job_id)
    comments = Comment.objects.filter( post=job_detail).order_by('-id')
    
    if request.method == 'POST':
       
        form = CommentForm(request.POST or None)
       
        if form.is_valid():

            form.instance.post_id=request.POST.get(id)
            body = request.POST.get('body', '')
            name = request.POST.get('name', '')
            comment = Comment.objects.create(  post=job_detail, name=name, body=body)
            form.save()
            # next = request.POST.get('next', '/')
            return redirect(request.META.get('HTTP_REFERER'))

    
    else:
        form = CommentForm()
    
    context = {
        'job_detail':job_detail,
        'comments':comments,
        'form':form,
    }

    return render(request, 'jobs/add_comment.html',context)

class AddCommentView(CreateView):
    model = Comment
    template_name = 'add_comment.html'
    fields = '__all__'