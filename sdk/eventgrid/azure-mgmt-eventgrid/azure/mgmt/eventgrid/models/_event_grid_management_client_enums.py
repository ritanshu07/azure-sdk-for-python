# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from enum import Enum, EnumMeta
from six import with_metaclass

class _CaseInsensitiveEnumMeta(EnumMeta):
    def __getitem__(self, name):
        return super().__getitem__(name.upper())

    def __getattr__(cls, name):
        """Return the enum member matching `name`
        We use __getattr__ instead of descriptors or inserting into the enum
        class' __dict__ in order to support `name` and `value` being both
        properties for enum members (which live in the class' __dict__) and
        enum members themselves.
        """
        try:
            return cls._member_map_[name.upper()]
        except KeyError:
            raise AttributeError(name)


class AdvancedFilterOperatorType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
    """

    NUMBER_IN = "NumberIn"
    NUMBER_NOT_IN = "NumberNotIn"
    NUMBER_LESS_THAN = "NumberLessThan"
    NUMBER_GREATER_THAN = "NumberGreaterThan"
    NUMBER_LESS_THAN_OR_EQUALS = "NumberLessThanOrEquals"
    NUMBER_GREATER_THAN_OR_EQUALS = "NumberGreaterThanOrEquals"
    BOOL_EQUALS = "BoolEquals"
    STRING_IN = "StringIn"
    STRING_NOT_IN = "StringNotIn"
    STRING_BEGINS_WITH = "StringBeginsWith"
    STRING_ENDS_WITH = "StringEndsWith"
    STRING_CONTAINS = "StringContains"

class CreatedByType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The type of identity that created the resource.
    """

    USER = "User"
    APPLICATION = "Application"
    MANAGED_IDENTITY = "ManagedIdentity"
    KEY = "Key"

class DeadLetterEndPointType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Type of the endpoint for the dead letter destination
    """

    STORAGE_BLOB = "StorageBlob"

class DeliveryAttributeMappingType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Type of the delivery attribute or header name.
    """

    STATIC = "Static"
    DYNAMIC = "Dynamic"

class DomainProvisioningState(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Provisioning state of the Event Grid Domain Resource.
    """

    CREATING = "Creating"
    UPDATING = "Updating"
    DELETING = "Deleting"
    SUCCEEDED = "Succeeded"
    CANCELED = "Canceled"
    FAILED = "Failed"

class DomainTopicProvisioningState(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Provisioning state of the domain topic.
    """

    CREATING = "Creating"
    UPDATING = "Updating"
    DELETING = "Deleting"
    SUCCEEDED = "Succeeded"
    CANCELED = "Canceled"
    FAILED = "Failed"

class EndpointType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Type of the endpoint for the event subscription destination.
    """

    WEB_HOOK = "WebHook"
    EVENT_HUB = "EventHub"
    STORAGE_QUEUE = "StorageQueue"
    HYBRID_CONNECTION = "HybridConnection"
    SERVICE_BUS_QUEUE = "ServiceBusQueue"
    SERVICE_BUS_TOPIC = "ServiceBusTopic"
    AZURE_FUNCTION = "AzureFunction"

class Enum18(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    TOPICS = "topics"
    DOMAINS = "domains"

class Enum19(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    TOPICS = "topics"
    DOMAINS = "domains"

class Enum20(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    TOPICS = "topics"
    DOMAINS = "domains"

class Enum21(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    TOPICS = "topics"
    DOMAINS = "domains"

class EventDeliverySchema(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The event delivery schema for the event subscription.
    """

    EVENT_GRID_SCHEMA = "EventGridSchema"
    CUSTOM_INPUT_SCHEMA = "CustomInputSchema"
    CLOUD_EVENT_SCHEMA_V1_0 = "CloudEventSchemaV1_0"

class EventSubscriptionIdentityType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The type of managed identity used. The type 'SystemAssigned, UserAssigned' includes both an
    implicitly created identity and a set of user-assigned identities. The type 'None' will remove
    any identity.
    """

    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"

class EventSubscriptionProvisioningState(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Provisioning state of the event subscription.
    """

    CREATING = "Creating"
    UPDATING = "Updating"
    DELETING = "Deleting"
    SUCCEEDED = "Succeeded"
    CANCELED = "Canceled"
    FAILED = "Failed"
    AWAITING_MANUAL_ACTION = "AwaitingManualAction"

class IdentityType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The type of managed identity used. The type 'SystemAssigned, UserAssigned' includes both an
    implicitly created identity and a set of user-assigned identities. The type 'None' will remove
    any identity.
    """

    NONE = "None"
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
    SYSTEM_ASSIGNED_USER_ASSIGNED = "SystemAssigned, UserAssigned"

class InputSchema(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """This determines the format that Event Grid should expect for incoming events published to the
    domain.
    """

    EVENT_GRID_SCHEMA = "EventGridSchema"
    CUSTOM_EVENT_SCHEMA = "CustomEventSchema"
    CLOUD_EVENT_SCHEMA_V1_0 = "CloudEventSchemaV1_0"

class InputSchemaMappingType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Type of the custom mapping
    """

    JSON = "Json"

class IpActionType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Action to perform based on the match or no match of the IpMask.
    """

    ALLOW = "Allow"

class PersistedConnectionStatus(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Status of the connection.
    """

    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    DISCONNECTED = "Disconnected"

class PublicNetworkAccess(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """This determines if traffic is allowed over public network. By default it is enabled.
    You can further restrict to specific IPs by configuring :code:`<seealso
    cref="P:Microsoft.Azure.Events.ResourceProvider.Common.Contracts.DomainProperties.InboundIpRules"
    />`
    """

    ENABLED = "Enabled"
    DISABLED = "Disabled"

class ResourceProvisioningState(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Provisioning state of the Private Endpoint Connection.
    """

    CREATING = "Creating"
    UPDATING = "Updating"
    DELETING = "Deleting"
    SUCCEEDED = "Succeeded"
    CANCELED = "Canceled"
    FAILED = "Failed"

class ResourceRegionType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Region type of the resource.
    """

    REGIONAL_RESOURCE = "RegionalResource"
    GLOBAL_RESOURCE = "GlobalResource"

class TopicProvisioningState(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Provisioning state of the topic.
    """

    CREATING = "Creating"
    UPDATING = "Updating"
    DELETING = "Deleting"
    SUCCEEDED = "Succeeded"
    CANCELED = "Canceled"
    FAILED = "Failed"

class TopicTypePropertiesSupportedScopesForSourceItem(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    RESOURCE = "Resource"
    RESOURCE_GROUP = "ResourceGroup"
    AZURE_SUBSCRIPTION = "AzureSubscription"

class TopicTypeProvisioningState(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Provisioning state of the topic type
    """

    CREATING = "Creating"
    UPDATING = "Updating"
    DELETING = "Deleting"
    SUCCEEDED = "Succeeded"
    CANCELED = "Canceled"
    FAILED = "Failed"
