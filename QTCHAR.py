import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPlainTextEdit, QPushButton, QGroupBox, QCheckBox, 
                             QLabel, QSpinBox, QLineEdit)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Qt_Page(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("零宽字符工具")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Input box
        self.input_box = QPlainTextEdit()
        self.input_box.setPlaceholderText("在这里输入内容...")
        left_layout.addWidget(QLabel("输入:"))
        left_layout.addWidget(self.input_box)

        # Output box
        self.output_box = QPlainTextEdit()
        self.output_box.setReadOnly(True)
        left_layout.addWidget(QLabel("输出:"))
        left_layout.addWidget(self.output_box)

        # Character limit
        limit_layout = QHBoxLayout()
        self.limit_checkbox = QCheckBox("启用字符限制:")
        self.limit_spinbox = QSpinBox()
        self.limit_spinbox.setRange(1, 1000)
        self.limit_spinbox.setValue(10)
        limit_layout.addWidget(self.limit_checkbox)
        limit_layout.addWidget(self.limit_spinbox)
        right_layout.addLayout(limit_layout)

        # Checkbox group
        self.checkbox_group = QGroupBox("选择想要插入的字符:")
        self.checkbox_layout = QVBoxLayout()
        self.checkboxes = {}
        
        characters = {
            "ZWSP[OK]": "\u200B",
            "ZWNBSP": "\uFEFF",
            "ZWJ[OK]": "\u200D",
            "ZWNJ": "\u200C",
            "Word Joiner": "\u2060",
            "Soft Hyphen": "\u00AD",
            "LRM": "\u200E",
            "RLM": "\u200F",
            "Line Separator": "\u2028",
            "Paragraph Separator": "\u2029"
        }

        default_checked = ["ZWSP", "ZWNBSP", "ZWJ", "ZWNJ", "Word Joiner", "Soft Hyphen", "LRM", "RLM"]

        for name, char in characters.items():
            checkbox = QCheckBox(name)
            checkbox.setChecked(name in default_checked)
            self.checkboxes[name] = (checkbox, char)
            self.checkbox_layout.addWidget(checkbox)

        self.checkbox_group.setLayout(self.checkbox_layout)
        right_layout.addWidget(self.checkbox_group)

        # Convert button
        self.convert_button = QPushButton("转换")
        self.convert_button.clicked.connect(self.convert)
        right_layout.addWidget(self.convert_button)

        # Stats label
        self.stats_label = QLabel()
        right_layout.addWidget(self.stats_label)

        # Copy button
        self.copy_button = QPushButton("复制结果")
        self.copy_button.clicked.connect(self.copy_result)
        right_layout.addWidget(self.copy_button)

        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 1)
        self.setLayout(main_layout)

    def convert(self):
        input_text = self.input_box.toPlainText()
        selected_chars = []
        
        for name, (checkbox, char) in self.checkboxes.items():
            if checkbox.isChecked():
                selected_chars.append(char)

        if not selected_chars:
            self.output_box.setPlainText("请选择至少一个要插入的字符。")
            return

        output_text = ""
        inserted_count = 0
        char_limit = self.limit_spinbox.value() if self.limit_checkbox.isChecked() else float('inf')

        for i, char in enumerate(input_text):
            output_text += char
            if i < len(input_text) - 1 and inserted_count < char_limit:
                for selected_char in selected_chars:
                    if inserted_count < char_limit:
                        output_text += selected_char
                        inserted_count += 1
                    else:
                        break

        self.output_box.setPlainText(output_text)

        # Update stats
        input_count = len(input_text)
        output_count = len(output_text)
        self.stats_label.setText(f"输入量: {input_count} → 插入量: {inserted_count} → 输出量: {output_count}")

    def copy_result(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_box.toPlainText())

def run():
    app = QApplication(sys.argv)
    ex = Qt_Page()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()