from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum
from categorias.models import Categoria
from platos.models import Plato
from mesas.models import Mesa
from meseros.models import Mesero
from detalles_pedido.models import DetallePedido
from .models import Pedido


# 1. Vista del Menú y Creación / Acumulación de Pedidos por Mesa
def lista_menu(request):
    categorias = Categoria.objects.prefetch_related('platos').all()
    mesas = Mesa.objects.all()
    meseros = Mesero.objects.all()

    if request.method == 'POST':
        mesa_id = request.POST.get('mesa_id')
        mesero_id = request.POST.get('mesero_id')
        plato_id = request.POST.get('plato_id')
        cantidad = int(request.POST.get('cantidad', 1))

        mesa = get_object_or_404(Mesa, id=mesa_id)
        mesero = get_object_or_404(Mesero, id=mesero_id)
        plato = get_object_or_404(Plato, id=plato_id)

        # Buscar si la mesa ya tiene un pedido en estado PENDIENTE para acumularle más platos.
        pedido, creado = Pedido.objects.get_or_create(
            mesa=mesa,
            estado='PENDIENTE',
            defaults={'mesero': mesero}
        )

        # Crear el detalle del plato y asociarlo al pedido (Relación N:M)
        DetallePedido.objects.create(
            pedido=pedido,
            plato=plato,
            cantidad=cantidad
        )

        # Marcar la mesa como ocupada
        mesa.ocupada = True
        mesa.save()

        messages.success(request, f'¡Plato "{plato.nombre}" agregado correctamente a la Mesa #{mesa.numero}!')
        return redirect('lista_menu')

    context = {
        'categorias': categorias,
        'mesas': mesas,
        'meseros': meseros,
    }
    return render(request, 'pedidos/menu.html', context)

# 2. Vista de Cocina (Pedidos pendientes y en preparación)
def vista_cocina(request):
    pedidos_pendientes = Pedido.objects.filter(estado__in=['PENDIENTE', 'EN_PREPARACION']).order_by('fecha_creacion')
    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        nuevo_estado = request.POST.get('nuevo_estado')
        pedido = get_object_or_404(Pedido, id=pedido_id)
        pedido.estado = nuevo_estado
        pedido.save()
        return redirect('vista_cocina')
        
    return render(request, 'pedidos/cocina.html', {'pedidos': pedidos_pendientes})

# 3. Vista de Caja / Factura de Mesa (Suma todos los pedidos activos de la mesa)
def detalle_cuenta(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    pedidos_activos = Pedido.objects.filter(mesa=mesa).exclude(estado='PAGADO')
    total_cuenta = sum(p.total_pedido for p in pedidos_activos)
    
    if request.method == 'POST':
        pedidos_activos.update(estado='PAGADO')
        mesa.ocupada = False
        mesa.save()
        return redirect('lista_menu')

    context = {
        'mesa': mesa,
        'pedidos_activos': pedidos_activos,
        'total_cuenta': total_cuenta,
    }
    return render(request, 'pedidos/cuenta.html', context)

# 4. Vista de Dashboard / Estadísticas para el Administrador
def dashboard(request):
    pedidos_pagados = Pedido.objects.filter(estado='PAGADO')
    ingresos_totales = sum(p.total_pedido for p in pedidos_pagados)

    platos_populares = Plato.objects.annotate(
        total_vendido=Sum('detallepedido__cantidad')
    ).filter(total_vendido__gt=0).order_by('-total_vendido')[:5]

    total_mesas = Mesa.objects.count()
    mesas_ocupadas = Mesa.objects.filter(ocupada=True).count()
    mesas_disponibles = total_mesas - mesas_ocupadas

    pedidos_pendientes = Pedido.objects.filter(estado='PENDIENTE').count()
    pedidos_cocina = Pedido.objects.filter(estado='EN_PREPARACION').count()

    context = {
        'ingresos_totales': ingresos_totales,
        'platos_populares': platos_populares,
        'total_mesas': total_mesas,
        'mesas_ocupadas': mesas_ocupadas,
        'mesas_disponibles': mesas_disponibles,
        'pedidos_pendientes': pedidos_pendientes,
        'pedidos_cocina': pedidos_cocina,
    }
    return render(request, 'pedidos/dashboard.html', context)