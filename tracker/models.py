from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField

# Create your models here.
class Squad(models.Model):
	name = models.CharField(max_length=200, blank=False)
	gender = models.CharField(max_length=20, blank=False)
	def __unicode__(self):
		return self.name

class Rower(models.Model):
	user = models.OneToOneField(User)
	squad = models.ForeignKey(Squad)
	nickname = models.CharField(max_length=20, blank= True)
	mobile = models.CharField(max_length = 14, blank= True)
	senior = models.BooleanField(blank=True, default=False, verbose_name="Senior rower?")
	def __unicode__(self):
		if str(self.nickname) =="":
			return str(self.user.first_name) + " " + str(self.user.last_name)
		else:
			return str(self.user.first_name) + " '" +str(self.nickname) + "' " + str(self.user.last_name)

class Session(models.Model):
	squad = models.ForeignKey(Squad)
	name = models.CharField(max_length=100, blank=False)
	location = models.CharField(max_length=40, blank=False)
	description = models.TextField(blank=True)
	date = models.DateField(auto_now=False, auto_now_add=False)
	slot1_time = models.TimeField(auto_now=False, auto_now_add=False)
	slot2_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
	slot3_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
	max_rowers1 = models.IntegerField(blank=True, null=True, verbose_name="Max number of rowers (slot1)?")
	max_rowers2 = models.IntegerField(blank=True, null=True, verbose_name="Max number of rowers (slot2)?")
	max_rowers3 = models.IntegerField(blank=True, null=True, verbose_name="Max number of rowers (slot3)?")
	senior_boolean1 = models.BooleanField(blank=True, default=False, verbose_name="Senior rower needed (slot1)?")
	senior_boolean2 = models.BooleanField(blank=True, default=False, verbose_name="Senior rower needed (slot2)?")
	senior_boolean3 = models.BooleanField(blank=True, default=False, verbose_name="Senior rower needed (slot3)?")
	rower = models.ManyToManyField(Rower, through='Performance')
	def __unicode__(self):
		return str(self.name) + ": " + str(self.date)

class Performance(models.Model):
	session = models.ForeignKey(Session)
	rower = models.ForeignKey(Rower)
	slot_choices = models.CharField(choices=(('slot_1', 'Slot 1'), ('slot_2', 'Slot 2'), ('slot_3', 'Slot 3')), blank=True, max_length=30)
	chosen_slot_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
	set_distance1 = models.CharField(max_length=20, blank=True)
	set_distance2 = models.CharField(max_length=20, blank=True)
	set_distance3 = models.CharField(max_length=20, blank=True)
	set_distance4 = models.CharField(max_length=20, blank=True)
	set_distance5 = models.CharField(max_length=20, blank=True)
	set_distance6 = models.CharField(max_length=20, blank=True)

	set_time1 = models.CharField(max_length=20, blank=True)
	set_time2 = models.CharField(max_length=20, blank=True)
	set_time3 = models.CharField(max_length=20, blank=True)
	set_time4 = models.CharField(max_length=20, blank=True)
	set_time5 = models.CharField(max_length=20, blank=True)
	set_time6 = models.CharField(max_length=20, blank=True)

	set_rate_cap1 = models.CharField(max_length=20, blank=True)
	set_rate_cap2 = models.CharField(max_length=20, blank=True)
	set_rate_cap3 = models.CharField(max_length=20, blank=True)
	set_rate_cap4 = models.CharField(max_length=20, blank=True)
	set_rate_cap5 = models.CharField(max_length=20, blank=True)
	set_rate_cap6 = models.CharField(max_length=20, blank=True)

	set_heart_zone1 = models.CharField(max_length=20, blank=True)
	set_heart_zone2 = models.CharField(max_length=20, blank=True)
	set_heart_zone3 = models.CharField(max_length=20, blank=True)
	set_heart_zone4 = models.CharField(max_length=20, blank=True)
	set_heart_zone5 = models.CharField(max_length=20, blank=True)
	set_heart_zone6 = models.CharField(max_length=20, blank=True)

	set_rest_time1 = models.CharField(max_length=20, blank=True)
	set_rest_time2 = models.CharField(max_length=20, blank=True)
	set_rest_time3 = models.CharField(max_length=20, blank=True)
	set_rest_time4 = models.CharField(max_length=20, blank=True)
	set_rest_time5 = models.CharField(max_length=20, blank=True)
	set_rest_time6 = models.CharField(max_length=20, blank=True)

	recorded_distance1 = models.CharField(max_length=20, blank=True)
	recorded_distance2 = models.CharField(max_length=20, blank=True)
	recorded_distance3 = models.CharField(max_length=20, blank=True)
	recorded_distance4 = models.CharField(max_length=20, blank=True)
	recorded_distance5 = models.CharField(max_length=20, blank=True)
	recorded_distance6 = models.CharField(max_length=20, blank=True)

	recorded_time1 = models.CharField(max_length=20, blank=True)
	recorded_time2 = models.CharField(max_length=20, blank=True)
	recorded_time3 = models.CharField(max_length=20, blank=True)
	recorded_time4 = models.CharField(max_length=20, blank=True)
	recorded_time5 = models.CharField(max_length=20, blank=True)
	recorded_time6 = models.CharField(max_length=20, blank=True)

	completed = models.CharField(max_length=40, blank=True)
	unavailable = models.BooleanField(default=False)

