from __future__ import annotations

from .base import Student


class GraduateStudent(Student):
    """Sinh viên Cao học (thạc sĩ/tiến sĩ).

    - Học phí = `fee_per_credit * credits` + `research_fee`.
    - Có thể có học bổng `scholarship_rate` giảm theo tỷ lệ.
    """

    def __init__(
        self,
        student_id: str,
        full_name: str,
        major: str,
        gpa: float = 0.0,
        fee_per_credit: float = 800_000.0,
        research_fee: float = 500_000.0,
        credits: int = 0,
        scholarship_rate: float = 0.0,
    ) -> None:
        super().__init__(student_id, full_name, major, gpa)
        if fee_per_credit < 0 or research_fee < 0:
            raise ValueError("Phí không được âm")
        if not (0.0 <= scholarship_rate <= 1.0):
            raise ValueError("scholarship_rate phải trong [0, 1]")
        self._fee_per_credit = float(fee_per_credit)
        self._research_fee = float(research_fee)
        self._credits = int(credits)
        self._scholarship_rate = float(scholarship_rate)

    @property
    def credits(self) -> int:
        return self._credits

    @credits.setter
    def credits(self, value: int) -> None:
        if int(value) < 0:
            raise ValueError("Số tín chỉ không được âm")
        self._credits = int(value)

    @property
    def fee_per_credit(self) -> float:
        return self._fee_per_credit

    @fee_per_credit.setter
    def fee_per_credit(self, value: float) -> None:
        if float(value) < 0:
            raise ValueError("Phí/tín chỉ không được âm")
        self._fee_per_credit = float(value)

    @property
    def research_fee(self) -> float:
        return self._research_fee

    @research_fee.setter
    def research_fee(self, value: float) -> None:
        if float(value) < 0:
            raise ValueError("Phí nghiên cứu không được âm")
        self._research_fee = float(value)

    @property
    def scholarship_rate(self) -> float:
        return self._scholarship_rate

    @scholarship_rate.setter
    def scholarship_rate(self, value: float) -> None:
        value_f = float(value)
        if not (0.0 <= value_f <= 1.0):
            raise ValueError("scholarship_rate phải trong [0, 1]")
        self._scholarship_rate = value_f

    def enroll(self, more_credits: int) -> None:
        if more_credits < 0:
            raise ValueError("Số tín chỉ không được âm")
        self._credits += int(more_credits)

    def reset_credits(self) -> None:
        self._credits = 0

    def calculate_tuition(self) -> float:
        gross = self._fee_per_credit * self._credits + self._research_fee
        return gross * (1.0 - self._scholarship_rate)