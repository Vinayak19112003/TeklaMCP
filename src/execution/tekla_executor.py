"""
Tekla Executor
Executes generated C# code in Tekla Structures
"""

import subprocess
from pathlib import Path
from typing import Optional
from ..utils import get_logger, Config, ensure_dir

logger = get_logger(__name__)


class TeklaExecutor:
    """
    Execute C# code in Tekla Structures
    """

    def __init__(self):
        self.logger = logger

    def execute(self, code: str, output_dir: Optional[Path] = None) -> bool:
        """
        Execute C# code

        Args:
            code: C# code to execute
            output_dir: Output directory for compiled files

        Returns:
            True if successful
        """
        self.logger.info("Executing Tekla code")

        try:
            # Save code to file
            if output_dir is None:
                output_dir = Config.OUTPUT_DIR / "temp"

            ensure_dir(output_dir)

            code_file = output_dir / "TeklaModel.cs"
            with open(code_file, 'w', encoding='utf-8') as f:
                f.write(code)

            self.logger.info("Code saved", path=str(code_file))

            # Compile code
            success = self._compile_code(code_file)

            if not success:
                self.logger.error("Compilation failed")
                return False

            # Execute in Tekla
            # ### TODO: USER MUST FILL THIS SECTION
            # Add Tekla execution logic:
            # - Check Tekla is running
            # - Load compiled assembly
            # - Execute Main method

            self.logger.info("Execution complete")

            return True

        except Exception as e:
            self.logger.error("Execution failed", error=str(e))
            return False

    def _compile_code(self, code_file: Path) -> bool:
        """
        Compile C# code

        Args:
            code_file: Path to .cs file

        Returns:
            True if compilation successful
        """
        try:
            result = subprocess.run(
                ["dotnet", "build", str(code_file)],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                self.logger.info("Compilation successful")
                return True
            else:
                self.logger.error("Compilation errors", stderr=result.stderr)
                return False

        except Exception as e:
            self.logger.error("Compilation failed", error=str(e))
            return False


if __name__ == "__main__":
    print("Tekla Executor ready.")
