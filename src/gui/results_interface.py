from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QFrame, QScrollArea, QToolTip,
                            QDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QCursor
from datetime import datetime
import sys
from src.utils.file_utils import load_fugl_meyer_tests

class ExerciseDetailsDialog(QDialog):
    def __init__(self, exercise, affected_score=None, unaffected_score=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Exercise Details")
        self.setFixedSize(500, 250)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel(exercise['name'])
        title_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #1a237e;
                background-color: transparent;
            }
        """)
        layout.addWidget(title_label)
        
        # Instructions
        instructions_label = QLabel("Instructions:")
        instructions_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #1a237e;
                background-color: transparent;
                margin-top: 10px;
            }
        """)
        layout.addWidget(instructions_label)
        
        desc_label = QLabel(exercise['instructions'])
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #2c3e50;
                background-color: transparent;
                padding: 5px;
            }
        """)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Scores frame
        scores_frame = QFrame()
        scores_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 4px;
                padding: 15px;
                margin-top: 10px;
            }
        """)
        scores_layout = QVBoxLayout(scores_frame)
        scores_layout.setSpacing(10)
        
        # Affected score
        affected_label = QLabel(f"Affected Side Score: {'Skipped' if affected_score is None else f'{affected_score}/{exercise['max_score']}'}")
        affected_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #1a237e;
                background-color: transparent;
                font-weight: bold;
            }
        """)
        scores_layout.addWidget(affected_label)
        
        # Unaffected score
        unaffected_label = QLabel(f"Unaffected Side Score: {'Skipped' if unaffected_score is None else f'{unaffected_score}/{exercise['max_score']}'}")
        unaffected_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #1a237e;
                background-color: transparent;
                font-weight: bold;
            }
        """)
        scores_layout.addWidget(unaffected_label)
        
        layout.addWidget(scores_frame)
        layout.addStretch()

