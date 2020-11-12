from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q

from django.views.generic.detail import DetailView
from django.http.response import Http404, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from enrollment.models import (Student, Teacher, classrooms, Enroll_Courses)
from enrollment.forms import Register_Form

def register(request):
    if request.method == 'POST':
        form = Register_Form(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            email_filed = User.objects.filter(email=email)
            if email_filed:
                messages.info("Email id exists")
            else:
                create_user = User.objects.create_user(email=email, username=username, password=password)
                create_user.is_active = True
                create_user.save()
                send_mail(
                    'Subject here',
                    'Here is the message.',
                    'pkbhanja07@gmail.com',
                    ['prakashbhanja9@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, "Registered Successfully")
                return HttpResponseRedirect(redirect_to='')
                # return HttpResponse("Added Successfully")
        else:
            pass
            # print(form.errors)

    else:
        form = Register_Form()
    context = {'form': form}
    template = 'enrollment/register.html'
    return render(request, template, context)


def home_page(request):
    classes = classrooms.objects.all()
    context = {'classes': classes}
    template = 'enrollment/home.html'
    return render(request, template, context)

def class_detail(request, pk):
    print("****name attr***", request.GET.get('obj_id'))
    try:
        class_obj = classrooms.objects.get(id=pk)
    except classrooms.DoesNotExists:
        raise Http404
    user = User.objects.get(username=student_session)
    context={'class_obj': class_obj}

    return render(request, 'enrollment/classrooms_detail.html', context)

class Class_Detail(DetailView):
    model = classrooms

@login_required(login_url="/login/")
def enroll_class(request, pk):
    print("****name attr_enrl_cls***", request.GET.get('obj_id'))
    course_id = request.GET.get('obj_id')
    try:
        student_session = request.session.get('user_name')
    except:
        student_session = request.user
    user = User.objects.get(username=student_session)
    print("*******", user.id)
    student_obj = Student.objects.get(id=request.user.student.id)
    class_rm_obj = classrooms.objects.get(id=pk)
    enrolled_cls_obj = Enroll_Courses.objects.filter(
        Q(student_name__user_std = user.id)
        &
         Q(enrolled_class=course_id)
        )
    print("********", enrolled_cls_obj)
    if enrolled_cls_obj:
        messages.warning(request, "Alreday enrolled")
    else:
        if class_rm_obj:
            Enroll_Courses.objects.create(enrolled_class=class_rm_obj, teacher_name=class_rm_obj.teacher,
            student_name = student_obj, is_enrolled=True )
            messages.success(request, "Enrolled Successfully, Thank you")
            return HttpResponseRedirect(redirect_to='/enrolled_class_list')
    return HttpResponseRedirect(redirect_to='/enrolled_class_list')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("***User****",User.objects.filter(Q(username=username)))
        if User.objects.filter(Q(username=username)):
            user = authenticate(request, username=username, password=password)
            print("****uu*****", user.id)
            if Student.objects.filter(user_std=user.id):
                login(request, user)
                request.session['user_name'] = user.username
                return HttpResponseRedirect(redirect_to='/')
            else:
                messages.warning(request, "Only Student can login here")
                return HttpResponseRedirect(redirect_to='/')

        else:

            messages.warning(request, "Provide credentials were not registered")
            return HttpResponseRedirect(redirect_to='/')

    else:
        # messages.warning(request, "Get request")
        pass
    template = 'enrollment/login.html'
    return render(request, template)


def enrolled_class_list(request):
    student = request.session['user_name']
    user = User.objects.get(username=student)
    enroll_class_list = Enroll_Courses.objects.filter(student_name__user_std = user.id)
    context={'enroll_class_list' : enroll_class_list}
    return render(request,'enrollment/enrolled_classes_list.html', context)