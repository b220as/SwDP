from tkinter import Tk, filedialog, Label, Entry, Button, Frame, Canvas

import fitz  # PyMuPDF

file_path = None
selected_page = None

def pdf_to_images(start_page, end_page, x1, y1, x2, y2):
    global file_path
    pdf_document = fitz.open(file_path)
    for page_num in range(start_page - 1, end_page):
        page = pdf_document.load_page(page_num)
        rect = fitz.Rect(x1, y1, x2, y2)
        image = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=rect)
        image.save(f'page_{page_num + 1}_selected.png')

    pdf_document.close()

def convert_pdf_to_images():
    global file_path, selected_page

    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF files", "*.pdf")])

    if file_path:
        range_window = Tk()
        range_window.title("Select Range")

        start_label = Label(range_window, text="Start Page:")
        start_label.grid(row=0, column=0)
        start_entry = Entry(range_window)
        start_entry.grid(row=0, column=1)

        end_label = Label(range_window, text="End Page:")
        end_label.grid(row=1, column=0)
        end_entry = Entry(range_window)
        end_entry.grid(row=1, column=1)

        def select_page():
            global selected_page
            selected_page = int(page_entry.get())
            canvas.delete("all")
            page = pdf_document.load_page(selected_page - 1)
            img = page.get_pixmap(matrix=fitz.Matrix(3, 3))
            canvas.create_image(0, 0, anchor="nw", image=img)

        def process_pdf():
            start_page = int(start_entry.get())
            end_page = int(end_entry.get())
            x1 = int(x1_entry.get())
            y1 = int(y1_entry.get())
            x2 = int(x2_entry.get())
            y2 = int(y2_entry.get())
            try:
                pdf_to_images(start_page, end_page, x1, y1, x2, y2)
                print("変換が完了しました。")
            except Exception as e:
                print(f"エラーが発生しました: {e}")
            range_window.destroy()

        page_label = Label(range_window, text="Page:")
        page_label.grid(row=2, column=0)
        page_entry = Entry(range_window)
        page_entry.grid(row=2, column=1)
        select_button = Button(range_window, text="Select Page", command=select_page)
        select_button.grid(row=2, column=2)

        selection_frame = Frame(range_window)
        selection_frame.grid(row=3, columnspan=3)

        x1_label = Label(selection_frame, text="X1:")
        x1_label.grid(row=0, column=0)
        x1_entry = Entry(selection_frame)
        x1_entry.grid(row=0, column=1)

        y1_label = Label(selection_frame, text="Y1:")
        y1_label.grid(row=0, column=2)
        y1_entry = Entry(selection_frame)
        y1_entry.grid(row=0, column=3)

        x2_label = Label(selection_frame, text="X2:")
        x2_label.grid(row=1, column=0)
        x2_entry = Entry(selection_frame)
        x2_entry.grid(row=1, column=1)

        y2_label = Label(selection_frame, text="Y2:")
        y2_label.grid(row=1, column=2)
        y2_entry = Entry(selection_frame)
        y2_entry.grid(row=1, column=3)

        canvas = Canvas(range_window, width=400, height=600)
        canvas.grid(row=4, columnspan=3)

        convert_button = Button(range_window, text="Convert", command=process_pdf)
        convert_button.grid(row=5, columnspan=3)

        pdf_document = fitz.open(file_path)
        range_window.mainloop()

convert_pdf_to_images()
