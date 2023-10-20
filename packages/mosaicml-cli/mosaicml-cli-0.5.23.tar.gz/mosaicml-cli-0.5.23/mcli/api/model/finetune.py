"""Finetuned model object"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Tuple

from mcli.api.exceptions import MAPIException
from mcli.api.schema.generic_model import DeserializableModel, convert_datetime
from mcli.utils.utils_run_status import RunStatus


@dataclass
class Finetune(DeserializableModel):
    """A Finetune that has been run on the MosaicML platform
    
    Args:
        id: The unique identifier for this finetuning run.
        name: The name of the finetuning run.
        status: The current status of the finetuning run. This is a RunStatus enum, which has values
            such as ``PENDING``, ``RUNNING``, or ``COMPLETED``.
        created_at: The timestamp at which the finetuning run was created.
        updated_at: The timestamp at which the finetuning run was last updated.
        created_by: The email address of the user who created the finetuning run.
        started_at: The timestamp at which the finetuning run was started.
        completed_at: The timestamp at which the finetuning run was completed.
        reason: The reason for the finetuning run's current status, such as ``Run completed successfully``.
    """
    id: str
    name: str
    status: RunStatus
    created_at: datetime
    updated_at: datetime
    created_by: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    reason: Optional[str] = None
    # TODO: add submitted config and events when shipped

    _required_properties: Tuple[str] = tuple([
        'id',
        'name',
        'status',
        'createdByEmail',
        'createdAt',
        'updatedAt',
    ])

    # TODO: implement stop and delete functions on this model

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> Finetune:
        missing = set(cls._required_properties) - set(response)
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message=f'Missing required key(s) in response to deserialize Finetune object: {", ".join(missing)}',
            )
        started_at = convert_datetime(response['startedAt']) if response.get('startedAt', None) else None
        completed_at = convert_datetime(response['completedAt']) if response.get('completedAt', None) else None

        args = {
            'id': response['id'],
            'name': response['name'],
            'created_at': convert_datetime(response['createdAt']),
            'updated_at': convert_datetime(response['updatedAt']),
            'started_at': started_at,
            'completed_at': completed_at,
            'status': RunStatus.from_string(response['status']),
            'reason': response.get('reason', ''),
            'created_by': response['createdByEmail'],
        }

        return Finetune(**args)
