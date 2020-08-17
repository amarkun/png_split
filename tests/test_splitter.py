import os

from png_split.splitter import Splitter


def test_splitter_with_dir():
    sourceDir = os.getcwd()
    outputDir = os.path.join(sourceDir, 'output')
    splits = 3
    buffer = 20
    s = Splitter(sourceDir, outputDir, splits, buffer)
    assert s
    assert os.path.abspath(sourceDir) == s.source
    assert os.path.abspath(outputDir) == s.target
    assert splits == s.splits
    assert buffer == s.buffer
    assert s.isDir
    assert os.listdir(sourceDir) == s.dirContents


# def test_splitter_with_file():
#     sourceFile = './test.png'
#     outputDir = './outputs'
#     splits = 3
#     buffer = 20
#     s = Splitter(sourceFile, outputDir, splits, buffer)
#     assert os.path.abspath(sourceFile) == s.source
#     assert os.path.abspath(outputDir) == s.output
#     assert splits == s.splits
#     assert buffer == s.buffer
#     assert '.png' == s.fileExt
#     assert False is s.isDir
#     assert [] == s.dirContents