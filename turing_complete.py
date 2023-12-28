import sys
from PyQt5.QtWidgets import QPushButton, QComboBox, QLineEdit, QLabel, QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QPointF,  QSequentialAnimationGroup
import yaml
from visualize import visualize_turing_machine
from tape_item import TapeItem
from styles import *
from head_item import HeadItem
from turing_machine import *

class TuringMachineWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_iter = 0
        self.iter_limit = 500
        self.setStyleSheet("QMainWindow { background-color: white; }")
        self.sequential_group = QSequentialAnimationGroup(self)
        self.input = ''
        self.loaded = False
        self.transitioned = False
    
        self.scene = QGraphicsScene(self)
        self.tape_length = 101
        self.tape_items = [TapeItem(' ', i) for i in range(self.tape_length)]
        self.head_initial_position = 50
        self.head_position = self.head_initial_position
        self.head_item = HeadItem(self.head_position)
        self.draw_tape()
        
        # Apply the stylesheet to each button
        self.load_button = QPushButton("Load")
        self.load_button.setStyleSheet(button_stylesheet)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setStyleSheet(button_stylesheet)

        self.step_button = QPushButton("Step")
        self.step_button.setStyleSheet(button_stylesheet)

        self.run_machine_button = QPushButton("Run")
        self.run_machine_button.setStyleSheet(button_stylesheet)

        self.load_button.clicked.connect(self.load)
        self.reset_button.clicked.connect(self.reset)
        self.step_button.clicked.connect(self.step)
        self.run_machine_button.clicked.connect(self.run)
        

        controls_layout = QVBoxLayout()

        user_controls_layout = QHBoxLayout()

        # Apply the stylesheet to QLineEdit and QComboBox
        self.input_box = QLineEdit()
        self.input_box.setStyleSheet(widget_stylesheet)

        self.program_selector = QComboBox()
        self.program_selector.setStyleSheet(widget_stylesheet)

        user_controls_layout.addWidget(self.input_box)
        user_controls_layout.addWidget(self.program_selector)
        # Layout for buttons
        program_controls_layout = QHBoxLayout()

        program_controls_layout.addWidget(self.load_button)
        program_controls_layout.addWidget(self.reset_button)
        program_controls_layout.addWidget(self.step_button)
        program_controls_layout.addWidget(self.run_machine_button)

        controls_layout.addLayout(user_controls_layout)
        controls_layout.addLayout(program_controls_layout)

        font = QFont()
        font.setFamily('roboto')
        font.setPointSize(20)

        self.yaml_dict = {
            "Binary Increment": "binary_inc.yaml",
            "Divisible by 3 (binary)": "divisible_by_3_binary.yaml",
            "Divisible by 3 (base 10)": "divisible_by_3_base_10.yaml",
            "Binary Multiplication": "binary_mult.yaml"
        }

        self.program_selector.addItems(list(self.yaml_dict.keys()))

        self.file_path = self.yaml_dict[self.program_selector.currentText()]

        self.turing_machine = TuringMachine(self.parse_yaml_file(self.file_path))
        self.current_state = self.turing_machine.initial_state
        
        # Main layout
        main_layout = QVBoxLayout()
        tape_view = QGraphicsView(self.scene)

       # Assuming matplotlib_graph is an instance of the MatplotlibGraph class
        self.diagram_image_label = QLabel(self)
        self.diagram_pixmap = QPixmap('diagram.png')
        self.diagram_image_label.setPixmap(self.diagram_pixmap)
        self.diagram_image_label.setAlignment(Qt.AlignCenter)

        #matplotlib_graph = MatplotlibGraph(self.turing_machine)

        title_for_user = QLabel("Turing Machine Simulator")
        self.program_state = QLabel("")
        title_for_user.setStyleSheet(title_stylesheet)
        title_for_user.setAlignment(Qt.AlignCenter)
        title_for_user.setFont(font)
        main_layout.addWidget(title_for_user)
        main_layout.addWidget(self.program_state)
        main_layout.addWidget(self.diagram_image_label)
        main_layout.addWidget(tape_view, 1)  # Tape view takes most of the space
        main_layout.addLayout(controls_layout)  # Button layout
        

        # Widget to hold everything
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def draw_tape(self):
        self.scene.clear()
        for tape_item in self.tape_items:
            self.scene.addItem(tape_item)
        self.scene.addItem(self.head_item)

    def move_head_left(self, symbol, head_position):
        if self.head_position > 0:
            position_animation = QPropertyAnimation(self.head_item, b'pos')
            position_animation.setStartValue(QPointF(self.head_position * 50, -40))
            self.head_position -= 1
            position_animation.setEndValue(QPointF(self.head_position * 50, -40))
            position_animation.setDuration(250)
            def change_text():
                if symbol != '':
                    self.tape_items[head_position].text_item.setPlainText(symbol)
            position_animation.finished.connect(change_text)
            self.sequential_group.addAnimation(position_animation)
            self.sequential_group.addPause(250)

    def move_head_right(self, symbol, head_position):
        if self.head_position < self.tape_length - 1:
            position_animation = QPropertyAnimation(self.head_item, b'pos')
            position_animation.setStartValue(QPointF(self.head_position * 50, -40))
            self.head_position += 1
            position_animation.setEndValue(QPointF(self.head_position * 50, -40))
            position_animation.setDuration(250)
            def change_text():
                if symbol != '':
                    self.tape_items[head_position].text_item.setPlainText(symbol)            
            position_animation.finished.connect(change_text)
            self.sequential_group.addAnimation(position_animation)
            self.sequential_group.addPause(250)

    def step_move_head_right(self):
        if self.head_position < self.tape_length - 1:
            position_animation = QPropertyAnimation(self.head_item, b'pos')
            position_animation.setStartValue(QPointF(self.head_position * 50, -40))
            self.head_position += 1
            position_animation.setEndValue(QPointF(self.head_position * 50, -40))
            position_animation.setDuration(250)
            self.sequential_group.addAnimation(position_animation)
            self.sequential_group.addPause(250)

    def step_move_head_left(self):
        if self.head_position > 0:
            position_animation = QPropertyAnimation(self.head_item, b'pos')
            position_animation.setStartValue(QPointF(self.head_position * 50, -40))
            self.head_position -= 1
            position_animation.setEndValue(QPointF(self.head_position * 50, -40))
            position_animation.setDuration(250)
            self.sequential_group.addAnimation(position_animation)
            self.sequential_group.addPause(250)

    def run(self):
        self.current_iter = 0
        if not self.loaded: 
            msg = QMessageBox()
            msg.setWindowTitle('Machine not loaded')
            msg.setText("The machine was not loaded, please type in your input and click the load button")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec_()
            return
        while self.current_state != self.turing_machine.accept_state and self.current_iter <= self.iter_limit:
            self.transitioned = False
            for transition in self.turing_machine.transitions:
                if self.current_state == transition['current_state'] and \
                    self.tape_items[self.head_position].value in [str(item) for item in transition['input_symbol']]: 
                    self.transitioned = True
                    self.current_state = transition['next_state']
                    if transition['write_symbol'] != '':
                        self.tape_items[self.head_position].value = str(transition['write_symbol'])
                    if transition['move'] == 'R':
                        self.move_head_right(str(transition['write_symbol']), self.head_position)
                    elif transition['move'] == "L":
                        self.move_head_left(str(transition['write_symbol']), self.head_position)
            if not self.transitioned:
                break
            self.current_iter += 1
        self.sequential_group.start()
        self.sequential_group.finished.connect(self.run_terminated)

        
        
    def step(self):
        if not self.loaded:
            msg = QMessageBox()
            msg.setWindowTitle('Machine not loaded')
            msg.setText("The machine was not loaded, please type in your input and click the load button")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec_()
            return
        self.transitioned = False
        for transition in self.turing_machine.transitions:
            if self.current_state == transition['current_state'] and \
                self.tape_items[self.head_position].value in [str(item) for item in transition['input_symbol']]:
                self.transitioned = True
                self.current_state = transition['next_state']
                if transition['write_symbol'] != '':
                    self.tape_items[self.head_position].text_item.setPlainText(str(transition['write_symbol']))
                    self.tape_items[self.head_position].value = str(transition['write_symbol'])
                    self.sequential_group.addPause(250)
                if transition['move'] == 'R':
                    self.step_move_head_right()
                elif transition['move'] == "L":
                    self.step_move_head_left()
                break
        self.sequential_group.start()
        self.sequential_group.finished.connect(self.run_terminated)

    def run_terminated(self):
        if self.current_state == self.turing_machine.accept_state:
            self.program_state.setText("ACCEPTED")
            self.program_state.setStyleSheet(accepted_stylesheet)

        elif self.current_state in [str(item) for item in self.turing_machine.reject_state] and not self.transitioned:
            self.program_state.setText("Rejected")
            self.program_state.setStyleSheet(rejected_stylesheet)

        elif self.current_iter >= self.iter_limit:
            self.program_state.setText("too many iterations")
            self.program_state.setStyleSheet(rejected_stylesheet)
        
        self.sequential_group.clear()

    def load(self):
        self.reset()
        if self.input_box.text() == "":
            msg = QMessageBox()
            msg.setWindowTitle('no input provided')
            msg.setText("You didn't enter any input, if your program doesn't require input type in a space")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec_()    
            return    
            
        self.input = self.input_box.text()
        for character, tapeItem in zip(self.input, self.tape_items[self.head_initial_position: self.head_initial_position + len(self.input)]):
            tapeItem.text_item.setPlainText(character)
            tapeItem.value = character
        
        self.file_path = self.yaml_dict[self.program_selector.currentText()]
        self.turing_machine = TuringMachine(self.parse_yaml_file(self.file_path))
        self.diagram_pixmap = QPixmap('diagram.png')
        self.diagram_image_label.setPixmap(self.diagram_pixmap)
        self.diagram_image_label.setAlignment(Qt.AlignCenter)
        self.current_state = self.turing_machine.initial_state
        self.loaded = True

    def reset(self):
        self.program_state.setStyleSheet(hide_stylesheet)
        self.sequential_group.clear()
        self.loaded = False
        self.clear_tape()
        self.head_position = self.head_initial_position
        self.head_item.setPos(QPointF(self.head_position * 50, -40)) 

        self.file_path = self.yaml_dict[self.program_selector.currentText()]
        self.turing_machine = TuringMachine(self.parse_yaml_file(self.file_path))
        self.diagram_pixmap = QPixmap('diagram.png')
        self.diagram_image_label.setPixmap(self.diagram_pixmap)
        self.diagram_image_label.setAlignment(Qt.AlignCenter)
        self.current_state = self.turing_machine.initial_state

    def clear_tape(self):
        for item in self.tape_items:
            item.text_item.setPlainText(' ')
            item.value = ' '
    
    def parse_yaml_file(self, file_path):
        with open(file_path, 'r') as file:
            yaml_file = yaml.safe_load(file)
            visualize_turing_machine(yaml_file)
            return yaml_file
        
def main():
    app = QApplication(sys.argv)
    tape_window = TuringMachineWindow()
    tape_window.setGeometry(100, 100, 800, 500)
    tape_window.setWindowTitle('Turing Machine Simulator')
    tape_window.setWindowIcon(QIcon('icon.png'))
    tape_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
