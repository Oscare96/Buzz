"""Safe system-information skills."""

from __future__ import annotations

import platform
from typing import Any

from buzz.security.risk import RiskLevel
from buzz.skills.base import Skill, SkillResult


class SystemInfoSkill(Skill):
    name = "system.info"
    description = "Read basic local operating-system information."
    risk_level = RiskLevel.READ

    def execute(self, **kwargs: Any) -> SkillResult:
        data = {"system": platform.system(), "release": platform.release(), "machine": platform.machine()}
        return SkillResult(True, "System information retrieved.", data)
