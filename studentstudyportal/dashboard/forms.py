from django import forms
from . models import *

#-------------------------Notes----------------------
class NotesForm(forms.ModelForm):
    class Meta:
        model=Notes   #Map the model 'Notes' here,no need to assign all 3 columns of Notes again.We can map our Model to the form directly.
        fields=['title','description']


#-------------------------Homework-------------------

class DateInput(forms.DateInput):
    input_type='date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model=Homework
        widgets={'due':DateInput()}
        fields=['subject','title','description','due','is_finished']
        # widgets = {'due': forms.DateInput(attrs={'type': 'date'})}  #Django's By Deafult DateInput class.

        

#--------------------------Youtube,Books,Wikipedia,Dictionary---------------------
class DashboardForm(forms.Form):    #This is a common class we are making like dictionary search,wikipedia search,youtube search,books search
    text=forms.CharField(max_length=100,label="Enter Your Search: ")



#---------------------------To-Do-----------------------
class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['title','is_finished']



#---------------------------Conversion-------------------

class ConversionForm(forms.Form):
    CHOICES=[
        ('length','Length'),
        ('mass','Mass'),
        ('time', 'Time'),
        ('volume', 'Volume'),
        ('area', 'Area'),
        ('temperature', 'Temperature'),
        ('digital storage', 'Digital Storage'),
        ('energy', 'Energy'),
        ('speed', 'Speed'),
        ('pressure', 'Pressure'),
        ('frequency', 'Frequency'),
        ('plane angle', 'Plane Angle'),
        
        ]
    measurement=forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': 'd-inline'}))


class ConversionLengthForm(forms.Form):
    CHOICES=[
        ('yard','Yard'),
        ('foot','Foot'),
        ('metre','Metre'),
        ('kilometre', 'Kilometre'),
        ('centimetre', 'Centimetre'),
        ('millimetre', 'Millimetre'),
        ('micrometre', 'Micrometre'),
        ('nanometre', 'Nanometre'),
        ('mile', 'Mile'),
        ('inch', 'Inch')
        ]
    input=forms.FloatField(required=False, label=False, widget=forms.NumberInput(
        attrs={'type':'number', 'placeholder':'Enter the Number'}
    ))
    measure1=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES, attrs={'class': 'form-control'})
    )
    measure2=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )



class ConversionMassForm(forms.Form):
    CHOICES=[
        ('pound','Pound'),
        ('kilogram','Kilogram'),
        ('gram', 'Gram'),
        ('tonne', 'Tonne'),
        ('milligram', 'Milligram'),
        ('microgram', 'Microgram'),
        ('us_ton', 'US Ton'),
        ('stone', 'Stone'),
        ('ounce', 'Ounce'),

        ]
    input=forms.FloatField(required=False, label=False, widget=forms.NumberInput(
        attrs={'type':'number', 'placeholder':'Enter the Number'}
    ))
    measure1=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )
    measure2=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )


class ConversionTimeForm(forms.Form):
    CHOICES=[
        ('second', 'Second'),
        ('nanosecond', 'Nanosecond'),
        ('microsecond', 'Microsecond'),
        ('millisecond', 'Millisecond'),
        ('minute', 'Minute'),
        ('hour', 'Hour'),
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
        ('calendar_year', 'Calendar Year'),
        ('decade', 'Decade'),
        ('century', 'Century'),
        ]
    input=forms.FloatField(required=False, label=False, widget=forms.NumberInput(
        attrs={'type':'number', 'placeholder':'Enter the Number'}
    ))
    measure1=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )
    measure2=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )


class ConversionVolumeForm(forms.Form):
    CHOICES=[
        ('litre', 'Litre'),
        ('millilitre', 'Millilitre'),
        ('cubic_metre', 'Cubic Metre'),
        ('cubic_foot', 'Cubic Foot'),
        ('cubic_inch', 'Cubic Inch')
        ]
    input=forms.FloatField(required=False, label=False, widget=forms.NumberInput(
        attrs={'type':'number', 'placeholder':'Enter the Number'}
    ))
    measure1=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )
    measure2=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )


class ConversionAreaForm(forms.Form):
    CHOICES=[
        ('square_metre', 'Square Metre'),
        ('square_kilometre', 'Square Kilometre'),
        ('square_mile', 'Square Mile'),
        ('square_yard', 'Square Yard'),
        ('square_foot', 'Square Foot'),
        ('square_inch', 'Square Inch'),
        ('hectare', 'Hectare'),
        ('acre', 'Acre'),
        ]
    input=forms.FloatField(required=False, label=False, widget=forms.NumberInput(
        attrs={'type':'number', 'placeholder':'Enter the Number'}
    ))
    measure1=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )
    measure2=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )


