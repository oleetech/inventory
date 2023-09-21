from django.shortcuts import render
from django.http import HttpResponse
from ItemMasterData.utils import calculate_instock
from django.db.models.functions import TruncMonth

from decimal import Decimal  # Import the Decimal type
from django.db.models import Sum
from datetime import date, timedelta
from Purchasing.models import PurchaseItem
from Sales.models import SalesOrderInfo
# Create your views here.
from .models import Header, Navigation, IntroSection, AboutUs
import plotly.graph_objs as go
from ItemMasterData.models import Item
def home(request):
    # Retrieve objects from your models
    header = Header.objects.first()
    navigation = Navigation.objects.all()
    intro_section = IntroSection.objects.first()
    about_us = AboutUs.objects.first()
    
    # Create a context dictionary with the data
    context = {
        'header': header,
        'navigation': navigation,
        'intro_section': intro_section,
        'about_us': about_us,
    }        
    return render(request, 'home.html',context)




def dashboard(request):
    
    
    # Fetch the first 3 items
    items = Item.objects.all()

    # Calculate instock values for each item and create a list of (item, instock_value) tuples
    item_data = [(item, calculate_instock(item.code)) for item in items]

    # Sort the items by instock values in descending order
    sorted_items = sorted(item_data, key=lambda x: x[1], reverse=True)

    # Select the top 3 items
    top_items = sorted_items[:3]

    # Create data for the chart
    item_data = [{'name': item.name, 'instock': float(instock)} for item, instock in top_items]
    
#
#  _   ____                                  _     _                                       _                          
# / | |___ \     _ __ ___     ___    _ __   | |_  | |__      _ __    _   _   _ __    ___  | |__     __ _   ___    ___ 
# | |   __) |   | '_ ` _ \   / _ \  | '_ \  | __| | '_ \    | '_ \  | | | | | '__|  / __| | '_ \   / _` | / __|  / _ \
# | |  / __/    | | | | | | | (_) | | | | | | |_  | | | |   | |_) | | |_| | | |    | (__  | | | | | (_| | \__ \ |  __/
# |_| |_____|   |_| |_| |_|  \___/  |_| |_|  \__| |_| |_|   | .__/   \__,_| |_|     \___| |_| |_|  \__,_| |___/  \___|
#                                                           |_|                                                       

    # Calculate the date 12 months ago from today
    twelve_months_ago = date.today() - timedelta(days=365)

    # Query the database to get purchase data for the last 12 months
    purchase_data = PurchaseItem.objects.filter(
        created__gte=twelve_months_ago
    ).values('name').annotate(total_amount=Sum('priceTotal')).order_by('-total_amount')

    # Extract item names and total amounts for the pie chart
    item_names = [item['name'] for item in purchase_data]
    total_amounts = [item['total_amount'] for item in purchase_data]

    # Create a Plotly pie chart
    fig = go.Figure(data=[go.Pie(labels=item_names, values=total_amounts)])

    # Convert the Plotly figure to JSON
    chart_data = fig.to_json()    
    
    
#  _____                      ____                 _                                         ____            _                     _                                          _     
# |_   _|   ___    _ __      / ___|  _   _   ___  | |_    ___    _ __ ___     ___   _ __    / ___|    __ _  | |   ___   ___       / \     _ __ ___     ___    _   _   _ __   | |_   
#   | |    / _ \  | '_ \    | |     | | | | / __| | __|  / _ \  | '_ ` _ \   / _ \ | '__|   \___ \   / _` | | |  / _ \ / __|     / _ \   | '_ ` _ \   / _ \  | | | | | '_ \  | __|  
#   | |   | (_) | | |_) |   | |___  | |_| | \__ \ | |_  | (_) | | | | | | | |  __/ | |       ___) | | (_| | | | |  __/ \__ \    / ___ \  | | | | | | | (_) | | |_| | | | | | | |_   
#   |_|    \___/  | .__/     \____|  \__,_| |___/  \__|  \___/  |_| |_| |_|  \___| |_|      |____/   \__,_| |_|  \___| |___/   /_/   \_\ |_| |_| |_|  \___/   \__,_| |_| |_|  \__|  
#                 |_|                                                                                                                                                               

  # Query the database to get the top 20 customers with total amounts
    customer_data = SalesOrderInfo.objects.filter(status='O').values('customerName__name').annotate(total_amount=Sum('totalAmount')).order_by('-total_amount')[:20]

    # Extract customer names and total amounts for the pie chart
    customer_names = [item['customerName__name'] for item in customer_data]
    total_amounts = [item['total_amount'] for item in customer_data]

    # Create a Plotly pie chart
    fig = go.Figure(data=[go.Pie(labels=customer_names, values=total_amounts)])

    # Convert the Plotly figure to JSON
    top_customer_sales_amount = fig.to_json()   
    
    
    
    
#  ____            _                 ___               _                 _____                             _ 
# / ___|    __ _  | |   ___   ___   / _ \   _ __    __| |   ___   _ __  |_   _|  _ __    ___   _ __     __| |
# \___ \   / _` | | |  / _ \ / __| | | | | | '__|  / _` |  / _ \ | '__|   | |   | '__|  / _ \ | '_ \   / _` |
#  ___) | | (_| | | | |  __/ \__ \ | |_| | | |    | (_| | |  __/ | |      | |   | |    |  __/ | | | | | (_| |
# |____/   \__,_| |_|  \___| |___/  \___/  |_|     \__,_|  \___| |_|      |_|   |_|     \___| |_| |_|  \__,_|
#                                                                                                            
  
    # Calculate the date 12 months ago from today
    twelve_months_ago = date.today() - timedelta(days=365)

    # Query the database to get sales order data for the last 12 months
    trend_data = SalesOrderInfo.objects.filter(
        created__gte=twelve_months_ago
    ).annotate(month=TruncMonth('created')).values('month').annotate(total_quantity=Sum('totalAmount')).order_by('month')

    # Extract month labels and total quantities for the bar chart
    month_labels = [item['month'].strftime('%Y-%m') for item in trend_data]
    total_quantities = [float(item['total_quantity']) for item in trend_data]    


    
    return render(request, 'dashboard.html',{'item_data': item_data,'chart_data': chart_data,'top_customer_sales_amount':top_customer_sales_amount,'month_labels': month_labels, 'total_quantities': total_quantities})