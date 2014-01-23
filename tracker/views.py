from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
from tracker.models import Squad, Rower, Session, Performance, PerformanceCopy, PerformanceTimeForm, SessionForm, PerformanceDistanceForm, ChosenSlotForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.utils import timezone
from tracker.templatetags import dictionary_extras

#Stuff taken from django.contrib version of views.py, to allow for custom login to work
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.utils.http import base36_to_int, is_safe_url, urlsafe_base64_decode, urlsafe_base64_encode
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import get_current_site

@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='tracker/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're in the tracker app for SJCBC.")

def thanks(request):
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
        active_first_name = request.user.first_name
        return render_to_response('tracker/thanks.html', {'active_first_name': active_first_name})

def created(request):
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
        active_first_name = request.user.first_name
        return render_to_response('tracker/created.html', {'active_first_name': active_first_name})

def logout_view(request):
    logout(request)
    return redirect('/tracker/login/')

def create_session(request):
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
        if request.method =='POST': # If the form has been submitted...
            form1 = SessionForm(request.POST, prefix="form1") # form bound to the POST data
            form2 = PerformanceDistanceForm(request.POST, prefix="form2")
            if form1.is_valid() and form2.is_valid(): # All validation rules pass
                f = Session(squad=form1.cleaned_data['squad'],
                            name=form1.cleaned_data['name'],
                            location=form1.cleaned_data['location'],
                            description=form1.cleaned_data['description'],
                            date=form1.cleaned_data['date'],
                            slot1_time=form1.cleaned_data['slot1_time'],
                            slot2_time=form1.cleaned_data['slot2_time'],
                            slot3_time=form1.cleaned_data['slot3_time'],
                            max_rowers1=form1.cleaned_data['max_rowers1'],
                            max_rowers2=form1.cleaned_data['max_rowers2'],
                            max_rowers3=form1.cleaned_data['max_rowers3'],
                            senior_boolean1=form1.cleaned_data['senior_boolean1'],
                            senior_boolean2=form1.cleaned_data['senior_boolean2'],
                            senior_boolean3=form1.cleaned_data['senior_boolean3']
                            )
                f.save()
                s = Session.objects.get(id=f.id)
                squad = form1.cleaned_data['squad']
                rower_list = squad.rower_set.all()[0:]
                for rower in rower_list:
                    p = Performance(session = s,
                                    rower= rower,
                                    set_distance1 = form2.cleaned_data['set_distance1'],
                                    set_distance2= form2.cleaned_data['set_distance2'],
                                    set_distance3= form2.cleaned_data['set_distance3'],
                                    set_distance4= form2.cleaned_data['set_distance4'],
                                    set_distance5= form2.cleaned_data['set_distance5'],
                                    set_distance6= form2.cleaned_data['set_distance6'],
                                    set_time1= form2.cleaned_data['set_time1'],
                                    set_time2= form2.cleaned_data['set_time2'],
                                    set_time3= form2.cleaned_data['set_time3'],
                                    set_time4= form2.cleaned_data['set_time4'],
                                    set_time5= form2.cleaned_data['set_time5'],
                                    set_time6= form2.cleaned_data['set_time6'],
                                    set_rate_cap1= form2.cleaned_data['set_rate_cap1'],
                                    set_rate_cap2= form2.cleaned_data['set_rate_cap2'],
                                    set_rate_cap3= form2.cleaned_data['set_rate_cap3'],
                                    set_rate_cap4= form2.cleaned_data['set_rate_cap4'],
                                    set_rate_cap5= form2.cleaned_data['set_rate_cap5'],
                                    set_rate_cap6= form2.cleaned_data['set_rate_cap6'],
                                    set_heart_zone1= form2.cleaned_data['set_heart_zone1'],
                                    set_heart_zone2= form2.cleaned_data['set_heart_zone2'],
                                    set_heart_zone3= form2.cleaned_data['set_heart_zone3'],
                                    set_heart_zone4= form2.cleaned_data['set_heart_zone4'],
                                    set_heart_zone5= form2.cleaned_data['set_heart_zone5'],
                                    set_heart_zone6= form2.cleaned_data['set_heart_zone6'],
                                    set_rest_time1= form2.cleaned_data['set_rest_time1'],
                                    set_rest_time2= form2.cleaned_data['set_rest_time2'],
                                    set_rest_time3= form2.cleaned_data['set_rest_time3'],
                                    set_rest_time4= form2.cleaned_data['set_rest_time4'],
                                    set_rest_time5= form2.cleaned_data['set_rest_time5'],
                                    set_rest_time6= form2.cleaned_data['set_rest_time6']
                                    )
                    p.save()

                # Now we create a carbon copy of the set performances to add to future rowers that may be added to the squad list

                pc = PerformanceCopy(session=s,
                                    set_distance1 = form2.cleaned_data['set_distance1'],
                                    set_distance2= form2.cleaned_data['set_distance2'],
                                    set_distance3= form2.cleaned_data['set_distance3'],
                                    set_distance4= form2.cleaned_data['set_distance4'],
                                    set_distance5= form2.cleaned_data['set_distance5'],
                                    set_distance6= form2.cleaned_data['set_distance6'],
                                    set_time1= form2.cleaned_data['set_time1'],
                                    set_time2= form2.cleaned_data['set_time2'],
                                    set_time3= form2.cleaned_data['set_time3'],
                                    set_time4= form2.cleaned_data['set_time4'],
                                    set_time5= form2.cleaned_data['set_time5'],
                                    set_time6= form2.cleaned_data['set_time6'],
                                    set_rate_cap1= form2.cleaned_data['set_rate_cap1'],
                                    set_rate_cap2= form2.cleaned_data['set_rate_cap2'],
                                    set_rate_cap3= form2.cleaned_data['set_rate_cap3'],
                                    set_rate_cap4= form2.cleaned_data['set_rate_cap4'],
                                    set_rate_cap5= form2.cleaned_data['set_rate_cap5'],
                                    set_rate_cap6= form2.cleaned_data['set_rate_cap6'],
                                    set_heart_zone1= form2.cleaned_data['set_heart_zone1'],
                                    set_heart_zone2= form2.cleaned_data['set_heart_zone2'],
                                    set_heart_zone3= form2.cleaned_data['set_heart_zone3'],
                                    set_heart_zone4= form2.cleaned_data['set_heart_zone4'],
                                    set_heart_zone5= form2.cleaned_data['set_heart_zone5'],
                                    set_heart_zone6= form2.cleaned_data['set_heart_zone6'],
                                    set_rest_time1= form2.cleaned_data['set_rest_time1'],
                                    set_rest_time2= form2.cleaned_data['set_rest_time2'],
                                    set_rest_time3= form2.cleaned_data['set_rest_time3'],
                                    set_rest_time4= form2.cleaned_data['set_rest_time4'],
                                    set_rest_time5= form2.cleaned_data['set_rest_time5'],
                                    set_rest_time6= form2.cleaned_data['set_rest_time6']
                                    )
                pc.save()

                return HttpResponseRedirect('/tracker/created/') # Redirect after POST
        else:
            form1 = SessionForm(prefix="form1")  # An unbound form
            form2 = PerformanceDistanceForm(prefix="form2")

        return render(request, 'tracker/create_session.html', {"form1": form1, 'form2': form2})


