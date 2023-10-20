from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_flow_json_body_value_modules_item_suspend_resume_form import (
        UpdateFlowJsonBodyValueModulesItemSuspendResumeForm,
    )


T = TypeVar("T", bound="UpdateFlowJsonBodyValueModulesItemSuspend")


@_attrs_define
class UpdateFlowJsonBodyValueModulesItemSuspend:
    """
    Attributes:
        required_events (Union[Unset, int]):
        timeout (Union[Unset, int]):
        resume_form (Union[Unset, UpdateFlowJsonBodyValueModulesItemSuspendResumeForm]):
    """

    required_events: Union[Unset, int] = UNSET
    timeout: Union[Unset, int] = UNSET
    resume_form: Union[Unset, "UpdateFlowJsonBodyValueModulesItemSuspendResumeForm"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        required_events = self.required_events
        timeout = self.timeout
        resume_form: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resume_form, Unset):
            resume_form = self.resume_form.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if required_events is not UNSET:
            field_dict["required_events"] = required_events
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if resume_form is not UNSET:
            field_dict["resume_form"] = resume_form

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_flow_json_body_value_modules_item_suspend_resume_form import (
            UpdateFlowJsonBodyValueModulesItemSuspendResumeForm,
        )

        d = src_dict.copy()
        required_events = d.pop("required_events", UNSET)

        timeout = d.pop("timeout", UNSET)

        _resume_form = d.pop("resume_form", UNSET)
        resume_form: Union[Unset, UpdateFlowJsonBodyValueModulesItemSuspendResumeForm]
        if isinstance(_resume_form, Unset):
            resume_form = UNSET
        else:
            resume_form = UpdateFlowJsonBodyValueModulesItemSuspendResumeForm.from_dict(_resume_form)

        update_flow_json_body_value_modules_item_suspend = cls(
            required_events=required_events,
            timeout=timeout,
            resume_form=resume_form,
        )

        update_flow_json_body_value_modules_item_suspend.additional_properties = d
        return update_flow_json_body_value_modules_item_suspend

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