class PerformanceCopy(models.Model):
	session = models.ForeignKey(Session)
	set_distance1 = models.CharField(max_length=20, blank=True)
	set_distance2 = models.CharField(max_length=20, blank=True)
	set_distance3 = models.CharField(max_length=20, blank=True)
	set_distance4 = models.CharField(max_length=20, blank=True)
	set_distance5 = models.CharField(max_length=20, blank=True)
	set_distance6 = models.CharField(max_length=20, blank=True)

	set_time1 = models.CharField(max_length=20, blank=True)
	set_time2 = models.CharField(max_length=20, blank=True)
	set_time3 = models.CharField(max_length=20, blank=True)
	set_time4 = models.CharField(max_length=20, blank=True)
	set_time5 = models.CharField(max_length=20, blank=True)
	set_time6 = models.CharField(max_length=20, blank=True)

	set_rate_cap1 = models.CharField(max_length=20, blank=True)
	set_rate_cap2 = models.CharField(max_length=20, blank=True)
	set_rate_cap3 = models.CharField(max_length=20, blank=True)
	set_rate_cap4 = models.CharField(max_length=20, blank=True)
	set_rate_cap5 = models.CharField(max_length=20, blank=True)
	set_rate_cap6 = models.CharField(max_length=20, blank=True)

	set_heart_zone1 = models.CharField(max_length=20, blank=True)
	set_heart_zone2 = models.CharField(max_length=20, blank=True)
	set_heart_zone3 = models.CharField(max_length=20, blank=True)
	set_heart_zone4 = models.CharField(max_length=20, blank=True)
	set_heart_zone5 = models.CharField(max_length=20, blank=True)
	set_heart_zone6 = models.CharField(max_length=20, blank=True)

	set_rest_time1 = models.CharField(max_length=20, blank=True)
	set_rest_time2 = models.CharField(max_length=20, blank=True)
	set_rest_time3 = models.CharField(max_length=20, blank=True)
	set_rest_time4 = models.CharField(max_length=20, blank=True)
	set_rest_time5 = models.CharField(max_length=20, blank=True)
	set_rest_time6 = models.CharField(max_length=20, blank=True)


	def __unicode__(self):
			return str(self.recorded_distance1) + "m: " + str(self.recorded_distance2) + "m:"

class ChosenSlotForm(ModelForm):
	class Meta:
		model = Performance
		fields = ['slot_choices']

class PerformanceTimeForm(ModelForm):
	class Meta:
		model = Performance
		fields = ['recorded_distance1', 'recorded_time1',
				  'recorded_distance2', 'recorded_time2',
				  'recorded_distance3', 'recorded_time3',
				  'recorded_distance4', 'recorded_time4',
				  'recorded_distance5', 'recorded_time5',
				  'recorded_distance6', 'recorded_time6',
				  'unavailable']

class PerformanceDistanceForm(ModelForm):
	class Meta:
		model = Performance
		fields = ['set_distance1', 'set_time1', 'set_rate_cap1', 'set_heart_zone1', 'set_rest_time1',
				  'set_distance2', 'set_time2', 'set_rate_cap2', 'set_heart_zone2', 'set_rest_time2',
				  'set_distance3', 'set_time3', 'set_rate_cap3', 'set_heart_zone3', 'set_rest_time3',
				  'set_distance4', 'set_time4', 'set_rate_cap4', 'set_heart_zone4', 'set_rest_time4',
				  'set_distance5', 'set_time5', 'set_rate_cap5', 'set_heart_zone5', 'set_rest_time5',
				  'set_distance6', 'set_time6', 'set_rate_cap6', 'set_heart_zone6', 'set_rest_time6',
				  ]


class SessionForm(ModelForm):
	class Meta:
		model = Session
		fields = ['squad', 'name', 'location', 'description', 'date', 'slot1_time', 'max_rowers1', 'senior_boolean1', 'slot2_time', 'max_rowers2', 'senior_boolean2', 'slot3_time', 'max_rowers3', 'senior_boolean3']




