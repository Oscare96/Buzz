"""Registry and lookup for trusted Buzz skills."""

from __future__ import annotations

from buzz.skills.base import Skill


class SkillRegistry:
    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        if not skill.name:
            raise ValueError("Skill name cannot be empty.")
        if skill.name in self._skills:
            raise ValueError(f"Skill already registered: {skill.name}")
        self._skills[skill.name] = skill

    def get(self, name: str) -> Skill:
        try:
            return self._skills[name]
        except KeyError as exc:
            raise KeyError(f"Unknown skill: {name}") from exc

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._skills))

    def planner_specs(self) -> tuple[dict, ...]:
        return tuple(self._skills[name].planner_spec() for name in sorted(self._skills))
