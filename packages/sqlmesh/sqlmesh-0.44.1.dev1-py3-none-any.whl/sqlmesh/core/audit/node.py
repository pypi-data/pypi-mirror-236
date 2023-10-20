from __future__ import annotations

from sqlmesh.core.node import Node
from sqlmesh.core.audit import Audit

class AuditNode(Node, Audit):
    pass