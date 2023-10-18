from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import (
    Any,
    Dict,
    Generator,
    List,
    Optional,
    Protocol,
    Set,
    Text,
    Union,
    runtime_checkable,
)
import structlog

from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.constants import RASA_DEFAULT_FLOW_PATTERN_PREFIX, UTTER_PREFIX
from rasa.shared.exceptions import RasaException
from rasa.shared.nlu.constants import ENTITY_ATTRIBUTE_TYPE, INTENT_NAME_KEY

import rasa.shared.utils.io
from rasa.shared.utils.llm import (
    DEFAULT_OPENAI_GENERATE_MODEL_NAME,
    DEFAULT_OPENAI_TEMPERATURE,
)

structlogger = structlog.get_logger()

START_STEP = "START"

END_STEP = "END"

DEFAULT_STEPS = {END_STEP, START_STEP}


class UnreachableFlowStepException(RasaException):
    """Raised when a flow step is unreachable."""

    def __init__(self, step: FlowStep, flow: Flow) -> None:
        """Initializes the exception."""
        self.step = step
        self.flow = flow

    def __str__(self) -> Text:
        """Return a string representation of the exception."""
        return (
            f"Step '{self.step.id}' in flow '{self.flow.id}' can not be reached "
            f"from the start step. Please make sure that all steps can be reached "
            f"from the start step, e.g. by "
            f"checking that another step points to this step."
        )


class MissingNextLinkException(RasaException):
    """Raised when a flow step is missing a next link."""

    def __init__(self, step: FlowStep, flow: Flow) -> None:
        """Initializes the exception."""
        self.step = step
        self.flow = flow

    def __str__(self) -> Text:
        """Return a string representation of the exception."""
        return (
            f"Step '{self.step.id}' in flow '{self.flow.id}' is missing a `next`. "
            f"As a last step of a branch, it is required to have one. "
        )


class ReservedFlowStepIdException(RasaException):
    """Raised when a flow step is using a reserved id."""

    def __init__(self, step: FlowStep, flow: Flow) -> None:
        """Initializes the exception."""
        self.step = step
        self.flow = flow

    def __str__(self) -> Text:
        """Return a string representation of the exception."""
        return (
            f"Step '{self.step.id}' in flow '{self.flow.id}' is using the reserved id "
            f"'{self.step.id}'. Please use a different id for your step."
        )


class MissingElseBranchException(RasaException):
    """Raised when a flow step is missing an else branch."""

    def __init__(self, step: FlowStep, flow: Flow) -> None:
        """Initializes the exception."""
        self.step = step
        self.flow = flow

    def __str__(self) -> Text:
        """Return a string representation of the exception."""
        return (
            f"Step '{self.step.id}' in flow '{self.flow.id}' is missing an `else` "
            f"branch. If a steps `next` statement contains an `if` it always "
            f"also needs an `else` branch. Please add the missing `else` branch."
        )


class NoNextAllowedForLinkException(RasaException):
    """Raised when a flow step has a next link but is not allowed to have one."""

    def __init__(self, step: FlowStep, flow: Flow) -> None:
        """Initializes the exception."""
        self.step = step
        self.flow = flow

    def __str__(self) -> Text:
        """Return a string representation of the exception."""
        return (
            f"Link step '{self.step.id}' in flow '{self.flow.id}' has a `next` but "
            f"as a link step is not allowed to have one."
        )


class UnresolvedFlowStepIdException(RasaException):
    """Raised when a flow step is referenced, but its id can not be resolved."""

    def __init__(
        self, step_id: Text, flow: Flow, referenced_from: Optional[FlowStep]
    ) -> None:
        """Initializes the exception."""
        self.step_id = step_id
        self.flow = flow
        self.referenced_from = referenced_from

    def __str__(self) -> Text:
        """Return a string representation of the exception."""
        if self.referenced_from:
            exception_message = (
                f"Step with id '{self.step_id}' could not be resolved. "
                f"'Step '{self.referenced_from.id}' in flow '{self.flow.id}' "
                f"referenced this step but it does not exist. "
            )
        else:
            exception_message = (
                f"Step '{self.step_id}' in flow '{self.flow.id}' can not be resolved. "
            )

        return exception_message + (
            "Please make sure that the step is defined in the same flow."
        )


class UnresolvedFlowException(RasaException):
    """Raised when a flow is referenced but it's id can not be resolved."""

    def __init__(self, flow_id: Text) -> None:
        """Initializes the exception."""
        self.flow_id = flow_id

    def __str__(self) -> Text:
        """Return a string representation of the exception."""
        return (
            f"Flow '{self.flow_id}' can not be resolved. "
            f"Please make sure that the flow is defined."
        )


