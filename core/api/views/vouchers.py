from django.contrib.auth import login
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Event, Voucher
from api.serializers import VoucherSerializer
from django.utils.decorators import method_decorator
from core.utils.decorators import OrganizerOnly, AppUserOnly


class VoucherListAPI(APIView):
    '''For getting all vouchers created by the user'''
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(OrganizerOnly)
    def get(self, request, *args, **kwargs):
        '''Uses get request to fetch all vouchers created by the user'''
        user = request.user
        voucher = Voucher.objects.filter(created_by=user).order_by("-id")
        serializer = VoucherSerializer(voucher, many=True)
        return Response({
            "vouchers": serializer.data,
        }, status=status.HTTP_200_OK)


class CUDVoucherAPI(APIView):
    '''For Create, Update, Delete of vouchers'''
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(OrganizerOnly)
    def post(self, request, *args, **kwargs):
        '''Uses the post request to create a new voucher'''
        user = request.user
        amount = request.data.get("amount")
        voucher_type = request.data.get("voucher_type")
        event_id = request.data.get("event_id")
        event = Event.objects.filter(id=event_id).first()
        if event is not None:
            voucher = Voucher.objects.create(
                event=event,
                amount=amount,
                voucher_type=voucher_type,
                created_by=user,
            )
            serializer = VoucherSerializer(voucher, many=False)
            return Response({
                "voucher": serializer.data,
            }, status=status.HTTP_201_CREATED)
        else:
            print("Event not found")
            return Response({
                "message": "Event Not Found",
            }, status=status.HTTP_404_NOT_FOUND)

    @method_decorator(OrganizerOnly)
    def put(self, request, *args, **kwargs):
        '''Uses the put request to update the voucher'''
        user = request.user
        voucher_id = request.data.get("voucher_id")
        voucher = Voucher.objects.filter(id=voucher_id, created_by=user).first()  # noqa
        amount = request.data.get("amount")
        voucher_type = request.data.get("voucher_type")
        event_id = request.data.get("event_id")
        event = Event.objects.filter(event_id=event_id).first()

        if (voucher is not None) and (event is not None):
            voucher.amount = amount
            voucher.voucher_type = voucher_type
            voucher.event = event
            voucher.save()
            serializer = VoucherSerializer(voucher, many=False)
            return Response({
                "voucher": serializer.data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Voucher or Event Not Found",
            }, status=status.HTTP_404_NOT_FOUND)

    @method_decorator(OrganizerOnly)
    def delete(self, request, *args, **kwargs):
        '''Uses the delete request to delete an event'''
        user = request.user
        voucher_id = request.data.get("voucher_id")
        voucher = Voucher.objects.filter(voucher_id=voucher_id, created_by=user).first()  # noqa
        if voucher is not None:
            voucher.delete()
            return Response({
                "message": "Voucher Deleted Successfully",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Voucher Not Found"
            }, status=status.HTTP_404_NOT_FOUND)
