from django.shortcuts import render
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from .models import Client, Project
import json
from rest_framework import viewsets
from .serializers import ClientSerializer, ProjectSerializer

def project_list(request):
    # Obtenemos proyectos y optimizamos la consulta a la BD
    projects = Project.objects.select_related('client').all().order_by('-start_date')
    return render(request, 'core/project_list.html', {'projects': projects})

def earnings_dashboard(request):
    # Agrupamos por mes usando start_date
    metrics = Project.objects.annotate(
        month=TruncMonth('start_date')
    ).values('month').annotate(
        total_projects=Count('id'),
        # Nota: Aquí sumamos los costos de ventanas + adicionales. 
        # Para simplificar en SQL puro, sumamos el precio de las ventanas relacionadas
        total_earnings=Sum('windows__price') + Sum('other_windows_value')
    ).order_by('month')

    # Preparamos datos para Chart.js
    labels = [m['month'].strftime("%B %Y") for m in metrics if m['month']]
    data = [float(m['total_earnings'] or 0) for m in metrics if m['month']]

    context = {
        'metrics': metrics,
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data)
    }
    return render(request, 'core/dashboard.html', context)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer