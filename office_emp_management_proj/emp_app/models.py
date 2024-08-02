from django.db import models

# Create your models here.
class Department(models.Model):
    name= models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Role(models.Model):
    name= models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)    #department same bhi ho sakte hai so we just make here table of it 
                                                                    #and then we will combine it with a foreign key.That tables should be alwasy above it.
    salary = models.IntegerField(default=0)
    bonus= models.IntegerField(default=0)
    role= models.ForeignKey(Role, on_delete=models.CASCADE)          #roles can also be same
    phone= models.IntegerField(default=0)
    hire_date= models.DateField()

    def __str__(self):
        return "%s %s %s" %(self.first_name,self.last_name,self.phone)  #The %s is a placeholder for a string.%(self.first_name, self.last_name, self.phone) is a tuple containing the values to be inserted into the placeholders in the format string.

