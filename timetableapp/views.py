import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from . import forms
from . import models
from .forms import ClassCourseForm,ActivityForm,CourseForm,ProfessorForm,SectionClassroomForm,SectionClassroom,ClassForm,AdminSignUpForm,ClassroomForm
from .models import Class,ClassCourse,Classroom,Lecturer,Activity,Course
from django.shortcuts import get_object_or_404
from datetime import datetime


def home_view(request):
    return render(request,'timetableapp/home.html')

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password1"]
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('mainpg')
        else:
            return render(request, 'login.html', {"error": "Invalid username or password."})
    
    return render(request, 'login.html')


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'timetableapp/studentclick.html')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('timetableapp/adminsignup.html')
    
def lecturerclick_view(request):
    if request.user.is_authenticated:
        # return HttpResponseRedirect('afterlogin')
        return render(request,'timetableapp/lecturersignup.html')


def adminsignup_view(request):
    form=forms.AdminSignUpForm()
    if request.method=='POST':
        form=forms.AdminSignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()

            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'timetableapp/adminsignup.html',{'form':form})



def lecturersignup_view(request):
    form = forms.ProfessorForm()
    if request.method == 'POST':
        form = forms.ProfessorForm(request.POST)
        if form.is_valid():
            user = form.save()  # Don't save the form to the database yet
            user.set_password(form.cleaned_data['password'])  # Set the password
            user.save()  # Save the User instance

            # Add the user to the 'LECTURER' group
            my_lecturer_group, created = Group.objects.get_or_create(name='LECTURER')
            my_lecturer_group.user_set.add(user)

            return HttpResponseRedirect('lecturerlogin')

    return render(request, 'timetableapp/lecturersignup.html', {'form': form})

def studentsignup_view(request):
    form1=forms.StudentSignUpForm()
    form2=forms.StudentSignUpForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentSignUpForm(request.POST)
        form2=forms.StudentSignUpForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'timetableapp/studentsignup.html',context=mydict)



def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'timetableapp/adminafterlogin.html')
    elif is_student:
        return render(request,'timetableapp/studentafterlogin.html')
   
    else:
        return render(request, 'timetableapp/lecturerafterlogin.html')




def loginPage(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('selection')
    else:
        
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password= password )
            if user is not None:
                login(request, user)
                return redirect('selection')
            else:
                messages.info(request, 'Username or Password is Incorrect')
                return render(request, 'timetableapp/login.html', context)

        
        return render(request, 'timetableapp/login.html', context)


def LogoutView(request):
    logout(request)
    return redirect('index')

    return render(request, 'timetableapp/register.html', context)


def adminPage(request):
    course = CourseForm()
    professor = ProfessorForm()
    classroom = ClassroomForm()
    section = ClassForm()
    sectioncourse = ClassCourseForm()
    sectionclassroom = SectionClassroomForm()
    activity = ActivityForm()
    context = {

                'course': course,'professor': professor,
                'classroom': classroom, 'section': section,
                'sectioncourse': sectioncourse, 'sectionclassroom': sectionclassroom, 'activity': activity

            }

    return render(request, 'timetableapp/adminPage.html', context)

def lecturerPage(request):
    course = CourseForm()
    professor = ProfessorForm()
    classroom = ClassroomForm()
    section = ClassForm()
    sectioncourse = ClassCourseForm()
    sectionclassroom = SectionClassroomForm()
    activity = ActivityForm()
    context = {

                'course': course,'professor': professor,
                'classroom': classroom, 'section': section,
                'sectioncourse': sectioncourse, 'sectionclassroom': sectionclassroom, 'activity': activity

            }

    return render(request, 'timetableapp/lecturerPage.html', context)


@login_required(login_url='login')
def CourseView(request):
    course = CourseForm()
    context = {'course': course}

    if request.method == 'POST':
        course = CourseForm(request.POST)
        if course.is_valid():
            messages.success(request, 'Course has been added successfully.')
            course.save()
        else:
            messages.success(request, 'Course already exists or you have added wrong attributes.')


    return render(request, 'timetableapp/AddCourse.html', context)

@login_required(login_url='login')
def CourseTable(request):
    course = Course.objects.all()
    context = {'course': course}
    return render(request, 'timetableapp/CourseTable.html', context)

@login_required(login_url='login')
def updateCourseView(request, pk):
    form = Course.objects.get(course_id=pk)
    course = CourseForm(instance=form)
    context = {'course': course}
    if request.method == 'POST':
        course = CourseForm(request.POST, instance=form)
        if course.is_valid():
            course.save()
            return redirect('/course_view')
    return render(request, 'timetableapp/AddCourse.html', context)

