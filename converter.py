"""
File watcher and conversion logic for the JXR → PNG Converter app.
Uses watchdog to monitor directories and subprocess to run jxr_to_png.exe.
"""

import os
import time
import subprocess
import logging
import tempfile
from pathlib import Path
from datetime import datetime

from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from translations import t

logger = logging.getLogger(__name__)


class JXRFileHandler(FileSystemEventHandler):
    """Watchdog handler that detects new .jxr files."""

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith('.jxr'):
            logger.info(f"Detected new JXR file: {event.src_path}")
            self.callback(event.src_path)

    def on_moved(self, event):
        """Handle files moved/renamed into the watched folder."""
        if event.is_directory:
            return
        if event.dest_path.lower().endswith('.jxr'):
            logger.info(f"Detected moved JXR file: {event.dest_path}")
            self.callback(event.dest_path)


class FileWatcherThread(QThread):
    """Thread that monitors a directory recursively for new .jxr files."""

    file_detected = pyqtSignal(str)  # Emits the full path of a new .jxr file

    def __init__(self, watch_path: str, parent=None):
        super().__init__(parent)
        self.watch_path = watch_path
        self._stop_requested = False
        self._observer = None

    def run(self):
        self._stop_requested = False
        handler = JXRFileHandler(self._on_file_found)
        self._observer = Observer()
        self._observer.schedule(handler, self.watch_path, recursive=True)
        self._observer.start()
        logger.info(f"Started watching: {self.watch_path}")

        while not self._stop_requested:
            time.sleep(0.5)

        self._observer.stop()
        self._observer.join()
        logger.info("File watcher stopped.")

    def _on_file_found(self, file_path: str):
        """Called when a new .jxr file is detected. Waits for file to be ready."""
        # Wait for the file to be fully written (debounce)
        time.sleep(1.5)

        # Verify the file still exists and is accessible
        try:
            if os.path.exists(file_path):
                size1 = os.path.getsize(file_path)
                time.sleep(0.5)
                size2 = os.path.getsize(file_path)
                if size1 == size2 and size1 > 0:
                    self.file_detected.emit(file_path)
                else:
                    # File still being written, wait more
                    time.sleep(2)
                    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                        self.file_detected.emit(file_path)
        except OSError as e:
            logger.warning(f"Error checking file {file_path}: {e}")

    def stop(self):
        self._stop_requested = True

    def update_path(self, new_path: str):
        self.watch_path = new_path


class ConversionResult:
    """Stores the result of a single conversion."""

    def __init__(self, input_path: str, output_path: str, success: bool,
                 message: str = "", timestamp: datetime = None):
        self.input_path = input_path
        self.output_path = output_path
        self.success = success
        self.message = message
        self.timestamp = timestamp or datetime.now()


