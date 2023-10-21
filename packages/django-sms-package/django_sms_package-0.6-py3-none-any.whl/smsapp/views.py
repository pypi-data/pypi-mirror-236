from django.shortcuts import render, redirect

from django.http import JsonResponse
from . models import Message
from django.db.models import Count, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import make_aware
import datetime
from datetime import datetime as dt

from . utils import data_perday, data_permonth

# Create your views here.
def index(request):
    sms_id = request.GET.get("smsId")
    phone = request.GET.get("to")
    response = request.GET.get('sendResult')
    dr = request.GET.get("dr")

    if dr == "000":
        message = Message.objects.get(sms_id=sms_id, phone=phone)
        message.success = True
        message.save()

    return JsonResponse({"message": response, "code": dr})

def chart_view(request):
    #Bar Chart Data for total number of messages per day
    
    end_date = timezone.now()
    start_date = end_date - datetime.timedelta(days=7)
    
    if "date_range" in request.GET:
        date_range = request.GET["date_range"]
        start, end = date_range.split('-')
        start_date = make_aware(dt.strptime(start, '%B %d, %Y '))
        # Upto the time the request came
        hour = timezone.now().hour
        min = timezone.now().minute + 1
        end_date = make_aware(dt.strptime(end, ' %B %d, %Y')) + datetime.timedelta(hours=hour, minutes=min)
    
    
    # If the date range is greater than a month group by month 
    trunc = TruncDate 
    diff = end_date - start_date
    if diff.days > 31:
        trunc = TruncMonth
    
    sms_data = Message.objects.filter(sent_at__range=(start_date, end_date))\
        .annotate(date=trunc('sent_at'))\
            .values('date')\
                .annotate(success_count=Count('id', filter=Q(success=True)), failed_count=Count('id', filter=Q(success=False)))\
                    .order_by('date')
    
    x_bardata, y_bardata = data_perday(sms_data, start_date, end_date)
    if diff.days > 31:
        x_bardata, y_bardata = data_permonth(sms_data, start_date, end_date)

    # Pie Chart Data
    providers_query = Message.objects.filter(success=True)\
        .values('provider').annotate(count = Count('id'))
    
    providers = list(map(str, Message.Providers))
    
    providers_data = []
    for provider in providers:
        item = providers_query.filter(provider = provider)
        count = item[0]['count'] if item else 0
        providers_data.append(count) 
    

    # Table Data
    
    all_message = Message.objects.all().order_by("-sent_at")
    
    paginator = Paginator(all_message, 3)
    table_data = []
    page = int(request.GET.get("page", 1))
    
    try:
        for i in range(page):
            page_data = paginator.page(i+1)
            table_data += page_data.object_list
    except PageNotAnInteger:
        table_data = paginator.page(1) 
    except EmptyPage:
        for p in paginator.page_range[paginator.num_pages]:
            page_data = paginator.page(p+1)
            table_data += page_data.object_list
    
    context = {
        "providers": providers,
        "providers_data": providers_data, 
        "y_bardata": y_bardata,
        "total_success_sms": sum(list(map(lambda x: x["success_count"], y_bardata))),
        "total_failed_sms": sum(list(map(lambda x: x["failed_count"], y_bardata))),
        "total_sms": sum(list(map(lambda x: x["failed_count"]+x["success_count"], y_bardata))),
        "x_bardata": x_bardata,
        "page_data": page_data,
        "table_data": table_data,
    }
    
    return render(request, 'chart/index.html', context)
    