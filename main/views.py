#from django.shortcuts import render
#from django.http import HttpResponse
#from .models import area
# Create your views here.
#def homepage(request):
#    return render(request=request,
#                  template_name="main/home.html",
#                  context={"areas": area.objects.all()})

from django.shortcuts import render, get_object_or_404
from .models import Area, TipoDocumento, Documento

# 1. Lista de todas las áreas 
def lista_areas(request):
    areas = Area.objects.all()
    return render(request, 'main/lista_areas.html', {'areas': areas})

# 2. Dentro de un área, mostrar los tipos de documentos
def detalle_area(request, area_slug):
    area = get_object_or_404(Area, slug=area_slug)
    # Obtenemos los tipos de documento asociados a esta área
    tipos = area.tipos_documento.all() 
    return render(request, 'main/detalle_area.html', {'area': area, 'tipos': tipos})

# 3. Lista de PDFs dentro de un tipo específico
def lista_documentos(request, area_slug, tipo_slug):
    area = get_object_or_404(Area, slug=area_slug)
    tipo = get_object_or_404(TipoDocumento, slug=tipo_slug, area=area)
    # Gracias al 'ordering' en el modelo, ya vienen ordenados por fecha descendente
    documentos = tipo.documentos.all()
    
    return render(request, 'main/lista_documentos.html', {
        'area': area,
        'tipo': tipo,
        'documentos': documentos
    })