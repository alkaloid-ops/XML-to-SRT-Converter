import sys
import os
import xml.etree.ElementTree as ET
from datetime import timedelta
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox


def convert_time(frame, frame_rate):
    """将帧号转换为 SRT 格式的时间。"""
    sec = frame / frame_rate
    td = timedelta(seconds=sec)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{td.microseconds // 1000:03}"


def xml_to_srt(xml_file, srt_directory):
    """将 XML 转换为 SRT 格式的文件，并保存在指定目录。"""
    srt_file = os.path.join(srt_directory, os.path.splitext(os.path.basename(xml_file))[0] + '.srt')
    tree = ET.parse(xml_file)
    root = tree.getroot()
    frame_rate = int(root.find(".//timebase").text)

    with open(srt_file, 'w') as f:
        for i, child in enumerate(root.iter('generatoritem'), start=1):
            start_time_str = child.find('start').text
            end_time_str = child.find('end').text
            text = child.find(".//parameter[parameterid='str']/value").text.strip()

            if not all([start_time_str, end_time_str, text]):
                continue

            start_time = int(start_time_str)
            end_time = int(end_time_str)
            f.write(f'{i}\n')
            f.write(f'{convert_time(start_time, frame_rate)} --> {convert_time(end_time, frame_rate)}\n')
            f.write(f'{text}\n\n')


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.xml_directory = ""
        self.srt_directory = ""
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.btn_choose_xml_dir = QPushButton('选择导入 XML 目录', self)
        self.btn_choose_xml_dir.clicked.connect(self.openDirectoryDialog)
        layout.addWidget(self.btn_choose_xml_dir)

        self.btn_choose_srt_dir = QPushButton('选择导出 SRT 目录', self)
        self.btn_choose_srt_dir.clicked.connect(self.openSRTDirectoryDialog)
        layout.addWidget(self.btn_choose_srt_dir)

        self.convert_btn = QPushButton('开始转换', self)
        self.convert_btn.clicked.connect(self.convert_files)
        layout.addWidget(self.convert_btn)

        self.setLayout(layout)
        self.setWindowTitle('XML2SRT')
        self.show()

    def openDirectoryDialog(self):
        directory = QFileDialog.getExistingDirectory(self, "选择导入 XML 目录")
        if directory:
            self.xml_directory = directory
            self.btn_choose_xml_dir.setText(os.path.basename(directory))

    def openSRTDirectoryDialog(self):
        directory = QFileDialog.getExistingDirectory(self, "选择导出 SRT 目录")
        if directory:
            self.srt_directory = directory
            self.btn_choose_srt_dir.setText(os.path.basename(directory))

    def convert_files(self):
        if not self.srt_directory or not self.xml_directory:
            QMessageBox.warning(self, "错误", "请选择 XML 目录和导出目录")
            return
        xml_files = [os.path.join(self.xml_directory, f) for f in os.listdir(self.xml_directory) if f.endswith('.xml')]
        for xml_file in xml_files:
            xml_to_srt(xml_file, self.srt_directory)
        QMessageBox.information(self, "转换完成！", f"已成功转换 {len(xml_files)} 个文件到目录 {self.srt_directory}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
