from __future__ import annotations

from typing import List, Optional, Type

from ..models import (
    Student,
    UndergraduateStudent,
    GraduateStudent,
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

    # Loại ExchangeStudent đã được lược bỏ để đơn giản hoá.

    # Tác vụ nghiệp vụ chung
    # Lược bỏ chức năng ghi danh tín chỉ để đơn giản hoá.

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

    # Lược bỏ tổng học phí để đơn giản hoá.

    def list_all(self) -> List[Student]:
        return self._repo.list_all()

    def list_by_major(self, major: str) -> List[Student]:
        return self._repo.list_by_major(major)

    def remove(self, student_id: str) -> bool:
        return self._repo.remove(student_id)

    def edit_student(
        self,
        student_id: str,
        full_name: Optional[str] = None,
        major: Optional[str] = None,
        gpa: Optional[float] = None,
        # Undergraduate
        fee_per_credit: Optional[float] = None,
        activity_fee: Optional[float] = None,
        credits: Optional[int] = None,
        # Graduate
        research_fee: Optional[float] = None,
        scholarship_rate: Optional[float] = None,
    ) -> Student:
        s = self._repo.get(student_id)
        if s is None:
            raise KeyError("Không tìm thấy sinh viên")

        # chung
        if full_name is not None:
            s.full_name = str(full_name)
        if major is not None:
            s.major = str(major)
        if gpa is not None:
            s.update_gpa(float(gpa))

        # chuyên biệt
        if isinstance(s, UndergraduateStudent):
            if fee_per_credit is not None:
                s.fee_per_credit = float(fee_per_credit)
            if activity_fee is not None:
                s.activity_fee = float(activity_fee)
            if credits is not None:
                s.credits = int(credits)
        elif isinstance(s, GraduateStudent):
            if fee_per_credit is not None:
                s.fee_per_credit = float(fee_per_credit)
            if research_fee is not None:
                s.research_fee = float(research_fee)
            if credits is not None:
                s.credits = int(credits)
            if scholarship_rate is not None:
                s.scholarship_rate = float(scholarship_rate)

        return s

    # CSV persistence
    def save_csv(self, file_path: str) -> int:
        return self._repo.save_csv(file_path)

    def load_csv(self, file_path: str, mode: str = "replace") -> int:
        return self._repo.load_csv(file_path, mode)