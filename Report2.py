import tkinter as tk
from tkinter import ttk, messagebox
from copy import deepcopy
import random

A = [1, 2, 3, 4, 5]

# ---------------------------
# 관계 판별 함수들
# ---------------------------
def is_reflexive(R):
    return all(R[i][i] == 1 for i in range(5))

def is_symmetric(R):
    return all(R[i][j] == R[j][i] for i in range(5) for j in range(5))

def is_transitive(R):
    for i in range(5):
        for j in range(5):
            if R[i][j]:
                for k in range(5):
                    if R[j][k] and not R[i][k]:
                        return False
    return True

def reflexive_closure(R):
    new_R = deepcopy(R)
    for i in range(5):
        new_R[i][i] = 1
    return new_R

def symmetric_closure(R):
    new_R = deepcopy(R)
    for i in range(5):
        for j in range(5):
            if R[i][j] == 1:
                new_R[j][i] = 1
    return new_R

def transitive_closure(R):
    new_R = deepcopy(R)
    for k in range(5):
        for i in range(5):
            for j in range(5):
                new_R[i][j] = new_R[i][j] or (new_R[i][k] and new_R[k][j])
    return new_R

def equivalence_classes(R):
    classes = []
    visited = set()
    for i in range(5):
        if A[i] not in visited:
            eq_class = {A[j] for j in range(5) if R[i][j] == 1}
            classes.append(eq_class)
            visited.update(eq_class)
    return classes

# ---------------------------
# Tkinter GUI 설정
# ---------------------------
root = tk.Tk()
root.title("동치 관계 판별 프로그램")
root.configure(bg="#eef6f9")

style = ttk.Style()
style.theme_use("clam")
style.configure("Pink.TButton",
                font=("Apple SD Gothic Neo", 11, "bold"),
                padding=6,
                background="#F48FB1",
                foreground="white")
style.map("Pink.TButton",
          background=[("active", "#F06292")])

# ---------------------------
# GUI Layout
# ---------------------------
top_frame = tk.Frame(root, bg="#eef6f9")
top_frame.pack(pady=15)

tk.Label(top_frame, text="5×5 관계 행렬 입력", font=("Apple SD Gothic Neo", 12, "bold"), bg="#eef6f9").pack(side="left", padx=5)

btn_check = ttk.Button(top_frame, text="관계 판별", style="Pink.TButton")
btn_check.pack(side="left", padx=8)
btn_closure = ttk.Button(top_frame, text="폐포 변환", style="Pink.TButton")
btn_closure.pack(side="left", padx=8)
btn_transitive_only = ttk.Button(top_frame, text="추이 폐포만", style="Pink.TButton")
btn_transitive_only.pack(side="left", padx=8)
btn_clear = ttk.Button(top_frame, text="초기화", style="Pink.TButton")
btn_clear.pack(side="left", padx=8)
btn_random = ttk.Button(top_frame, text="랜덤 생성", style="Pink.TButton")
btn_random.pack(side="left", padx=8)

matrix_frame = tk.Frame(root, bg="#eef6f9")
matrix_frame.pack(pady=10)

result_frame = tk.Frame(root, bg="#eef6f9")
result_frame.pack(pady=15, fill="both", expand=True)

matrix_entries = []
for i in range(5):
    row_entries = []
    for j in range(5):
        e = tk.Entry(matrix_frame, width=5, font=("Apple SD Gothic Neo", 12), justify="center", bg="white")
        e.grid(row=i, column=j, padx=3, pady=3)
        row_entries.append(e)
    matrix_entries.append(row_entries)

def get_matrix():
    R = []
    for i in range(5):
        row = []
        for j in range(5):
            val = matrix_entries[i][j].get().strip()
            if val == "":
                messagebox.showwarning("입력 오류", "모든 칸에 값을 입력하세요.")
                return None
            row.append(int(val))
        R.append(row)
    return R

def display_matrix(mat, title):
    frame = tk.Frame(result_frame, bg="white", bd=1, relief="solid")
    frame.pack(padx=5, pady=5)
    tk.Label(frame, text=title, font=("Apple SD Gothic Neo", 10, "bold"), bg="white").pack()
    grid = tk.Frame(frame, bg="white")
    grid.pack(pady=5)
    for i in range(5):
        for j in range(5):
            tk.Label(grid, text=str(mat[i][j]), width=4, font=("Apple SD Gothic Neo", 12),
                     relief="ridge", bg="#fdfdfd").grid(row=i, column=j, padx=1, pady=1)

def display_matrix_in_center(parent, mat, title):
    frame = tk.Frame(parent, bg="white", bd=1, relief="solid")
    frame.pack(padx=5, pady=5, anchor="center")
    tk.Label(frame, text=title,
             font=("Apple SD Gothic Neo", 10, "bold"),
             bg="white").pack(pady=3, anchor="center")
    grid = tk.Frame(frame, bg="white")
    grid.pack(pady=5)
    for i in range(5):
        for j in range(5):
            tk.Label(grid, text=str(mat[i][j]), width=4, font=("Apple SD Gothic Neo", 12),
                     relief="ridge", bg="#fdfdfd").grid(row=i, column=j, padx=1, pady=1)

def clear_results():
    for w in result_frame.winfo_children():
        w.destroy()

