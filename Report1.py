import tkinter as tk
from tkinter import ttk, messagebox
from copy import deepcopy

def pretty_two_matrices(A, I):
    n = len(A)
    lines = []
    for i in range(n):
        if i == 0:
            lA = "⎡ " + "   ".join(f"{x:6.2f}" for x in A[i]) + " ⎤"
            lI = "⎡ " + "   ".join(f"{x:6.2f}" for x in I[i]) + " ⎤"
        elif i == n-1:
            lA = "⎣ " + "   ".join(f"{x:6.2f}" for x in A[i]) + " ⎦"
            lI = "⎣ " + "   ".join(f"{x:6.2f}" for x in I[i]) + " ⎦"
        else:
            lA = "⎢ " + "   ".join(f"{x:6.2f}" for x in A[i]) + " ⎥"
            lI = "⎢ " + "   ".join(f"{x:6.2f}" for x in I[i]) + " ⎥"
        lines.append(f"{lA}     {lI}")
    return "\n".join(lines)

# ---------------------------
# 행렬식 계산 
# ---------------------------

def pretty_matrix(M):
    n = len(M)
    lines = []
    for i in range(n):
        if i == 0:
            line = "⎡ " + "   ".join(f"{x:6.2f}" for x in M[i]) + " ⎤"
        elif i == n-1:
            line = "⎣ " + "   ".join(f"{x:6.2f}" for x in M[i]) + " ⎦"
        else:
            line = "⎢ " + "   ".join(f"{x:6.2f}" for x in M[i]) + " ⎥"
        lines.append(line)
    return "\n".join(lines)

def determinant_with_steps(matrix, depth=0):
    n = len(matrix)
    indent = "  " * depth
    if n == 1:
        return matrix[0][0], f"{indent}det(\n{pretty_matrix(matrix)}\n) = {matrix[0][0]:.2f}\n"
    if n == 2:
        val = matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
        log = (f"{indent}det(\n{pretty_matrix(matrix)}\n{indent})\n"
       f"{indent}= {matrix[0][0]}×{matrix[1][1]} - {matrix[0][1]}×{matrix[1][0]} "
       f"= {val:.2f}\n")
        return val, log

    det_val = 0
    log = f"{indent}det({n}×{n} 행렬)\n{pretty_matrix(matrix)}\n"

    superscripts = {0:"⁰", 1:"¹", 2:"²", 3:"³", 4:"⁴",
                5:"⁵", 6:"⁶", 7:"⁷", 8:"⁸", 9:"⁹"}
    for c in range(n):
        minor = [row[:c] + row[c+1:] for row in matrix[1:]]
        sub_val, sub_log = determinant_with_steps(minor, depth+1)
        term = ((-1)**c) * matrix[0][c] * sub_val
        det_val += term
        exp = superscripts.get(c, f"^{c}")   
        log += (f"{indent}{matrix[0][c]:.2f} × det(\n"
            f"{pretty_matrix(minor)}\n"
            f"{indent}) × (−1){exp} → {term:.2f}\n")

        log += sub_log
    log += f"{indent}=> det = {det_val:.2f}\n"
    return det_val, log

