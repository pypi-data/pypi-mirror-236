"""
Type annotations for pinpoint-sms-voice-v2 service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/type_defs/)

Usage::

    ```python
    from types_aiobotocore_pinpoint_sms_voice_v2.type_defs import AccountAttributeTypeDef

    data: AccountAttributeTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AccountLimitNameType,
    ConfigurationSetFilterNameType,
    DestinationCountryParameterKeyType,
    EventTypeType,
    KeywordActionType,
    MessageTypeType,
    NumberCapabilityType,
    NumberStatusType,
    NumberTypeType,
    PhoneNumberFilterNameType,
    PoolFilterNameType,
    PoolOriginationIdentitiesFilterNameType,
    PoolStatusType,
    RequestableNumberTypeType,
    SenderIdFilterNameType,
    SpendLimitNameType,
    VoiceIdType,
    VoiceMessageBodyTextTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AccountAttributeTypeDef",
    "AccountLimitTypeDef",
    "AssociateOriginationIdentityRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CloudWatchLogsDestinationTypeDef",
    "ConfigurationSetFilterTypeDef",
    "TagTypeDef",
    "KinesisFirehoseDestinationTypeDef",
    "SnsDestinationTypeDef",
    "DeleteConfigurationSetRequestRequestTypeDef",
    "DeleteDefaultMessageTypeRequestRequestTypeDef",
    "DeleteDefaultSenderIdRequestRequestTypeDef",
    "DeleteEventDestinationRequestRequestTypeDef",
    "DeleteKeywordRequestRequestTypeDef",
    "DeleteOptOutListRequestRequestTypeDef",
    "DeleteOptedOutNumberRequestRequestTypeDef",
    "DeletePoolRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeAccountAttributesRequestRequestTypeDef",
    "DescribeAccountLimitsRequestRequestTypeDef",
    "KeywordFilterTypeDef",
    "KeywordInformationTypeDef",
    "DescribeOptOutListsRequestRequestTypeDef",
    "OptOutListInformationTypeDef",
    "OptedOutFilterTypeDef",
    "OptedOutNumberInformationTypeDef",
    "PhoneNumberFilterTypeDef",
    "PhoneNumberInformationTypeDef",
    "PoolFilterTypeDef",
    "PoolInformationTypeDef",
    "SenderIdAndCountryTypeDef",
    "SenderIdFilterTypeDef",
    "SenderIdInformationTypeDef",
    "DescribeSpendLimitsRequestRequestTypeDef",
    "SpendLimitTypeDef",
    "DisassociateOriginationIdentityRequestRequestTypeDef",
    "PoolOriginationIdentitiesFilterTypeDef",
    "OriginationIdentityMetadataTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PutKeywordRequestRequestTypeDef",
    "PutOptedOutNumberRequestRequestTypeDef",
    "ReleasePhoneNumberRequestRequestTypeDef",
    "SendTextMessageRequestRequestTypeDef",
    "SendVoiceMessageRequestRequestTypeDef",
    "SetDefaultMessageTypeRequestRequestTypeDef",
    "SetDefaultSenderIdRequestRequestTypeDef",
    "SetTextMessageSpendLimitOverrideRequestRequestTypeDef",
    "SetVoiceMessageSpendLimitOverrideRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdatePhoneNumberRequestRequestTypeDef",
    "UpdatePoolRequestRequestTypeDef",
    "AssociateOriginationIdentityResultTypeDef",
    "DeleteDefaultMessageTypeResultTypeDef",
    "DeleteDefaultSenderIdResultTypeDef",
    "DeleteKeywordResultTypeDef",
    "DeleteOptOutListResultTypeDef",
    "DeleteOptedOutNumberResultTypeDef",
    "DeletePoolResultTypeDef",
    "DeleteTextMessageSpendLimitOverrideResultTypeDef",
    "DeleteVoiceMessageSpendLimitOverrideResultTypeDef",
    "DescribeAccountAttributesResultTypeDef",
    "DescribeAccountLimitsResultTypeDef",
    "DisassociateOriginationIdentityResultTypeDef",
    "PutKeywordResultTypeDef",
    "PutOptedOutNumberResultTypeDef",
    "ReleasePhoneNumberResultTypeDef",
    "SendTextMessageResultTypeDef",
    "SendVoiceMessageResultTypeDef",
    "SetDefaultMessageTypeResultTypeDef",
    "SetDefaultSenderIdResultTypeDef",
    "SetTextMessageSpendLimitOverrideResultTypeDef",
    "SetVoiceMessageSpendLimitOverrideResultTypeDef",
    "UpdatePhoneNumberResultTypeDef",
    "UpdatePoolResultTypeDef",
    "DescribeConfigurationSetsRequestRequestTypeDef",
    "CreateConfigurationSetRequestRequestTypeDef",
    "CreateConfigurationSetResultTypeDef",
    "CreateOptOutListRequestRequestTypeDef",
    "CreateOptOutListResultTypeDef",
    "CreatePoolRequestRequestTypeDef",
    "CreatePoolResultTypeDef",
    "ListTagsForResourceResultTypeDef",
    "RequestPhoneNumberRequestRequestTypeDef",
    "RequestPhoneNumberResultTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateEventDestinationRequestRequestTypeDef",
    "EventDestinationTypeDef",
    "UpdateEventDestinationRequestRequestTypeDef",
    "DescribeAccountAttributesRequestDescribeAccountAttributesPaginateTypeDef",
    "DescribeAccountLimitsRequestDescribeAccountLimitsPaginateTypeDef",
    "DescribeConfigurationSetsRequestDescribeConfigurationSetsPaginateTypeDef",
    "DescribeOptOutListsRequestDescribeOptOutListsPaginateTypeDef",
    "DescribeSpendLimitsRequestDescribeSpendLimitsPaginateTypeDef",
    "DescribeKeywordsRequestDescribeKeywordsPaginateTypeDef",
    "DescribeKeywordsRequestRequestTypeDef",
    "DescribeKeywordsResultTypeDef",
    "DescribeOptOutListsResultTypeDef",
    "DescribeOptedOutNumbersRequestDescribeOptedOutNumbersPaginateTypeDef",
    "DescribeOptedOutNumbersRequestRequestTypeDef",
    "DescribeOptedOutNumbersResultTypeDef",
    "DescribePhoneNumbersRequestDescribePhoneNumbersPaginateTypeDef",
    "DescribePhoneNumbersRequestRequestTypeDef",
    "DescribePhoneNumbersResultTypeDef",
    "DescribePoolsRequestDescribePoolsPaginateTypeDef",
    "DescribePoolsRequestRequestTypeDef",
    "DescribePoolsResultTypeDef",
    "DescribeSenderIdsRequestDescribeSenderIdsPaginateTypeDef",
    "DescribeSenderIdsRequestRequestTypeDef",
    "DescribeSenderIdsResultTypeDef",
    "DescribeSpendLimitsResultTypeDef",
    "ListPoolOriginationIdentitiesRequestListPoolOriginationIdentitiesPaginateTypeDef",
    "ListPoolOriginationIdentitiesRequestRequestTypeDef",
    "ListPoolOriginationIdentitiesResultTypeDef",
    "ConfigurationSetInformationTypeDef",
    "CreateEventDestinationResultTypeDef",
    "DeleteConfigurationSetResultTypeDef",
    "DeleteEventDestinationResultTypeDef",
    "UpdateEventDestinationResultTypeDef",
    "DescribeConfigurationSetsResultTypeDef",
)

AccountAttributeTypeDef = TypedDict(
    "AccountAttributeTypeDef",
    {
        "Name": Literal["ACCOUNT_TIER"],
        "Value": str,
    },
)

AccountLimitTypeDef = TypedDict(
    "AccountLimitTypeDef",
    {
        "Name": AccountLimitNameType,
        "Used": int,
        "Max": int,
    },
)

AssociateOriginationIdentityRequestRequestTypeDef = TypedDict(
    "AssociateOriginationIdentityRequestRequestTypeDef",
    {
        "PoolId": str,
        "OriginationIdentity": str,
        "IsoCountryCode": str,
        "ClientToken": NotRequired[str],
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

CloudWatchLogsDestinationTypeDef = TypedDict(
    "CloudWatchLogsDestinationTypeDef",
    {
        "IamRoleArn": str,
        "LogGroupArn": str,
    },
)

ConfigurationSetFilterTypeDef = TypedDict(
    "ConfigurationSetFilterTypeDef",
    {
        "Name": ConfigurationSetFilterNameType,
        "Values": Sequence[str],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

KinesisFirehoseDestinationTypeDef = TypedDict(
    "KinesisFirehoseDestinationTypeDef",
    {
        "IamRoleArn": str,
        "DeliveryStreamArn": str,
    },
)

SnsDestinationTypeDef = TypedDict(
    "SnsDestinationTypeDef",
    {
        "TopicArn": str,
    },
)

DeleteConfigurationSetRequestRequestTypeDef = TypedDict(
    "DeleteConfigurationSetRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)

DeleteDefaultMessageTypeRequestRequestTypeDef = TypedDict(
    "DeleteDefaultMessageTypeRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)

DeleteDefaultSenderIdRequestRequestTypeDef = TypedDict(
    "DeleteDefaultSenderIdRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
    },
)

DeleteEventDestinationRequestRequestTypeDef = TypedDict(
    "DeleteEventDestinationRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "EventDestinationName": str,
    },
)

DeleteKeywordRequestRequestTypeDef = TypedDict(
    "DeleteKeywordRequestRequestTypeDef",
    {
        "OriginationIdentity": str,
        "Keyword": str,
    },
)

DeleteOptOutListRequestRequestTypeDef = TypedDict(
    "DeleteOptOutListRequestRequestTypeDef",
    {
        "OptOutListName": str,
    },
)

DeleteOptedOutNumberRequestRequestTypeDef = TypedDict(
    "DeleteOptedOutNumberRequestRequestTypeDef",
    {
        "OptOutListName": str,
        "OptedOutNumber": str,
    },
)

DeletePoolRequestRequestTypeDef = TypedDict(
    "DeletePoolRequestRequestTypeDef",
    {
        "PoolId": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)

DescribeAccountAttributesRequestRequestTypeDef = TypedDict(
    "DescribeAccountAttributesRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

DescribeAccountLimitsRequestRequestTypeDef = TypedDict(
    "DescribeAccountLimitsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

KeywordFilterTypeDef = TypedDict(
    "KeywordFilterTypeDef",
    {
        "Name": Literal["keyword-action"],
        "Values": Sequence[str],
    },
)

KeywordInformationTypeDef = TypedDict(
    "KeywordInformationTypeDef",
    {
        "Keyword": str,
        "KeywordMessage": str,
        "KeywordAction": KeywordActionType,
    },
)

DescribeOptOutListsRequestRequestTypeDef = TypedDict(
    "DescribeOptOutListsRequestRequestTypeDef",
    {
        "OptOutListNames": NotRequired[Sequence[str]],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

OptOutListInformationTypeDef = TypedDict(
    "OptOutListInformationTypeDef",
    {
        "OptOutListArn": str,
        "OptOutListName": str,
        "CreatedTimestamp": datetime,
    },
)

OptedOutFilterTypeDef = TypedDict(
    "OptedOutFilterTypeDef",
    {
        "Name": Literal["end-user-opted-out"],
        "Values": Sequence[str],
    },
)

OptedOutNumberInformationTypeDef = TypedDict(
    "OptedOutNumberInformationTypeDef",
    {
        "OptedOutNumber": str,
        "OptedOutTimestamp": datetime,
        "EndUserOptedOut": bool,
    },
)

PhoneNumberFilterTypeDef = TypedDict(
    "PhoneNumberFilterTypeDef",
    {
        "Name": PhoneNumberFilterNameType,
        "Values": Sequence[str],
    },
)

PhoneNumberInformationTypeDef = TypedDict(
    "PhoneNumberInformationTypeDef",
    {
        "PhoneNumberArn": str,
        "PhoneNumber": str,
        "Status": NumberStatusType,
        "IsoCountryCode": str,
        "MessageType": MessageTypeType,
        "NumberCapabilities": List[NumberCapabilityType],
        "NumberType": NumberTypeType,
        "MonthlyLeasingPrice": str,
        "TwoWayEnabled": bool,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "DeletionProtectionEnabled": bool,
        "CreatedTimestamp": datetime,
        "PhoneNumberId": NotRequired[str],
        "TwoWayChannelArn": NotRequired[str],
        "PoolId": NotRequired[str],
    },
)

PoolFilterTypeDef = TypedDict(
    "PoolFilterTypeDef",
    {
        "Name": PoolFilterNameType,
        "Values": Sequence[str],
    },
)

PoolInformationTypeDef = TypedDict(
    "PoolInformationTypeDef",
    {
        "PoolArn": str,
        "PoolId": str,
        "Status": PoolStatusType,
        "MessageType": MessageTypeType,
        "TwoWayEnabled": bool,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "SharedRoutesEnabled": bool,
        "DeletionProtectionEnabled": bool,
        "CreatedTimestamp": datetime,
        "TwoWayChannelArn": NotRequired[str],
    },
)

SenderIdAndCountryTypeDef = TypedDict(
    "SenderIdAndCountryTypeDef",
    {
        "SenderId": str,
        "IsoCountryCode": str,
    },
)

SenderIdFilterTypeDef = TypedDict(
    "SenderIdFilterTypeDef",
    {
        "Name": SenderIdFilterNameType,
        "Values": Sequence[str],
    },
)

SenderIdInformationTypeDef = TypedDict(
    "SenderIdInformationTypeDef",
    {
        "SenderIdArn": str,
        "SenderId": str,
        "IsoCountryCode": str,
        "MessageTypes": List[MessageTypeType],
        "MonthlyLeasingPrice": str,
    },
)

DescribeSpendLimitsRequestRequestTypeDef = TypedDict(
    "DescribeSpendLimitsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

SpendLimitTypeDef = TypedDict(
    "SpendLimitTypeDef",
    {
        "Name": SpendLimitNameType,
        "EnforcedLimit": int,
        "MaxLimit": int,
        "Overridden": bool,
    },
)

DisassociateOriginationIdentityRequestRequestTypeDef = TypedDict(
    "DisassociateOriginationIdentityRequestRequestTypeDef",
    {
        "PoolId": str,
        "OriginationIdentity": str,
        "IsoCountryCode": str,
        "ClientToken": NotRequired[str],
    },
)

PoolOriginationIdentitiesFilterTypeDef = TypedDict(
    "PoolOriginationIdentitiesFilterTypeDef",
    {
        "Name": PoolOriginationIdentitiesFilterNameType,
        "Values": Sequence[str],
    },
)

OriginationIdentityMetadataTypeDef = TypedDict(
    "OriginationIdentityMetadataTypeDef",
    {
        "OriginationIdentityArn": str,
        "OriginationIdentity": str,
        "IsoCountryCode": str,
        "NumberCapabilities": List[NumberCapabilityType],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

PutKeywordRequestRequestTypeDef = TypedDict(
    "PutKeywordRequestRequestTypeDef",
    {
        "OriginationIdentity": str,
        "Keyword": str,
        "KeywordMessage": str,
        "KeywordAction": NotRequired[KeywordActionType],
    },
)

PutOptedOutNumberRequestRequestTypeDef = TypedDict(
    "PutOptedOutNumberRequestRequestTypeDef",
    {
        "OptOutListName": str,
        "OptedOutNumber": str,
    },
)

ReleasePhoneNumberRequestRequestTypeDef = TypedDict(
    "ReleasePhoneNumberRequestRequestTypeDef",
    {
        "PhoneNumberId": str,
    },
)

SendTextMessageRequestRequestTypeDef = TypedDict(
    "SendTextMessageRequestRequestTypeDef",
    {
        "DestinationPhoneNumber": str,
        "OriginationIdentity": NotRequired[str],
        "MessageBody": NotRequired[str],
        "MessageType": NotRequired[MessageTypeType],
        "Keyword": NotRequired[str],
        "ConfigurationSetName": NotRequired[str],
        "MaxPrice": NotRequired[str],
        "TimeToLive": NotRequired[int],
        "Context": NotRequired[Mapping[str, str]],
        "DestinationCountryParameters": NotRequired[
            Mapping[DestinationCountryParameterKeyType, str]
        ],
        "DryRun": NotRequired[bool],
    },
)

SendVoiceMessageRequestRequestTypeDef = TypedDict(
    "SendVoiceMessageRequestRequestTypeDef",
    {
        "DestinationPhoneNumber": str,
        "OriginationIdentity": str,
        "MessageBody": NotRequired[str],
        "MessageBodyTextType": NotRequired[VoiceMessageBodyTextTypeType],
        "VoiceId": NotRequired[VoiceIdType],
        "ConfigurationSetName": NotRequired[str],
        "MaxPricePerMinute": NotRequired[str],
        "TimeToLive": NotRequired[int],
        "Context": NotRequired[Mapping[str, str]],
        "DryRun": NotRequired[bool],
    },
)

SetDefaultMessageTypeRequestRequestTypeDef = TypedDict(
    "SetDefaultMessageTypeRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "MessageType": MessageTypeType,
    },
)

SetDefaultSenderIdRequestRequestTypeDef = TypedDict(
    "SetDefaultSenderIdRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "SenderId": str,
    },
)

SetTextMessageSpendLimitOverrideRequestRequestTypeDef = TypedDict(
    "SetTextMessageSpendLimitOverrideRequestRequestTypeDef",
    {
        "MonthlyLimit": int,
    },
)

SetVoiceMessageSpendLimitOverrideRequestRequestTypeDef = TypedDict(
    "SetVoiceMessageSpendLimitOverrideRequestRequestTypeDef",
    {
        "MonthlyLimit": int,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdatePhoneNumberRequestRequestTypeDef = TypedDict(
    "UpdatePhoneNumberRequestRequestTypeDef",
    {
        "PhoneNumberId": str,
        "TwoWayEnabled": NotRequired[bool],
        "TwoWayChannelArn": NotRequired[str],
        "SelfManagedOptOutsEnabled": NotRequired[bool],
        "OptOutListName": NotRequired[str],
        "DeletionProtectionEnabled": NotRequired[bool],
    },
)

UpdatePoolRequestRequestTypeDef = TypedDict(
    "UpdatePoolRequestRequestTypeDef",
    {
        "PoolId": str,
        "TwoWayEnabled": NotRequired[bool],
        "TwoWayChannelArn": NotRequired[str],
        "SelfManagedOptOutsEnabled": NotRequired[bool],
        "OptOutListName": NotRequired[str],
        "SharedRoutesEnabled": NotRequired[bool],
        "DeletionProtectionEnabled": NotRequired[bool],
    },
)

AssociateOriginationIdentityResultTypeDef = TypedDict(
    "AssociateOriginationIdentityResultTypeDef",
    {
        "PoolArn": str,
        "PoolId": str,
        "OriginationIdentityArn": str,
        "OriginationIdentity": str,
        "IsoCountryCode": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDefaultMessageTypeResultTypeDef = TypedDict(
    "DeleteDefaultMessageTypeResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "MessageType": MessageTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDefaultSenderIdResultTypeDef = TypedDict(
    "DeleteDefaultSenderIdResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "SenderId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteKeywordResultTypeDef = TypedDict(
    "DeleteKeywordResultTypeDef",
    {
        "OriginationIdentityArn": str,
        "OriginationIdentity": str,
        "Keyword": str,
        "KeywordMessage": str,
        "KeywordAction": KeywordActionType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteOptOutListResultTypeDef = TypedDict(
    "DeleteOptOutListResultTypeDef",
    {
        "OptOutListArn": str,
        "OptOutListName": str,
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteOptedOutNumberResultTypeDef = TypedDict(
    "DeleteOptedOutNumberResultTypeDef",
    {
        "OptOutListArn": str,
        "OptOutListName": str,
        "OptedOutNumber": str,
        "OptedOutTimestamp": datetime,
        "EndUserOptedOut": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeletePoolResultTypeDef = TypedDict(
    "DeletePoolResultTypeDef",
    {
        "PoolArn": str,
        "PoolId": str,
        "Status": PoolStatusType,
        "MessageType": MessageTypeType,
        "TwoWayEnabled": bool,
        "TwoWayChannelArn": str,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "SharedRoutesEnabled": bool,
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTextMessageSpendLimitOverrideResultTypeDef = TypedDict(
    "DeleteTextMessageSpendLimitOverrideResultTypeDef",
    {
        "MonthlyLimit": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVoiceMessageSpendLimitOverrideResultTypeDef = TypedDict(
    "DeleteVoiceMessageSpendLimitOverrideResultTypeDef",
    {
        "MonthlyLimit": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountAttributesResultTypeDef = TypedDict(
    "DescribeAccountAttributesResultTypeDef",
    {
        "AccountAttributes": List[AccountAttributeTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountLimitsResultTypeDef = TypedDict(
    "DescribeAccountLimitsResultTypeDef",
    {
        "AccountLimits": List[AccountLimitTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateOriginationIdentityResultTypeDef = TypedDict(
    "DisassociateOriginationIdentityResultTypeDef",
    {
        "PoolArn": str,
        "PoolId": str,
        "OriginationIdentityArn": str,
        "OriginationIdentity": str,
        "IsoCountryCode": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutKeywordResultTypeDef = TypedDict(
    "PutKeywordResultTypeDef",
    {
        "OriginationIdentityArn": str,
        "OriginationIdentity": str,
        "Keyword": str,
        "KeywordMessage": str,
        "KeywordAction": KeywordActionType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutOptedOutNumberResultTypeDef = TypedDict(
    "PutOptedOutNumberResultTypeDef",
    {
        "OptOutListArn": str,
        "OptOutListName": str,
        "OptedOutNumber": str,
        "OptedOutTimestamp": datetime,
        "EndUserOptedOut": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReleasePhoneNumberResultTypeDef = TypedDict(
    "ReleasePhoneNumberResultTypeDef",
    {
        "PhoneNumberArn": str,
        "PhoneNumberId": str,
        "PhoneNumber": str,
        "Status": NumberStatusType,
        "IsoCountryCode": str,
        "MessageType": MessageTypeType,
        "NumberCapabilities": List[NumberCapabilityType],
        "NumberType": NumberTypeType,
        "MonthlyLeasingPrice": str,
        "TwoWayEnabled": bool,
        "TwoWayChannelArn": str,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendTextMessageResultTypeDef = TypedDict(
    "SendTextMessageResultTypeDef",
    {
        "MessageId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendVoiceMessageResultTypeDef = TypedDict(
    "SendVoiceMessageResultTypeDef",
    {
        "MessageId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetDefaultMessageTypeResultTypeDef = TypedDict(
    "SetDefaultMessageTypeResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "MessageType": MessageTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetDefaultSenderIdResultTypeDef = TypedDict(
    "SetDefaultSenderIdResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "SenderId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetTextMessageSpendLimitOverrideResultTypeDef = TypedDict(
    "SetTextMessageSpendLimitOverrideResultTypeDef",
    {
        "MonthlyLimit": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetVoiceMessageSpendLimitOverrideResultTypeDef = TypedDict(
    "SetVoiceMessageSpendLimitOverrideResultTypeDef",
    {
        "MonthlyLimit": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePhoneNumberResultTypeDef = TypedDict(
    "UpdatePhoneNumberResultTypeDef",
    {
        "PhoneNumberArn": str,
        "PhoneNumberId": str,
        "PhoneNumber": str,
        "Status": NumberStatusType,
        "IsoCountryCode": str,
        "MessageType": MessageTypeType,
        "NumberCapabilities": List[NumberCapabilityType],
        "NumberType": NumberTypeType,
        "MonthlyLeasingPrice": str,
        "TwoWayEnabled": bool,
        "TwoWayChannelArn": str,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "DeletionProtectionEnabled": bool,
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePoolResultTypeDef = TypedDict(
    "UpdatePoolResultTypeDef",
    {
        "PoolArn": str,
        "PoolId": str,
        "Status": PoolStatusType,
        "MessageType": MessageTypeType,
        "TwoWayEnabled": bool,
        "TwoWayChannelArn": str,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "SharedRoutesEnabled": bool,
        "DeletionProtectionEnabled": bool,
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeConfigurationSetsRequestRequestTypeDef = TypedDict(
    "DescribeConfigurationSetsRequestRequestTypeDef",
    {
        "ConfigurationSetNames": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[ConfigurationSetFilterTypeDef]],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

CreateConfigurationSetRequestRequestTypeDef = TypedDict(
    "CreateConfigurationSetRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "ClientToken": NotRequired[str],
    },
)

CreateConfigurationSetResultTypeDef = TypedDict(
    "CreateConfigurationSetResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "Tags": List[TagTypeDef],
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateOptOutListRequestRequestTypeDef = TypedDict(
    "CreateOptOutListRequestRequestTypeDef",
    {
        "OptOutListName": str,
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "ClientToken": NotRequired[str],
    },
)

CreateOptOutListResultTypeDef = TypedDict(
    "CreateOptOutListResultTypeDef",
    {
        "OptOutListArn": str,
        "OptOutListName": str,
        "Tags": List[TagTypeDef],
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePoolRequestRequestTypeDef = TypedDict(
    "CreatePoolRequestRequestTypeDef",
    {
        "OriginationIdentity": str,
        "IsoCountryCode": str,
        "MessageType": MessageTypeType,
        "DeletionProtectionEnabled": NotRequired[bool],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "ClientToken": NotRequired[str],
    },
)

CreatePoolResultTypeDef = TypedDict(
    "CreatePoolResultTypeDef",
    {
        "PoolArn": str,
        "PoolId": str,
        "Status": PoolStatusType,
        "MessageType": MessageTypeType,
        "TwoWayEnabled": bool,
        "TwoWayChannelArn": str,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "SharedRoutesEnabled": bool,
        "DeletionProtectionEnabled": bool,
        "Tags": List[TagTypeDef],
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResultTypeDef = TypedDict(
    "ListTagsForResourceResultTypeDef",
    {
        "ResourceArn": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RequestPhoneNumberRequestRequestTypeDef = TypedDict(
    "RequestPhoneNumberRequestRequestTypeDef",
    {
        "IsoCountryCode": str,
        "MessageType": MessageTypeType,
        "NumberCapabilities": Sequence[NumberCapabilityType],
        "NumberType": RequestableNumberTypeType,
        "OptOutListName": NotRequired[str],
        "PoolId": NotRequired[str],
        "RegistrationId": NotRequired[str],
        "DeletionProtectionEnabled": NotRequired[bool],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "ClientToken": NotRequired[str],
    },
)

RequestPhoneNumberResultTypeDef = TypedDict(
    "RequestPhoneNumberResultTypeDef",
    {
        "PhoneNumberArn": str,
        "PhoneNumberId": str,
        "PhoneNumber": str,
        "Status": NumberStatusType,
        "IsoCountryCode": str,
        "MessageType": MessageTypeType,
        "NumberCapabilities": List[NumberCapabilityType],
        "NumberType": RequestableNumberTypeType,
        "MonthlyLeasingPrice": str,
        "TwoWayEnabled": bool,
        "TwoWayChannelArn": str,
        "SelfManagedOptOutsEnabled": bool,
        "OptOutListName": str,
        "DeletionProtectionEnabled": bool,
        "PoolId": str,
        "Tags": List[TagTypeDef],
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateEventDestinationRequestRequestTypeDef = TypedDict(
    "CreateEventDestinationRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "EventDestinationName": str,
        "MatchingEventTypes": Sequence[EventTypeType],
        "CloudWatchLogsDestination": NotRequired[CloudWatchLogsDestinationTypeDef],
        "KinesisFirehoseDestination": NotRequired[KinesisFirehoseDestinationTypeDef],
        "SnsDestination": NotRequired[SnsDestinationTypeDef],
        "ClientToken": NotRequired[str],
    },
)

EventDestinationTypeDef = TypedDict(
    "EventDestinationTypeDef",
    {
        "EventDestinationName": str,
        "Enabled": bool,
        "MatchingEventTypes": List[EventTypeType],
        "CloudWatchLogsDestination": NotRequired[CloudWatchLogsDestinationTypeDef],
        "KinesisFirehoseDestination": NotRequired[KinesisFirehoseDestinationTypeDef],
        "SnsDestination": NotRequired[SnsDestinationTypeDef],
    },
)

UpdateEventDestinationRequestRequestTypeDef = TypedDict(
    "UpdateEventDestinationRequestRequestTypeDef",
    {
        "ConfigurationSetName": str,
        "EventDestinationName": str,
        "Enabled": NotRequired[bool],
        "MatchingEventTypes": NotRequired[Sequence[EventTypeType]],
        "CloudWatchLogsDestination": NotRequired[CloudWatchLogsDestinationTypeDef],
        "KinesisFirehoseDestination": NotRequired[KinesisFirehoseDestinationTypeDef],
        "SnsDestination": NotRequired[SnsDestinationTypeDef],
    },
)

DescribeAccountAttributesRequestDescribeAccountAttributesPaginateTypeDef = TypedDict(
    "DescribeAccountAttributesRequestDescribeAccountAttributesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeAccountLimitsRequestDescribeAccountLimitsPaginateTypeDef = TypedDict(
    "DescribeAccountLimitsRequestDescribeAccountLimitsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeConfigurationSetsRequestDescribeConfigurationSetsPaginateTypeDef = TypedDict(
    "DescribeConfigurationSetsRequestDescribeConfigurationSetsPaginateTypeDef",
    {
        "ConfigurationSetNames": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[ConfigurationSetFilterTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeOptOutListsRequestDescribeOptOutListsPaginateTypeDef = TypedDict(
    "DescribeOptOutListsRequestDescribeOptOutListsPaginateTypeDef",
    {
        "OptOutListNames": NotRequired[Sequence[str]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeSpendLimitsRequestDescribeSpendLimitsPaginateTypeDef = TypedDict(
    "DescribeSpendLimitsRequestDescribeSpendLimitsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeKeywordsRequestDescribeKeywordsPaginateTypeDef = TypedDict(
    "DescribeKeywordsRequestDescribeKeywordsPaginateTypeDef",
    {
        "OriginationIdentity": str,
        "Keywords": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[KeywordFilterTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeKeywordsRequestRequestTypeDef = TypedDict(
    "DescribeKeywordsRequestRequestTypeDef",
    {
        "OriginationIdentity": str,
        "Keywords": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[KeywordFilterTypeDef]],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

DescribeKeywordsResultTypeDef = TypedDict(
    "DescribeKeywordsResultTypeDef",
    {
        "OriginationIdentityArn": str,
        "OriginationIdentity": str,
        "Keywords": List[KeywordInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeOptOutListsResultTypeDef = TypedDict(
    "DescribeOptOutListsResultTypeDef",
    {
        "OptOutLists": List[OptOutListInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeOptedOutNumbersRequestDescribeOptedOutNumbersPaginateTypeDef = TypedDict(
    "DescribeOptedOutNumbersRequestDescribeOptedOutNumbersPaginateTypeDef",
    {
        "OptOutListName": str,
        "OptedOutNumbers": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[OptedOutFilterTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeOptedOutNumbersRequestRequestTypeDef = TypedDict(
    "DescribeOptedOutNumbersRequestRequestTypeDef",
    {
        "OptOutListName": str,
        "OptedOutNumbers": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[OptedOutFilterTypeDef]],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

DescribeOptedOutNumbersResultTypeDef = TypedDict(
    "DescribeOptedOutNumbersResultTypeDef",
    {
        "OptOutListArn": str,
        "OptOutListName": str,
        "OptedOutNumbers": List[OptedOutNumberInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePhoneNumbersRequestDescribePhoneNumbersPaginateTypeDef = TypedDict(
    "DescribePhoneNumbersRequestDescribePhoneNumbersPaginateTypeDef",
    {
        "PhoneNumberIds": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[PhoneNumberFilterTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribePhoneNumbersRequestRequestTypeDef = TypedDict(
    "DescribePhoneNumbersRequestRequestTypeDef",
    {
        "PhoneNumberIds": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[PhoneNumberFilterTypeDef]],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

DescribePhoneNumbersResultTypeDef = TypedDict(
    "DescribePhoneNumbersResultTypeDef",
    {
        "PhoneNumbers": List[PhoneNumberInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePoolsRequestDescribePoolsPaginateTypeDef = TypedDict(
    "DescribePoolsRequestDescribePoolsPaginateTypeDef",
    {
        "PoolIds": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[PoolFilterTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribePoolsRequestRequestTypeDef = TypedDict(
    "DescribePoolsRequestRequestTypeDef",
    {
        "PoolIds": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[PoolFilterTypeDef]],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

DescribePoolsResultTypeDef = TypedDict(
    "DescribePoolsResultTypeDef",
    {
        "Pools": List[PoolInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSenderIdsRequestDescribeSenderIdsPaginateTypeDef = TypedDict(
    "DescribeSenderIdsRequestDescribeSenderIdsPaginateTypeDef",
    {
        "SenderIds": NotRequired[Sequence[SenderIdAndCountryTypeDef]],
        "Filters": NotRequired[Sequence[SenderIdFilterTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeSenderIdsRequestRequestTypeDef = TypedDict(
    "DescribeSenderIdsRequestRequestTypeDef",
    {
        "SenderIds": NotRequired[Sequence[SenderIdAndCountryTypeDef]],
        "Filters": NotRequired[Sequence[SenderIdFilterTypeDef]],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

DescribeSenderIdsResultTypeDef = TypedDict(
    "DescribeSenderIdsResultTypeDef",
    {
        "SenderIds": List[SenderIdInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSpendLimitsResultTypeDef = TypedDict(
    "DescribeSpendLimitsResultTypeDef",
    {
        "SpendLimits": List[SpendLimitTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPoolOriginationIdentitiesRequestListPoolOriginationIdentitiesPaginateTypeDef = TypedDict(
    "ListPoolOriginationIdentitiesRequestListPoolOriginationIdentitiesPaginateTypeDef",
    {
        "PoolId": str,
        "Filters": NotRequired[Sequence[PoolOriginationIdentitiesFilterTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListPoolOriginationIdentitiesRequestRequestTypeDef = TypedDict(
    "ListPoolOriginationIdentitiesRequestRequestTypeDef",
    {
        "PoolId": str,
        "Filters": NotRequired[Sequence[PoolOriginationIdentitiesFilterTypeDef]],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListPoolOriginationIdentitiesResultTypeDef = TypedDict(
    "ListPoolOriginationIdentitiesResultTypeDef",
    {
        "PoolArn": str,
        "PoolId": str,
        "OriginationIdentities": List[OriginationIdentityMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConfigurationSetInformationTypeDef = TypedDict(
    "ConfigurationSetInformationTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "EventDestinations": List[EventDestinationTypeDef],
        "CreatedTimestamp": datetime,
        "DefaultMessageType": NotRequired[MessageTypeType],
        "DefaultSenderId": NotRequired[str],
    },
)

CreateEventDestinationResultTypeDef = TypedDict(
    "CreateEventDestinationResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "EventDestination": EventDestinationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteConfigurationSetResultTypeDef = TypedDict(
    "DeleteConfigurationSetResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "EventDestinations": List[EventDestinationTypeDef],
        "DefaultMessageType": MessageTypeType,
        "DefaultSenderId": str,
        "CreatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteEventDestinationResultTypeDef = TypedDict(
    "DeleteEventDestinationResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "EventDestination": EventDestinationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEventDestinationResultTypeDef = TypedDict(
    "UpdateEventDestinationResultTypeDef",
    {
        "ConfigurationSetArn": str,
        "ConfigurationSetName": str,
        "EventDestination": EventDestinationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeConfigurationSetsResultTypeDef = TypedDict(
    "DescribeConfigurationSetsResultTypeDef",
    {
        "ConfigurationSets": List[ConfigurationSetInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