def choose_slot(request, session_id):
    if not request.user.is_authenticated:
        return redirect('/login/next=%s' % request.path)
    else:
        #Setting the correct identifiers
        session = get_object_or_404(Session, pk=session_id)
        active_rower = request.user.rower   #To differentiate from rower below
        performance = session.performance_set.get(rower_id=active_rower.id)

        # Create error dictionary and see who's filled what slot, to then test if a slot is full already. These values are mostly placeholders - it's what they turn into that's important
        error_dictionary = {'slot1_max': 'not full', "slot2_max": "not full", "slot3_max": "not full", "slot1_senior": "none", "slot2_senior": "none", "slot3_senior": "none"}
        # To fill up with rowers that have selected each slot
        slot_selection_dictionary = {'slot_time1':[], 'slot_time2':[], 'slot_time3':[]}

        # Below puts rowers into their chosen slots and marks whether they are a senior rower or not.
        for rower in session.squad.rower_set.all()[0:]:
            if session.performance_set.get(rower_id=rower.id).chosen_slot_time == session.slot1_time:
                slot_selection_dictionary['slot_time1'].append(rower)
                if rower.senior == True:
                    error_dictionary['slot1_senior']="some"
            elif session.performance_set.get(rower_id=rower.id).chosen_slot_time == session.slot2_time:
                slot_selection_dictionary['slot_time2'].append(rower)
                if rower.senior == True:
                    error_dictionary['slot2_senior']="some"
            elif session.performance_set.get(rower_id=rower.id).chosen_slot_time == session.slot3_time:
                slot_selection_dictionary['slot_time3'].append(rower)
                if rower.senior == True:
                    error_dictionary['slot3_senior']="some"

        # Now we want to measure the length of each slot_selection_dictionary list value, for comparison against the max no. of rowers for the session
        slot_selection_dictionary_length = {}
        slot_selection_dictionary_length['slot_time1'] = len(slot_selection_dictionary['slot_time1'])
        slot_selection_dictionary_length['slot_time2'] = len(slot_selection_dictionary['slot_time2'])
        slot_selection_dictionary_length['slot_time3'] = len(slot_selection_dictionary['slot_time3'])

        # Now we see whether there is no senior rower, but one is required
        if session.senior_boolean1 == True and error_dictionary['slot1_senior']=="none":
            error_dictionary['slot1_senior']="lacking"
        if session.senior_boolean2 == True and error_dictionary['slot2_senior']=="none":
            error_dictionary['slot2_senior']="lacking"
        if session.senior_boolean3 == True and error_dictionary['slot3_senior']=="none":
            error_dictionary['slot3_senior']="lacking"

        if active_rower.senior == False and error_dictionary['slot1_senior'] == "lacking":
            slot_selection_dictionary_length['slot_time1'] += 1
        if active_rower.senior == False and error_dictionary['slot2_senior'] == "lacking":
            slot_selection_dictionary_length['slot_time2'] += 1
        if active_rower.senior == False and error_dictionary['slot3_senior'] == "lacking":
            slot_selection_dictionary_length['slot_time3'] += 1

        # Make list full if capacity is reached
        if session.slot1_time != None and slot_selection_dictionary_length['slot_time1'] >= session.max_rowers1 > 0:
            error_dictionary['slot1_max'] = 'full'
        if session.slot2_time != None and slot_selection_dictionary_length['slot_time2'] >= session.max_rowers2 > 0:
            error_dictionary['slot2_max'] = 'full'
        if session.slot3_time != None and slot_selection_dictionary_length['slot_time3'] >= session.max_rowers3 > 0:
            error_dictionary['slot3_max'] = 'full'


        if request.method == 'POST': # If the form has been submitted...
            form = ChosenSlotForm(request.POST) # A form bound to the POST data
            if form.is_valid():
                # Send back with correct error dictionary if slots are full
                if form.cleaned_data['slot_choices'] == 'slot_1' and error_dictionary['slot1_max'] == 'full':
                    return render(request, 'tracker/choose_slot.html', {'slot_selection_dictionary': slot_selection_dictionary,
                                                                        'session': session,
                                                                        'form': form,
                                                                        'error_dictionary': error_dictionary,
                                                                        'session_id': session_id
                                                                        })
                if form.cleaned_data['slot_choices'] == 'slot_2' and error_dictionary['slot2_max'] == 'full':
                    return render(request, 'tracker/choose_slot.html', {'slot_selection_dictionary': slot_selection_dictionary,
                                                                        'session': session,
                                                                        'form': form,
                                                                        'error_dictionary': error_dictionary,
                                                                        'session_id': session_id
                                                                        })
                if form.cleaned_data['slot_choices'] == 'slot_3' and error_dictionary['slot3_max'] == 'full':
                    return render(request, 'tracker/choose_slot.html', {'slot_selection_dictionary': slot_selection_dictionary,
                                                                        'session': session,
                                                                        'form': form,
                                                                        'error_dictionary': error_dictionary,
                                                                        'session_id': session_id
                                                                        })
                if form.cleaned_data['slot_choices'] == 'slot_1':
                    performance.chosen_slot_time = session.slot1_time
                elif form.cleaned_data['slot_choices'] == 'slot_2':
                    performance.chosen_slot_time = session.slot2_time
                elif form.cleaned_data['slot_choices'] == 'slot_3':
                    performance.chosen_slot_time = session.slot3_time
                performance.save()
                return HttpResponseRedirect('/tracker/john/') # Redirect after POST
        else:
            form = ChosenSlotForm() # An unbound form

        return render(request, 'tracker/choose_slot.html', {'slot_selection_dictionary': slot_selection_dictionary,
                                                            'session': session,
                                                            'form': form,
                                                            'error_dictionary': error_dictionary,
                                                            'session_id': session_id,
                                                            'slot_selection_dictionary_length': slot_selection_dictionary_length
                                                            })


