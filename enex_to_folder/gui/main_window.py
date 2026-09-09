"""ENEX to Folder Converter의 메인 GUI 창.

이 클래스는 화면 구성과 사용자 입력 처리만 담당하며,
실제 변환 로직은 BatchConverter에 위임합니다 (의존관계 역전 원칙).
"""
import os
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

from enex_to_folder.orchestration.batch_converter import BatchConverter

APP_VERSION = "v1.1.0"


class MainWindow:
    """ENEX → 노트별 폴더 변환기의 메인 윈도우."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(f"ENEX to Folder 변환기 {APP_VERSION}")
        self.root.geometry("640x480")
        self.root.resizable(True, True)

        self.source_dir = tk.StringVar()
        self.output_dir = tk.StringVar()

        self._log_queue: "queue.Queue" = queue.Queue()
        self._worker_thread: "threading.Thread | None" = None
        self._stop_requested = False

        self._build_widgets()
        self._poll_log_queue()

    # ------------------------------------------------------------------
    # 화면 구성
    # ------------------------------------------------------------------
    def _build_widgets(self) -> None:
        padding = {"padx": 10, "pady": 6}

        # 소스 폴더 선택
        source_frame = ttk.Frame(self.root)
        source_frame.pack(fill="x", **padding)
        ttk.Label(source_frame, text="ENEX 파일 폴더:").pack(side="left")
        ttk.Entry(source_frame, textvariable=self.source_dir).pack(
            side="left", fill="x", expand=True, padx=5
        )
        ttk.Button(source_frame, text="폴더 선택", command=self._select_source_dir).pack(
            side="left"
        )

        # 출력 폴더 선택
        output_frame = ttk.Frame(self.root)
        output_frame.pack(fill="x", **padding)
        ttk.Label(output_frame, text="출력 폴더:").pack(side="left")
        ttk.Entry(output_frame, textvariable=self.output_dir).pack(
            side="left", fill="x", expand=True, padx=5
        )
        ttk.Button(output_frame, text="폴더 선택", command=self._select_output_dir).pack(
            side="left"
        )

        # 실행/중지 버튼
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", **padding)
        self.start_button = ttk.Button(
            button_frame, text="변환 시작", command=self._start_conversion
        )
        self.start_button.pack(side="left")
        self.stop_button = ttk.Button(
            button_frame, text="중지", command=self._request_stop, state="disabled"
        )
        self.stop_button.pack(side="left", padx=5)

        # 진행률 표시
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(fill="x", **padding)
        self.progress_bar = ttk.Progressbar(progress_frame, mode="determinate")
        self.progress_bar.pack(fill="x", expand=True, side="left")
        self.progress_label = ttk.Label(progress_frame, text="0 / 0")
        self.progress_label.pack(side="left", padx=5)

        # 로그 창
        log_frame = ttk.Frame(self.root)
        log_frame.pack(fill="both", expand=True, **padding)
        ttk.Label(log_frame, text="작업 로그:").pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(log_frame, state="disabled", height=15)
        self.log_text.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    # 이벤트 핸들러
    # ------------------------------------------------------------------
    def _select_source_dir(self) -> None:
        selected = filedialog.askdirectory(title="ENEX 파일이 들어있는 폴더를 선택하세요")
        if selected:
            self.source_dir.set(selected)

    def _select_output_dir(self) -> None:
        selected = filedialog.askdirectory(title="결과를 저장할 폴더를 선택하세요")
        if selected:
            self.output_dir.set(selected)

    def _start_conversion(self) -> None:
        source = self.source_dir.get().strip()
        output = self.output_dir.get().strip()

        if not source or not os.path.isdir(source):
            messagebox.showerror("오류", "유효한 ENEX 파일 폴더를 선택해주세요.")
            return
        if not output:
            messagebox.showerror("오류", "출력 폴더를 선택해주세요.")
            return

        self._stop_requested = False
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self._clear_log()
        self.progress_bar["value"] = 0
        self.progress_label.config(text="0 / 0")

        self._worker_thread = threading.Thread(
            target=self._run_conversion_worker, args=(source, output), daemon=True
        )
        self._worker_thread.start()

    def _request_stop(self) -> None:
        self._stop_requested = True
        self._log_queue.put((None, None, "중지 요청됨. 현재 노트 처리 후 중단합니다..."))

    # ------------------------------------------------------------------
    # 백그라운드 작업 (별도 스레드에서 실행되어 GUI가 멈추지 않도록 함)
    # ------------------------------------------------------------------
    def _run_conversion_worker(self, source: str, output: str) -> None:
        converter = BatchConverter()

        def progress_callback(current: int, total: int, message: str) -> None:
            self._log_queue.put((current, total, message))

        try:
            converter.convert_folder(
                source,
                output,
                progress_callback=progress_callback,
                should_stop=lambda: self._stop_requested,
            )
        except Exception as exc:  # noqa: BLE001 - GUI 표시를 위해 모든 예외를 잡음
            self._log_queue.put((None, None, f"❌ 예기치 않은 오류: {exc}"))
        finally:
            self._log_queue.put(("__DONE__", None, None))

    # ------------------------------------------------------------------
    # 로그 큐 처리 (스레드 안전하게 GUI 갱신)
    # ------------------------------------------------------------------
    def _poll_log_queue(self) -> None:
        try:
            while True:
                current, total, message = self._log_queue.get_nowait()
                if current == "__DONE__":
                    self.start_button.config(state="normal")
                    self.stop_button.config(state="disabled")
                    continue

                if total:
                    self.progress_bar["maximum"] = total
                    self.progress_bar["value"] = current
                    self.progress_label.config(text=f"{current} / {total}")

                if message:
                    self._append_log(message)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self._poll_log_queue)

    def _append_log(self, message: str) -> None:
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _clear_log(self) -> None:
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")