@login_required(login_url='login')
def deleteCourse(request, pk):
    delete_course = Course.objects.get(course_id=pk)
    context = {'course_delete': delete_course}
    if request.method == 'POST':
        delete_course.delete()
        return redirect('/course_view')

    return render(request, 'timetableapp/delete.html', context)

@login_required(login_url='login')
def ProfessorView(request):
    professor = ProfessorForm()
    professor1 = Lecturer.objects.all()

    context = {'professor': professor, 'professor1': professor1}
    if request.method == 'POST':
        professor = ProfessorForm(request.POST)
        if professor.is_valid():
            messages.success(request, 'Professor has been added successfully.')
            professor.save()
        else:
            messages.success(request, 'Professor already exists or you have added wrong attributes.')
    return render(request, 'timetableapp/AddProfessor.html', context)


@login_required(login_url='login')
def ProfessorTable(request):
    lecturer = Lecturer.objects.all()
    context = {'lecturer': lecturer}
    return render(request, 'timetableapp/ProfessorTable.html', context)


@login_required(login_url='login')
def updateProfessorView(request, pk):
    professor = Lecturer.objects.get(lecturer_id=pk)
    form = ProfessorForm(instance=professor)
    context = {'form': form}
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            return redirect('add-professor')
    return render(request, 'timetableapp/ViewSection.html', context)

@login_required(login_url='login')
def deleteProfessor(request, pk):
    deleteprofessor = Lecturer.objects.get(lecturer_id=pk)
    context = {'delete': deleteprofessor}
    if request.method == 'POST':
        deleteprofessor.delete()
        return redirect('/professor_view')

    return render(request, 'timetableapp/deleteProfessor.html', context)



@login_required(login_url='login')
def ClassroomView(request):
    classroom = ClassroomForm()
    classes = Classroom.objects.all()
    context = {'classroom': classroom, 'classes': classes}
    if request.method == 'POST':
        classroom = ClassroomForm(request.POST)
        if classroom.is_valid():
            messages.success(request, 'Classroom has been added.')
            classroom.save()
        else:
            messages.error(request, 'Do not enter the same class ID')
    return render(request, 'timetableapp/AddClassroom.html', context)


@login_required(login_url='login')
def ClassroomTable(request):
    classrooms = Classroom.objects.all()
    context = {'classrooms': classrooms}
    return render(request, 'timetableapp/ClassroomTable.html', context)


@login_required(login_url='login')
def updateClassroomView(request, pk):
    classroom = Classroom.objects.get(classroom_id=pk)
    form = ClassroomForm(instance=classroom)
    context = {'form': form}
    if request.method == 'POST':
        form = ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            return redirect('/classroom_view')
    return render(request, 'timetableapp/ViewSection.html', context)


@login_required(login_url='login')
def deleteClassroom(request, pk):
    deleteClassroom = Classroom.objects.get(classroom_id=pk)
    context = {'delete': deleteClassroom}
    if request.method == 'POST':
        deleteClassroom.delete()
        return redirect('classroom-view')

    return render(request, 'timetableapp/deleteClassroom.html', context)


# @login_required(login_url='login')
# def deleteClassroom(request, pk):
#     deleteClassroom = get_object_or_404(Classroom, pk=pk)
#     context = {'deleteClassroom': deleteClassroom}

#     if request.method == 'POST':
#         deleteClassroom.delete()
#         return redirect('/classroom_view')  # Change 'classroom_list' to your actual URL name for the classroom list

#     return render(request, 'timetableapp/deleteClassroom.html', context)


@login_required(login_url='login')
def ClassView(request):
    section = ClassForm()
    sections = Class.objects.all()
    context = {'section': section, 'sections': sections}
    if request.method == 'POST':
        section = ClassForm(request.POST)
        if section.is_valid():  
            messages.success(request, 'Class has been added.')
            section.save()
            return redirect('/add-classcourse')    # add 
        else:
            messages.error(request, 'Do not enter the same class ID')
    return render(request, 'timetableapp/AddClass.html', context)


@login_required(login_url='login')
def ClassCourseView(request):
    sectioncourse = ClassCourseForm()
    sectioncourses = ClassCourse.objects.all()
    #section = Class.objects.get(class_id=id)
    context = {'sectioncourse': sectioncourse, 'sectioncourses': sectioncourses}
    if request.method == 'POST':
        sectioncourse = ClassCourseForm(request.POST)
        if sectioncourse.is_valid():
            messages.success(request, "Course added for class.")
            sectioncourse.save()
        else:
            messages.error(request, 'Can not add duplicate course for class.')
    return render(request, 'timetableapp/AddClassCourse.html', context)

