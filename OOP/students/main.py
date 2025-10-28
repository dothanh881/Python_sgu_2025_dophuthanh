from __future__ import annotations

import sys

import os
from .data.repository import StudentRepository
from .services.student_service import StudentService


def print_menu() -> None:
    print("\n=== Quản lý Sinh viên ===")
    print("1) Thêm SV đại học")
    print("2) Thêm SV cao học")
    print("3) Liệt kê tất cả ")
    print("4) Tìm theo chuyên ngành ")
    print("5) Sửa thông tin SV")
    print("6) Xoá SV theo ID")
    print("7) Lưu danh sách ra CSV")
    print("8) Đọc danh sách từ CSV")
    print("0) Thoát")


def main() -> None:
    repo = StudentRepository()
    service = StudentService(repo)

    while True:
        print_menu()
        choice = input("Chọn chức năng: ").strip()
        try:
            if choice == "0":
                print("Tạm biệt!")
                break
            elif choice == "1":
                add_undergrad(service)
            elif choice == "2":
                add_grad(service)
            elif choice == "3":
                show_table_current(service)
            elif choice == "4":
                show_table_by_major(service)
            elif choice == "5":
                edit_student(service)
            elif choice == "6":
                remove_student(service)
            elif choice == "7":
                save_csv(service)
            elif choice == "8":
                load_csv(service)
            else:
                print("Lựa chọn không hợp lệ.")
        except Exception as e:
            print(f"Lỗi: {e}")


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


# Lược bỏ thêm SV trao đổi để đơn giản hoá.


def list_all(service: StudentService) -> None:
    for s in service.list_all():
        print(s)


def show_table_by_major(service: StudentService) -> None:
    major = input("Major: ").strip()
    results = service.list_by_major(major)
    if not results:
        print("Không có sinh viên thuộc major này.")
        return
    # In bảng riêng cho kết quả lọc
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
        "Tuition",
    ]
    def fmt_money(x):
        try:
            return f"{float(x):,.0f}"
        except Exception:
            return ""
    rows = []
    for s in results:
        role = "Undergraduate" if s.__class__.__name__ == "UndergraduateStudent" else "Graduate"
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


# Lược bỏ ghi danh tín chỉ để đơn giản.


def update_gpa(service: StudentService) -> None:
    sid = input("ID: ").strip()
    gpa = float(input("GPA mới [0-4]: ") or 0.0)
    service.update_gpa(sid, gpa)
    print("Đã cập nhật GPA.")


# Có thể tính học phí từng SV khi hiển thị bảng, lược bỏ menu riêng.


# Lược bỏ tổng học phí.


def remove_student(service: StudentService) -> None:
    sid = input("ID: ").strip()
    ok = service.remove(sid)
    print("Đã xoá." if ok else "Không tìm thấy.")

def edit_student(service: StudentService) -> None:
    sid = input("ID cần sửa: ").strip()
    s = service._repo.get(sid)
    if s is None:
        print("Không tìm thấy.")
        return
    print(f"Đang sửa: {s}")
    # chung
    name = input(f"Họ tên ({s.full_name}): ").strip() or s.full_name
    major = input(f"Chuyên ngành ({s.major}): ").strip() or s.major
    gpa_in = input(f"GPA ({s.gpa:.2f}) [0-4]: ").strip()
    gpa = float(gpa_in) if gpa_in != "" else s.gpa

    # chuyên biệt
    fee_per_credit = activity_fee = credits = None
    research_fee = scholarship_rate = None
    if s.__class__.__name__ == "UndergraduateStudent":
        fee_per_credit_in = input(f"Phí/tín chỉ ({s.fee_per_credit}): ").strip()
        activity_fee_in = input(f"Phí hoạt động ({s.activity_fee}): ").strip()
        credits_in = input(f"Tín chỉ ({s.credits}): ").strip()
        fee_per_credit = float(fee_per_credit_in) if fee_per_credit_in != "" else s.fee_per_credit
        activity_fee = float(activity_fee_in) if activity_fee_in != "" else s.activity_fee
        credits = int(credits_in) if credits_in != "" else s.credits
    else:
        fee_per_credit_in = input(f"Phí/tín chỉ ({getattr(s,'fee_per_credit','')}): ").strip()
        research_fee_in = input(f"Phí nghiên cứu ({getattr(s,'research_fee','')}): ").strip()
        credits_in = input(f"Tín chỉ ({getattr(s,'credits','')}): ").strip()
        scholarship_in = input(f"Học bổng [0-1] ({getattr(s,'scholarship_rate','')}): ").strip()
        fee_per_credit = float(fee_per_credit_in) if fee_per_credit_in != "" else getattr(s,'fee_per_credit','')
        research_fee = float(research_fee_in) if research_fee_in != "" else getattr(s,'research_fee','')
        credits = int(credits_in) if credits_in != "" else getattr(s,'credits','')
        scholarship_rate = float(scholarship_in) if scholarship_in != "" else getattr(s,'scholarship_rate','')

    updated = service.edit_student(
        student_id=sid,
        full_name=name,
        major=major,
        gpa=gpa,
        fee_per_credit=fee_per_credit,
        activity_fee=activity_fee,
        credits=credits,
        research_fee=research_fee,
        scholarship_rate=scholarship_rate,
    )
    print("Đã cập nhật:", updated)


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
        "Tuition",
    ]

    rows = []
    for s in students:
        if s.__class__.__name__ == "UndergraduateStudent":
            role = "Undergraduate"
        elif s.__class__.__name__ == "GraduateStudent":
            role = "Graduate"
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


# Lược bỏ hiển thị CSV bất kỳ để đơn giản hoá.


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nThoát.")
        sys.exit(0)