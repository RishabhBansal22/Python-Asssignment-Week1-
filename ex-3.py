# Exercise 3 : Student Marks Processor (20 points) 
# Develop a program that: 
# 1. Reads student marks data from a file (registration number, exam mark, coursework mark) 
# 2. Computes overall marks using given weighting 
# 3. Assigns grades based on specific rules 
# 4. Creates a structured NumPy array 
# 5. Sorts students by overall mark 
# 6. Writes results to an output file 
# 7. Displays grade statistics 
# 8. Handles all errors gracefully

import numpy as np
import os


class StudentMarksProcessor:
    """A class to process student marks data and generate grade reports."""
    
    def __init__(self, exam_weight=0.6, coursework_weight=0.4):
        """
        Initialize the processor with mark weightings.
        Default: 60% exam, 40% coursework.
        """
        self.exam_weight = exam_weight
        self.coursework_weight = coursework_weight
        self.students_data = None
    
    def read_marks_file(self, filename):
        """
        Reads student marks data from a file.
        Expected format: registration_number exam_mark coursework_mark
        Returns True if successful, False otherwise.
        """
        try:
            # Check if file exists
            if not os.path.exists(filename):
                print(f"Error: File '{filename}' not found!")
                return False
            
            # Lists to store data
            reg_numbers = []
            exam_marks = []
            coursework_marks = []
            
            # Read the file line by line
            with open(filename, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    
                    # Skip empty lines or comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Split the line into parts
                    parts = line.split()
                    
                    if len(parts) != 3:
                        print(f"Warning: Line {line_num} has invalid format. Skipping...")
                        continue
                    
                    try:
                        reg_num = parts[0]
                        exam = float(parts[1])
                        coursework = float(parts[2])
                        
                        # Validate marks are in valid range (0-100)
                        if not (0 <= exam <= 100 and 0 <= coursework <= 100):
                            print(f"Warning: Line {line_num} has marks out of range (0-100). Skipping...")
                            continue
                        
                        reg_numbers.append(reg_num)
                        exam_marks.append(exam)
                        coursework_marks.append(coursework)
                        
                    except ValueError:
                        print(f"Warning: Line {line_num} has invalid numeric values. Skipping...")
                        continue
            
            if not reg_numbers:
                print("Error: No valid student data found in the file!")
                return False
            
            # Calculate overall marks
            overall_marks = [
                (exam * self.exam_weight) + (coursework * self.coursework_weight)
                for exam, coursework in zip(exam_marks, coursework_marks)
            ]
            
            # Assign grades
            grades = [self.assign_grade(mark) for mark in overall_marks]
            
            # Create structured NumPy array
            self.students_data = np.array(
                list(zip(reg_numbers, exam_marks, coursework_marks, overall_marks, grades)),
                dtype=[
                    ('reg_number', 'U20'),
                    ('exam_mark', 'f4'),
                    ('coursework_mark', 'f4'),
                    ('overall_mark', 'f4'),
                    ('grade', 'U2')
                ]
            )
            
            print(f"Successfully read {len(reg_numbers)} student records.")
            return True
            
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
    
    def assign_grade(self, overall_mark):
        """
        Assigns a grade based on the overall mark.
        Grading rules:
        - A: 70 and above
        - B: 60-69
        - C: 50-59
        - D: 40-49
        - F: Below 40
        """
        if overall_mark >= 70:
            return 'A'
        elif overall_mark >= 60:
            return 'B'
        elif overall_mark >= 50:
            return 'C'
        elif overall_mark >= 40:
            return 'D'
        else:
            return 'F'
    
    def sort_by_overall_mark(self):
        """
        Sorts students by overall mark in descending order.
        """
        if self.students_data is not None:
            # Sort in descending order (highest marks first)
            self.students_data = np.sort(self.students_data, order='overall_mark')[::-1]
    
    def write_results(self, output_filename):
        """
        Writes the processed results to an output file.
        Returns True if successful, False otherwise.
        """
        try:
            if self.students_data is None:
                print("Error: No data to write!")
                return False
            
            with open(output_filename, 'w') as file:
                # Write header
                file.write("=" * 80 + "\n")
                file.write("STUDENT MARKS REPORT\n")
                file.write("=" * 80 + "\n\n")
                file.write(f"Weighting: Exam {self.exam_weight*100:.0f}%, Coursework {self.coursework_weight*100:.0f}%\n\n")
                
                # Write column headers
                file.write(f"{'Reg Number':<15} {'Exam':<8} {'Coursework':<12} {'Overall':<10} {'Grade':<5}\n")
                file.write("-" * 80 + "\n")
                
                # Write student data
                for student in self.students_data:
                    file.write(
                        f"{student['reg_number']:<15} "
                        f"{student['exam_mark']:<8.2f} "
                        f"{student['coursework_mark']:<12.2f} "
                        f"{student['overall_mark']:<10.2f} "
                        f"{student['grade']:<5}\n"
                    )
                
                file.write("\n" + "=" * 80 + "\n")
            
            print(f"Results written to '{output_filename}' successfully.")
            return True
            
        except Exception as e:
            print(f"Error writing to file: {e}")
            return False
    
    def display_statistics(self):
        """
        Displays grade statistics including count and percentage for each grade.
        """
        if self.students_data is None:
            print("Error: No data available for statistics!")
            return
        
        print("\n" + "=" * 60)
        print("GRADE STATISTICS")
        print("=" * 60)
        
        # Count grades
        grades = ['A', 'B', 'C', 'D', 'F']
        total_students = len(self.students_data)
        
        print(f"\nTotal Students: {total_students}\n")
        print(f"{'Grade':<10} {'Count':<10} {'Percentage':<15}")
        print("-" * 60)
        
        for grade in grades:
            count = np.sum(self.students_data['grade'] == grade)
            percentage = (count / total_students * 100) if total_students > 0 else 0
            print(f"{grade:<10} {count:<10} {percentage:<15.2f}%")
        
        # Calculate and display average marks
        avg_exam = np.mean(self.students_data['exam_mark'])
        avg_coursework = np.mean(self.students_data['coursework_mark'])
        avg_overall = np.mean(self.students_data['overall_mark'])
        
        print("\n" + "-" * 60)
        print("\nAVERAGE MARKS")
        print("-" * 60)
        print(f"Average Exam Mark:       {avg_exam:.2f}")
        print(f"Average Coursework Mark: {avg_coursework:.2f}")
        print(f"Average Overall Mark:    {avg_overall:.2f}")
        print("\n" + "=" * 60)
    
    def run(self):
        """
        Main method to run the student marks processor.
        """
        print("=" * 60)
        print("STUDENT MARKS PROCESSOR")
        print("=" * 60)
        
        try:
            # Get input file name
            input_file = input("\nEnter the input file name (default: student_marks.txt): ").strip()
            if not input_file:
                input_file = "student_marks.txt"
            
            # Read the marks file
            if not self.read_marks_file(input_file):
                return
            
            # Sort students by overall mark
            self.sort_by_overall_mark()
            print("Students sorted by overall mark (descending).")
            
            # Get output file name
            output_file = input("Enter the output file name (default: results.txt): ").strip()
            if not output_file:
                output_file = "results.txt"
            
            # Write results to file
            if not self.write_results(output_file):
                return
            
            # Display statistics
            self.display_statistics()
            
            print("\nProcessing completed successfully!")
            
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Create processor with default weighting (60% exam, 40% coursework)
    processor = StudentMarksProcessor()
    processor.run()