import logging
from ctypes import cast
from typing import List, Optional
from chardet import ResultDict
from promptmanager.runtime.flow import PMNodeOutput
from promptmanager.script.schema.document import PMDocument
import concurrent.futures

logger = logging.getLogger("pm_log")


class TextLoader():
    """Load text file.


    Args:
        file_path: Path to the file to load.

        encoding: File encoding to use. If `None`, the file will be loaded
        with the default system encoding.

        autodetect_encoding: Whether to try to autodetect the file encoding
            if the specified encoding fails.
    """

    def __init__(
        self,
        file_path: str,
        encoding: Optional[str] = None,
        autodetect_encoding: bool = False,
    ):
        """Initialize with file path."""
        self.file_path = file_path
        self.encoding = encoding
        self.autodetect_encoding = autodetect_encoding

    def detect_file_encodings(file_path: str, timeout: int = 5) -> List[dict]:
        """Try to detect the file encoding.

        Returns a list of `FileEncoding` tuples with the detected encodings ordered
        by confidence.

        Args:
            file_path: The path to the file to detect the encoding for.
            timeout: The timeout in seconds for the encoding detection.
        """
        import chardet

        def read_and_detect(file_path: str) -> List[dict]:
            with open(file_path, "rb") as f:
                rawdata = f.read()
            return cast(List[dict], chardet.detect_all(rawdata))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(read_and_detect, file_path)
            try:
                encodings = future.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                raise TimeoutError(
                    f"Timeout reached while detecting encoding for {file_path}"
                )

        if all(encoding["encoding"] is None for encoding in encodings):
            raise RuntimeError(f"Could not detect encoding for {file_path}")

        return [ResultDict(enc) for enc in encodings if enc["encoding"] is not None]

    def exec(self) -> List[PMDocument]:
        """Load from file path."""
        text = ""
        try:
            with open(self.file_path, encoding=self.encoding) as f:
                text = f.read()
        except UnicodeDecodeError as e:
            if self.autodetect_encoding:
                detected_encodings = self.detect_file_encodings(self.file_path)
                for encoding in detected_encodings:
                    logger.debug(f"Trying encoding: {encoding.encoding}")
                    try:
                        with open(self.file_path, encoding=encoding.encoding) as f:
                            text = f.read()
                        break
                    except UnicodeDecodeError:
                        continue
            else:
                raise RuntimeError(f"Error loading {self.file_path}") from e
        except Exception as e:
            raise RuntimeError(f"Error loading {self.file_path}") from e

        metadata = {"source": self.file_path}
        return [PMDocument(page_content=text, metadata=metadata)]

    def run(params: dict = None, inputs: dict = None, outputs=None) -> PMNodeOutput:
        logger.info("Welcome to Use Csv Loader!")
        logger.info("This is params info:")
        logger.info(params)
        logger.info("This is inputs info:")
        logger.info(inputs)
        logger.info("This is outputs info:")
        logger.info(outputs)

        file_path = params['script']['text_path']['value']

        text_loader = TextLoader(file_path)
        result = text_loader.exec()

        output = TextLoader()
        for output_name in outputs.keys():
            output.add_output(output_name, result)

        return output
