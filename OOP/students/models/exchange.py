from __future__ import annotations

from .base import Student


class ExchangeStudent(Student):
    """Sinh viên trao đổi quốc tế.

    - Học phí cố định theo chương trình `program_fee`.
    - Không quản lý tín chỉ nội bộ (credits có thể do trường đối tác)."""

    def __init__(
        self,
        student_id: str,
        full_name: str,
        major: str,
        gpa: float = 0.0,
        program_fee: float = 5_000_000.0,
    ) -> None:
        super().__init__(student_id, full_name, major, gpa)
        if program_fee < 0:
            raise ValueError("program_fee không được âm")
        self._program_fee = float(program_fee)

    def calculate_tuition(self) -> float:
        return self._program_fee

    @property
    def program_fee(self) -> float:
        return self._program_fee