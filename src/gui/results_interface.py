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
        self.setFixedSize(500, 400)
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
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 20, 30, 20)
        
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
                padding: 10px;
            }
        """)
        title_layout = QVBoxLayout(title_frame)
        
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
        summary_label = QLabel("Summary")
        summary_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #1a237e;
                background-color: transparent;
            }
        """)
        parent_layout.addWidget(summary_label)
        
        # Calculate scores
        total_score = self.results.total_score
        max_possible = sum(exercise['max_score'] for exercise in self.exercise_data['exercises'])
        percentage = (total_score / max_possible * 100) if max_possible > 0 else 0
        asymmetry = self.results.generate_report()['asymmetry_index']
        
        # Create score layout
        score_layout = QVBoxLayout()
        score_layout.setSpacing(10)
        
        # Total score
        total_label = QLabel(f"Overall Score: {total_score}/{max_possible} ({percentage:.1f}%)")
        total_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1a237e;
                background-color: transparent;
                padding: 12px;
                border-radius: 4px;
                background-color: #e3f2fd;
            }
        """)
        score_layout.addWidget(total_label)
        
        # Affected side
        affected_side_label = QLabel(f"Affected Side: {self.affected_side.capitalize()}")
        affected_side_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #1a237e;
                background-color: transparent;
                padding: 8px;
                border-radius: 4px;
                background-color: #e8f5e9;
            }
        """)
        score_layout.addWidget(affected_side_label)
        
        asymmetry_label = QLabel(f"Symmetry Index: {asymmetry:.1f}%")
        asymmetry_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #1a237e;
                background-color: transparent;
                padding: 8px;
                border-radius: 4px;
                background-color: #fff3e0;
            }
        """)
        score_layout.addWidget(asymmetry_label)
        
        parent_layout.addLayout(score_layout)
        
    def create_scores_list(self, parent_layout):
        scores_label = QLabel("Detailed Scores")
        scores_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #1a237e;
                background-color: transparent;
                margin-top: 10px;
            }
        """)
        parent_layout.addWidget(scores_label)
        
        # Create scrollable area for scores
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        scores_widget = QWidget()
        scores_layout = QVBoxLayout(scores_widget)
        scores_layout.setSpacing(8)
        
        # Add scores for all exercises
        for exercise in self.exercise_data['exercises']:
            exercise_id = exercise['id']
            exercise_frame = QFrame()
            exercise_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 4px;
                }
                QFrame:hover {
                    border: 1px solid #90caf9;
                    background-color: #f5f9ff;
                }
            """)
            exercise_frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            
            exercise_layout = QHBoxLayout(exercise_frame)
            exercise_layout.setContentsMargins(8, 3, 8, 3)
            
            # Exercise title
            title_label = QLabel(exercise['name'])
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    color: #2c3e50;
                    background-color: transparent;
                }
            """)
            
            # Score or Skipped label
            if exercise_id in self.results.affected_scores:
                score = self.results.affected_scores[exercise_id]
                max_score = exercise['max_score']
                score_label = QLabel(f"{score}/{max_score}")
                score_label.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        color: #1a237e;
                        background-color: transparent;
                        font-weight: bold;
                    }
                """)
            else:
                score_label = QLabel("Skipped")
                score_label.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        color: #78909c;
                        background-color: transparent;
                        font-style: italic;
                    }
                """)
            
            exercise_layout.addWidget(title_label)
            exercise_layout.addStretch()
            exercise_layout.addWidget(score_label)
            
            # Connect click event
            exercise_frame.mousePressEvent = lambda event, e=exercise, a=self.results.affected_scores.get(exercise_id), u=self.results.unaffected_scores.get(exercise_id): self.show_exercise_details(e, a, u)
            
            scores_layout.addWidget(exercise_frame)
        
        scores_layout.addStretch()
        scroll.setWidget(scores_widget)
        parent_layout.addWidget(scroll)
        
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