def log_performance(request, session_id):
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
        session = get_object_or_404(Session, pk=session_id)
        
        performance_dictionary = {'distance':{}, 'time':{}}

        performance_dictionary['distance'][1] = request.user.rower.performance_set.get(session_id=session_id).set_distance1
        performance_dictionary['distance'][2] = request.user.rower.performance_set.get(session_id=session_id).set_distance2
        performance_dictionary['distance'][3] = request.user.rower.performance_set.get(session_id=session_id).set_distance3
        performance_dictionary['distance'][4] = request.user.rower.performance_set.get(session_id=session_id).set_distance4
        performance_dictionary['distance'][5] = request.user.rower.performance_set.get(session_id=session_id).set_distance5
        performance_dictionary['distance'][6] = request.user.rower.performance_set.get(session_id=session_id).set_distance6

        performance_dictionary['time'][1] = request.user.rower.performance_set.get(session_id=session_id).set_time1
        performance_dictionary['time'][2] = request.user.rower.performance_set.get(session_id=session_id).set_time2
        performance_dictionary['time'][3] = request.user.rower.performance_set.get(session_id=session_id).set_time3
        performance_dictionary['time'][4] = request.user.rower.performance_set.get(session_id=session_id).set_time4
        performance_dictionary['time'][5] = request.user.rower.performance_set.get(session_id=session_id).set_time5
        performance_dictionary['time'][6] = request.user.rower.performance_set.get(session_id=session_id).set_time6

        for number in range(1,7):
            if performance_dictionary['distance'][number] == "" and performance_dictionary['time'][number] =="":
                session_reps = number - 1
                break
            else:
                session_reps = 7


        if request.method =='POST': # If the form has been submitted...
            form1 = PerformanceTimeForm(request.POST) # form1 bound to the POST data
            if form1.is_valid(): # All validation rules pass
                # Process some data
                t = request.user.rower.performance_set.get(session_id=session_id)   # Get the correct performance for this session and user
                if form1.cleaned_data['recorded_time1'] != "":
                    t.recorded_time1 = form1.cleaned_data['recorded_time1']    # Make it's time1 attribute equal that submitted in the form
                    t.save()    # Save this performance with the new data
                if form1.cleaned_data['recorded_time2'] != "":
                    t.recorded_time2 = form1.cleaned_data['recorded_time2']
                    t.save()
                if form1.cleaned_data['recorded_time3'] != "":
                    t.recorded_time3 = form1.cleaned_data['recorded_time3']
                    t.save()
                if form1.cleaned_data['recorded_time4'] != "":
                    t.recorded_time_4 = form1.cleaned_data['recorded_time4']
                    t.save()
                if form1.cleaned_data['recorded_time5'] != "":
                    t.recorded_time5 = form1.cleaned_data['recorded_time5']
                    t.save()
                if form1.cleaned_data['recorded_time6'] != "":
                    t.recorded_time6 = form1.cleaned_data['recorded_time6']
                    t.save()
                if form1.cleaned_data['recorded_distance1'] != "":
                    t.recorded_distance1 = form1.cleaned_data['recorded_distance1']
                    t.save()
                if form1.cleaned_data['recorded_distance2'] != "":
                    t.recorded_distance2 = form1.cleaned_data['recorded_distance2']
                    t.save()
                if form1.cleaned_data['recorded_distance3'] != "":
                    t.recorded_distance3 = form1.cleaned_data['recorded_distance3']
                    t.save()
                if form1.cleaned_data['recorded_distance4'] != "":
                    t.recorded_distance4 = form1.cleaned_data['recorded_distance4']
                    t.save()
                if form1.cleaned_data['recorded_distance5'] != "":
                    t.recorded_distance5 = form1.cleaned_data['recorded_distance5']
                    t.save()
                if form1.cleaned_data['recorded_distance6'] != "":
                    t.recorded_distance6 = form1.cleaned_data['recorded_distance6']
                    t.save()

                t.unavailable = form1.cleaned_data['unavailable']
                t.completed = "yes"
                t.save()
                return HttpResponseRedirect('/tracker/thanks/') # Redirect after POST
        else:
            form1 = PerformanceTimeForm()  # An unbound form

        return render(request, 'tracker/log_performance.html', {'form1': form1, 'performance_dictionary': performance_dictionary, 'session_reps': session_reps,'session': session})


