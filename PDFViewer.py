import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import fitz  # PyMuPDF
from tkinter import messagebox

# 메인 창 생성
root = tk.Tk()
root.title("PDF 뷰어")
root.geometry("900x700")

# 현재 페이지 번호와 총 페이지 수를 저장할 변수
current_page = 0
total_pages = 0
pdf_document = None
current_image = None

# 메인 프레임 생성
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Canvas와 스크롤바 생성
canvas = tk.Canvas(main_frame, bg='gray90')
scrollbar_y = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar_x = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=canvas.xview)

# 스크롤바 배치
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Canvas 스크롤 설정
canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

# 하단 제어 프레임
control_frame = ttk.Frame(root)
control_frame.pack(fill=tk.X, padx=5, pady=5)

# 페이지 레이블
page_label = ttk.Label(control_frame, text="페이지: 0/0")
page_label.pack(side=tk.LEFT, padx=5)

def update_page_display():
    global current_page, total_pages
    if pdf_document:
        page_label.config(text=f"페이지: {current_page + 1}/{total_pages}")

def show_page(page_num):
    global current_image, current_page, pdf_document
    if pdf_document and 0 <= page_num < total_pages:
        current_page = page_num
        
        # 현재 페이지 가져오기
        page = pdf_document[page_num]
        
        # 페이지를 이미지로 변환 (해상도 향상)
        zoom = 2  # 해상도를 2배로 증가
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # PIL 이미지로 변환
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Tkinter 이미지로 변환
        photo = ImageTk.PhotoImage(img)
        
        # 이전 이미지 참조 유지
        current_image = photo
        
        # Canvas 크기 조정
        canvas.config(scrollregion=(0, 0, img.width, img.height))
        
        # Canvas 내용 초기화 및 새 이미지 표시
        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=photo)
        
        update_page_display()

def prev_page():
    global current_page
    if current_page > 0:
        show_page(current_page - 1)

def next_page():
    global current_page, total_pages
    if current_page < total_pages - 1:
        show_page(current_page + 1)

# 이전/다음 페이지 버튼
prev_button = ttk.Button(control_frame, text="이전 페이지", command=prev_page)
prev_button.pack(side=tk.LEFT, padx=5)

next_button = ttk.Button(control_frame, text="다음 페이지", command=next_page)
next_button.pack(side=tk.LEFT, padx=5)

def open_pdf():
    global pdf_document, total_pages, current_page
    try:
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF 파일", "*.pdf")]
        )
        
        if file_path:
            # 이전 PDF 문서가 열려있다면 닫기
            if pdf_document:
                pdf_document.close()
            
            # 새 PDF 문서 열기
            pdf_document = fitz.open(file_path)
            total_pages = pdf_document.page_count
            current_page = 0
            
            # 첫 페이지 표시
            show_page(0)
            
    except Exception as e:
        messagebox.showerror("에러", f"PDF를 여는 중 오류가 발생했습니다:\n{str(e)}")

# 메뉴바 생성
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="PDF 열기", command=open_pdf)
filemenu.add_separator()
filemenu.add_command(label="종료", command=root.quit)
menubar.add_cascade(label="파일", menu=filemenu)
root.config(menu=menubar)

# 마우스 휠 이벤트 바인딩
def on_mousewheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")
canvas.bind_all("<MouseWheel>", on_mousewheel)

# 메인 루프 실행
root.mainloop()