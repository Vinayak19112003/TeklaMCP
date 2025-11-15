"""
C# Compiler
Compiles C# code using Roslyn or dotnet CLI
"""

import subprocess
from pathlib import Path
from ..utils import get_logger

logger = get_logger(__name__)


class CSharpCompiler:
    """
    Compile C# code
    """

    def __init__(self):
        self.logger = logger

    def compile(self, code_file: Path) -> bool:
        """
        Compile C# file

        Args:
            code_file: Path to .cs file

        Returns:
            True if successful
        """
        ### TODO: USER MUST FILL THIS SECTION
        # Add proper C# compilation with Tekla references

        return True


if __name__ == "__main__":
    print("C# Compiler ready.")