@login_required(login_url='login')
def SectionRoomView(request):
    sectionroom = SectionClassroomForm()
    sectionrooms = SectionClassroom.objects.all()
    context = {'sectionroom': sectionroom, 'sectionrooms': sectionrooms}
    if request.method == 'POST':
        sectionroom == SectionClassroomForm(request.POST)
        if sectionroom.is_valid():
            messages.success(request, "Room added for the class")
            sectionroom.save()
        else:
            messages.error(request, 'Can not add duplicate rooms for a class')
    return render(request, 'timetableapp/AddSectionClassrooms.html', context)

@login_required(login_url='login')
def updateClassView(request, pk):
    section = Class.objects.get(class_id=pk)
    form = ClassForm(instance=section)
    context = {'form': form}
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect('/add-classcourse')
    return render(request, 'timetableapp/ViewClass.html', context)


@login_required(login_url='login')
def deleteClass(request, pk):
    deleteClass = Class.objects.get(class_id=pk)
    context = {'delete': deleteClass}
    if request.method == 'POST':
        deleteActivities(pk)
        deleteCLassCourses(pk)
        deleteSectionClassrooms(pk)
        deleteClass.delete()

        return redirect('class-view')

    return render(request, 'timetableapp/deleteClass.html', context)


def deleteCLassCourses(id):
    ClassCourse.objects.filter(class_id=id).delete()

def deleteSectionClassrooms(id):
    SectionClassroom.objects.filter(class_id=id).delete()




@login_required(login_url='login')
def ClassTable(request):
    sections = Class.objects.all()
    context = {'sections': sections}
    return render(request, 'timetableapp/ClassTable.html', context)


def WeekDayFormView(request):
    weekdayform = WeekDaysForm()
    context = {'form':weekdayform}
    if request.method == 'POST':
        weekdayform = WeekDaysForm(request.POST)
        if weekdayform.is_valid():
            weekdayform.save()
            messages.success(request, 'Class has been added.')
        else:
            messages.error(request, 'Do not enter the same class ID')
    return render(request, 'timetableapp/weekdays.html', context)



class Room:
    def __init__(self):
        self.ID = None
        self.TYPE = None

    #def __init__(self, id, type):
     #   self.ID = id
      #  self.TYPE = type




def AddSchedule(request):
    schedule = ScheduleForm()
    schedules = WeekSchedule.objects.all()
    context = {'schedule': schedule, 'schedules': schedules}
    if request.method == 'POST':
        schedule = ScheduleForm(request.POST)
        if schedule.is_valid():
            messages.success(request, "Schedule Added.")
            schedule.save()
        else:
            messages.error(request, 'Do not enter the same class ID')
    return render(request, 'timetableapp/AddClass.html', context)


@login_required(login_url='login')
def TimeTable(request):
    sections = Class.objects.all()
    context = {'sections': sections}
    return render(request, 'timetableapp/TimeTable.html', context)



