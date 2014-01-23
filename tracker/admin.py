from django.contrib import admin
from tracker.models import Squad, Rower, Session, Performance

# Register your models here.

class PerformanceInline(admin.StackedInline):
	model= Performance
	fields= ('rower', ('completed', 'unavailable'),
					  ('chosen_slot_time'),
					  ('set_distance1', 'set_time1', 'set_rate_cap1', 'set_heart_zone1', 'set_rest_time1', 'recorded_time1', 'recorded_distance1'),
					  ('set_distance2', 'set_time2', 'set_rate_cap2', 'set_heart_zone2', 'set_rest_time2', 'recorded_time2', 'recorded_distance2'),
					  ('set_distance3', 'set_time3', 'set_rate_cap3', 'set_heart_zone3', 'set_rest_time3', 'recorded_time3', 'recorded_distance3'),
					  ('set_distance4', 'set_time4', 'set_rate_cap4', 'set_heart_zone4', 'set_rest_time4', 'recorded_time4', 'recorded_distance4'),
					  ('set_distance5', 'set_time5', 'set_rate_cap5', 'set_heart_zone5', 'set_rest_time5', 'recorded_time5', 'recorded_distance5'),
					  ('set_distance6', 'set_time6', 'set_rate_cap6', 'set_heart_zone6', 'set_rest_time6', 'recorded_time6', 'recorded_distance6')
					  )
	extra= 1

class RowerInline(admin.TabularInline):
	model= Rower
	extra= 0

class SessionAdmin(admin.ModelAdmin):
	fieldsets = [
		('New Session',		{'fields': ['squad', 'name', 'location', 'description', 'date', 'slot1_time', 'slot2_time', 'slot3_time', 'max_rowers1', 'max_rowers2', 'max_rowers3', 'senior_boolean1', 'senior_boolean2', 'senior_boolean3']}),
	]
	list_display=('name', 'squad', 'location', 'date', 'slot1_time')
	list_filter=['squad', 'date']
	inlines = [PerformanceInline]

class SquadAdmin(admin.ModelAdmin):
	fieldsets = [
		('Squads',		{'fields': ['name', 'gender']}),
	]
	list_display=('name', 'gender')
	inlines = [RowerInline]


admin.site.register(Squad, SquadAdmin)
admin.site.register(Rower)
admin.site.register(Session, SessionAdmin)
admin.site.register(Performance)