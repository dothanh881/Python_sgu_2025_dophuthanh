from __future__ import annotations

from abc import ABC, abstractmethod


class Student(ABC):
    """Lớp trừu tượng mô tả sinh viên chung.

    Thể hiện OOP:
    - Trừu tượng: phương thức `calculate_tuition` bắt buộc lớp con triển khai.
    - Đóng gói: thuộc tính tiền tố `_` và property kiểm soát.
    - Kế thừa/Đa hình: các lớp con thay đổi cách tính học phí.
    """

    def __init__(
        self,
        student_id: str,
        full_name: str,
        major: str,
        gpa: float = 0.0,
    ) -> None:
        if not student_id or not student_id.strip():
            raise ValueError("student_id không hợp lệ")
        if not full_name or not full_name.strip():
            raise ValueError("Tên không được rỗng")
        if not major or not major.strip():
            raise ValueError("major không được rỗng")
        self._id = student_id.strip()
        self._full_name = full_name.strip()
        self._major = major.strip()
        self._gpa = float(gpa)
        self._active = True

    @property
    def id(self) -> str:
        return self._id

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Tên không được rỗng")
        self._full_name = value.strip()

    @property
    def major(self) -> str:
        return self._major

    @major.setter
    def major(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("major không được rỗng")
        self._major = value.strip()

    @property
    def gpa(self) -> float:
        return self._gpa

    def update_gpa(self, new_gpa: float) -> None:
        if not (0.0 <= new_gpa <= 4.0):
            raise ValueError("GPA phải trong khoảng 0.0 - 4.0")
        self._gpa = float(new_gpa)

    @property
    def active(self) -> bool:
        return self._active

    def deactivate(self) -> None:
        self._active = False

    def activate(self) -> None:
        self._active = True

    @property
    def role(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def calculate_tuition(self) -> float:
        """Tính học phí theo loại sinh viên và thông tin lưu trữ."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{self.role} id={self.id} name={self.full_name} major={self.major} gpa={self.gpa}>"