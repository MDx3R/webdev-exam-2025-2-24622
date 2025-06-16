from dataclasses import dataclass


@dataclass(frozen=True)
class Id:
    value: int

    def __post_init__(self):
        assert self.value is not None, "ID is not set"
        assert self.value > 0, "ID must be positive"


@dataclass
class Entity:
    entity_id: Id | None

    @property
    def id(self) -> Id | None:
        return self.entity_id

    @property
    def id_safe(self) -> Id:
        assert self.entity_id, "ID is not set"
        return self.entity_id

    def has_id(self) -> bool:
        return self.entity_id is not None