class ConversionWorker(QThread):
    """Thread that handles the actual .jxr → .png conversion."""

    conversion_started = pyqtSignal(str)  # input file path
    conversion_finished = pyqtSignal(object)  # ConversionResult
    queue_size_changed = pyqtSignal(int)  # current queue size

    def __init__(self, jxr_to_png_path: str, parent=None):
        super().__init__(parent)
        self.jxr_to_png_path = jxr_to_png_path
        self._stop_requested = False
        self._queue = []
        self._mutex = QMutex()
        self._condition = QWaitCondition()

    def run(self):
        self._stop_requested = False
        import concurrent.futures

        # Usa fino a 3 thread in parallelo
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            self._futures = []

            while not self._stop_requested:
                self._mutex.lock()
                
                # Cleanup completed futures
                self._futures = [f for f in self._futures if not f.done()]
                
                # Attendi se non ci sono file da elaborare e nessuna conversione in corso
                if not self._queue and not self._futures:
                    self._condition.wait(self._mutex, 200)

                # Preleva dalla coda finché ci sono "slot" liberi per elaborare
                while self._queue and len(self._futures) < 3 and not self._stop_requested:
                    file_path = self._queue.pop(0)
                    self.queue_size_changed.emit(len(self._queue))
                    fut = executor.submit(self._convert, file_path)
                    self._futures.append(fut)
                    
                self._mutex.unlock()
                
                # Se la coda dei worker è piena e quelli in background lavorano, riposa per non affaticare la CPU
                if len(self._futures) >= 3:
                     time.sleep(0.2)

    def add_file(self, file_path: str):
        """Add a file to the conversion queue."""
        self._mutex.lock()
        # Avoid duplicates
        if file_path not in self._queue:
            self._queue.append(file_path)
            self.queue_size_changed.emit(len(self._queue))
            self._condition.wakeOne()
        self._mutex.unlock()

    def _convert(self, input_path: str):
        """Convert a single .jxr file to .png."""
        self.conversion_started.emit(input_path)

        # Build output path: same folder, same name, .png extension
        input_p = Path(input_path)
        output_path = str(input_p.with_suffix('.png'))

        # Check if the .jxr is actually a improperly named .png file
        try:
            with open(input_path, 'rb') as f:
                header = f.read(8)
            if header == b'\x89PNG\r\n\x1a\n':
                # It's actually a PNG! Let's just fix the extension.
                import os
                if os.path.exists(output_path):
                    # Se il VERO png esiste già, questo finto jxr è un doppione buggato, eliminiamolo
                    os.remove(input_path)
                    res_msg = t("conv_deleted_fake")
                else:
                    # Altrimenti rinominiamo e sistemiamo i danni di NVIDIA
                    os.rename(input_path, output_path)
                    res_msg = t("conv_fixed_fake")
                    
                result = ConversionResult(input_path, output_path, True, res_msg)
                self.conversion_finished.emit(result)
                return
        except Exception as e:
            pass

        # Skip if PNG already exists
        import os
        if os.path.exists(output_path):
            result = ConversionResult(
                input_path, output_path, True,
                t("conv_already_exists")
            )
            self.conversion_finished.emit(result)
            return

        # 1. Decode JXR to PNG (HDR) using jxr_to_png
        fd, temp_png = tempfile.mkstemp(suffix=".png")
        os.close(fd)
        
        jxr_path = os.path.join(os.path.dirname(self.jxr_to_png_path), "jxr_to_png.exe")
        hdrfix_path = os.path.join(os.path.dirname(self.jxr_to_png_path), "hdrfix.exe")
        
        try:
            # Step 1: Decode
            if not os.path.isfile(jxr_path):
                raise FileNotFoundError(t("conv_error_jxr_not_found", path=jxr_path))
            
            p1 = subprocess.Popen(
                [jxr_path, input_path, temp_png],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            out1, err1 = p1.communicate(timeout=60)
            if p1.returncode != 0:
                os.remove(temp_png)
                stderr_text = err1.decode('utf-8', errors='ignore').strip() or out1.decode('utf-8', errors='ignore').strip()
                return ConversionResult(input_path, output_path, False, t("conv_error_jxr", detail=stderr_text if stderr_text else 'Exit code 1'))
            
            if self._stop_requested:
                os.remove(temp_png)
                return ConversionResult(input_path, output_path, False, t("conv_interrupted"))
                
            # Step 2: Tonemap using hdrfix
            if not os.path.isfile(hdrfix_path):
                os.remove(temp_png)
                raise FileNotFoundError(t("conv_error_hdrfix_not_found", path=hdrfix_path))

            p2 = subprocess.Popen(
                [hdrfix_path, "--tone-map", "hable", "--saturation", "1.2", temp_png, output_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            out2, err2 = p2.communicate(timeout=60)
            
            # Clean up temp
            try:
                os.remove(temp_png)
            except:
                pass
                
            if p2.returncode == 0:
                result = ConversionResult(input_path, output_path, True, t("conv_success"))
            else:
                stderr_text = err2.decode('utf-8', errors='ignore').strip()
                result = ConversionResult(
                    input_path, output_path, False,
                    t("conv_error_hdrfix", detail=stderr_text if stderr_text else '?')
                )

        except FileNotFoundError as e:
            result = ConversionResult(
                input_path, output_path, False,
                t("conv_error_generic", detail=str(e))
            )
        except Exception as e:
            result = ConversionResult(
                input_path, output_path, False,
                t("conv_error_generic", detail=str(e))
            )

        self.conversion_finished.emit(result)

    def stop(self):
        self._stop_requested = True
        self._condition.wakeAll()

    def update_exe_path(self, new_path: str):
        self.jxr_to_png_path = new_path


def find_unconverted_jxr_files(watch_path: str) -> list:
    """Find all .jxr files in the watch path that don't have a corresponding .png."""
    unconverted = []
    watch = Path(watch_path)

    if not watch.exists():
        return unconverted

    for jxr_file in watch.rglob("*.jxr"):
        png_file = jxr_file.with_suffix('.png')
        if not png_file.exists():
            unconverted.append(str(jxr_file))

    unconverted.sort(key=lambda f: os.path.getmtime(f), reverse=True)
    return unconverted