def john(request):
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
        try:
            active_squad = request.user.rower.squad
        except ObjectDoesNotExist:  #In case data doesn't exist
            active_squad=""
        try:
            active_session_list = request.user.rower.squad.session_set.all().order_by('date')[0:] #Gives us all sessions for the relevant rower.
        except ObjectDoesNotExist:
            active_session_list = []
        try:
            squad_list = Rower.objects.all().order_by('-id')[:5]
        except ObjectDoesNotExist:
            squad_list = []

        # Now we only take relevant sessions with regards to our current date.
        relevant_active_session_list = []    #For active sessions in required time period.
        length_active_session_list = len(active_session_list)
        rower_id = request.user.rower.id # Rower id to match up against session to find relevant performance --> then check to see if it's already been completed
        for y in range(length_active_session_list):
            if timezone.now().date() - datetime.timedelta(days=3) <= active_session_list[y].date < timezone.now().date() + datetime.timedelta(days=7):
                try:
                    if active_session_list[y].performance_set.get(rower_id=rower_id).completed != "yes" and not active_session_list[y].performance_set.get(rower_id=rower_id).unavailable:
                        relevant_active_session_list.append(active_session_list[y])
                except:
                    pc = PerformanceCopy.objects.get(session_id = active_session_list[y].id)
                    p = Performance(session = active_session_list[y],
                                    rower = request.user.rower,
                                    set_distance1 = pc.set_distance1,
                                    set_distance2 = pc.set_distance2,
                                    set_distance3 = pc.set_distance3,
                                    set_distance4 = pc.set_distance4,
                                    set_distance5 = pc.set_distance5,
                                    set_distance6 = pc.set_distance6,
                                    set_time1 = pc.set_time1,
                                    set_time2 = pc.set_time2,
                                    set_time3 = pc.set_time3,
                                    set_time4 = pc.set_time4,
                                    set_time5 = pc.set_time5,
                                    set_time6 = pc.set_time6,
                                    set_rate_cap1 = pc.set_rate_cap1,
                                    set_rate_cap2 = pc.set_rate_cap2,
                                    set_rate_cap3 = pc.set_rate_cap3,
                                    set_rate_cap4 = pc.set_rate_cap4,
                                    set_rate_cap5 = pc.set_rate_cap5,
                                    set_rate_cap6 = pc.set_rate_cap6,
                                    set_heart_zone1 = pc.set_heart_zone1,
                                    set_heart_zone2 = pc.set_heart_zone2,
                                    set_heart_zone3 = pc.set_heart_zone3,
                                    set_heart_zone4 = pc.set_heart_zone4,
                                    set_heart_zone5 = pc.set_heart_zone5,
                                    set_heart_zone6 = pc.set_heart_zone6,
                                    set_rest_time1 = pc.set_rest_time1,
                                    set_rest_time2 = pc.set_rest_time2,
                                    set_rest_time3 = pc.set_rest_time3,
                                    set_rest_time4 = pc.set_rest_time4,
                                    set_rest_time5 = pc.set_rest_time5,
                                    set_rest_time6 = pc.set_rest_time6
                                    )
                    p.save()
                    relevant_active_session_list.append(active_session_list[y])


        dictionary_session = {'name':{}, 'location':{}, 'date':{}, 'chosen_slot_time':{}, 'description':{}}
        
        for session in relevant_active_session_list:
            if session.slot2_time == None and session.slot3_time == None and session.slot1_time != None:
                rower_performance = request.user.rower.performance_set.get(session_id=session.id)
                rower_performance.chosen_slot_time = session.slot1_time
                rower_performance.save()
            try:
                dictionary_session['name'][session.id] = session.name
            except ObjectDoesNotExist:
                dictionary_session['name'][session.id] ="TBD"
            try:
                dictionary_session['location'][session.id] = session.location
            except ObjectDoesNotExist:
                dictionary_session['location'][session.id] ="TBD"
            try:
                dictionary_session['date'][session.id] = session.date
            except ObjectDoesNotExist:
                dictionary_session['date'][session.id]="TBD"
            try:
                dictionary_session['chosen_slot_time'][session.id] = session.performance_set.get(rower_id=rower_id).chosen_slot_time                
            except ObjectDoesNotExist:
                dictionary_session['chosen_slot_time'][session.id] ="TBD"
            try:
                dictionary_session['description'][session.id] = session.description
            except ObjectDoesNotExist:
                dictionary_session['description'][session.id] ="TBD"            

        #Establishes the list that orders the primary IDs by date.
        date_ordered_id = []
        for session in relevant_active_session_list:
            date_ordered_id.append(session.id)

        # Below is a way of storing the relevant set data to display for each training session
        # The opening dictionary key is based on the session that we're displaying from the date_ordered_id: we loop through sessions first!
        # Each session is a list of 6 dictionarys, matching the possible 6 performances within each session (allowing us to loop a second time)
        # Each dictionary has the key word and data for the relevant training data

        dictionary_performance = {}
        dictionary_performance_length = {}
        for x in date_ordered_id:
            dictionary_performance[x] = [{}, {}, {}, {}, {}, {}]
            dictionary_performance[x][0]['set_distance']=request.user.rower.performance_set.get(session_id=x).set_distance1
            dictionary_performance[x][0]['set_time']=request.user.rower.performance_set.get(session_id=x).set_time1
            dictionary_performance[x][0]['set_rate_cap']=request.user.rower.performance_set.get(session_id=x).set_rate_cap1
            dictionary_performance[x][0]['set_heart_zone']=request.user.rower.performance_set.get(session_id=x).set_heart_zone1
            dictionary_performance[x][0]['set_rest_time']=request.user.rower.performance_set.get(session_id=x).set_rest_time1

            dictionary_performance[x][1]['set_distance']=request.user.rower.performance_set.get(session_id=x).set_distance2
            dictionary_performance[x][1]['set_time']=request.user.rower.performance_set.get(session_id=x).set_time2
            dictionary_performance[x][1]['set_rate_cap']=request.user.rower.performance_set.get(session_id=x).set_rate_cap2
            dictionary_performance[x][1]['set_heart_zone']=request.user.rower.performance_set.get(session_id=x).set_heart_zone2
            dictionary_performance[x][1]['set_rest_time']=request.user.rower.performance_set.get(session_id=x).set_rest_time2

            dictionary_performance[x][2]['set_distance']=request.user.rower.performance_set.get(session_id=x).set_distance3
            dictionary_performance[x][2]['set_time']=request.user.rower.performance_set.get(session_id=x).set_time3
            dictionary_performance[x][2]['set_rate_cap']=request.user.rower.performance_set.get(session_id=x).set_rate_cap3
            dictionary_performance[x][2]['set_heart_zone']=request.user.rower.performance_set.get(session_id=x).set_heart_zone3
            dictionary_performance[x][2]['set_rest_time']=request.user.rower.performance_set.get(session_id=x).set_rest_time3

            dictionary_performance[x][3]['set_distance']=request.user.rower.performance_set.get(session_id=x).set_distance4
            dictionary_performance[x][3]['set_time']=request.user.rower.performance_set.get(session_id=x).set_time4
            dictionary_performance[x][3]['set_rate_cap']=request.user.rower.performance_set.get(session_id=x).set_rate_cap4
            dictionary_performance[x][3]['set_heart_zone']=request.user.rower.performance_set.get(session_id=x).set_heart_zone4
            dictionary_performance[x][3]['set_rest_time']=request.user.rower.performance_set.get(session_id=x).set_rest_time4

            dictionary_performance[x][4]['set_distance']=request.user.rower.performance_set.get(session_id=x).set_distance5
            dictionary_performance[x][4]['set_time']=request.user.rower.performance_set.get(session_id=x).set_time5
            dictionary_performance[x][4]['set_rate_cap']=request.user.rower.performance_set.get(session_id=x).set_rate_cap5
            dictionary_performance[x][4]['set_heart_zone']=request.user.rower.performance_set.get(session_id=x).set_heart_zone5
            dictionary_performance[x][4]['set_rest_time']=request.user.rower.performance_set.get(session_id=x).set_rest_time5

            dictionary_performance[x][5]['set_distance']=request.user.rower.performance_set.get(session_id=x).set_distance6
            dictionary_performance[x][5]['set_time']=request.user.rower.performance_set.get(session_id=x).set_time6
            dictionary_performance[x][5]['set_rate_cap']=request.user.rower.performance_set.get(session_id=x).set_rate_cap6
            dictionary_performance[x][5]['set_heart_zone']=request.user.rower.performance_set.get(session_id=x).set_heart_zone6
            dictionary_performance[x][5]['set_rest_time']=request.user.rower.performance_set.get(session_id=x).set_rest_time6

            # Here we shorten the list of 6 to only include those where a set_date or set_time exist - creating the right number of rows in html

            if request.user.rower.performance_set.get(session_id=x).set_distance1 == "" and request.user.rower.performance_set.get(session_id=x).set_time1 == "":
                dictionary_performance[x]= dictionary_performance[x][:0]
            elif request.user.rower.performance_set.get(session_id=x).set_distance2 == "" and request.user.rower.performance_set.get(session_id=x).set_time2 == "":
                dictionary_performance[x]= dictionary_performance[x][:1]
            elif request.user.rower.performance_set.get(session_id=x).set_distance3 == "" and request.user.rower.performance_set.get(session_id=x).set_time3 == "":
                dictionary_performance[x]= dictionary_performance[x][:2]
            elif request.user.rower.performance_set.get(session_id=x).set_distance4 == "" and request.user.rower.performance_set.get(session_id=x).set_time4 == "":
                dictionary_performance[x]= dictionary_performance[x][:3]
            elif request.user.rower.performance_set.get(session_id=x).set_distance5 == "" and request.user.rower.performance_set.get(session_id=x).set_time5 == "":
                dictionary_performance[x]= dictionary_performance[x][:4]
            elif request.user.rower.performance_set.get(session_id=x).set_distance6 == "" and request.user.rower.performance_set.get(session_id=x).set_time6 == "":
                dictionary_performance[x]= dictionary_performance[x][:5]

            # The list length for each session allows us to see when no set_distance/set_time has been set at all => thus displaying the 'No distances set yet' html content
            dictionary_performance_length[x] = len(dictionary_performance[x])


        user_list = User.objects.all()[:5]
        active_username = request.user.username
        active_first_name = request.user.first_name
        active_squad = request.user.rower.squad

        return render_to_response('tracker/john.html', {'dictionary_performance': dictionary_performance,
                                                        'dictionary_performance_length': dictionary_performance_length,
                                                        'relevant_active_session_list': relevant_active_session_list,
                                                        'date_ordered_id': date_ordered_id,
                                                        'dictionary_session': dictionary_session,
                                                        'active_session_list': active_session_list,
                                                        'active_squad': active_squad,
                                                        'squad_list': squad_list,
                                                        'user_list': user_list,
                                                        'active_username': active_username,
                                                        'active_first_name': active_first_name})