class FlowsList:
    """Represents the configuration of a list of flow.

    We need this class to be able to fingerprint the flows configuration.
    Fingerprinting is needed to make sure that the model is retrained if the
    flows configuration changes.
    """

    def __init__(self, flows: List[Flow]) -> None:
        """Initializes the configuration of flows.

        Args:
            flows: The flows to be configured.
        """
        self.underlying_flows = flows

    def is_empty(self) -> bool:
        """Returns whether the flows list is empty."""
        return len(self.underlying_flows) == 0

    @classmethod
    def from_json(
        cls, flows_configs: Optional[Dict[Text, Dict[Text, Any]]]
    ) -> FlowsList:
        """Used to read flows from parsed YAML.

        Args:
            flows_configs: The parsed YAML as a dictionary.

        Returns:
            The parsed flows.
        """
        if not flows_configs:
            return cls([])

        return cls(
            [
                Flow.from_json(flow_id, flow_config)
                for flow_id, flow_config in flows_configs.items()
            ]
        )

    def as_json(self) -> List[Dict[Text, Any]]:
        """Returns the flows as a dictionary.

        Returns:
            The flows as a dictionary.
        """
        return [flow.as_json() for flow in self.underlying_flows]

    def fingerprint(self) -> str:
        """Creates a fingerprint of the flows configuration.

        Returns:
            The fingerprint of the flows configuration.
        """
        flow_dicts = [flow.as_json() for flow in self.underlying_flows]
        return rasa.shared.utils.io.get_list_fingerprint(flow_dicts)

    def merge(self, other: FlowsList) -> FlowsList:
        """Merges two lists of flows together."""
        return FlowsList(self.underlying_flows + other.underlying_flows)

    def flow_by_id(self, id: Optional[Text]) -> Optional[Flow]:
        """Return the flow with the given id."""
        if not id:
            return None

        for flow in self.underlying_flows:
            if flow.id == id:
                return flow
        else:
            return None

    def step_by_id(self, step_id: Text, flow_id: Text) -> FlowStep:
        """Return the step with the given id."""
        flow = self.flow_by_id(flow_id)
        if not flow:
            raise UnresolvedFlowException(flow_id)

        step = flow.step_by_id(step_id)
        if not step:
            raise UnresolvedFlowStepIdException(step_id, flow, referenced_from=None)

        return step

    def validate(self) -> None:
        """Validate the flows."""
        for flow in self.underlying_flows:
            flow.validate()

    def non_pattern_flows(self) -> List[str]:
        """Get all flows that can be started.

        Args:
            all_flows: All flows.

        Returns:
            All flows that can be started."""
        return [f.id for f in self.underlying_flows if not f.is_handling_pattern()]

    @property
    def utterances(self) -> Set[str]:
        """Retrieve all utterances of all flows"""
        return set().union(*[flow.utterances for flow in self.underlying_flows])


