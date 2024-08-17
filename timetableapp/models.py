from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.hashers import make_password

TIME_CHOICES = (
    ('08:00 AM', '08:00 AM'),
    ('09:00 AM', '09:00 AM'),
    ('10:00 AM', '10:00 AM'),
    ('11:00 AM', '11:00 AM'),
    ('12:00 PM', '12:00 PM'),
    ('01:00 PM', '01:00 PM'),
    ('02:00 PM', '02:00 PM'),
    ('03:00 PM', '03:00 PM'),
    ('04:00 PM', '04:00 PM'),
    ('05:00 PM', '05:00 PM'),
    ('06:00 PM', '06:00 PM'),
    ('07:00 PM', '07:00 PM'),
    ('08:00 PM', '08:00 PM'),
)

WEEK_DAY = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday')
)

class Course(models.Model):
    COURSE_TYPE = (
        ('Theory', 'Theory'),
        ('Lab', 'Lab')
    )

    course_id = models.CharField(max_length=1000, primary_key=True)
    course_name = models.CharField(max_length=1000, null=True)
    course_type = models.CharField(max_length=200, null=True, choices=COURSE_TYPE)
    credit_hours = models.IntegerField(null=True)
    contact_hours = models.IntegerField(null=True)

    def __str__(self):
        return self.course_id + ' - ' + self.course_name


class Lecturer(models.Model):
    lecturer_id = models.CharField(max_length=2000,primary_key=True)
    first_name=models.CharField(max_length=2000, null=False)
    last_name=models.CharField(max_length=2000,null=False)
    email=models.EmailField(max_length=20,unique=True)
    password=models.CharField(max_length=128)
    working_hours = models.IntegerField(null=False)
    available_hours = models.IntegerField(null=False)

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.password.startswith('pbkdf2_sha256$'):  # Example check for Django's default hash
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Classroom(models.Model):
    CLASSRoom_TYPE = (
        ('Theory', 'Theory'),
        ('Lab', 'Lab')
    )
    classroom_id = models.IntegerField(primary_key=True)
    classroom_name = models.CharField(max_length=2000, null=True)
    classroom_type = models.CharField(max_length=2000, null=True, choices=CLASSRoom_TYPE)
    def __str__(self):
        return self.classroom_name #+ ' - ' + self.classroom_name


class Class(models.Model):
    WEEK_DAY = WEEK_DAY
    TIME_CHOICES = TIME_CHOICES

    class_id = models.IntegerField(primary_key=True)
    class_name = models.CharField(max_length=2000, null=True)
    week_day = MultiSelectField(max_length=2000, choices=WEEK_DAY, max_choices=7)
    start_time = models.CharField(max_length=10, choices=TIME_CHOICES)
    end_time = models.CharField(max_length=10, choices=TIME_CHOICES)

    def __str__(self):
        return f"{self.class_name}, {self.week_day}" #+ ' - ' + self.class_name


# table to store courses for class
class ClassCourse(models.Model):
    class Meta:
        unique_together = (('class_id', 'course_id'),)
    class_id = models.ForeignKey(Class, null=True, on_delete=models.CASCADE)
    lecturer_id = models.ForeignKey(Lecturer, null=True, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course,null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.class_id}"


class RequestChange(models.Model):
    lecturer=models.ForeignKey(Lecturer,on_delete=models.CASCADE)
    messange=models.CharField(max_length=300)

    def __str__(self):
        return f"{self.lecturer}, {self.messange}"


class Student(models.Model):
    admission_number=models.CharField(primary_key=True, max_length=10,unique=True)
    first_name=models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email=models.EmailField()
    course=models.CharField(max_length=2000)
    year_of_study=models.IntegerField()

    def __str__(self):
        return f"{self.admission_number}, {self.first_name},{self.last_name}, {self.email},{self.course}, {self.year_of_study}"


# to store classrooms for class
class SectionClassroom(models.Model):
    class Meta:
        unique_together = (('class_id', 'classroom_id'),)

    class_id = models.ForeignKey(Class,on_delete=models.CASCADE)
    classroom_id = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.class_id},{self.classroom_id}' 


class Activity(models.Model):
    ACTIVITY_TYPE = (
        ('Fixed', 'Fixed'),
        ('Replaceable', 'Replaceable')
    )
    WEEK_DAY = WEEK_DAY
    TIME_CHOICES = TIME_CHOICES
  
    activity_id = models.CharField(max_length=2000, primary_key=True)
    activity_type = models.CharField(max_length=2000, null=True, choices=ACTIVITY_TYPE)
    lecturer_id = models.ForeignKey(Lecturer, null=True, on_delete=models.CASCADE)
    classroom_id = models.ForeignKey(Classroom,null=True, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class,null=True, on_delete=models.CASCADE)
    day = models.CharField(max_length=20, choices=WEEK_DAY)
    start_time = models.CharField(max_length=10, choices=TIME_CHOICES)
    end_time = models.CharField(max_length=10, choices=TIME_CHOICES)

    def __str__(self):
        return f"{self.lecturer_id}, {self.class_id},{self.classroom_id}"