@login_required(login_url='login')
def GenerateTimeTable(request, id):
    try:
        section = Class.objects.get(class_id=id)
        sectioncourses = list(ClassCourse.objects.filter(class_id=id))
        sectionrooms = list(SectionClassroom.objects.filter(class_id=id))
        if len(sectioncourses) > 0:
            if len(sectionrooms) > 0:
                if Activity.objects.filter(class_id=id).count() != 0:
                    #Activity.objects.filter(class_id=section.class_id).delete()
                    deleteActivities(id)
                totalDays = len(section.week_day)
                totalRooms = len(sectionrooms)
                workingHours = totalDays * (int(section.end_time) - int(section.start_time))
                # getting class room data
                class_rooms = [Room() for i in range(totalRooms)]
                for i in range(len(sectionrooms)):
                    room = Classroom.objects.get(classroom_id=sectionrooms[i].classroom_id)
                    class_rooms[i].ID = room.classroom_id
                    class_rooms[i].TYPE = room.classroom_type
                    # variable to save index of class room being used
                roomNum = random.randint(0, totalRooms - 1)
                lecDay = 0
                lecStartTime = 0
                DupNum = 0
                for k in range(0, len(sectioncourses)):
                    if DupNum > (workingHours + 5):
                        break
                    try:
                        course: Course = Course.objects.get(course_id=sectioncourses[k].course_id_id)
                    except Course.DoesNotExist:
                        messages.error(request, 'Course not found')
                    else:
                        try:
                            professor = Lecturer.objects.get(professor_id=sectioncourses[k].professor_id_id)
                        except Lecturer.DoesNotExist:
                            messages.error(request, 'Professor not found')
                        else:
                            courseLecs = course.credit_hours
                            lecDuration = course.contact_hours / course.credit_hours
                            j = 0
                            while j < courseLecs:
                                lecFlag = True
                                if DupNum < workingHours + 5:
                                    if DupNum < 5:
                                        lecDay = random.randint(0, totalDays - 1)
                                        lecStartTime = random.randint(section.start_time, section.end_time - 1)
                                        if not lecStartTime <= section.end_time - lecDuration:
                                            lecFlag = False
                                    else:
                                        lecStartTime += 1
                                        if not lecStartTime <= section.end_time - lecDuration:
                                            lecDay = (lecDay + 1) % totalDays
                                            lecStartTime = section.start_time

                                    if lecFlag:
                                        if lecStartTime <= section.end_time - lecDuration:
                                            tot = 0
                                            while course.course_type != class_rooms[roomNum].TYPE or tot < totalRooms:
                                                roomNum = (roomNum + 1) % totalRooms
                                                tot += 1
                                            activityFlag = True
                                            activityID = [section.week_day[lecDay]] * int(lecDuration)
                                            for i in range(int(lecDuration)):
                                                activityID[i] += '-' + str(lecStartTime + i)
                                                # for activity in activities:
                                                if Activity.objects.filter(activity_id=activityID[i],
                                                                        class_id=section.class_id).count() != 0 or \
                                                        Activity.objects.filter(activity_id=activityID[i],
                                                                                professor_id=professor.professor_id).count() != 0 or \
                                                        Activity.objects.filter(activity_id=activityID[i],
                                                                                classroom_id=class_rooms[
                                                                                    roomNum].ID).count() != 0:
                                                    activityFlag = False
                                                    DupNum += 1
                                                # break
                                            if activityFlag:
                                                print('Activity generated')
                                                for i in range(int(lecDuration)):
                                                    newActivity = Activity(activity_id=activityID[i],
                                                                        activity_type='Replaceable',
                                                                        class_id=section.class_id,
                                                                        classroom_id=class_rooms[roomNum].ID,
                                                                        course_id=course.course_id,
                                                                        professor_id=professor.professor_id,
                                                                        day=section.week_day[lecDay],
                                                                        start_time=lecStartTime + i,
                                                                        end_time=lecStartTime + i + 1)
                                                    newActivity.save()
                                                    professor.available_hours = professor.available_hours - 1
                                                    professor.save()
                                                DupNum = 0
                                                j += 1
                                else:
                                    #Activity.objects.filter(class_id=section.class_id).delete()
                                    deleteActivities(id)
                                    messages.error(request, 'Solution does not exist.')
                                    DupNum +=1
                                    break
                messages.success(request, 'Timetable generated')
                #return redirect('timetable/')

            else:
                messages.error(request, 'Classroom does not exist.')
        else:
            messages.error(request, 'Courses does not exist.')
    except Class.DoesNotExist:
        messages.error(request, 'Class does not exist')
    
    
    sections = Class.objects.all()
    context = {'sections': sections}
    return render(request, 'timetableapp/ClassTable.html', context)



def deleteActivities(id):
    activities = list(Activity.objects.filter(class_id=id))
    for activity in activities:
        course = Course.objects.get(course_id=activity.course_id)
        professor = Lecturer.objects.get(professor_id=activity.professor_id)
        professor.available_hours += 1
        professor.save()
    Activity.objects.filter(class_id=id).delete()






@login_required(login_url='login')

def TimeTableView(request, id):
    try:
        # Fetching required data
        section = Class.objects.get(class_id=id)
        print(section.activity_set.all())
        courses = Course.objects.all()
        lecturers = Lecturer.objects.all()
        activities = Activity.objects.filter(class_id=id)
        rooms = Classroom.objects.all()

        # Adjust the format based on the actual format in your database
        time_format = '%I:%M %p'  # Use '%H:%M' if times are in 24-hour format
        
        try:
            start_time = datetime.strptime(section.start_time, time_format)
            end_time = datetime.strptime(section.end_time, time_format)
        except ValueError:
            messages.error(request, 'Time format error in class schedule. Please ensure times are in 12-hour format (e.g., 01:00 PM).')
            return render(request, 'timetableapp/TimeTable.html', {
                'section': section, 
                'courses': courses, 
                'lecturers': lecturers, 
                'rooms': rooms, 
                'activities': activities
            })

        
        time_range = (end_time - start_time).seconds // 3600
        time = [start_time + timedelta(hours=i) for i in range(time_range)]
        time_slot = [f"{(start_time + timedelta(hours=i)).strftime('%I:%M %p')} - {(start_time + timedelta(hours=i + 1)).strftime('%I:%M %p')}" for i in range(time_range)]

        context = {
            'section': section, 
            'courses': courses, 
            'lecturers': lecturers, 
            'rooms': rooms, 
            'activities': activities, 
            'time': time, 
            'time_slot': time_slot
        }
        return render(request, 'timetableapp/TimeTable.html', context)
    
    except Class.DoesNotExist:
        messages.error(request, 'Class does not exist.')
        sections = Class.objects.all()
        context = {'sections': sections}
        return render(request, 'timetableapp/ClassTable.html', context)
    