@dataclass
class Flow:
    """Represents the configuration of a flow."""

    id: Text
    """The id of the flow."""
    name: Text
    """The human-readable name of the flow."""
    description: Optional[Text]
    """The description of the flow."""
    step_sequence: StepSequence
    """The steps of the flow."""

    @staticmethod
    def from_json(flow_id: Text, flow_config: Dict[Text, Any]) -> Flow:
        """Used to read flows from parsed YAML.

        Args:
            flow_config: The parsed YAML as a dictionary.

        Returns:
            The parsed flow.
        """
        step_sequence = StepSequence.from_json(flow_config.get("steps"))

        return Flow(
            id=flow_id,
            name=flow_config.get("name", Flow.create_default_name(flow_id)),
            description=flow_config.get("description"),
            step_sequence=Flow.resolve_default_ids(step_sequence),
        )

    @staticmethod
    def create_default_name(flow_id: str) -> str:
        """Create a default flow name for when it is missing."""
        return flow_id.replace("_", " ").replace("-", " ")

    @staticmethod
    def resolve_default_ids(step_sequence: StepSequence) -> StepSequence:
        """Resolves the default ids of all steps in the sequence.

        If a step does not have an id, a default id is assigned to it based
        on the type of the step and its position in the flow.

        Similarly, if a step doesn't have an explicit next assigned we resolve
        the default next step id.

        Args:
            step_sequence: The step sequence to resolve the default ids for.

        Returns:
            The step sequence with the default ids resolved.
        """
        # assign an index to all steps
        for idx, step in enumerate(step_sequence.steps):
            step.idx = idx

        def resolve_default_next(steps: List[FlowStep], is_root_sequence: bool) -> None:
            for i, step in enumerate(steps):
                if step.next.no_link_available():
                    if i == len(steps) - 1:
                        # can't attach end to link step
                        if is_root_sequence and not isinstance(step, LinkFlowStep):
                            # if this is the root sequence, we need to add an end step
                            # to the end of the sequence. other sequences, e.g.
                            # in branches need to explicitly add a next step.
                            step.next.links.append(StaticFlowLink(target=END_STEP))
                    else:
                        step.next.links.append(StaticFlowLink(target=steps[i + 1].id))
                for link in step.next.links:
                    if sub_steps := link.child_steps():
                        resolve_default_next(sub_steps, is_root_sequence=False)

        resolve_default_next(step_sequence.child_steps, is_root_sequence=True)
        return step_sequence

    def as_json(self) -> Dict[Text, Any]:
        """Returns the flow as a dictionary.

        Returns:
            The flow as a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "steps": self.step_sequence.as_json(),
        }

    def readable_name(self) -> str:
        """Returns the name of the flow or its id if no name is set."""
        return self.name or self.id

    def validate(self) -> None:
        """Validates the flow configuration.

        This ensures that the flow semantically makes sense. E.g. it
        checks:
            - whether all next links point to existing steps
            - whether all steps can be reached from the start step
        """
        self._validate_all_steps_next_property()
        self._validate_all_next_ids_are_availble_steps()
        self._validate_all_steps_can_be_reached()
        self._validate_all_branches_have_an_else()
        self._validate_not_using_buildin_ids()

    def _validate_not_using_buildin_ids(self) -> None:
        """Validates that the flow does not use any of the build in ids."""
        for step in self.steps:
            if step.id in DEFAULT_STEPS or step.id.startswith(CONTINUE_STEP_PREFIX):
                raise ReservedFlowStepIdException(step, self)

    def _validate_all_branches_have_an_else(self) -> None:
        """Validates that all branches have an else link."""
        for step in self.steps:
            links = step.next.links

            has_an_if = any(isinstance(link, IfFlowLink) for link in links)
            has_an_else = any(isinstance(link, ElseFlowLink) for link in links)

            if has_an_if and not has_an_else:
                raise MissingElseBranchException(step, self)

    def _validate_all_steps_next_property(self) -> None:
        """Validates that every step has a next link."""
        for step in self.steps:
            if isinstance(step, LinkFlowStep):
                # link steps can't have a next link!
                if not step.next.no_link_available():
                    raise NoNextAllowedForLinkException(step, self)
            elif step.next.no_link_available():
                # all other steps should have a next link
                raise MissingNextLinkException(step, self)

    def _validate_all_next_ids_are_availble_steps(self) -> None:
        """Validates that all next links point to existing steps."""
        available_steps = {step.id for step in self.steps} | DEFAULT_STEPS
        for step in self.steps:
            for link in step.next.links:
                if link.target not in available_steps:
                    raise UnresolvedFlowStepIdException(link.target, self, step)

    def _validate_all_steps_can_be_reached(self) -> None:
        """Validates that all steps can be reached from the start step."""

        def _reachable_steps(
            step: Optional[FlowStep], reached_steps: Set[Text]
        ) -> Set[Text]:
            """Validates that the given step can be reached from the start step."""
            if step is None or step.id in reached_steps:
                return reached_steps

            reached_steps.add(step.id)
            for link in step.next.links:
                reached_steps = _reachable_steps(
                    self.step_by_id(link.target), reached_steps
                )
            return reached_steps

        reached_steps = _reachable_steps(self.first_step_in_flow(), set())

        for step in self.steps:
            if step.id not in reached_steps:
                raise UnreachableFlowStepException(step, self)

    def step_by_id(self, step_id: Optional[Text]) -> Optional[FlowStep]:
        """Returns the step with the given id."""
        if not step_id:
            return None

        if step_id == START_STEP:
            first_step_in_flow = self.first_step_in_flow()
            return StartFlowStep(first_step_in_flow.id if first_step_in_flow else None)

        if step_id == END_STEP:
            return EndFlowStep()

        if step_id.startswith(CONTINUE_STEP_PREFIX):
            return ContinueFlowStep(step_id[len(CONTINUE_STEP_PREFIX) :])

        for step in self.steps:
            if step.id == step_id:
                return step

        return None

    def first_step_in_flow(self) -> Optional[FlowStep]:
        """Returns the start step of this flow."""
        if len(self.steps) == 0:
            return None
        return self.steps[0]

    def previous_collect_steps(
        self, step_id: Optional[str]
    ) -> List[CollectInformationFlowStep]:
        """Returns the collect informations asked before the given step.

        CollectInformations are returned roughly in reverse order, i.e. the first
        collect information in the list is the one asked last. But due to circles
        in the flow the order is not guaranteed to be exactly reverse.
        """

        def _previously_asked_collect(
            current_step_id: str, visited_steps: Set[str]
        ) -> List[CollectInformationFlowStep]:
            """Returns the collect informations asked before the given step.

            Keeps track of the steps that have been visited to avoid circles.
            """
            current_step = self.step_by_id(current_step_id)

            collects: List[CollectInformationFlowStep] = []

            if not current_step:
                return collects

            if isinstance(current_step, CollectInformationFlowStep):
                collects.append(current_step)

            visited_steps.add(current_step.id)

            for previous_step in self.steps:
                for next_link in previous_step.next.links:
                    if next_link.target != current_step_id:
                        continue
                    if previous_step.id in visited_steps:
                        continue
                    collects.extend(
                        _previously_asked_collect(previous_step.id, visited_steps)
                    )
            return collects

        return _previously_asked_collect(step_id or START_STEP, set())

    def is_handling_pattern(self) -> bool:
        """Returns whether the flow is handling a pattern."""
        return self.id.startswith(RASA_DEFAULT_FLOW_PATTERN_PREFIX)

    def get_trigger_intents(self) -> Set[str]:
        """Returns the trigger intents of the flow"""
        results: Set[str] = set()
        if len(self.steps) == 0:
            return results

        first_step = self.steps[0]

        if not isinstance(first_step, UserMessageStep):
            return results

        for condition in first_step.trigger_conditions:
            results.add(condition.intent)

        return results

    def is_user_triggerable(self) -> bool:
        """Test whether a user can trigger the flow with an intent."""
        return len(self.get_trigger_intents()) > 0

    def is_rasa_default_flow(self) -> bool:
        """Test whether something is a rasa default flow."""
        return self.id.startswith(RASA_DEFAULT_FLOW_PATTERN_PREFIX)

    def get_collect_steps(self) -> List[CollectInformationFlowStep]:
        """Return the collect information steps of the flow."""
        collect_steps = []
        for step in self.steps:
            if isinstance(step, CollectInformationFlowStep):
                collect_steps.append(step)
        return collect_steps

    @property
    def steps(self) -> List[FlowStep]:
        """Returns the steps of the flow."""
        return self.step_sequence.steps

    @cached_property
    def fingerprint(self) -> str:
        """Create a fingerprint identifying this step sequence."""
        return rasa.shared.utils.io.deep_container_fingerprint(self.as_json())

    @property
    def utterances(self) -> Set[str]:
        """Retrieve all utterances of this flow"""
        return set().union(*[step.utterances for step in self.step_sequence.steps])


@dataclass
class StepSequence:
    child_steps: List[FlowStep]

    @staticmethod
    def from_json(steps_config: List[Dict[Text, Any]]) -> StepSequence:
        """Used to read steps from parsed YAML.

        Args:
            steps_config: The parsed YAML as a dictionary.

        Returns:
            The parsed steps.
        """

        flow_steps: List[FlowStep] = [step_from_json(config) for config in steps_config]

        return StepSequence(child_steps=flow_steps)

    def as_json(self) -> List[Dict[Text, Any]]:
        """Returns the steps as a dictionary.

        Returns:
            The steps as a dictionary.
        """
        return [
            step.as_json()
            for step in self.child_steps
            if not isinstance(step, InternalFlowStep)
        ]

    @property
    def steps(self) -> List[FlowStep]:
        """Returns the steps of the flow."""
        return [
            step
            for child_step in self.child_steps
            for step in child_step.steps_in_tree()
        ]

    def first(self) -> Optional[FlowStep]:
        """Returns the first step of the sequence."""
        if len(self.child_steps) == 0:
            return None
        return self.child_steps[0]


def step_from_json(flow_step_config: Dict[Text, Any]) -> FlowStep:
    """Used to read flow steps from parsed YAML.

    Args:
        flow_step_config: The parsed YAML as a dictionary.

    Returns:
        The parsed flow step.
    """
    if "action" in flow_step_config:
        return ActionFlowStep.from_json(flow_step_config)
    if "intent" in flow_step_config:
        return UserMessageStep.from_json(flow_step_config)
    if "collect" in flow_step_config:
        return CollectInformationFlowStep.from_json(flow_step_config)
    if "link" in flow_step_config:
        return LinkFlowStep.from_json(flow_step_config)
    if "set_slots" in flow_step_config:
        return SetSlotsFlowStep.from_json(flow_step_config)
    if "entry_prompt" in flow_step_config:
        return EntryPromptFlowStep.from_json(flow_step_config)
    if "generation_prompt" in flow_step_config:
        return GenerateResponseFlowStep.from_json(flow_step_config)
    else:
        return BranchFlowStep.from_json(flow_step_config)


@dataclass
class FlowStep:
    """Represents the configuration of a flow step."""

    custom_id: Optional[Text]
    """The id of the flow step."""
    idx: int
    """The index of the step in the flow."""
    description: Optional[Text]
    """The description of the flow step."""
    metadata: Dict[Text, Any]
    """Additional, unstructured information about this flow step."""
    next: "FlowLinks"
    """The next steps of the flow step."""

    @classmethod
    def _from_json(cls, flow_step_config: Dict[Text, Any]) -> FlowStep:
        """Used to read flow steps from parsed YAML.

        Args:
            flow_step_config: The parsed YAML as a dictionary.

        Returns:
            The parsed flow step.
        """
        return FlowStep(
            # the idx is set later once the flow is created that contains
            # this step
            idx=-1,
            custom_id=flow_step_config.get("id"),
            description=flow_step_config.get("description"),
            metadata=flow_step_config.get("metadata", {}),
            next=FlowLinks.from_json(flow_step_config.get("next", [])),
        )

    def as_json(self) -> Dict[Text, Any]:
        """Returns the flow step as a dictionary.

        Returns:
            The flow step as a dictionary.
        """
        dump = {"next": self.next.as_json(), "id": self.id}

        if self.description:
            dump["description"] = self.description
        if self.metadata:
            dump["metadata"] = self.metadata
        return dump

    def steps_in_tree(self) -> Generator[FlowStep, None, None]:
        """Returns the steps in the tree of the flow step."""
        yield self
        yield from self.next.steps_in_tree()

    @property
    def id(self) -> Text:
        """Returns the id of the flow step."""
        return self.custom_id or self.default_id()

    def default_id(self) -> str:
        """Returns the default id of the flow step."""
        return f"{self.idx}_{self.default_id_postfix()}"

    def default_id_postfix(self) -> str:
        """Returns the default id postfix of the flow step."""
        raise NotImplementedError()

    @property
    def utterances(self) -> Set[str]:
        """Return all the utterances used in this step"""
        return set()


class InternalFlowStep(FlowStep):
    """Represents the configuration of a built-in flow step.

    Built in flow steps are required to manage the lifecycle of a
    flow and are not intended to be used by users.
    """

    @classmethod
    def from_json(cls, flow_step_config: Dict[Text, Any]) -> ActionFlowStep:
        """Used to read flow steps from parsed JSON.

        Args:
            flow_step_config: The parsed JSON as a dictionary.

        Returns:
            The parsed flow step.
        """
        raise ValueError("A start step cannot be parsed.")

    def as_json(self) -> Dict[Text, Any]:
        """Returns the flow step as a dictionary.

        Returns:
            The flow step as a dictionary.
        """
        raise ValueError("A start step cannot be dumped.")


@dataclass
class StartFlowStep(InternalFlowStep):
    """Represents the configuration of a start flow step."""

    def __init__(self, start_step_id: Optional[Text]) -> None:
        """Initializes a start flow step.

        Args:
            start_step: The step to start the flow from.
        """
        if start_step_id is not None:
            links: List[FlowLink] = [StaticFlowLink(target=start_step_id)]
        else:
            links = []

        super().__init__(
            idx=0,
            custom_id=START_STEP,
            description=None,
            metadata={},
            next=FlowLinks(links=links),
        )


@dataclass
class EndFlowStep(InternalFlowStep):
    """Represents the configuration of an end to a flow."""

    def __init__(self) -> None:
        """Initializes an end flow step."""
        super().__init__(
            idx=0,
            custom_id=END_STEP,
            description=None,
            metadata={},
            next=FlowLinks(links=[]),
        )


CONTINUE_STEP_PREFIX = "NEXT:"


@dataclass
class ContinueFlowStep(InternalFlowStep):
    """Represents the configuration of a continue-step flow step."""

    def __init__(self, next: str) -> None:
        """Initializes a continue-step flow step."""
        super().__init__(
            idx=0,
            custom_id=CONTINUE_STEP_PREFIX + next,
            description=None,
            metadata={},
            # The continue step links to the step that should be continued.
            # The flow policy in a sense only "runs" the logic of a step
            # when it transitions to that step, once it is there it will use
            # the next link to transition to the next step. This means that
            # if we want to "re-run" a step, we need to link to it again.
            # This is why the continue step links to the step that should be
            # continued.
            next=FlowLinks(links=[StaticFlowLink(target=next)]),
        )

    @staticmethod
    def continue_step_for_id(step_id: str) -> str:
        return CONTINUE_STEP_PREFIX + step_id


@dataclass
class ActionFlowStep(FlowStep):
    """Represents the configuration of an action flow step."""

    action: Text
    """The action of the flow step."""

    @classmethod
    def from_json(cls, flow_step_config: Dict[Text, Any]) -> ActionFlowStep:
        """Used to read flow steps from parsed YAML.

        Args:
            flow_step_config: The parsed YAML as a dictionary.

        Returns:
            The parsed flow step.
        """
        base = super()._from_json(flow_step_config)
        return ActionFlowStep(
            action=flow_step_config.get("action", ""),
            **base.__dict__,
        )

    def as_json(self) -> Dict[Text, Any]:
        """Returns the flow step as a dictionary.

        Returns:
            The flow step as a dictionary.
        """
        dump = super().as_json()
        dump["action"] = self.action
        return dump

    def default_id_postfix(self) -> str:
        return self.action

    @property
    def utterances(self) -> Set[str]:
        """Return all the utterances used in this step"""
        return {self.action} if self.action.startswith(UTTER_PREFIX) else set()


@dataclass
class BranchFlowStep(FlowStep):
    """Represents the configuration of a branch flow step."""

    @classmethod
    def from_json(cls, flow_step_config: Dict[Text, Any]) -> BranchFlowStep:
        """Used to read flow steps from parsed YAML.

        Args:
            flow_step_config: The parsed YAML as a dictionary.

        Returns:
            The parsed flow step.
        """
        base = super()._from_json(flow_step_config)
        return BranchFlowStep(**base.__dict__)

    def as_json(self) -> Dict[Text, Any]:
        """Returns the flow step as a dictionary.

        Returns:
            The flow step as a dictionary.
        """
        dump = super().as_json()
        return dump

    def default_id_postfix(self) -> str:
        """Returns the default id postfix of the flow step."""
        return "branch"


@dataclass
class LinkFlowStep(FlowStep):
    """Represents the configuration of a link flow step."""

    link: Text
    """The link of the flow step."""

    @classmethod
    def from_json(cls, flow_step_config: Dict[Text, Any]) -> LinkFlowStep:
        """Used to read flow steps from parsed YAML.

        Args:
            flow_step_config: The parsed YAML as a dictionary.

        Returns:
            The parsed flow step.
        """
        base = super()._from_json(flow_step_config)
        return LinkFlowStep(
            link=flow_step_config.get("link", ""),
            **base.__dict__,
        )

    def as_json(self) -> Dict[Text, Any]:
        """Returns the flow step as a dictionary.

        Returns:
            The flow step as a dictionary.
        """
        dump = super().as_json()
        dump["link"] = self.link
        return dump

    def default_id_postfix(self) -> str:
        """Returns the default id postfix of the flow step."""
        return f"link_{self.link}"


@dataclass
class TriggerCondition:
    """Represents the configuration of a trigger condition."""

    intent: Text
    """The intent to trigger the flow."""
    entities: List[Text]
    """The entities to trigger the flow."""

    def is_triggered(self, intent: Text, entities: List[Text]) -> bool:
        """Check if condition is triggered by the given intent and entities.

        Args:
            intent: The intent to check.
            entities: The entities to check.

        Returns:
            Whether the trigger condition is triggered by the given intent and entities.
        """
        if self.intent != intent:
            return False
        if len(self.entities) == 0:
            return True
        return all(entity in entities for entity in self.entities)


@runtime_checkable
class StepThatCanStartAFlow(Protocol):
    """Represents a step that can start a flow."""

    def is_triggered(self, tracker: DialogueStateTracker) -> bool:
        """Check if a flow should be started for the tracker

        Args:
            tracker: The tracker to check.

        Returns:
            Whether a flow should be started for the tracker.
        """
        ...


@dataclass
class UserMessageStep(FlowStep, StepThatCanStartAFlow):
    """Represents the configuration of an intent flow step."""

    trigger_conditions: List[TriggerCondition]
    """The trigger conditions of the flow step."""

    @classmethod
    def from_json(cls, flow_step_config: Dict[Text, Any]) -> UserMessageStep:
        """Used to read flow steps from parsed YAML.

        Args:
            flow_step_config: The parsed YAML as a dictionary.

        Returns:
            The parsed flow step.
        """
        base = super()._from_json(flow_step_config)

        trigger_conditions = []
        if "intent" in flow_step_config:
            trigger_conditions.append(
                TriggerCondition(
                    intent=flow_step_config["intent"],
                    entities=flow_step_config.get("entities", []),
                )
            )
        elif "or" in flow_step_config:
            for trigger_condition in flow_step_config["or"]:
                trigger_conditions.append(
                    TriggerCondition(
                        intent=trigger_condition.get("intent", ""),
                        entities=trigger_condition.get("entities", []),
                    )
                )

        return UserMessageStep(
            trigger_conditions=trigger_conditions,
            **base.__dict__,
        )

    def as_json(self) -> Dict[Text, Any]:
        """Returns the flow step as a dictionary.

        Returns:
            The flow step as a dictionary.
        """
        dump = super().as_json()

        if len(self.trigger_conditions) == 1:
            dump["intent"] = self.trigger_conditions[0].intent
            if self.trigger_conditions[0].entities:
                dump["entities"] = self.trigger_conditions[0].entities
        elif len(self.trigger_conditions) > 1:
            dump["or"] = [
                {
                    "intent": trigger_condition.intent,
                    "entities": trigger_condition.entities,
                }
                for trigger_condition in self.trigger_conditions
            ]

        return dump

    def is_triggered(self, tracker: DialogueStateTracker) -> bool:
        """Returns whether the flow step is triggered by the given intent and entities.

        Args:
            intent: The intent to check.
            entities: The entities to check.

        Returns:
            Whether the flow step is triggered by the given intent and entities.
        """
        if not tracker.latest_message:
            return False

        intent: Text = tracker.latest_message.intent.get(INTENT_NAME_KEY, "")
        entities: List[Text] = [
            e.get(ENTITY_ATTRIBUTE_TYPE, "") for e in tracker.latest_message.entities
        ]
        return any(
            trigger_condition.is_triggered(intent, entities)
            for trigger_condition in self.trigger_conditions
        )

    def default_id_postfix(self) -> str:
        """Returns the default id postfix of the flow step."""
        return "intent"


DEFAULT_LLM_CONFIG = {
    "_type": "openai",
    "request_timeout": 5,
    "temperature": DEFAULT_OPENAI_TEMPERATURE,
    "model_name": DEFAULT_OPENAI_GENERATE_MODEL_NAME,
}


@dataclass
class GenerateResponseFlowStep(FlowStep):
    """Represents the configuration of a step prompting an LLM."""

    generation_prompt: Text
    """The prompt template of the flow step."""
    llm_config: Optional[Dict[Text, Any]] = None
    """The LLM configuration of the flow step."""

    @classmethod
    def from_json(cls, flow_step_config: Dict[Text, Any]) -> GenerateResponseFlowStep:
        """Used to read flow steps from parsed YAML.

        Args:
            flow_step_config: The parsed YAML as a dictionary.

        Returns:
            The parsed flow step.
        """
        base = super()._from_json(flow_step_config)
        return GenerateResponseFlowStep(
            generation_prompt=flow_step_config.get("generation_prompt", ""),
            llm_config=flow_step_config.get("llm", None),
            **base.__dict__,
        )

    def as_json(self) -> Dict[Text, Any]:
        """Returns the flow step as a dictionary.

        Returns:
            The flow step as a dictionary.
        """
        dump = super().as_json()
        dump["generation_prompt"] = self.generation_prompt
        if self.llm_config:
            dump["llm"] = self.llm_config

        return dump

    def generate(self, tracker: DialogueStateTracker) -> Optional[Text]:
        """Generates a response for the given tracker.

        Args:
            tracker: The tracker to generate a response for.

        Returns:
            The generated response.
        """
        from rasa.shared.utils.llm import llm_factory, tracker_as_readable_transcript
        from jinja2 import Template

        context = {
            "history": tracker_as_readable_transcript(tracker, max_turns=5),
            "latest_user_message": tracker.latest_message.text
            if tracker.latest_message
            else "",
        }
        context.update(tracker.current_slot_values())

        llm = llm_factory(self.llm_config, DEFAULT_LLM_CONFIG)
        prompt = Template(self.generation_prompt).render(context)

        try:
            return llm(prompt)
        except Exception as e:
            # unfortunately, langchain does not wrap LLM exceptions which means
            # we have to catch all exceptions here
            structlogger.error(
                "flow.generate_step.llm.error", error=e, step=self.id, prompt=prompt
            )
            return None

    def default_id_postfix(self) -> str:
        return "generate"


@dataclass
class EntryPromptFlowStep(FlowStep, StepThatCanStartAFlow):
    """Represents the configuration of a step prompting an LLM."""

    entry_prompt: Text
    """The prompt template of the flow step."""
    advance_if: Optional[Text]
    """The expected response to start the flow"""
    llm_config: Optional[Dict[Text, Any]] = None
    """The LLM configuration of the flow step."""

    @classmethod
    def from_json(cls, flow_step_config: Dict[Text, Any]) -> EntryPromptFlowStep:
        """Used to read flow steps from parsed YAML.

        Args:
            flow_step_config: The parsed YAML as a dictionary.

        Returns:
            The parsed flow step.
        """
        base = super()._from_json(flow_step_config)
        return EntryPromptFlowStep(
            entry_prompt=flow_step_config.get("entry_prompt", ""),
            advance_if=flow_step_config.get("advance_if"),
            llm_config=flow_step_config.get("llm", None),
            **base.__dict__,
        )

    def as_json(self) -> Dict[Text, Any]:
        """Returns the flow step as a dictionary.

        Returns:
            The flow step as a dictionary.
        """
        dump = super().as_json()
        dump["entry_prompt"] = self.entry_prompt
        if self.advance_if:
            dump["advance_if"] = self.advance_if

        if self.llm_config:
            dump["llm"] = self.llm_config
        return dump

    def _generate_using_llm(self, prompt: str) -> Optional[str]:
        """Use LLM to generate a response.

        Args:
            prompt: the prompt to send to the LLM

        Returns:
            generated text
        """
        from rasa.shared.utils.llm import llm_factory

        llm = llm_factory(self.llm_config, DEFAULT_LLM_CONFIG)

        try:
            return llm(prompt)
        except Exception as e:
            # unfortunately, langchain does not wrap LLM exceptions which means
            # we have to catch all exceptions here
            structlogger.error(
                "flow.entry_step.llm.error", error=e, step=self.id, prompt=prompt
            )
            return None

    def is_triggered(self, tracker: DialogueStateTracker) -> bool:
        """Returns whether the flow step is triggered by the given intent and entities.

        Args:
            intent: The intent to check.
            entities: The entities to check.

        Returns:
            Whether the flow step is triggered by the given intent and entities.
        """
        from rasa.shared.utils import llm
        from jinja2 import Template

        if not self.entry_prompt:
            return False

        context = {
            "history": llm.tracker_as_readable_transcript(tracker, max_turns=5),
            "latest_user_message": tracker.latest_message.text
            if tracker.latest_message
            else "",
        }
        context.update(tracker.current_slot_values())
        prompt = Template(self.entry_prompt).render(context)

        generated = self._generate_using_llm(prompt)

        expected_response = self.advance_if.lower() if self.advance_if else "yes"
        if generated and generated.lower() == expected_response:
            return True
        else:
            return False

    def default_id_postfix(self) -> str:
        """Returns the default id postfix of the flow step."""
        return "entry_prompt"


@dataclass
class SlotRejection:
    """A slot rejection."""

    if_: str
    """The condition that should be checked."""
    utter: str
    """The utterance that should be executed if the condition is met."""

    @staticmethod
    def from_dict(rejection_config: Dict[Text, Any]) -> SlotRejection:
        """Used to read slot rejections from parsed YAML.

        Args:
            rejection_config: The parsed YAML as a dictionary.

        Returns:
            The parsed slot rejection.
        """
        return SlotRejection(
            if_=rejection_config["if"],
            utter=rejection_config["utter"],
        )

    def as_dict(self) -> Dict[Text, Any]:
        """Returns the slot rejection as a dictionary.

        Returns:
            The slot rejection as a dictionary.
        """
        return {
            "if": self.if_,
            "utter": self.utter,
        }


@dataclass
class CollectInformationFlowStep(FlowStep):
    """Represents the configuration of a collect information flow step."""

    collect: Text
    """The collect information of the flow step."""
    utter: Text
    """The utterance that the assistant uses to ask for the slot."""
    rejections: List[SlotRejection]
    """how the slot value is validated using predicate evaluation."""
    ask_before_filling: bool = False
    """Whether to always ask the question even if the slot is already filled."""
    reset_after_flow_ends: bool = True
    """Determines whether to reset the slot value at the end of the flow."""

    @classmethod
    def from_json(cls, flow_step_config: Dict[Text, Any]) -> CollectInformationFlowStep:
        """Used to read flow steps from parsed YAML.

        Args:
            flow_step_config: The parsed YAML as a dictionary.

        Returns:
            The parsed flow step.
        """
        base = super()._from_json(flow_step_config)
        return CollectInformationFlowStep(
            collect=flow_step_config["collect"],
            utter=flow_step_config.get(
                "utter", f"utter_ask_{flow_step_config['collect']}"
            ),
            ask_before_filling=flow_step_config.get("ask_before_filling", False),
            reset_after_flow_ends=flow_step_config.get("reset_after_flow_ends", True),
            rejections=[
                SlotRejection.from_dict(rejection)
                for rejection in flow_step_config.get("rejections", [])
            ],
            **base.__dict__,
        )

    def as_json(self) -> Dict[Text, Any]:
        """Returns the flow step as a dictionary.

        Returns:
            The flow step as a dictionary.
        """
        dump = super().as_json()
        dump["collect"] = self.collect
        dump["utter"] = self.utter
        dump["ask_before_filling"] = self.ask_before_filling
        dump["reset_after_flow_ends"] = self.reset_after_flow_ends
        dump["rejections"] = [rejection.as_dict() for rejection in self.rejections]

        return dump

    def default_id_postfix(self) -> str:
        """Returns the default id postfix of the flow step."""
        return f"collect_{self.collect}"

    @property
    def utterances(self) -> Set[str]:
        """Return all the utterances used in this step"""
        return {self.utter} | {r.utter for r in self.rejections}


@dataclass
class SetSlotsFlowStep(FlowStep):
    """Represents the configuration of a set_slots flow step."""

    slots: List[Dict[str, Any]]
    """Slots to set of the flow step."""

    @classmethod
    def from_json(cls, flow_step_config: Dict[Text, Any]) -> SetSlotsFlowStep:
        """Used to read flow steps from parsed YAML.

        Args:
            flow_step_config: The parsed YAML as a dictionary.

        Returns:
            The parsed flow step.
        """
        base = super()._from_json(flow_step_config)
        slots = [
            {"key": k, "value": v}
            for slot in flow_step_config.get("set_slots", [])
            for k, v in slot.items()
        ]
        return SetSlotsFlowStep(
            slots=slots,
            **base.__dict__,
        )

    def as_json(self) -> Dict[Text, Any]:
        """Returns the flow step as a dictionary.

        Returns:
            The flow step as a dictionary.
        """
        dump = super().as_json()
        dump["set_slots"] = [{slot["key"]: slot["value"]} for slot in self.slots]
        return dump

    def default_id_postfix(self) -> str:
        """Returns the default id postfix of the flow step."""
        return "set_slots"


@dataclass
class FlowLinks:
    """Represents the configuration of a list of flow links."""

    links: List[FlowLink]

    @staticmethod
    def from_json(flow_links_config: List[Dict[Text, Any]]) -> FlowLinks:
        """Used to read flow links from parsed YAML.

        Args:
            flow_links_config: The parsed YAML as a dictionary.

        Returns:
            The parsed flow links.
        """
        if not flow_links_config:
            return FlowLinks(links=[])

        if isinstance(flow_links_config, str):
            return FlowLinks(links=[StaticFlowLink.from_json(flow_links_config)])

        return FlowLinks(
            links=[
                FlowLinks.link_from_json(link_config)
                for link_config in flow_links_config
                if link_config
            ]
        )

    @staticmethod
    def link_from_json(link_config: Dict[Text, Any]) -> FlowLink:
        """Used to read a single flow links from parsed YAML.

        Args:
            link_config: The parsed YAML as a dictionary.

        Returns:
            The parsed flow link.
        """
        if "if" in link_config:
            return IfFlowLink.from_json(link_config)
        elif "else" in link_config:
            return ElseFlowLink.from_json(link_config)
        else:
            raise Exception("Invalid flow link")

    def as_json(self) -> Any:
        """Returns the flow links as a dictionary.

        Returns:
            The flow links as a dictionary.
        """
        if not self.links:
            return None

        if len(self.links) == 1 and isinstance(self.links[0], StaticFlowLink):
            return self.links[0].as_json()

        return [link.as_json() for link in self.links]

    def no_link_available(self) -> bool:
        """Returns whether no link is available."""
        return len(self.links) == 0

    def steps_in_tree(self) -> Generator[FlowStep, None, None]:
        """Returns the steps in the tree of the flow links."""
        for link in self.links:
            yield from link.steps_in_tree()


class FlowLink(Protocol):
    """Represents a flow link."""

    @property
    def target(self) -> Optional[Text]:
        """Returns the target of the flow link.

        Returns:
            The target of the flow link.
        """
        ...

    def as_json(self) -> Any:
        """Returns the flow link as a dictionary.

        Returns:
            The flow link as a dictionary.
        """
        ...

    @staticmethod
    def from_json(link_config: Any) -> FlowLink:
        """Used to read flow links from parsed YAML.

        Args:
            link_config: The parsed YAML as a dictionary.

        Returns:
            The parsed flow link.
        """
        ...

    def steps_in_tree(self) -> Generator[FlowStep, None, None]:
        """Returns the steps in the tree of the flow link."""
        ...

    def child_steps(self) -> List[FlowStep]:
        """Returns the child steps of the flow link."""
        ...


@dataclass
class BranchBasedLink:
    target_reference: Union[Text, StepSequence]
    """The id of the linked flow."""

    def steps_in_tree(self) -> Generator[FlowStep, None, None]:
        """Returns the steps in the tree of the flow link."""
        if isinstance(self.target_reference, StepSequence):
            yield from self.target_reference.steps

    def child_steps(self) -> List[FlowStep]:
        """Returns the child steps of the flow link."""
        if isinstance(self.target_reference, StepSequence):
            return self.target_reference.child_steps
        else:
            return []

    @property
    def target(self) -> Optional[Text]:
        """Returns the target of the flow link."""
        if isinstance(self.target_reference, StepSequence):
            if first := self.target_reference.first():
                return first.id
            else:
                return None
        else:
            return self.target_reference


@dataclass
class IfFlowLink(BranchBasedLink):
    """Represents the configuration of an if flow link."""

    condition: Optional[Text]
    """The condition of the linked flow."""

    @staticmethod
    def from_json(link_config: Dict[Text, Any]) -> IfFlowLink:
        """Used to read flow links from parsed YAML.

        Args:
            link_config: The parsed YAML as a dictionary.

        Returns:
            The parsed flow link.
        """
        if isinstance(link_config["then"], str):
            return IfFlowLink(
                target_reference=link_config["then"], condition=link_config.get("if")
            )
        else:
            return IfFlowLink(
                target_reference=StepSequence.from_json(link_config["then"]),
                condition=link_config.get("if"),
            )

    def as_json(self) -> Dict[Text, Any]:
        """Returns the flow link as a dictionary.

        Returns:
            The flow link as a dictionary.
        """
        return {
            "if": self.condition,
            "then": self.target_reference.as_json()
            if isinstance(self.target_reference, StepSequence)
            else self.target_reference,
        }


@dataclass
class ElseFlowLink(BranchBasedLink):
    """Represents the configuration of an else flow link."""

    @staticmethod
    def from_json(link_config: Dict[Text, Any]) -> ElseFlowLink:
        """Used to read flow links from parsed YAML.

        Args:
            link_config: The parsed YAML as a dictionary.

        Returns:
            The parsed flow link.
        """
        if isinstance(link_config["else"], str):
            return ElseFlowLink(target_reference=link_config["else"])
        else:
            return ElseFlowLink(
                target_reference=StepSequence.from_json(link_config["else"])
            )

    def as_json(self) -> Dict[Text, Any]:
        """Returns the flow link as a dictionary.

        Returns:
            The flow link as a dictionary.
        """
        return {
            "else": self.target_reference.as_json()
            if isinstance(self.target_reference, StepSequence)
            else self.target_reference
        }


@dataclass
class StaticFlowLink:
    """Represents the configuration of a static flow link."""

    target: Text
    """The id of the linked flow."""

    @staticmethod
    def from_json(link_config: Text) -> StaticFlowLink:
        """Used to read flow links from parsed YAML.

        Args:
            link_config: The parsed YAML as a dictionary.

        Returns:
            The parsed flow link.
        """
        return StaticFlowLink(target=link_config)

    def as_json(self) -> Text:
        """Returns the flow link as a dictionary.

        Returns:
            The flow link as a dictionary.
        """
        return self.target

    def steps_in_tree(self) -> Generator[FlowStep, None, None]:
        """Returns the steps in the tree of the flow link."""
        # static links do not have any child steps
        yield from []

    def child_steps(self) -> List[FlowStep]:
        """Returns the child steps of the flow link."""
        return []
