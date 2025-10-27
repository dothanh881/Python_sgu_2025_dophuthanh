from __future__ import annotations

import sys

import os
import csv
from .data.repository import StudentRepository
from .services.student_service import StudentService


def print_menu() -> None:
    print("\n=== Quản lý Sinh viên (3 lớp) ===")
    print("1) Thêm SV đại học")
    print("2) Thêm SV cao học")
    print("3) Thêm SV trao đổi")
    print("4) Liệt kê tất cả")
    print("5) Tìm theo chuyên ngành (major)")
    print("6) Ghi danh thêm tín chỉ")
    print("7) Cập nhật GPA")
    print("8) Tính học phí SV")
    print("9) Tổng học phí tất cả")
    print("10) Xoá SV theo ID")
    print("11) Lưu danh sách ra CSV")
    print("12) Đọc danh sách từ CSV")
    print("13) Nạp dataset mẫu")
    print("14) Hiển thị danh sách hiện tại dạng bảng")
    print("15) Hiển thị CSV bất kỳ dạng bảng")
    print("0) Thoát")


def main() -> None:
    repo = StudentRepository()
    service = StudentService(repo)

    actions = {
        "1": lambda: add_undergrad(service),
        "2": lambda: add_grad(service),
        "3": lambda: add_exchange(service),
        "4": lambda: list_all(service),
        "5": lambda: list_by_major(service),
        "6": lambda: enroll_credits(service),
        "7": lambda: update_gpa(service),
        "8": lambda: compute_tuition(service),
        "9": lambda: compute_total_tuition(service),
        "10": lambda: remove_student(service),
        "11": lambda: save_csv(service),
        "12": lambda: load_csv(service),
        "13": lambda: load_sample(service),
        "14": lambda: show_table_current(service),
        "15": lambda: show_csv_table(),
    }

    while True:
        print_menu()
        choice = input("Chọn chức năng: ").strip()
        if choice == "0":
            print("Tạm biệt!")
            break
        action = actions.get(choice)
        if action:
            try:
                action()
            except Exception as e:
                print(f"Lỗi: {e}")
        else:
            print("Lựa chọn không hợp lệ.")


def add_undergrad(service: StudentService) -> None:
    sid = input("ID: ").strip()
    name = input("Họ tên: ").strip()
    major = input("Chuyên ngành: ").strip()
    fee = float(input("Phí/tín chỉ (mặc định 500000): ") or 500000)
    act = float(input("Phí hoạt động (mặc định 200000): ") or 200000)
    credits = int(input("Số tín chỉ ban đầu (mặc định 0): ") or 0)
    s = service.register_undergrad(sid, name, major, fee, act, credits)
    print("Đã thêm:", s)


def add_grad(service: StudentService) -> None:
    sid = input("ID: ").strip()
    name = input("Họ tên: ").strip()
    major = input("Chuyên ngành: ").strip()
    fee = float(input("Phí/tín chỉ (mặc định 800000): ") or 800000)
    research = float(input("Phí nghiên cứu (mặc định 500000): ") or 500000)
    credits = int(input("Số tín chỉ ban đầu (mặc định 0): ") or 0)
    scholarship = float(input("Tỉ lệ học bổng [0-1] (mặc định 0): ") or 0.0)
    s = service.register_grad(sid, name, major, fee, research, credits, scholarship)
    print("Đã thêm:", s)


def add_exchange(service: StudentService) -> None:
    sid = input("ID: ").strip()
    name = input("Họ tên: ").strip()
    major = input("Chuyên ngành: ").strip()
    program_fee = float(input("Học phí chương trình (mặc định 5000000): ") or 5000000)
    s = service.register_exchange(sid, name, major, program_fee)
    print("Đã thêm:", s)


def list_all(service: StudentService) -> None:
    for s in service.list_all():
        print(s)


def list_by_major(service: StudentService) -> None:
    major = input("Major: ").strip()
    results = service.list_by_major(major)
    if not results:
        print("Không có sinh viên thuộc major này.")
    else:
        for s in results:
            print(s)


def enroll_credits(service: StudentService) -> None:
    sid = input("ID: ").strip()
    more = int(input("Thêm tín chỉ: ") or 0)
    service.enroll_credits(sid, more)
    print("Đã ghi danh tín chỉ.")


def update_gpa(service: StudentService) -> None:
    sid = input("ID: ").strip()
    gpa = float(input("GPA mới [0-4]: ") or 0.0)
    service.update_gpa(sid, gpa)
    print("Đã cập nhật GPA.")


