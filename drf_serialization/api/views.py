from django.shortcuts import render
from .models import Student
from .serializers import StudentSerializers
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
# Create your views here.


# Model Object - Single Student Data
def student_details(request,pk):
    stu = Student.objects.get(id=pk)
    print(stu)
    serializer = StudentSerializers(stu)
    print(serializer)
    print(serializer.data)
    json_data = JSONRenderer().render(serializer.data)
    print(json_data)
    return HttpResponse(json_data, content_type='application/json')
