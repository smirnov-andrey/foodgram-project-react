from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response


class AddRemoveListMixin:

    def add_remove_to_list(self, requested_id, field_name, target_model,):
        qs_object = get_object_or_404(self.get_queryset(), pk=requested_id)
        target_kwargs = {
            'user': self.request.user,
            field_name: qs_object
        }
        target_list = target_model.objects.filter(**target_kwargs)
        deleted_msg = {
            'detail': f'{qs_object._meta.verbose_name} удален из '
                      f'списка {target_model._meta.verbose_name}'
        }
        in_list_err_msg = {
            'errors': f'{qs_object._meta.verbose_name} уже есть '
                      f'в списке {target_model._meta.verbose_name}'
        }
        not_in_list_err_msg = {
            'errors': f'{qs_object._meta.verbose_name} нет в списке '
                      f'{target_model._meta.verbose_name}'
        }
        if self.request.method == 'POST':
            if target_list.exists():
                return Response(
                    in_list_err_msg,
                    status=status.HTTP_400_BAD_REQUEST
                )
            target_model.objects.create(**target_kwargs)
            serializer = self.get_serializer_class()
            return Response(
                serializer(
                    qs_object,
                    context={'request': self.request}
                ).data,
                status=status.HTTP_201_CREATED
            )
        if self.request.method == 'DELETE':
            if target_list.exists():
                target_list.delete()
                return Response(
                    deleted_msg,
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                not_in_list_err_msg,
                status=status.HTTP_400_BAD_REQUEST
            )
        return None