# ---------------------------
# 역행렬 계산 (가우스 소거법)
# ---------------------------
def gauss_elimination_inverse(matrix):
    n = len(matrix)
    A = deepcopy(matrix)
    I = [[float(i == j) for j in range(n)] for i in range(n)]
    logs = []
    logs.append("초기 상태 \n" + pretty_two_matrices(A, I))

    for i in range(n):
        if A[i][i] == 0:
            for j in range(i+1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    I[i], I[j] = I[j], I[i]
                    logs.append(f"\n행 {i} ↔ 행 {j} 교환 \n{pretty_two_matrices(A,I)}")
                    break
            else:
                raise ValueError("역행렬 불가: 행렬식이 0입니다.")
        pivot = A[i][i]
        for k in range(n):
            A[i][k] /= pivot
            I[i][k] /= pivot
        logs.append(f"\n행 {i}를 피벗 {pivot:.2f}로 나눔 \n{pretty_two_matrices(A,I)}")

        for j in range(i+1, n):
            factor = A[j][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
                I[j][k] -= factor * I[i][k]
            logs.append(f"\n행 {j}에서 {factor:.2f} × 행 {i} 빼기 \n{pretty_two_matrices(A,I)}")

    for i in range(n-1, -1, -1):
        for j in range(i-1, -1, -1):
            factor = A[j][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
                I[j][k] -= factor * I[i][k]
            logs.append(f"\n행 {j}에서 {factor:.2f} × 행 {i} 빼기 (후진 대입) \n{pretty_two_matrices(A,I)}")

    return I, "\n".join(logs)

# ---------------------------
# 역행렬 계산 (가우스-조던)
# ---------------------------
def gauss_jordan_inverse(matrix):
    n = len(matrix)
    A = deepcopy(matrix)
    I = [[float(i == j) for j in range(n)] for i in range(n)]
    logs = []
    logs.append("초기 상태 \n" + pretty_two_matrices(A, I))

    for i in range(n):
        if A[i][i] == 0:
            for j in range(i+1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    I[i], I[j] = I[j], I[i]
                    logs.append(f"\n행 {i} ↔ 행 {j} 교환 \n{pretty_two_matrices(A,I)}")
                    break
            else:
                raise ValueError("역행렬 불가: 행렬식이 0입니다.")
        pivot = A[i][i]
        for k in range(n):
            A[i][k] /= pivot
            I[i][k] /= pivot
        logs.append(f"\n행 {i}를 피벗 {pivot:.2f}로 나눔 \n{pretty_two_matrices(A,I)}")

        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                    I[j][k] -= factor * I[i][k]
                logs.append(f"\n행 {j}에서 {factor:.2f} × 행 {i} 빼기 \n{pretty_two_matrices(A,I)}")

    return I, "\n".join(logs)

# ---------------------------
# 두 행렬 비교
# ---------------------------
def compare_matrices(m1, m2, tol=1e-9):
    n = len(m1)
    for i in range(n):
        for j in range(n):
            if abs(m1[i][j] - m2[i][j]) > tol:
                return False
    return True

# ---------------------------
# Tkinter GUI
# ---------------------------
root = tk.Tk()
root.title("행렬 계산기")
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

top_frame = tk.Frame(root, bg="#eef6f9")
top_frame.pack(pady=15)

tk.Label(top_frame, text="Matrix size(n)", font=("Apple SD Gothic Neo", 11,"bold"), bg="#eef6f9").pack(side="left", padx=5)
entry_n = tk.Entry(top_frame, width=5, font=("Apple SD Gothic Neo", 12), justify="center", bg="white")
entry_n.pack(side="left", padx=5)

btn_create = ttk.Button(top_frame, text="Input", style="Pink.TButton")
btn_create.pack(side="left", padx=10)
btn_calc = ttk.Button(top_frame, text="Inverse", style="Pink.TButton")
btn_calc.pack(side="left", padx=10)
btn_det = ttk.Button(top_frame, text="Determinant", style="Pink.TButton")
btn_det.pack(side="left", padx=10)

matrix_frame = tk.Frame(root, bg="#eef6f9")
matrix_frame.pack(pady=10)
result_frame = tk.Frame(root, bg="#eef6f9")
result_frame.pack(pady=15)

matrix_entries = []

def create_matrix_inputs():
    global matrix_entries
    for widget in matrix_frame.winfo_children():
        widget.destroy()
    matrix_entries = []
    try:
        n = int(entry_n.get())
    except ValueError:
        messagebox.showerror("오류", "정수를 입력하세요.")
        return
    if n == 1:
        messagebox.showwarning("안내", "1×1 행렬은 입력칸 생성이 필요 없습니다.")
        return
    for i in range(n):
        row_entries = []
        for j in range(n):
            e = tk.Entry(matrix_frame, width=7, font=("Arial", 11), justify="center", bg="white")
            e.grid(row=i, column=j, padx=3, pady=3)
            row_entries.append(e)
        matrix_entries.append(row_entries)

def show_results(inv_gauss, log_gauss, inv_jordan, log_jordan):
    for widget in result_frame.winfo_children():
        widget.destroy()
    titles = ["가우스 소거법 역행렬", "가우스-조던 역행렬"]
    matrices = [inv_gauss, inv_jordan]
    logs = [log_gauss, log_jordan]

    for idx, (title, mat, log) in enumerate(zip(titles, matrices, logs)):
        frame = tk.Frame(result_frame, bg="white", bd=1, relief="solid")
        frame.grid(row=0, column=idx, padx=10, pady=10, sticky="n")
        tk.Label(frame, text=title, font=("Apple SD Gothic Neo", 10, "bold"),
                 bg="white", fg="#333").pack(pady=5)
        grid_frame = tk.Frame(frame, bg="white")
        grid_frame.pack(padx=5, pady=5)
        n = len(mat)
        for i in range(n):
            for j in range(n):
                lbl = tk.Label(grid_frame, text=f"{mat[i][j]:.2f}",
                               font=("Apple SD Gothic Neo", 12),
                               width=8, borderwidth=1, relief="ridge",
                               bg="#fdfdfd")
                lbl.grid(row=i, column=j, padx=1, pady=1)
        log_box = tk.Text(frame, height=18, width=55,
                          wrap="word", font=("Courier New", 10),
                          bg="#F5FBFF", fg="black",
                          insertbackground="#1E3A5F",
                          highlightthickness=0, borderwidth=0)
        log_box.pack(pady=5)
        log_box.tag_config("explain", foreground="black")
        log_box.tag_config("matrix", foreground="#1565C0")
        for line in log.split("\n"):
            if "⎡" in line or "⎣" in line:
                log_box.insert("end", line + "\n", "matrix")
            else:
                log_box.insert("end", line + "\n", "explain")
        log_box.config(state="disabled")

def calculate_inverse():
    try:
        n = len(matrix_entries)
        if n == 0:
            messagebox.showwarning("입력 오류", "먼저 입력칸을 생성하세요.")
            return
        matrix = []
        for i in range(n):
            row = []
            for j in range(n):
                val = matrix_entries[i][j].get().strip()
                if val == "":
                    messagebox.showwarning("입력 오류", "모든 칸에 값을 입력하세요.")
                    return
                row.append(float(val))
            matrix.append(row)
        det, _ = determinant_with_steps(matrix)
        if abs(det) < 1e-9:
            messagebox.showerror("역행렬 불가", "det(A) = 0 이므로 역행렬을 구할 수 없습니다.")
            return
        inv_gauss, log_gauss = gauss_elimination_inverse(matrix)
        inv_jordan, log_jordan = gauss_jordan_inverse(matrix)
        show_results(inv_gauss, log_gauss, inv_jordan, log_jordan)
        if compare_matrices(inv_gauss, inv_jordan):
            messagebox.showinfo("비교 결과", "✅ 두 방법의 결과가 동일합니다.")
        else:
            messagebox.showwarning("비교 결과", "⚠️ 두 방법의 결과가 다릅니다.")
    except Exception as e:
        messagebox.showerror("오류", str(e))


def calculate_determinant_only():
    try:
        n = len(matrix_entries)
        if n == 0:
            messagebox.showwarning("입력 오류", "먼저 입력칸을 생성하세요.")
            return
        matrix = []
        for i in range(n):
            row = []
            for j in range(n):
                val = matrix_entries[i][j].get().strip()
                if val == "":
                    messagebox.showwarning("입력 오류", "모든 칸에 값을 입력하세요.")
                    return
                row.append(float(val))
            matrix.append(row)

        det, log = determinant_with_steps(matrix)
        for widget in result_frame.winfo_children():
            widget.destroy()

        frame = tk.Frame(result_frame, bg="white", bd=1, relief="solid")
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Label(frame, text="행렬식",
                 font=("Arial", 11, "bold"),
                 bg="white", fg="#333").pack(pady=5)

        log_box = tk.Text(frame, height=20, width=30,
                          wrap="word", font=("Courier New", 10),
                          bg="#F5FBFF", fg="black",
                          insertbackground="#1E3A5F",
                          highlightthickness=0, borderwidth=0)
        log_box.pack(padx=10, pady=10, fill="both", expand=True)
        log_box.tag_config("explain", foreground="black")
        log_box.tag_config("matrix", foreground="#1565C0")

        for line in log.split("\n"):
            if any(bracket in line for bracket in ["⎡", "⎣", "⎢"]):
                log_box.insert("end", line + "\n", "matrix")  
            else:
                log_box.insert("end", line + "\n", "explain") 

        log_box.insert("end", f"\ndet(A) = {det:.2f}", "explain")
        log_box.config(state="disabled")

    except Exception as e:
        messagebox.showerror("오류", str(e))


btn_create.config(command=create_matrix_inputs)
btn_calc.config(command=calculate_inverse)
btn_det.config(command=calculate_determinant_only)

root.mainloop()
