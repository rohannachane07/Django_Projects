from django.shortcuts import render,HttpResponse

from .models import Employee ,Role, Department

from datetime import datetime

from django.db.models import Q
# Create your views here.
def index(request):
    return render(request, 'index.html' )

def all_emp(request):
    emps= Employee.objects.all()
    context= {
        'emps': emps
    }
    print(context)
    return render(request, 'view_all_emp.html' ,context)

def add_emp(request):
    if request.method=="POST":
       first_name=request.POST['first_name']
       last_name=request.POST['last_name']
       salary=request.POST['salary']
       bonus=request.POST['bonus']
       phone=request.POST['phone']
       dept_name=request.POST['dept']
       role_name=request.POST['role']
       try:
           dept=Department.objects.get(name__iexact=dept_name)
       except:
           return HttpResponse("<div style='color:darkblue; font-weight: bold; text-align:center; font-size:2em;'>Department Does Not Exist!!!</div>")
       
       try:
           role=Role.objects.get(name__iexact=role_name)
       except:
           return HttpResponse("<div style='color:darkblue; font-weight: bold; text-align:center; font-size:2em;'>Role Does Not Exist!!!</div>")
       
       new_emp=Employee(first_name=first_name, last_name=last_name,salary=salary, bonus=bonus, phone=phone, dept=dept , role=role,hire_date=datetime.now())
       new_emp.save()
       return HttpResponse("<div style='color:darkblue; font-weight: bold; text-align:center; font-size:2em;'>Employee Has Been Added Succesfully!!!</div>")
    elif request.method=='GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("<div style='color:darkblue; font-weight: bold; text-align:center; font-size:2em;'>An Exception Occured...Employee Has Not Been Added!!!</div>")


def remove_emp(request,emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed= Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("<div style='color:darkblue; font-weight: bold; text-align:center; font-size:2em;'>Employee Has Been Removed Succesfully!!!</div>")
        except:
            return HttpResponse("<div style='color:darkblue; font-weight: bold; text-align:center; font-size:2em;'>Invalid Employee ID!!!</div>")
    emps = Employee.objects.all()
    context={
        'emps': emps
    }
    return render(request, 'remove_emp.html',context )

def filter_emp(request):
    if request.method=='POST':
        name= request.POST['name']
        dept= request.POST['dept']
        role= request.POST['role']

        emps= Employee.objects.all()
        if name:
            emps=emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps= emps.filter(dept__name__icontains=dept)
        if role:
            emps= emps.filter(role__name__icontains=role)
        
        context={
            'emps':emps
        }
        return render(request, 'view_all_emp.html',context)
    elif request.method== 'GET':
        return render(request, 'filter_emp.html' )
    
    else:
        return HttpResponse("<div style='color:darkblue; font-weight: bold; text-align:center; font-size:2em;'>An Exception Occured!!!</div>")