def compute_tuition(service: StudentService) -> None:
    sid = input("ID: ").strip()
    fee = service.compute_tuition(sid)
    print(f"Học phí: {fee:,.0f}")


def compute_total_tuition(service: StudentService) -> None:
    total = service.compute_total_tuition()
    print(f"Tổng học phí tất cả: {total:,.0f}")


def remove_student(service: StudentService) -> None:
    sid = input("ID: ").strip()
    ok = service.remove(sid)
    print("Đã xoá." if ok else "Không tìm thấy.")


def save_csv(service: StudentService) -> None:
    default_path = os.path.join("OOP", "students", "datasets", "students_out.csv")
    path = input(f"Đường dẫn file CSV (mặc định {default_path}): ") or default_path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    count = service.save_csv(path)
    print(f"Đã lưu {count} sinh viên vào '{path}'.")


def load_csv(service: StudentService) -> None:
    default_path = os.path.join("OOP", "students", "datasets", "students_sample.csv")
    path = input(f"Đường dẫn file CSV (mặc định {default_path}): ") or default_path
    mode = (input("Chế độ [replace/append] (mặc định replace): ").strip().lower() or "replace")
    if mode not in {"replace", "append"}:
        mode = "replace"
    count = service.load_csv(path, mode)
    print(f"Đã nạp {count} sinh viên từ '{path}' với chế độ {mode}.")


def load_sample(service: StudentService) -> None:
    path = os.path.join("OOP", "students", "datasets", "students_sample.csv")
    count = service.load_csv(path, mode="replace")
    print(f"Đã nạp dataset mẫu: {count} sinh viên từ '{path}'.")


def show_table_current(service: StudentService) -> None:
    students = service.list_all()
    if not students:
        print("Danh sách trống. Hãy nạp hoặc thêm sinh viên trước.")
        return

    headers = [
        "ID",
        "Họ tên",
        "Major",
        "GPA",
        "Loại",
        "Credits",
        "Fee/Credit",
        "ActivityFee",
        "ResearchFee",
        "Scholarship",
        "ProgramFee",
        "Tuition",
    ]

    rows = []
    for s in students:
        if s.__class__.__name__ == "UndergraduateStudent":
            role = "Undergraduate"
        elif s.__class__.__name__ == "GraduateStudent":
            role = "Graduate"
        elif s.__class__.__name__ == "ExchangeStudent":
            role = "Exchange"
        else:
            role = s.__class__.__name__

        def fmt_money(x):
            try:
                return f"{float(x):,.0f}"
            except Exception:
                return ""

        rows.append([
            s.id,
            s.full_name,
            s.major,
            f"{s.gpa:.2f}",
            role,
            str(getattr(s, "credits", "")),
            fmt_money(getattr(s, "fee_per_credit", "")),
            fmt_money(getattr(s, "activity_fee", "")),
            fmt_money(getattr(s, "research_fee", "")),
            (
                f"{getattr(s, 'scholarship_rate', ''):.2f}"
                if hasattr(s, "scholarship_rate")
                else ""
            ),
            fmt_money(getattr(s, "program_fee", "")),
            fmt_money(s.calculate_tuition()),
        ])

    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    def print_row(cells):
        print(" | ".join(str(cells[i]).ljust(widths[i]) for i in range(len(headers))))

    print_row(headers)
    print("-" * (sum(widths) + 3 * (len(headers) - 1)))
    for row in rows:
        print_row(row)


def show_csv_table() -> None:
    default_path = os.path.join("OOP", "students", "datasets", "students_sample.csv")
    path = input(f"Đường dẫn CSV để hiển thị (mặc định {default_path}): ") or default_path
    if not os.path.exists(path):
        print(f"Không tìm thấy file: {path}")
        return

    with open(path, mode="r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = [row for row in reader]

    if not headers or not rows:
        print("File CSV rỗng hoặc không có header.")
        return

    widths = [len(h) for h in headers]
    for row in rows:
        for i, h in enumerate(headers):
            widths[i] = max(widths[i], len(str(row.get(h, ""))))

    def print_row_dict(row_dict):
        print(" | ".join(str(row_dict.get(h, "")).ljust(widths[i]) for i, h in enumerate(headers)))

    print(" | ".join(h.ljust(widths[i]) for i, h in enumerate(headers)))
    print("-" * (sum(widths) + 3 * (len(headers) - 1)))
    for row in rows:
        print_row_dict(row)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nThoát.")
        sys.exit(0)