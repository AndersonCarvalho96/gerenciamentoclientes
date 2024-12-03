from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Cliente
from .forms import ClienteForm
from django.utils import timezone
from datetime import timedelta


def home(request):
    # Estatísticas
    total_clientes = Cliente.objects.count()
    clientes_ativos = Cliente.objects.filter(ativo=True).count()

    # Clientes cadastrados no último mês
    data_atual = timezone.now()
    data_inicial_mes = data_atual - timedelta(days=30)
    novos_clientes_mes = Cliente.objects.filter(
        criado_em__gte=data_inicial_mes).count()

    context = {
        'total_clientes': total_clientes,
        'clientes_ativos': clientes_ativos,
        'novos_clientes_mes': novos_clientes_mes,
    }
    return render(request, 'clientes\home.html', context)


def listar_clientes(request):
    clientes_list = Cliente.objects.all()
    paginator = Paginator(clientes_list, 10)  # 10 clientes por página
    page = request.GET.get('page')
    clientes = paginator.get_page(page)
    return render(request, 'clientes/listar_clientes.html', {'clientes': clientes})


def adicionar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)  # Não salva ainda
            cliente.ativo = True  # Define o cliente como ativo
            cliente.save()  # Agora salva no banco de dados
            messages.success(request, 'Cliente adicionado com sucesso!')
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/adicionar_cliente.html', {'form': form})


def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/editar_cliente.html', {'form': form, 'cliente': cliente})


def excluir_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente excluído com sucesso!')
        return redirect('listar_clientes')

    return render(request, 'clientes/excluir_cliente.html', {'cliente': cliente})
