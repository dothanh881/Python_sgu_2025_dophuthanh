from __future__ import annotations

from typing import List, Optional, Type

from ..models import (
    Student,
    UndergraduateStudent,
    GraduateStudent,
    ExchangeStudent,
)
from ..data.repository import StudentRepository


class StudentService:
    """Lớp nghiệp vụ quản lý sinh viên.

    - Điều phối tạo sinh viên theo loại (kế thừa/đa hình).
    - Áp dụng quy tắc nghiệp vụ (ví dụ cập nhật GPA, ghi danh tín chỉ).
    """

    def __init__(self, repo: StudentRepository) -> None:
        self._repo = repo

    # Đăng ký sinh viên theo loại
    def register_undergrad(
        self,
        student_id: str,
        full_name: str,
        major: str,
        fee_per_credit: float = 500_000.0,
        activity_fee: float = 200_000.0,
        credits: int = 0,
        gpa: float = 0.0,
    ) -> UndergraduateStudent:
        s = UndergraduateStudent(
            student_id=student_id,
            full_name=full_name,
            major=major,
            gpa=gpa,
            fee_per_credit=fee_per_credit,
            activity_fee=activity_fee,
            credits=credits,
        )
        self._repo.add(s)
        return s

    def register_grad(
        self,
        student_id: str,
        full_name: str,
        major: str,
        fee_per_credit: float = 800_000.0,
        research_fee: float = 500_000.0,
        credits: int = 0,
        scholarship_rate: float = 0.0,
        gpa: float = 0.0,
    ) -> GraduateStudent:
        s = GraduateStudent(
            student_id=student_id,
            full_name=full_name,
            major=major,
            gpa=gpa,
            fee_per_credit=fee_per_credit,
            research_fee=research_fee,
            credits=credits,
            scholarship_rate=scholarship_rate,
        )
        self._repo.add(s)
        return s

    def register_exchange(
        self,
        student_id: str,
        full_name: str,
        major: str,
        program_fee: float = 5_000_000.0,
        gpa: float = 0.0,
    ) -> ExchangeStudent:
        s = ExchangeStudent(
            student_id=student_id,
            full_name=full_name,
            major=major,
            gpa=gpa,
            program_fee=program_fee,
        )
        self._repo.add(s)
        return s

    # Tác vụ nghiệp vụ chung
    def enroll_credits(self, student_id: str, more_credits: int) -> None:
        s = self._repo.get(student_id)
        if s is None:
            raise KeyError("Không tìm thấy sinh viên")
        # chỉ áp dụng cho loại có credits
        if hasattr(s, "enroll"):
            getattr(s, "enroll")(more_credits)
        else:
            raise ValueError("Loại sinh viên này không quản lý tín chỉ")

    def update_gpa(self, student_id: str, new_gpa: float) -> None:
        s = self._repo.get(student_id)
        if s is None:
            raise KeyError("Không tìm thấy sinh viên")
        s.update_gpa(new_gpa)

    def compute_tuition(self, student_id: str) -> float:
        s = self._repo.get(student_id)
        if s is None:
            raise KeyError("Không tìm thấy sinh viên")
        return s.calculate_tuition()

    def compute_total_tuition(self) -> float:
        return sum(s.calculate_tuition() for s in self._repo.list_all())

    def list_all(self) -> List[Student]:
        return self._repo.list_all()

    def list_by_major(self, major: str) -> List[Student]:
        return self._repo.list_by_major(major)

    def remove(self, student_id: str) -> bool:
        return self._repo.remove(student_id)

    # CSV persistence
    def save_csv(self, file_path: str) -> int:
        return self._repo.save_csv(file_path)

    def load_csv(self, file_path: str, mode: str = "replace") -> int:
        return self._repo.load_csv(file_path, mode)