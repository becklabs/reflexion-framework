# ADAPTED FROM https://huggingface.co/spaces/Muennighoff/code_eval_octopack/blob/main/execute.py 

import os
from typing import Any, List, Optional
from .base import LocalTestingEnv
import tempfile
from .util import temporary_directory
import subprocess
import shutil
from contextlib import contextmanager
import re
from queue import Queue
import time


BASE_CARGO = """[package]
name = "rust"
version = "0.1.0"
edition = "2021"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]
rand = "0.4"
regex = "1"
md5 = "0.7.0"
"""

PROGRAM_TEMPLATE = """
fn main(){}

use std::{slice::Iter, cmp::{max, self}, mem::replace, collections::{HashSet, HashMap}, ops::Index, ascii::AsciiExt};
use rand::Rng;
use regex::Regex;
use md5;
use std::any::{Any, TypeId};

{{program}}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_program() {
        {{test}}
    }
}
"""



class RustTestingEnv(LocalTestingEnv):
    """
    Local Testing environment for Rust programs. 
    """
    def __init__(self, directory: str = os.getcwd(), timeout: int = 10):
        self.working_directory = directory
        rust_directory = os.path.join(self.working_directory, "rust")
        self.RUST_EXT: str = ".rs"
        super().__init__(rust_directory, timeout)

    def _unsafe_execute(self, program: str, test: str, result: Queue) -> None:
        with temporary_directory(self.directory) as self.RUST_DIR:
            now = time.time()
            self._build_directory()
            print(f"Building directory took {time.time() - now} seconds")

            with tempfile.NamedTemporaryFile(dir=self.RUST_BIN, delete=False) as f:
                file_name: str = "test" + self.RUST_EXT
                os.rename(f.name, os.path.join(self.RUST_BIN, file_name))
                formatted_program = PROGRAM_TEMPLATE.replace(
                    "{{program}}", program
                ).replace("{{test}}", test)
                f.write(formatted_program.encode("utf-8"))

            # Proceed towards Rust binaries compilation. Therefore move to Rust module root dir.
            os.chdir(self.RUST_DIR)

            compilation_result = subprocess.run(
                ["cargo", "check", "--bin", "test"],
                timeout=self.timeout,
                capture_output=True,
            )
            if compilation_result.returncode == 0:
                exec_result = subprocess.run(
                    ["cargo", "test", "--bin", "test"],
                    timeout=self.timeout,
                    capture_output=True,
                )
                if exec_result.returncode == 0:
                    result.put("passed")
                else:
                    err = (
                        exec_result.stdout.decode()
                        if exec_result.stdout
                        else exec_result.stderr.decode()
                    )
                    err = self._parse_execution_message(err)
                    result.put("failed: execution error: " + err)
            else:
                err = (
                    compilation_result.stderr.decode()
                    if compilation_result.stderr
                    else compilation_result.stdout.decode()
                )
                err = self._parse_compilation_message(err)
                result.put("failed: compilation error: " + err)

            # Move back to the original working directory
            os.chdir(self.working_directory)


    def _build_directory(self):
        self.RUST_SRC: str = os.path.join(self.RUST_DIR, "src")
        self.RUST_BIN: str = os.path.join(self.RUST_SRC, "bin")
        self.RUST_TMP_DIR: str = os.path.join(self.RUST_DIR, "tmp")
        self.RUST_LOGS: str = os.path.join(self.RUST_TMP_DIR, "logs")

        # Create mandatory tmp directories
        os.makedirs(self.RUST_TMP_DIR, exist_ok=True)
        os.makedirs(self.RUST_LOGS, exist_ok=True)
        os.makedirs(self.RUST_SRC, exist_ok=True)
        os.makedirs(self.RUST_BIN, exist_ok=True)

        # Create Cargo.toml file
        if not os.path.exists(f"{self.RUST_DIR}/Cargo.toml"):
            open(f"{self.RUST_DIR}/Cargo.toml", "w").write(BASE_CARGO)
    
    def _parse_execution_message(self, message: str) -> str:
        pattern = r"left: [`'](.*?)[`']\s*,\s*right: [`'](.*?)[`']"
        match = re.search(pattern, message)

        if match:
            left_value = match.group(1)
            right_value = match.group(2)
            message = f'{left_value} != {right_value}'
        elif 'assertion failed: ' in message:
            message = 'assertion failed'
        
        return message
    
    def _parse_compilation_message(self, message: str) -> str:
        pattern = r"(error(\[.*?\])?.*?\n\n)"
        matches = re.findall(pattern, message, re.DOTALL)
        if matches:
            message = '\n'.join([m[0] for m in matches])
        return message
