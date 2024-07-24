from rest_framework import serializers

from circuits.choices import CircuitStatusChoices
from circuits.models import Circuit, CircuitTermination, CircuitType
from dcim.api.serializers_.cables import CabledObjectSerializer
from dcim.api.serializers_.sites import SiteSerializer
from netbox.api.fields import ChoiceField, RelatedObjectCountField
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from tenancy.api.serializers_.tenants import TenantSerializer

from .providers import ProviderAccountSerializer, ProviderNetworkSerializer, ProviderSerializer

__all__ = (
    'CircuitSerializer',
    'CircuitTerminationSerializer',
    'CircuitTypeSerializer',
)


class CircuitTypeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='circuits-api:circuittype-detail')

    # Related object counts
    circuit_count = RelatedObjectCountField('circuits')

    class Meta:
        model = CircuitType
        fields = [
            'id', 'url', 'display', 'name', 'slug', 'color', 'description', 'tags', 'custom_fields', 'created',
            'last_updated', 'circuit_count',
        ]
        brief_fields = ('id', 'url', 'display', 'name', 'slug', 'description', 'circuit_count')


class CircuitCircuitTerminationSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='circuits-api:circuittermination-detail')
    site = SiteSerializer(nested=True, allow_null=True)
    provider_network = ProviderNetworkSerializer(nested=True, allow_null=True)

    class Meta:
        model = CircuitTermination
        fields = [
            'id', 'url', 'display', 'site', 'provider_network', 'port_speed', 'upstream_speed', 'xconnect_id',
            'description',
        ]


class CircuitSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='circuits-api:circuit-detail')
    provider = ProviderSerializer(nested=True)
    provider_account = ProviderAccountSerializer(nested=True, required=False, allow_null=True, default=None)
    status = ChoiceField(choices=CircuitStatusChoices, required=False)
    type = CircuitTypeSerializer(nested=True)
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)
    termination_a = CircuitCircuitTerminationSerializer(read_only=True, allow_null=True)
    termination_z = CircuitCircuitTerminationSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Circuit
        fields = [
            'id', 'url', 'display', 'cid', 'provider', 'provider_account', 'type', 'status', 'tenant', 'install_date',
            'termination_date', 'commit_rate', 'description', 'termination_a', 'termination_z', 'comments', 'tags',
            'custom_fields', 'created', 'last_updated',
        ]
        brief_fields = ('id', 'url', 'display', 'cid', 'description')


class CircuitTerminationSerializer(NetBoxModelSerializer, CabledObjectSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='circuits-api:circuittermination-detail')
    circuit = CircuitSerializer(nested=True)
    site = SiteSerializer(nested=True, required=False, allow_null=True)
    provider_network = ProviderNetworkSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = CircuitTermination
        fields = [
            'id', 'url', 'display', 'circuit', 'term_side', 'site', 'provider_network', 'port_speed', 'upstream_speed',
            'xconnect_id', 'pp_info', 'description', 'mark_connected', 'cable', 'cable_end', 'link_peers',
            'link_peers_type', 'tags', 'custom_fields', 'created', 'last_updated', '_occupied',
        ]
        brief_fields = ('id', 'url', 'display', 'circuit', 'term_side', 'description', 'cable', '_occupied')