def random_relation():
    for i in range(5):
        for j in range(5):
            matrix_entries[i][j].delete(0, tk.END)
            matrix_entries[i][j].insert(0, str(random.randint(0, 1)))
    clear_results()
    messagebox.showinfo("랜덤 행렬 생성 완료", "무작위 관계 행렬이 생성되었습니다!")

def check_relation():
    R = get_matrix()
    if R is None: return
    clear_results()
    reflexive = is_reflexive(R)
    symmetric = is_symmetric(R)
    transitive = is_transitive(R)

    text = f"반사적: {reflexive}\n대칭적: {symmetric}\n추이적: {transitive}"
    label = tk.Label(result_frame, text=text, font=("Apple SD Gothic Neo", 12, "bold"), bg="#eef6f9", fg="#333")
    label.pack(pady=5)

    if reflexive and symmetric and transitive:
        tk.Label(result_frame, text="✅ 이 관계는 동치 관계입니다!", fg="green",
                 font=("Apple SD Gothic Neo", 10, "bold"), bg="#eef6f9").pack()
        classes = equivalence_classes(R)
        for i, eq in enumerate(classes):
            tk.Label(result_frame, text=f"{A[i]}의 동치류: {eq}",
                     font=("Apple SD Gothic Neo", 11), bg="#eef6f9").pack()
    else:
        tk.Label(result_frame, text="❌ 동치 관계가 아닙니다.", fg="red",
                 font=("Apple SD Gothic Neo", 10, "bold"), bg="#eef6f9").pack()

def closure_transform():
    R = get_matrix()
    if R is None:
        return
    clear_results()

    outer_canvas = tk.Canvas(result_frame, bg="#eef6f9", highlightthickness=0)
    outer_canvas.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=outer_canvas.yview)
    scrollbar.pack(side="right", fill="y")

    outer_wrapper = tk.Frame(outer_canvas, bg="#eef6f9")
    outer_canvas.create_window((0, 0), window=outer_wrapper, anchor="n")
    inner_frame = tk.Frame(outer_wrapper, bg="#eef6f9")
    inner_frame.pack(anchor="center")

    def on_configure(event):
        outer_canvas.configure(scrollregion=outer_canvas.bbox("all"))
        outer_canvas.itemconfig("all", width=outer_canvas.winfo_width())

    outer_wrapper.bind("<Configure>", on_configure)
    outer_canvas.configure(yscrollcommand=scrollbar.set)

    # ---------------------------
    # 폐포 변환 단계별 출력
    # ---------------------------
    display_matrix_in_center(inner_frame, R, "입력 관계행렬 (Before)")

    if not is_reflexive(R):
        R = reflexive_closure(R)
        display_matrix_in_center(inner_frame, R, "반사 폐포 적용 (Reflexive Closure)")
    if not is_symmetric(R):
        R = symmetric_closure(R)
        display_matrix_in_center(inner_frame, R, "대칭 폐포 적용 (Symmetric Closure)")
    if not is_transitive(R):
        R = transitive_closure(R)
        display_matrix_in_center(inner_frame, R, "추이 폐포 적용 (Transitive Closure)")

    tk.Label(inner_frame, text="변환 후 관계행렬 (After)",
             font=("Apple SD Gothic Neo", 10, "bold"),
             bg="#eef6f9").pack(pady=5)

    display_matrix_in_center(inner_frame, R, "최종 폐포")

    if is_reflexive(R) and is_symmetric(R) and is_transitive(R):
        tk.Label(inner_frame, text="✅ 폐포 적용 후 동치 관계입니다.",
                 fg="green", font=("Apple SD Gothic Neo", 10, "bold"),
                 bg="#eef6f9").pack(pady=5)
        classes = equivalence_classes(R)
        for i, eq in enumerate(classes):
            tk.Label(inner_frame, text=f"{A[i]}의 동치류: {eq}",
                     font=("Apple SD Gothic Neo", 11),
                     bg="#eef6f9").pack()
    else:
        tk.Label(inner_frame, text="❌ 폐포 적용 후에도 동치 관계가 아닙니다.",
                 fg="red", font=("Apple SD Gothic Neo", 10, "bold"),
                 bg="#eef6f9").pack(pady=5)


def show_transitive_closure():
    R = get_matrix()
    if R is None:
        return
    clear_results()
    display_matrix(R, "입력 관계행렬 (R)")
    if is_transitive(R):
        tk.Label(result_frame, text="이미 추이적 관계입니다.",
                 font=("Apple SD Gothic Neo", 11, "bold"),
                 bg="#eef6f9", fg="green").pack(pady=5)
    else:
        R_plus = transitive_closure(R)
        display_matrix(R_plus, "추이 폐포 (R⁺)")
        tk.Label(result_frame, text="✅ 추이 폐포 R⁺가 계산되었습니다.",
                 font=("Apple SD Gothic Neo", 11, "bold"),
                 bg="#eef6f9", fg="blue").pack(pady=5)

def reset_matrix():
    for i in range(5):
        for j in range(5):
            matrix_entries[i][j].delete(0, tk.END)
    clear_results()

# ---------------------------
# 버튼 연결
# ---------------------------
btn_check.config(command=check_relation)
btn_closure.config(command=closure_transform)
btn_clear.config(command=reset_matrix)
btn_random.config(command=random_relation)
btn_transitive_only.config(command=show_transitive_closure)

root.mainloop()
