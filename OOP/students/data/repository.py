from __future__ import annotations

from typing import Dict, List, Optional
import csv

from ..models import Student
from ..models import UndergraduateStudent, GraduateStudent


class StudentRepository:
    """Kho dữ liệu sinh viên (in-memory)."""

    def __init__(self) -> None:
        self._students: Dict[str, Student] = {}

    def add(self, student: Student) -> None:
        if student.id in self._students:
            raise ValueError(f"Đã tồn tại sinh viên id={student.id}")
        self._students[student.id] = student

    def get(self, student_id: str) -> Optional[Student]:
        return self._students.get(student_id)

    def remove(self, student_id: str) -> bool:
        return self._students.pop(student_id, None) is not None

    def list_all(self) -> List[Student]:
        return list(self._students.values())

    def list_by_major(self, major: str) -> List[Student]:
        return [s for s in self._students.values() if s.major == major]

    def clear(self) -> None:
        self._students.clear()

    # CSV Persistence
    def save_csv(self, file_path: str) -> int:
        """Ghi toàn bộ danh sách sinh viên ra file CSV.

        Trả về số bản ghi đã ghi.
        """
        headers = [
            "id",
            "full_name",
            "major",
            "gpa",
            "role",
            "fee_per_credit",
            "activity_fee",
            "credits",
            "research_fee",
            "scholarship_rate",
        ]

        rows: List[Dict[str, str]] = []
        for s in self.list_all():
            base = {
                "id": s.id,
                "full_name": s.full_name,
                "major": s.major,
                "gpa": f"{s.gpa}",
                "role": "",
                "fee_per_credit": "",
                "activity_fee": "",
                "credits": "",
                "research_fee": "",
                "scholarship_rate": "",
            }
            if isinstance(s, UndergraduateStudent):
                base["role"] = "Undergraduate"
                base["fee_per_credit"] = f"{s.fee_per_credit}"
                base["activity_fee"] = f"{s.activity_fee}"
                base["credits"] = f"{s.credits}"
            elif isinstance(s, GraduateStudent):
                base["role"] = "Graduate"
                base["fee_per_credit"] = f"{s.fee_per_credit}"
                base["research_fee"] = f"{s.research_fee}"
                base["credits"] = f"{s.credits}"
                base["scholarship_rate"] = f"{s.scholarship_rate}"
            else:
                base["role"] = s.__class__.__name__

            rows.append(base)

        with open(file_path, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

        return len(rows)

    def load_csv(self, file_path: str, mode: str = "replace") -> int:
        """Đọc danh sách sinh viên từ file CSV.

        - mode="replace": xóa hết dữ liệu hiện tại rồi nạp mới.
        - mode="append": giữ lại dữ liệu cũ, thêm dữ liệu mới (bỏ qua id trùng).

        Trả về số bản ghi đã nạp.
        """
        def parse_float(v: str, default: float = 0.0) -> float:
            try:
                return float(v) if v not in (None, "") else default
            except ValueError:
                return default

        def parse_int(v: str, default: int = 0) -> int:
            try:
                return int(float(v)) if v not in (None, "") else default
            except ValueError:
                return default

        count = 0
        if mode == "replace":
            self.clear()

        with open(file_path, mode="r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                role = (row.get("role") or "").strip()
                student_id = (row.get("id") or "").strip()
                full_name = (row.get("full_name") or "").strip()
                major = (row.get("major") or "").strip()
                gpa = parse_float(row.get("gpa"))

                if not student_id or not full_name:
                    continue

                try:
                    if role == "Undergraduate":
                        s = UndergraduateStudent(
                            student_id=student_id,
                            full_name=full_name,
                            major=major,
                            gpa=gpa,
                            fee_per_credit=parse_float(row.get("fee_per_credit")),
                            activity_fee=parse_float(row.get("activity_fee")),
                            credits=parse_int(row.get("credits")),
                        )
                    elif role == "Graduate":
                        s = GraduateStudent(
                            student_id=student_id,
                            full_name=full_name,
                            major=major,
                            gpa=gpa,
                            fee_per_credit=parse_float(row.get("fee_per_credit")),
                            research_fee=parse_float(row.get("research_fee")),
                            credits=parse_int(row.get("credits")),
                            scholarship_rate=parse_float(row.get("scholarship_rate")),
                        )
                    else:
                        # Không rõ role -> bỏ qua.
                        continue

                    if mode == "append" and self.get(s.id):
                        continue
                    self.add(s)
                    count += 1
                except Exception:
                    # Bỏ qua dòng lỗi.
                    continue

        return count