from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import status

from maestro.models import Medicamento
from .models import (
    Consumo,
    Movimiento
)
from .serializers import (
    MovimientoMedicamentoResponseSerializer,
    MovimientoSerializer,
    ConsumoSerializer
)

from rest_framework.views import APIView


class MovimientoListCreateView(viewsets.ModelViewSet):
    serializer_class = MovimientoSerializer
    queryset = Movimiento.objects.all()


class MovimientoRetrieveDestroyView(viewsets.ModelViewSet):
    serializer_class = MovimientoSerializer
    queryset = Movimiento.objects.all()


class MovimientoLoteRetrieveView:
    pass


class MovimientoMedicamentoView(APIView):
    def get(self, request):
        # Obtener todos los movimientos
        movimientos = Movimiento.objects.select_related(
            'institucion', 'lote__medicamento')

        # Crear un diccionario para agrupar movimientos por medicamento
        medicamentos_movimientos = {}

        for movimiento in movimientos:
            medicamento = movimiento.lote.medicamento.id # type: ignore

            if medicamento not in medicamentos_movimientos:
                medicamentos_movimientos[medicamento] = {
                    "medicamento": medicamento,
                    "movimientos": []
                }

            medicamentos_movimientos[medicamento]["movimientos"].append({
                "lote": movimiento.lote.id, # type: ignore
                "institucion": movimiento.institucion.id, # type: ignore
                "fecha": movimiento.fecha
            })

        # Convertir el diccionario a una lista
        resultado = list(medicamentos_movimientos.values())

        return Response(resultado, status=status.HTTP_200_OK)


class ConsumoListCreateView(viewsets.ModelViewSet):
    serializer_class = ConsumoSerializer
    queryset = Consumo.objects.all()


class ConsumoRetrieveDestroyView(viewsets.ModelViewSet):
    serializer_class = ConsumoSerializer
    queryset = Consumo.objects.all()


# class ConsumoMedicamentoAPIView(viewsets.ModelViewSet):
#     serializer_class = ConsumoSerializer
#     queryset = Consumo.objects.all()

# IMPLEMENTACION PARA EL TEST AVANZADO 101_a_stock_endpoints_tests ->test_consumo_medicamento
# class ConsumoMedicamentoAPIView(APIView):
#     def get(self, request):
#         consumos = Consumo.objects.select_related('institucion', 'medicamento')

#         medicamentos_consumos = {}
#         for consumo in consumos:
#             medicamento_id = consumo.medicamento.id
#             if medicamento_id not in medicamentos_consumos:
#                 medicamentos_consumos[medicamento_id] = {
#                     "medicamento": medicamento_id,
#                     "cantidad": 0,
#                     "consumos": []
#                 }

#             medicamentos_consumos[medicamento_id]["cantidad"] += consumo.cantidad
#             medicamentos_consumos[medicamento_id]["consumos"].append({
#                 "institucion": consumo.institucion.id,
#                 "cantidad": consumo.cantidad,
#                 "fecha": consumo.fecha
#             })

#         resultado = medicamentos_consumos

#         return Response(resultado, status=status.HTTP_200_OK)
    
# IMPLEMENTACION PARA EL TEST AVANZADO 101_a_stock_endpoints_tests ->test_consumo_medicamento_id
class ConsumoMedicamentoAPIView(APIView):
    def get(self, request, medicamento=None):
        if medicamento:
            consumos = Consumo.objects.filter(medicamento_id=medicamento).select_related('institucion', 'medicamento')

            if not consumos.exists():
                return Response([], status=status.HTTP_200_OK)

            medicamento_consumos = {
                "medicamento": medicamento,
                "cantidad": 0,
                "consumos": []
            }

            for consumo in consumos:
                medicamento_consumos["cantidad"] += consumo.cantidad
                medicamento_consumos["consumos"].append({
                    "institucion": consumo.institucion.id, # type: ignore
                    "cantidad": consumo.cantidad,
                    "fecha": consumo.fecha
                })

            resultado = [medicamento_consumos]

            return Response(resultado, status=status.HTTP_200_OK)
        else:
            consumos = Consumo.objects.select_related('institucion', 'medicamento')

            medicamentos_consumos = {}
            for consumo in consumos:
                medicamento_id = consumo.medicamento.id # type: ignore
                if medicamento_id not in medicamentos_consumos:
                    medicamentos_consumos[medicamento_id] = {
                        "medicamento": medicamento_id,
                        "cantidad": 0,
                        "consumos": []
                    }

                medicamentos_consumos[medicamento_id]["cantidad"] += consumo.cantidad
                medicamentos_consumos[medicamento_id]["consumos"].append({
                    "institucion": consumo.institucion.id, # type: ignore
                    "cantidad": consumo.cantidad,
                    "fecha": consumo.fecha
                })

            resultado = medicamentos_consumos

            return Response(resultado, status=status.HTTP_200_OK)    
