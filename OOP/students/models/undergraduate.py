from __future__ import annotations

from .base import Student


class UndergraduateStudent(Student):
    """Sinh viên Đại học (cử nhân).

    - Học phí = `fee_per_credit * credits` + `activity_fee`.
    """

    def __init__(
        self,
        student_id: str,
        full_name: str,
        major: str,
        gpa: float = 0.0,
        fee_per_credit: float = 500_000.0,
        activity_fee: float = 200_000.0,
        credits: int = 0,
    ) -> None:
        super().__init__(student_id, full_name, major, gpa)
        if fee_per_credit < 0 or activity_fee < 0:
            raise ValueError("Phí không được âm")
        self._fee_per_credit = float(fee_per_credit)
        self._activity_fee = float(activity_fee)
        self._credits = int(credits)

    @property
    def credits(self) -> int:
        return self._credits

    @property
    def fee_per_credit(self) -> float:
        return self._fee_per_credit

    @property
    def activity_fee(self) -> float:
        return self._activity_fee

    def enroll(self, more_credits: int) -> None:
        if more_credits < 0:
            raise ValueError("Số tín chỉ không được âm")
        self._credits += int(more_credits)

    def reset_credits(self) -> None:
        self._credits = 0

    def calculate_tuition(self) -> float:
        return self._fee_per_credit * self._credits + self._activity_fee