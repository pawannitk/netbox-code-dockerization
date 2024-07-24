from django.utils.translation import gettext as _
from rest_framework import serializers

from dcim.choices import *
from dcim.constants import *
from dcim.models import Rack, RackReservation, RackRole
from netbox.api.fields import ChoiceField, RelatedObjectCountField
from netbox.api.serializers import NetBoxModelSerializer
from netbox.config import ConfigItem
from tenancy.api.serializers_.tenants import TenantSerializer
from users.api.serializers_.users import UserSerializer
from .sites import LocationSerializer, SiteSerializer

__all__ = (
    'RackElevationDetailFilterSerializer',
    'RackReservationSerializer',
    'RackRoleSerializer',
    'RackSerializer',
)


class RackRoleSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:rackrole-detail')

    # Related object counts
    rack_count = RelatedObjectCountField('racks')

    class Meta:
        model = RackRole
        fields = [
            'id', 'url', 'display', 'name', 'slug', 'color', 'description', 'tags', 'custom_fields', 'created',
            'last_updated', 'rack_count',
        ]
        brief_fields = ('id', 'url', 'display', 'name', 'slug', 'description', 'rack_count')


class RackSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:rack-detail')
    site = SiteSerializer(nested=True)
    location = LocationSerializer(nested=True, required=False, allow_null=True, default=None)
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)
    status = ChoiceField(choices=RackStatusChoices, required=False)
    role = RackRoleSerializer(nested=True, required=False, allow_null=True)
    type = ChoiceField(choices=RackTypeChoices, allow_blank=True, required=False, allow_null=True)
    facility_id = serializers.CharField(max_length=50, allow_blank=True, allow_null=True, label=_('Facility ID'),
                                        default=None)
    width = ChoiceField(choices=RackWidthChoices, required=False)
    outer_unit = ChoiceField(choices=RackDimensionUnitChoices, allow_blank=True, required=False, allow_null=True)
    weight_unit = ChoiceField(choices=WeightUnitChoices, allow_blank=True, required=False, allow_null=True)

    # Related object counts
    device_count = RelatedObjectCountField('devices')
    powerfeed_count = RelatedObjectCountField('powerfeeds')

    class Meta:
        model = Rack
        fields = [
            'id', 'url', 'display', 'name', 'facility_id', 'site', 'location', 'tenant', 'status', 'role', 'serial',
            'asset_tag', 'type', 'width', 'u_height', 'starting_unit', 'weight', 'max_weight', 'weight_unit',
            'desc_units', 'outer_width', 'outer_depth', 'outer_unit', 'mounting_depth', 'description', 'comments',
            'tags', 'custom_fields', 'created', 'last_updated', 'device_count', 'powerfeed_count',
        ]
        brief_fields = ('id', 'url', 'display', 'name', 'description', 'device_count')


class RackReservationSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:rackreservation-detail')
    rack = RackSerializer(nested=True)
    user = UserSerializer(nested=True)
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = RackReservation
        fields = [
            'id', 'url', 'display', 'rack', 'units', 'created', 'last_updated', 'user', 'tenant', 'description',
            'comments', 'tags', 'custom_fields',
        ]
        brief_fields = ('id', 'url', 'display', 'user', 'description', 'units')


class RackElevationDetailFilterSerializer(serializers.Serializer):
    q = serializers.CharField(
        required=False,
        default=None
    )
    face = serializers.ChoiceField(
        choices=DeviceFaceChoices,
        default=DeviceFaceChoices.FACE_FRONT
    )
    render = serializers.ChoiceField(
        choices=RackElevationDetailRenderChoices,
        default=RackElevationDetailRenderChoices.RENDER_JSON
    )
    unit_width = serializers.IntegerField(
        default=ConfigItem('RACK_ELEVATION_DEFAULT_UNIT_WIDTH')
    )
    unit_height = serializers.IntegerField(
        default=ConfigItem('RACK_ELEVATION_DEFAULT_UNIT_HEIGHT')
    )
    legend_width = serializers.IntegerField(
        default=RACK_ELEVATION_DEFAULT_LEGEND_WIDTH
    )
    margin_width = serializers.IntegerField(
        default=RACK_ELEVATION_DEFAULT_MARGIN_WIDTH
    )
    exclude = serializers.IntegerField(
        required=False,
        default=None
    )
    expand_devices = serializers.BooleanField(
        required=False,
        default=True
    )
    include_images = serializers.BooleanField(
        required=False,
        default=True
    )
