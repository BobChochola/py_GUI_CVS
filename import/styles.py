# styles.py


class StyleSheet:
    MAIN = """
    QWidget {
        background-color: #f0f4f8;
        font-family: 'Segoe UI', Arial, sans-serif;
        color: black;
    }
    QLabel {
        font-size: 14px;
        color: #2d3748;
        margin-bottom: 3px;
    }
    QLineEdit, QComboBox, QSpinBox {
        padding: 8px;
        border: 1px solid #cbd5e0;
        border-radius: 4px;
        font-size: 14px;
        background-color: white;
    }
    QPushButton {
        background-color: #4299e1;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #3182ce;
    }
    QCheckBox, QRadioButton {
        font-size: 14px;
        spacing: 5px;
    }
    QGroupBox {
        font-size: 14px;
        font-weight: bold;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        margin-top: 15px;
        padding: 10px;
        background-color: #edf2f7;
    }
    QScrollArea {
        border: none;
    }
    QSpinBox::up-button {
        subcontrol-origin: margin;
    }
    QSpinBox::up-button:hover {
        top: 1px;
        left: 1px;
    }
    QSpinBox::down-button {
        subcontrol-origin: margin;
    }
    QSpinBox::down-button:hover {
        bottom: 1px;
        left: 1px;
    }
    """
