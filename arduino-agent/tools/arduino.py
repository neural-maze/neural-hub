import re
import subprocess

from crewai_tools import BaseTool


class CompileAndUploadToArduinoTool(BaseTool):
    name: str = "CompileAndUploadToArduinoTool"
    description: str = "Compiles and Uploads an Arduino Sketch script to an Arduino"
    ino_file_dir: str = "The directory that contains the ino file"
    board_fqbn: str = "The board type, e.g. 'arduino:avr:uno'"
    port: str = "The port where the Arduino is connected"

    def __init__(self, ino_file_dir: str, board_fqbn: str, port: str, **kwargs):
        super().__init__(**kwargs)
        self.ino_file_dir = ino_file_dir
        self.board_fqbn = board_fqbn
        self.port = port

    def _fix_ino_file(self):
        """
        This is a helper method for fixing the output .ino file when Llama3 adds some unintended text
        that invalidates the compilation.
        """
        with open(f"{self.ino_file_dir}/tmp.ino", "r") as f:
            content = f.read()

        pattern = r'```.*?\n(.*?)```'
        match = re.search(pattern, content, re.DOTALL).group(1).strip()

        with open(f"{self.ino_file_dir}/tmp.ino", "w") as f:
            f.write(match)

    def _run(self):
        self._fix_ino_file()

        try:
            subprocess.check_call([
                "arduino-cli", "compile", "--fqbn", self.board_fqbn, self.ino_file_dir
            ])
            subprocess.check_call([
                "arduino-cli", "upload", "--port", self.port, "--fqbn", self.board_fqbn, self.ino_file_dir
            ])
        except subprocess.CalledProcessError:
            return "Compilation failed"

        return "Code successfully uploaded to the board"
