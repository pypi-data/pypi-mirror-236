"""
Type annotations for macie service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/type_defs/)

Usage::

    ```python
    from types_aiobotocore_macie.type_defs import AssociateMemberAccountRequestRequestTypeDef

    data: AssociateMemberAccountRequestRequestTypeDef = ...
    ```
"""

import sys
from typing import Dict, List, Sequence

from .literals import S3OneTimeClassificationTypeType

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
    "AssociateMemberAccountRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ClassificationTypeTypeDef",
    "ClassificationTypeUpdateTypeDef",
    "DisassociateMemberAccountRequestRequestTypeDef",
    "S3ResourceTypeDef",
    "PaginatorConfigTypeDef",
    "ListMemberAccountsRequestRequestTypeDef",
    "MemberAccountTypeDef",
    "ListS3ResourcesRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "S3ResourceClassificationTypeDef",
    "S3ResourceClassificationUpdateTypeDef",
    "DisassociateS3ResourcesRequestRequestTypeDef",
    "FailedS3ResourceTypeDef",
    "ListMemberAccountsRequestListMemberAccountsPaginateTypeDef",
    "ListS3ResourcesRequestListS3ResourcesPaginateTypeDef",
    "ListMemberAccountsResultTypeDef",
    "AssociateS3ResourcesRequestRequestTypeDef",
    "ListS3ResourcesResultTypeDef",
    "UpdateS3ResourcesRequestRequestTypeDef",
    "AssociateS3ResourcesResultTypeDef",
    "DisassociateS3ResourcesResultTypeDef",
    "UpdateS3ResourcesResultTypeDef",
)

AssociateMemberAccountRequestRequestTypeDef = TypedDict(
    "AssociateMemberAccountRequestRequestTypeDef",
    {
        "memberAccountId": str,
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

ClassificationTypeTypeDef = TypedDict(
    "ClassificationTypeTypeDef",
    {
        "oneTime": S3OneTimeClassificationTypeType,
        "continuous": Literal["FULL"],
    },
)

ClassificationTypeUpdateTypeDef = TypedDict(
    "ClassificationTypeUpdateTypeDef",
    {
        "oneTime": NotRequired[S3OneTimeClassificationTypeType],
        "continuous": NotRequired[Literal["FULL"]],
    },
)

DisassociateMemberAccountRequestRequestTypeDef = TypedDict(
    "DisassociateMemberAccountRequestRequestTypeDef",
    {
        "memberAccountId": str,
    },
)

S3ResourceTypeDef = TypedDict(
    "S3ResourceTypeDef",
    {
        "bucketName": str,
        "prefix": NotRequired[str],
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

ListMemberAccountsRequestRequestTypeDef = TypedDict(
    "ListMemberAccountsRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

MemberAccountTypeDef = TypedDict(
    "MemberAccountTypeDef",
    {
        "accountId": NotRequired[str],
    },
)

ListS3ResourcesRequestRequestTypeDef = TypedDict(
    "ListS3ResourcesRequestRequestTypeDef",
    {
        "memberAccountId": NotRequired[str],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

S3ResourceClassificationTypeDef = TypedDict(
    "S3ResourceClassificationTypeDef",
    {
        "bucketName": str,
        "classificationType": ClassificationTypeTypeDef,
        "prefix": NotRequired[str],
    },
)

S3ResourceClassificationUpdateTypeDef = TypedDict(
    "S3ResourceClassificationUpdateTypeDef",
    {
        "bucketName": str,
        "classificationTypeUpdate": ClassificationTypeUpdateTypeDef,
        "prefix": NotRequired[str],
    },
)

DisassociateS3ResourcesRequestRequestTypeDef = TypedDict(
    "DisassociateS3ResourcesRequestRequestTypeDef",
    {
        "associatedS3Resources": Sequence[S3ResourceTypeDef],
        "memberAccountId": NotRequired[str],
    },
)

FailedS3ResourceTypeDef = TypedDict(
    "FailedS3ResourceTypeDef",
    {
        "failedItem": NotRequired[S3ResourceTypeDef],
        "errorCode": NotRequired[str],
        "errorMessage": NotRequired[str],
    },
)

ListMemberAccountsRequestListMemberAccountsPaginateTypeDef = TypedDict(
    "ListMemberAccountsRequestListMemberAccountsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListS3ResourcesRequestListS3ResourcesPaginateTypeDef = TypedDict(
    "ListS3ResourcesRequestListS3ResourcesPaginateTypeDef",
    {
        "memberAccountId": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListMemberAccountsResultTypeDef = TypedDict(
    "ListMemberAccountsResultTypeDef",
    {
        "memberAccounts": List[MemberAccountTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateS3ResourcesRequestRequestTypeDef = TypedDict(
    "AssociateS3ResourcesRequestRequestTypeDef",
    {
        "s3Resources": Sequence[S3ResourceClassificationTypeDef],
        "memberAccountId": NotRequired[str],
    },
)

ListS3ResourcesResultTypeDef = TypedDict(
    "ListS3ResourcesResultTypeDef",
    {
        "s3Resources": List[S3ResourceClassificationTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateS3ResourcesRequestRequestTypeDef = TypedDict(
    "UpdateS3ResourcesRequestRequestTypeDef",
    {
        "s3ResourcesUpdate": Sequence[S3ResourceClassificationUpdateTypeDef],
        "memberAccountId": NotRequired[str],
    },
)

AssociateS3ResourcesResultTypeDef = TypedDict(
    "AssociateS3ResourcesResultTypeDef",
    {
        "failedS3Resources": List[FailedS3ResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateS3ResourcesResultTypeDef = TypedDict(
    "DisassociateS3ResourcesResultTypeDef",
    {
        "failedS3Resources": List[FailedS3ResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateS3ResourcesResultTypeDef = TypedDict(
    "UpdateS3ResourcesResultTypeDef",
    {
        "failedS3Resources": List[FailedS3ResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