class ResultsInterface:
    def __init__(self, results, affected_side):
        self.results = results
        self.affected_side = affected_side
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.window = QMainWindow()
        self.window.setWindowTitle("Fugl Meyer Assessment Results")
        self.window.setGeometry(100, 100, 1000, 800)
        
        # Set window background to white
        self.window.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
        """)
        
        # Load exercise data for titles
        self.exercise_data = load_fugl_meyer_tests()
        self.exercise_map = {ex['id']: ex for ex in self.exercise_data['exercises']} if self.exercise_data else {}
        
        # Create central widget and main layout
        central_widget = QWidget()
        central_widget.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
            }
        """)
        self.window.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(15, 10, 15, 10)
        
        # Create main title
        self.create_main_title(main_layout)
        
        # Create title and date
        self.create_header(main_layout)
        
        # Create content container
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(10)
        
        # Create summary section
        self.create_summary_section(content_layout)
        
        # Create scores list
        self.create_scores_list(content_layout)
        
        main_layout.addWidget(content_frame)
        
    def create_main_title(self, parent_layout):
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background-color: #1a237e;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(5, 5, 5, 5)
        
        title_label = QLabel("Fugl-Meyer Assessment")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: white;
                background-color: transparent;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title_label)
        
        parent_layout.addWidget(title_frame)
        
    def create_header(self, parent_layout):
        # Title
        title_label = QLabel("These are your results for today's session")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #1a237e;
                padding: 2px;
                background-color: transparent;
            }
        """)
        parent_layout.addWidget(title_label)
        
        # Date and time
        current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        date_label = QLabel(current_time)
        date_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #546e7a;
                padding: 0px 5px;
                background-color: transparent;
            }
        """)
        parent_layout.addWidget(date_label)
        
    def create_summary_section(self, parent_layout):
        # Card container for summary
        summary_card = QFrame()
        summary_card.setStyleSheet("""
            QFrame {
                background-color: #bfc3cc;
                border-radius: 18px;
                border: none;
                padding: 10px 14px 10px 14px;
            }
        """)
        summary_layout = QVBoxLayout(summary_card)
        summary_layout.setSpacing(8)
        summary_layout.setContentsMargins(0, 0, 0, 0)

        # Section title
        summary_label = QLabel("Summary")
        summary_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #1a237e;
                background-color: transparent;
                margin-bottom: 2px;
            }
        """)
        summary_layout.addWidget(summary_label)

        # Overall Score (blue pill)
        total_score = self.results.total_score
        max_possible = sum(exercise['max_score'] for exercise in self.exercise_data['exercises'])
        percentage = (total_score / max_possible * 100) if max_possible > 0 else 0
        overall_frame = QFrame()
        overall_frame.setStyleSheet("""
            QFrame {
                background-color: #8fa6e6;
                border-radius: 14px;
                border: none;
                padding: 8px 16px;
            }
        """)
        overall_layout = QHBoxLayout(overall_frame)
        overall_layout.setContentsMargins(0, 0, 0, 0)
        overall_layout.setSpacing(0)
        overall_label = QLabel("Overall Score")
        overall_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #1a237e;
                background-color: transparent;
            }
        """)
        overall_value = QLabel(f"{total_score}/{max_possible} ({percentage:.0f}%)")
        overall_value.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #1a237e;
                background-color: transparent;
            }
        """)
        overall_layout.addWidget(overall_label)
        overall_layout.addStretch()
        overall_layout.addWidget(overall_value)
        summary_layout.addWidget(overall_frame)


        asymmetry = self.results.generate_report()['asymmetry_index']
        pills_row = QFrame()
        pills_row.setStyleSheet("QFrame { background: transparent; border: none; }")
        pills_layout = QHBoxLayout(pills_row)
        pills_layout.setContentsMargins(0, 0, 0, 0)
        pills_layout.setSpacing(0)
 
        symmetry_pill = QLabel(f"Symmetry index  <b>{asymmetry:.0f}%</b>")
        symmetry_pill.setStyleSheet("""
            QLabel {
                background-color: #d6e9c6;
                color: #1a237e;
                border-radius: 12px;
                border: none;
                padding: 4px 14px;
                font-size: 15px;
            }
        """)
        # Affected side pill
        affected_pill = QLabel(f"Affected side  <b>{self.affected_side.upper()}</b>")
        affected_pill.setStyleSheet("""
            QLabel {
                background-color: #f7c7a3;
                color: #1a237e;
                border-radius: 12px;
                border: none;
                padding: 4px 14px;
                font-size: 15px;
            }
        """)
        pills_layout.addWidget(symmetry_pill)
        pills_layout.addStretch()
        pills_layout.addWidget(affected_pill)
        summary_layout.addWidget(pills_row)
        parent_layout.addWidget(summary_card)
        
    def create_scores_list(self, parent_layout):
        # Card container for scores
        scores_card = QFrame()
        scores_card.setStyleSheet("""
            QFrame {
                background-color: #bfc3cc;
                border-radius: 18px;
                border: none;
                padding: 10px 14px 10px 14px;
            }
        """)
        scores_layout = QVBoxLayout(scores_card)
        scores_layout.setSpacing(8)
        scores_layout.setContentsMargins(0, 0, 0, 0)

        # Section title
        scores_label = QLabel("Exercise scores")
        scores_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #1a237e;
                background-color: transparent;
                margin-bottom: 2px;
            }
        """)
        scores_layout.addWidget(scores_label)

        # Scroll area for exercises
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #bfc3cc;
            }
        """)
        scores_widget = QWidget()
        exercises_layout = QVBoxLayout(scores_widget)
        exercises_layout.setSpacing(8)
        exercises_layout.setContentsMargins(0, 0, 0, 0)
        for exercise in self.exercise_data['exercises']:
            exercise_id = exercise['id']
            ex_frame = QFrame()
            ex_frame.setStyleSheet("""
                QFrame {
                    background-color: #f5f6fa;
                    border-radius: 14px;
                    border: none;
                }
            """)
            ex_layout = QHBoxLayout(ex_frame)
            ex_layout.setContentsMargins(16, 4, 16, 4)
            ex_layout.setSpacing(0)
            title_label = QLabel(exercise['name'])
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 15px;
                    color: #1a237e;
                    background-color: transparent;
                }
            """)
            if exercise_id in self.results.affected_scores:
                score = self.results.affected_scores[exercise_id]
                max_score = exercise['max_score']
                score_label = QLabel(f"<b>{score}</b>")
                score_label.setStyleSheet("""
                    QLabel {
                        font-size: 18px;
                        color: #1a237e;
                        background-color: transparent;
                        font-weight: bold;
                    }
                """)
            else:
                score_label = QLabel("<i>Skipped</i>")
                score_label.setStyleSheet("""
                    QLabel {
                        font-size: 15px;
                        color: #78909c;
                        background-color: transparent;
                        font-style: italic;
                    }
                """)
            ex_layout.addWidget(title_label)
            ex_layout.addStretch()
            ex_layout.addWidget(score_label)
            # Restore clickable modal
            ex_frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            ex_frame.mousePressEvent = lambda event, e=exercise, a=self.results.affected_scores.get(exercise_id), u=self.results.unaffected_scores.get(exercise_id): self.show_exercise_details(e, a, u)
            exercises_layout.addWidget(ex_frame)
        exercises_layout.addStretch()
        scroll.setWidget(scores_widget)
        scores_layout.addWidget(scroll)
        parent_layout.addWidget(scores_card)
        
    def show_exercise_details(self, exercise, affected_score, unaffected_score):
        dialog = ExerciseDetailsDialog(exercise, affected_score, unaffected_score, self.window)
        dialog.exec()
        
    def get_exercise_title(self, exercise_id):
        if exercise_id in self.exercise_map:
            return self.exercise_map[exercise_id]['name']
        return exercise_id
        
    def get_exercise_max_score(self, exercise_id):
        if exercise_id in self.exercise_map:
            return self.exercise_map[exercise_id]['max_score']
        return self.results.max_possible_score
        
    def show(self):
        self.window.show()
        return self.app.exec() 