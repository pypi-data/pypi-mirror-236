from django.utils.translation import gettext_lazy as _
from rest_framework import serializers as _serializers
from rest_framework.exceptions import ValidationError as _ValidationError
from rest_framework.request import Request as _Request

from b2_utils import models as _models
from b2_utils.serializers.relations import PrimaryKeyRelatedFieldWithSerializer

__all__ = [
    "PrimaryKeyRelatedFieldWithSerializer",
    "PhoneSerializer",
    "CitySerializer",
    "AddressSerializer",
]


class PhoneSerializer(_serializers.ModelSerializer):
    """A Phone serializer"""

    class Meta:
        model = _models.Phone
        fields = ["id", "country_code", "area_code", "number", "created", "modified"]


class CitySerializer(_serializers.ModelSerializer):
    """A City serializer"""

    class Meta:
        model = _models.City
        fields = [
            "id",
            "name",
            "state",
            "created",
            "modified",
        ]


class AddressSerializer(_serializers.ModelSerializer):
    """An Address serializer"""

    city = PrimaryKeyRelatedFieldWithSerializer(
        CitySerializer,
        queryset=_models.City.objects.all(),
    )

    class Meta:
        model = _models.Address
        fields = [
            "id",
            "city",
            "street",
            "number",
            "additional_info",
            "district",
            "zip_code",
            "created",
            "modified",
        ]


class UpdatableFieldsSerializer(_serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        meta = getattr(self, "Meta", None)
        updatable_fields = getattr(meta, "updatable_fields", {})
        non_updatable_fields = getattr(meta, "non_updatable_fields", {})

        assert not (updatable_fields and non_updatable_fields), (  # noqa: S101
            "Cannot set both 'updatable_fields' and 'non_updatable_fields' options on "
            f"serializer {self.__class__.__name__}."
        )

        method = getattr(kwargs.get("context", {}).get("request", {}), "method", None)
        data = kwargs.get("data", {})

        if method in {"PATCH", "PUT"}:
            if updatable_fields:
                kwargs["data"] = {
                    key: value for key, value in data.items() if key in updatable_fields
                }
            if non_updatable_fields:
                kwargs["data"] = {
                    key: value
                    for key, value in data.items()
                    if key not in non_updatable_fields
                }

        super().__init__(*args, **kwargs)


class ModelSerializerWithRequest(_serializers.ModelSerializer):
    default_error_messages = {
        "insuficient_permissions": _(
            _(
                "You cannot modify this property. Please contact the system"
                " administrator",
            ),
        ),
    }

    @property
    def _request(self) -> _Request | None:
        return self.context.get("request")

    def _allow_to_user(self, user_cls, role=None):
        if not isinstance(self._request.user, user_cls) or (
            role and self._request.user.role != role
        ):
            error = "insuficient_permissions"
            raise _ValidationError(self.default_error_messages[error], error)

    def _deny_to_user(self, user_cls, role=None):
        if isinstance(self._request.user, user_cls) and (
            not role or self._request.user.role == role
        ):
            error = "insuficient_permissions"
            raise _ValidationError(self.default_error_messages[error], error)