# def TimeTableView(request, id):
#     try:
#         section = Class.objects.get(class_id=id)
#         courses = Course.objects.all()
#         lecturers = Lecturer.objects.all()
#         activities = Activity.objects.filter(class_id=id)
#         rooms = Classroom.objects.all()

#         # Adjust the format based on the actual format in your database
#         time_format = '%I:%M %p'  # Use '%H:%M' if times are in 24-hour format
        
#         try:
#             start_time = datetime.strptime(section.start_time, time_format)
#             end_time = datetime.strptime(section.end_time, time_format)
#         except ValueError:
#             messages.error(request, 'Time format error in class schedule')
#             return render(request, 'timetableapp/ClassTable.html', {'sections': Class.objects.all()})

       
#         time_range = (end_time - start_time).seconds // 3600 
#         time = [start_time + timedelta(hours=i) for i in range(time_range)]
#         time_slot = [f"{(start_time + timedelta(hours=i)).strftime('%I:%M %p')} - {(start_time + timedelta(hours=i + 1)).strftime('%I:%M %p')}" for i in range(time_range)]

#         context_1 = {
#             'section': section, 
#             'courses': courses, 
#             'lecturers': lecturers, 
#             'rooms': rooms, 
#             'activities': activities, 
#             'time': time, 
#             'time_slot': time_slot
#         }
#         return render(request, 'timetableapp/TimeTable.html', context_1)
    
#     except Class.DoesNotExist:
#         messages.error(request, 'Class does not exist')
#         sections = Class.objects.all()
#         context_2 = {'sections': sections}
#         return render(request, 'timetableapp/ClassTable.html', context_2)
    


    
# def TimeTableView(request, id):
#     try:
#         section = Class.objects.get(class_id=id)
#         courses = Course.objects.all()
#         professors = Lecturer.objects.all()
#         activities = Activity.objects.filter(class_id=id)
#         rooms = Classroom.objects.all()

#         # Parse start_time and end_time using datetime
#         start_time = datetime.strptime(section.start_time, '%I:%M %p').hour
#         end_time = datetime.strptime(section.end_time, '%I:%M %p').hour

#         time_range = end_time - start_time
#         time = [start_time + i for i in range(time_range)]
#         time_slot = [f"{start_time + i}:00 - {start_time + i + 1}:00" for i in range(time_range)]

#         context_1 = {
#             'section': section, 
#             'courses': courses, 
#             'professors': professors, 
#             'rooms': rooms, 
#             'activities': activities, 
#             'time': time, 
#             'time_slot': time_slot
#         }
#         return render(request, 'timetableapp/TimeTable.html', context_1)
    
#     except Class.DoesNotExist:
#         messages.error(request, 'Class does not exist')
#         sections = Class.objects.all()
#         context_2 = {'sections': sections}
#         return render(request, 'timetableapp/ClassTable.html', context_2)



# # @login_required(login_url='login')
# # def TimeTableView(request, id):
    # try:
    #     section = Class.objects.get(class_id=id)
    #     courses = Course.objects.all()
    #     professors = Lecturer.objects.all()
    #     activities = Activity.objects.filter(class_id=id)
    #     rooms = Classroom.objects.all()
    #     time = [0] * (section.end_time - section.start_time)
    #     time_slot = [''] * (section.end_time - section.start_time)
    #     for x in range(0, len(time)):
    #         time_slot[x] = str(section.start_time + x) + ':00 - ' + str(section.start_time + x + 1) + ':00'
    #         time[x] = section.start_time + x
    #     context_1 = {'section': section, 'courses': courses, 'professors':professors, 'rooms': rooms, 
    #                  'activities': activities, 'time': time, 'time_slot': time_slot  }
    #     return render(request, 'timetableapp/TimeTable.html', context_1)
    # except Class.DoesNotExist:
    #     messages.error(request, 'Activity does not exist')
    
    #     sections = Class.objects.all()
    #     context_2 = {'sections': sections}
    #     return render(request, 'timetableapp/ClassTable.html', context_2)