class ConversionTemperatureForm(forms.Form):
    CHOICES=[
        ('celsius', 'Degree Celsius'),
        ('kelvin', 'Kelvin'),
        ('fahrenheit', 'Fahrenheit')
        ]
    input=forms.FloatField(required=False, label=False, widget=forms.NumberInput(
        attrs={'type':'number', 'placeholder':'Enter the Number'}
    ))
    measure1=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )
    measure2=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )


class ConversionDigitalStorageForm(forms.Form):
    CHOICES=[
        ('byte', 'Byte'),
        ('kilobyte', 'Kilobyte'),
        ('megabyte', 'Megabyte'),
        ('gigabyte', 'Gigabyte'),
        ('terabyte', 'Terabyte'),
        ('petabyte', 'Petabyte'),
        ('bit', 'Bit'),
        ('kilobit', 'Kilobit'),
        ('megabit', 'Megabit'),
        ('gigabit', 'Gigabit'),
        ('terabit', 'Terabit'),
        ('petabit', 'Petabit'),

        ]
    input=forms.FloatField(required=False, label=False, widget=forms.NumberInput(
        attrs={'type':'number', 'placeholder':'Enter the Number'}
    ))
    measure1=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )
    measure2=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )


class ConversionEnergyForm(forms.Form):
    CHOICES=[
        ('joule', 'Joule'),
        ('kilojoule', 'Kilojoule'),
        ('calorie', 'Gram calorie'),
        ('kilocalorie', 'Kilocalorie'),
        ('watt_hour', 'Watt hour'),
        ('kilowatt_hour', 'Kilowatt hour'),
        ('electronvolt', 'ElectronVolt'),
        ('foot_pound', 'Foot-pound'),

        ]
    input=forms.FloatField(required=False, label=False, widget=forms.NumberInput(
        attrs={'type':'number', 'placeholder':'Enter the Number'}
    ))
    measure1=forms.CharField(
       required=False,  label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )
    measure2=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )


class ConversionSpeedForm(forms.Form):
    CHOICES=[
        ('metre_per_second', 'Metre Per Second'),
        ('mile_per_hour', 'Mile Per Hour'),
        ('foot_per_second', 'Foot Per Second'),
        ('kilometre_per_hour', 'Kilometre Per Hour'),
        ('knot', 'Knot'),
        ]
    input=forms.FloatField(required=False, label=False, widget=forms.NumberInput(
        attrs={'type':'number', 'placeholder':'Enter the Number'}
    ))
    measure1=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )
    measure2=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )


class ConversionPressureForm(forms.Form):
    CHOICES=[
         ('bar', 'Bar'),
        ('pascal', 'Pascal'),
        ('torr', 'Torr'),
        ('standard_atmosphere', 'Standard Atmosphere'),
        ('psi', 'Pound Per Square Inch (PSI)'),
        ]
    input=forms.FloatField(required=False, label=False, widget=forms.NumberInput(
        attrs={'type':'number', 'placeholder':'Enter the Number'}
    ))
    measure1=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )
    measure2=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )


class ConversionFrequencyForm(forms.Form):
    CHOICES=[
        ('hertz', 'Hertz'),
        ('kilohertz', 'KiloHertz'),
        ('megahertz', 'MegaHertz'),
        ('gigahertz', 'GigaHertz'),
        ]
    input=forms.FloatField(required=False, label=False, widget=forms.NumberInput(
        attrs={'type':'number', 'placeholder':'Enter the Number'}
    ))
    measure1=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )
    measure2=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )


class ConversionPlaneAngleForm(forms.Form):
    CHOICES=[
         ('degree', 'Degree'),
        ('gradian', 'Gradian'),
        ('radian', 'Radian'),
        ('milliradian', 'Milliradian'),
        ('minute_of_arc', 'Minute of Arc'),
        ]
    input=forms.FloatField(required=False, label=False, widget=forms.NumberInput(
        attrs={'type':'number', 'placeholder':'Enter the Number'}
    ))
    measure1=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )
    measure2=forms.CharField(
        required=False, label='', widget=forms.Select(choices=CHOICES,  attrs={'class': 'form-control'})
    )


#---------------------------Registration-------------------
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']


