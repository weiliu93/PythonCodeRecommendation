from pcr.computational_graph.source_task import SourceTask
from pcr.computational_graph.data_bundle import DataBundle
from pcr.logger.log_util import logger
from pcr.util import string_util

import os
import tarfile
import zipfile
import shutil
import ast


class AppSetPreprocessingTask(SourceTask):

    def _execute(self, data_bundle):
        """
        collect all information in python codes
        """
        work_dir = data_bundle["work_dir"]
        for package_name in os.listdir(work_dir):
            package_path = os.path.join(work_dir, package_name)
            # check tmp directory first
            tmp_path = os.path.join(os.curdir, "tmp")
            if os.path.exists(tmp_path):
                shutil.rmtree(tmp_path)
            # file
            if os.path.isfile(package_path):
                if package_path.endswith(".py"):
                    self._handle_python_code(package_path)
            # directory
            elif os.path.isdir(package_path):
                for root, dirs, files in os.walk(package_path):
                    for f in files:
                        filepath = os.path.join(root, f)
                        if filepath.endswith(".py"):
                            self._handle_python_code(filepath)
            else:
                # extract package
                if tarfile.is_tarfile(package_path):
                    tar_file = tarfile.open(package_path)
                    tar_file.extractall(os.path.join(os.curdir, "tmp"))

                    extract_app_dir = os.path.join(os.curdir, "tmp", os.listdir("tmp")[0])
                    self._handle_python_codes_in_app_dir(extract_app_dir)
                elif zipfile.is_zipfile(package_path):
                    zip_file = zipfile.ZipFile(package_path)
                    zip_file.extractall(os.path.join(os.curdir, "tmp"))

                    extract_app_dir = os.path.join(os.curdir, "tmp", os.listdir("tmp")[0])
                    self._handle_python_codes_in_app_dir(extract_app_dir)
                else:
                    logger.warn("{} could not be extracted".format(package_path))
            # double check tmp path
            if os.path.exists(tmp_path):
                shutil.rmtree(tmp_path)

    def _handle_python_codes_in_app_dir(self, app_dir):
        """
        traverse app set dir
        """
        for root, dirs, files in os.walk(app_dir):
            for f in files:
                filepath = os.path.abspath(os.path.join(root, f))
                # filter py code
                if filepath.endswith(".py"):
                    self._handle_python_code(filepath)

    def _handle_python_code(self, filepath):
        """
        split the python codes into several chunks with different threshold
        """
        # Algorithm 1: sliding windows
        chunk_sizes = [1, 2, 5, 10, 20]
        code_piece_set = set()
        for chunk_size in chunk_sizes:
            lines = []
            with open(filepath, "r") as f:
                for line in f:
                    # preprocessing line string, remove \n and replace \t with four spaces
                    line = line.strip("\n").replace("\t", "    ")
                    # empty line and comments will be ignored
                    if not self._filter(line):
                        lines.append(line)
                        # maintain a sliding window
                        if len(lines) > chunk_size:
                            lines.pop(0)
                        code_piece = "\n".join(string_util.left_padding_strings(lines))
                        # dedup code piece
                        if code_piece not in code_piece_set:
                            code_piece_set.add(code_piece)
                            data_bundle = DataBundle(data_dict={"filepath": filepath, "code": code_piece})
                            self._emit(data_bundle)
        # Algorithm 2: check classes and functions
        text = open(filepath, "r").read()
        lines = text.split("\n")
        try:
            ast_root = ast.parse(text)
            class_linenos, function_linenos = [], []
            for node in ast.walk(ast_root):
                if isinstance(node, ast.ClassDef):
                    class_linenos.append(node.lineno - 1)
                elif isinstance(node, ast.FunctionDef):
                    function_linenos.append(node.lineno - 1)
            # collect classes and functions
            for lineno in (class_linenos + function_linenos):
                code_block = []
                left_padding = string_util.get_left_padding_spaces(lines[lineno])
                code_block.append(lines[lineno])
                lineno += 1
                while lineno < len(lines) and \
                    (string_util.is_empty_string(lines[lineno]) or
                         (string_util.get_left_padding_spaces(lines[lineno]) > left_padding)):
                    if not string_util.is_empty_string(lines[lineno]):
                        code_block.append(lines[lineno])
                    lineno += 1
                code_piece = "\n".join(string_util.left_padding_strings(code_block))
                # dedup code piece
                if code_piece not in code_piece_set:
                    data_bundle = DataBundle(data_dict={"filepath": filepath, "code": code_piece})
                    self._emit(data_bundle)
        except:
            logger.warn("handle python file: {} failed".format(filepath))

    def _filter(self, line):
        # ignore leading spaces
        line = line[string_util.get_left_padding_spaces(line) : ]
        # empty line
        if line == "":
            return True
        # comments
        if line.startswith("#") or line.startswith("'''") or line.startswith('"""'):
            return True
        return False
