from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from datetime import timedelta
from django.utils.dateformat import format
from .models import CarouselItem, Service, DutyStaff, Course, Registration, Event, Story, USRAchievement, TechProject, ExperienceCourse, TechSection
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import RegistrationForm

def home(request):
    carousels = CarouselItem.objects.filter(is_active=True).order_by('order')
    services = Service.objects.filter(is_active=True)
    duty_staffs = DutyStaff.objects.filter(is_on_duty=True)
    
    # 門戶平台展示內容 (Portal Sections)
    latest_stories = Story.objects.all()[:3]
    latest_achievements = USRAchievement.objects.all()[:3]
    tech_projects = TechProject.objects.filter(is_active=True)[:4]
    
    return render(request, 'inn_app/home.html', {
        'carousels': carousels,
        'services': services,
        'duty_staffs': duty_staffs,
        'latest_stories': latest_stories,
        'latest_achievements': latest_achievements,
        'tech_projects': tech_projects
    })

def course_list(request):
    courses = Course.objects.filter(is_active=True).order_by('-start_time')
    return render(request, 'inn_app/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    from django.utils import timezone
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # 時效過濾器
    now = timezone.now()
    is_reg_open = True
    reg_status_msg = ""
    
    if course.reg_start_time and now < course.reg_start_time:
        is_reg_open = False
        reg_status_msg = "報名尚未開放"
    elif course.reg_end_time and now > course.reg_end_time:
        is_reg_open = False
        reg_status_msg = "報名已截止"
        
    from django.db.models import Sum
    current_regs = Registration.objects.filter(course=course, is_waitlisted=False).aggregate(total=Sum('headcount'))['total'] or 0
    is_full = current_regs >= course.capacity

    if request.method == 'POST':
        # 把接收到的資料送入表單過濾器
        form = RegistrationForm(request.POST, course_instance=course)
        
        # Check time
        if not is_reg_open:
            messages.error(request, f'無法進行報名：{reg_status_msg}')
            return redirect('inn_app:course_detail', course_id=course.id)
            
        if form.is_valid():
            from django.db.models import Sum
            current_registrations = Registration.objects.filter(course=course, is_waitlisted=False).aggregate(total=Sum('headcount'))['total'] or 0
            registration = form.save(commit=False)
            registration.course = course
            
            requested = registration.headcount
            from django.core.mail import send_mail
            
            if current_registrations + requested > course.capacity:
                # [候補機制] 額滿則轉為候補單
                registration.is_waitlisted = True
                registration.save()
                messages.warning(request, f'⚠️ 正常名額已滿，您已成功排入候補名單（目前為候補第 {registration.waitlist_number} 號）！若有民眾取消釋出名額，我們將第一時間與您聯繫。')
                send_mail(
                    f'【水井村風雲客棧】候補通知：{course.title}',
                    f'{registration.name} 您好：\n\n您已成功排入 {course.title} 的候補名單，順位為第 {registration.waitlist_number} 號。\n若有釋出名額我們將主動與您聯繫，謝謝！',
                    'noreply@fengyuninn.com',
                    [registration.email],
                    fail_silently=True,
                )
            else:
                # [正取機制]
                registration.save()
                messages.success(request, '✅ 報名成功！我們已發送確認通知信至您的信箱，現場報到請出示專屬 QR 條碼。')
                checkin_url = request.build_absolute_uri(reverse('inn_app:check_in_scan', args=[str(registration.checkin_token)]))
                send_mail(
                    f'【水井村風雲客棧】報名成功通知：{course.title}',
                    f'{registration.name} 您好：\n\n恭喜您已成功報名！\n- 參與課程：{course.title}\n- 報名人數：{registration.headcount} 人\n\n【您的專屬QR報到憑證】（請保存此網址或截圖供現場工作人員掃描）\n{checkin_url}\n\n期待與您在客棧相見！',
                    'noreply@fengyuninn.com',
                    [registration.email],
                    fail_silently=True,
                )
                
            return redirect('inn_app:course_detail', course_id=course.id)
        else:
            # 若資料異常或違反重複報名，將錯誤訊息提示給外層
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
            
    # Generate Google Calendar URL
    from urllib.parse import quote
    end_time = course.end_time if course.end_time else course.start_time + timedelta(hours=2)
    dtstart = format(course.start_time, 'Ymd\\THis')
    dtend = format(end_time, 'Ymd\\THis')
    gcal_url = (
        f"https://calendar.google.com/calendar/render?action=TEMPLATE"
        f"&text={quote(course.title)}&dates={dtstart}/{dtend}"
        f"&details={quote(course.description)}&location={quote('水井村風雲客棧')}"
    )
    
    return render(request, 'inn_app/course_detail.html', {
        'course': course, 
        'gcal_url': gcal_url,
        'is_reg_open': is_reg_open,
        'reg_status_msg': reg_status_msg,
        'is_full': is_full
    })

def duty_staff(request):
    staffs = DutyStaff.objects.all().order_by('-is_on_duty')
    return render(request, 'inn_app/duty_staff.html', {'staffs': staffs})

def calendar_view(request):
    return render(request, 'inn_app/calendar.html')

def course_events_api(request):
    courses = Course.objects.filter(is_active=True)
    events = []
    for c in courses:
        end_time = c.end_time if c.end_time else c.start_time + timedelta(hours=2)
        events.append({
            'id': c.id,
            'title': f"🎓[上課] {c.title}",
            'start': c.start_time.isoformat(),
            'end': end_time.isoformat(),
            'url': reverse('inn_app:course_detail', args=[c.id]),
            'color': '#5D4037'
        })
        
        # 將報名時間也加為行事曆上的事件（綠色標籤）
        if c.reg_start_time and c.reg_end_time:
            events.append({
                'id': f"reg-{c.id}",
                'title': f"📝[報名開放] {c.title}",
                'start': c.reg_start_time.isoformat(),
                'end': c.reg_end_time.isoformat(),
                'url': reverse('inn_app:course_detail', args=[c.id]),
                'color': '#2E8B57'
            })
    return JsonResponse(events, safe=False)

def download_ics(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    end_time = course.end_time if course.end_time else course.start_time + timedelta(hours=2)
    
    dtstart = format(course.start_time, 'Ymd\\THis')
    dtend = format(end_time, 'Ymd\\THis')
    desc = course.description.replace('\n', '\\n').replace('\r', '')
    
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//FengYunInn//NONSGML v1.0//EN
BEGIN:VEVENT
UID:course-{course.id}@fengyuninn.com
DTSTAMP:{dtstart}
DTSTART;TZID=Asia/Taipei:{dtstart}
DTEND;TZID=Asia/Taipei:{dtend}
SUMMARY:{course.title}
DESCRIPTION:{desc}
LOCATION:水井村風雲客棧
END:VEVENT
END:VCALENDAR"""
    
    response = HttpResponse(ics_content, content_type='text/calendar')
    response['Content-Disposition'] = f'attachment; filename="course_{course.id}.ics"'
    return response

def my_bookings(request):
    registrations = None
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        if phone and email:
            registrations = Registration.objects.filter(phone=phone, email=email).select_related('course').order_by('-created_at')
            if not registrations.exists():
                messages.error(request, '❌ 找不到相符的報名紀錄，請確認電話與 Email 是否完全正確（過去無填寫 Email 的紀錄將無法被查詢）。')
            else:
                messages.success(request, '✅ 查詢成功！以下是您的報名紀錄。')
        else:
            messages.error(request, '❌ 請確認已經輸入【聯絡電話】與【Email】再送出查詢。')
            
    return render(request, 'inn_app/my_bookings.html', {'registrations': registrations})

def cancel_booking(request, reg_id):
    if request.method == 'POST':
        registration = get_object_or_404(Registration, id=reg_id)
        course_title = registration.course.title
        is_wait = registration.is_waitlisted
        registration.delete()
        if is_wait:
            messages.success(request, f'✅ 已取消【{course_title}】的候補登記！')
        else:
            messages.success(request, f'✅ 已成功取消【{course_title}】的報名紀錄！該名額已經重新釋出。')
    # Because my_bookings requires POST to show results, we just redirect it to a clean GET state. 
    # Or ideally, redirect to home page with success message.
    return redirect('inn_app:home')

def check_in_scan(request, token):
    if not request.user.is_staff:
        from django.contrib.auth.views import redirect_to_login
        # 沒有權限的手機一掃描，直接被踢去登入畫面
        return redirect_to_login(request.get_full_path())
        
    registration = get_object_or_404(Registration, checkin_token=token)
    
    if registration.is_attended:
        messages.warning(request, f"⚠️ 【{registration.name}】（共 {registration.headcount} 人）稍早已經報到過了喔！請勿重複核銷。")
    else:
        registration.is_attended = True
        registration.save()
        messages.success(request, f"🎉 掃碼核銷成功！【{registration.name}】（共 {registration.headcount} 人）已成功登記入場。")
        
    return redirect('inn_app:home')

def about(request):
    return render(request, 'inn_app/about.html')

def event_list(request):
    query = request.GET.get('q', '')
    events = Event.objects.all().order_by('-date')
    
    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    
    paginator = Paginator(events, 6) # 6 events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'inn_app/event_list.html', {
        'page_obj': page_obj,
        'query': query
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'inn_app/event_detail.html', {'event': event})

def contact(request):
    if request.method == 'POST':
        # 在實際應用中可以在此處理表單發送，目前僅作示範
        messages.success(request, '感謝您的訊息！我們將盡快與您聯絡。')
        return redirect('inn_app:contact')
    return render(request, 'inn_app/contact.html')

def story_list(request):
    cat = request.GET.get('cat')
    stories = Story.objects.all()
    if cat:
        stories = stories.filter(category=cat)
    
    paginator = Paginator(stories, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'inn_app/story_list.html', {
        'page_obj': page_obj,
        'active_cat': cat
    })

def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    return render(request, 'inn_app/story_detail.html', {'story': story})

def usr_showcase(request):
    achievements = USRAchievement.objects.all()
    return render(request, 'inn_app/usr_showcase.html', {'achievements': achievements})

def aiot_guide(request):
    sections = TechSection.objects.filter(is_active=True).prefetch_related('projects')
    return render(request, 'inn_app/aiot_guide.html', {'sections': sections})

def workshop_list(request):
    workshops = ExperienceCourse.objects.all()
    return render(request, 'inn_app/workshop_list.html', {'workshops': workshops})
