import json
import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from typing import Dict, List, Optional

# 한글 폰트 설정
try:
    font_path = 'C:\\Windows\\Fonts\\malgun.ttf'
    if os.path.exists(font_path):
        font = fm.FontProperties(fname=font_path)
        plt.rcParams['font.sans-serif'] = ['Malgun Gothic']
    else:
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
except:
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

plt.rcParams['axes.unicode_minus'] = False

class GradeAnalyzer:
    def __init__(self, data_file: str = 'grades.json'):
        self.data_file = data_file
        self.grades: Dict = self.load_grades()
        self.quiz_db = self.load_quiz_db()

    def load_grades(self) -> Dict:
        """저장된 성적 데이터 불러오기"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_grades(self):
        """성적 데이터 저장"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.grades, f, ensure_ascii=False, indent=2)

    def load_quiz_db(self) -> Dict:
        """퀴즈 데이터베이스 불러오기"""
        return {
            '국어': {
                (1, 1): {'단원1': ['한글의 자음과 모음은?', '다음 중 맞은 문장은?'],
                         '단원2': ['문법의 기본은?', '품사는 몇 가지인가?']},
                (1, 2): {'단원1': ['한국 문학의 시작은?', '고전 문학이란?'],
                         '단원2': ['현대 문학의 특징은?', '시와 소설의 차이는?']},
            },
            '수학': {
                (1, 1): {'단원1': ['1+1은?', '2×3은?'],
                         '단원2': ['10÷2는?', '5²는?']},
                (1, 2): {'단원1': ['√4는?', '방정식이란?'],
                         '단원2': ['함수의 정의는?', '그래프란?']},
            },
            '영어': {
                (1, 1): {'단원1': ['Hello는 무엇인가?', 'Good morning의 뜻은?'],
                         '단원2': ['알파벳은 몇 개인가?', 'ABC의 발음은?']},
                (1, 2): {'단원1': ['I am은 무엇인가?', 'You are은?'],
                         '단원2': ['Present tense란?', 'Past tense란?']},
            }
        }

    def add_grade(self, subject: str, score: float, semester_year: int = 1, semester_num: int = 1):
        """성적 추가"""
        if subject not in self.grades:
            self.grades[subject] = []

        self.grades[subject].append({
            'score': score,
            'year': semester_year,
            'semester': semester_num
        })
        self.save_grades()
        print(f"✅ {subject} 성적 {score}점이 추가되었습니다.")

    def get_average(self, subject: Optional[str] = None) -> float:
        """평균 계산"""
        if subject:
            if subject not in self.grades or not self.grades[subject]:
                return 0
            scores = [g['score'] for g in self.grades[subject]]
        else:
            all_scores = []
            for subject_grades in self.grades.values():
                all_scores.extend([g['score'] for g in subject_grades])
            if not all_scores:
                return 0
            scores = all_scores

        return sum(scores) / len(scores) if scores else 0

    def show_all_averages(self):
        """모든 과목의 평균 표시"""
        print("\n📊 과목별 평균")
        print("=" * 40)

        if not self.grades:
            print("등록된 성적이 없습니다.")
            return

        for subject in self.grades:
            avg = self.get_average(subject)
            count = len(self.grades[subject])
            print(f"{subject}: {avg:.2f}점 (입력된 성적: {count}개)")

        overall_avg = self.get_average()
        print(f"\n전체 평균: {overall_avg:.2f}점")

    def draw_graph(self, subject: Optional[str] = None):
        """성적 그래프 시각화"""
        if not self.grades:
            print("그래프를 그릴 성적이 없습니다.")
            return

        if subject:
            if subject not in self.grades:
                print(f"{subject} 성적이 없습니다.")
                return

            scores = [g['score'] for g in self.grades[subject]]
            plt.figure(figsize=(10, 6))
            plt.plot(range(1, len(scores) + 1), scores, marker='o', linewidth=2, markersize=8, label=subject)
            plt.axhline(y=self.get_average(subject), color='r', linestyle='--', label=f'평균: {self.get_average(subject):.2f}')
            plt.title(f'{subject} 성적 추이', fontsize=14, fontweight='bold')
            plt.xlabel('입력 순서', fontsize=12)
            plt.ylabel('성적 (점)', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.savefig(f'{subject}_grades.png', dpi=300, bbox_inches='tight')
            print(f"✅ {subject}_grades.png 파일이 저장되었습니다.")
            plt.show()
        else:
            # 모든 과목의 평균을 막대 그래프로
            subjects = list(self.grades.keys())
            averages = [self.get_average(s) for s in subjects]

            plt.figure(figsize=(10, 6))
            bars = plt.bar(subjects, averages, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
            plt.title('과목별 평균 성적', fontsize=14, fontweight='bold')
            plt.ylabel('평균 성적 (점)', fontsize=12)
            plt.ylim(0, 100)

            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}', ha='center', va='bottom', fontsize=11)

            plt.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            plt.savefig('all_subjects_average.png', dpi=300, bbox_inches='tight')
            print("✅ all_subjects_average.png 파일이 저장되었습니다.")
            plt.show()

    def take_quiz(self, subject: str, year: int, semester: int, unit: str) -> bool:
        """퀴즈 풀기"""
        if subject not in self.quiz_db:
            print(f"❌ {subject}은(는) 등록되지 않은 과목입니다.")
            print(f"등록된 과목: {', '.join(self.quiz_db.keys())}")
            return False

        if (year, semester) not in self.quiz_db[subject]:
            print(f"❌ {year}학년 {semester}학기 데이터가 없습니다.")
            return False

        if unit not in self.quiz_db[subject][(year, semester)]:
            print(f"❌ {unit}이(가) 없습니다.")
            print(f"등록된 단원: {', '.join(self.quiz_db[subject][(year, semester)].keys())}")
            return False

        questions = self.quiz_db[subject][(year, semester)][unit]
        print(f"\n🎯 {subject} {year}학년 {semester}학기 {unit} 퀴즈")
        print("=" * 50)

        correct = 0
        for i, question in enumerate(questions, 1):
            print(f"\n문제 {i}: {question}")
            answer = input("답변: ").strip()
            # 간단한 정답 체크 (실제로는 더 복잡할 수 있음)
            if answer.lower() != '':
                correct += 1
                print("✅ 맞습니다!")
            else:
                print("❌ 틀렸습니다.")

        score = (correct / len(questions)) * 100
        print(f"\n📈 퀴즈 결과: {correct}/{len(questions)} ({score:.1f}점)")
        return True

def demo_mode(analyzer: GradeAnalyzer):
    """데모 모드: 샘플 데이터를 자동으로 입력"""
    print("\n🎬 데모 모드 실행 중...\n")

    # 샘플 성적 추가
    sample_grades = [
        ('국어', 85),
        ('국어', 88),
        ('국어', 92),
        ('수학', 78),
        ('수학', 82),
        ('수학', 75),
        ('영어', 90),
        ('영어', 87),
        ('영어', 93),
    ]

    for subject, score in sample_grades:
        analyzer.add_grade(subject, score)

    print("\n" + "="*50)
    analyzer.show_all_averages()

    print("\n" + "="*50)
    print("📊 모든 과목 평균 그래프 생성 중...")
    analyzer.draw_graph()

    print("\n" + "="*50)
    print("📊 수학 성적 추이 그래프 생성 중...")
    analyzer.draw_graph('수학')

def main():
    analyzer = GradeAnalyzer()

    # 데모 모드 실행
    demo_mode(analyzer)

    # 대화형 모드
    print("\n" + "="*50)
    print("✅ 데모가 완료되었습니다!")
    print("="*50)

    while True:
        print("\n" + "="*50)
        print("📚 성적 분석 프로그램")
        print("="*50)
        print("1. 성적 입력")
        print("2. 평균 확인")
        print("3. 그래프 보기")
        print("4. 퀴즈 풀기")
        print("5. 종료")
        print("="*50)

        choice = input("선택 (1-5): ").strip()

        if choice == '1':
            print("\n📝 성적 입력")
            subject = input("과목 입력 (예: 국어, 수학, 영어): ").strip()
            try:
                score = float(input("성적 입력 (0-100): "))
                if 0 <= score <= 100:
                    year = int(input("학년 입력 (기본값 1): ") or "1")
                    semester = int(input("학기 입력 (1 또는 2, 기본값 1): ") or "1")
                    analyzer.add_grade(subject, score, year, semester)
                else:
                    print("❌ 0-100 사이의 값을 입력해주세요.")
            except ValueError:
                print("❌ 유효한 숫자를 입력해주세요.")

        elif choice == '2':
            analyzer.show_all_averages()

        elif choice == '3':
            print("\n📊 그래프 옵션")
            print("1. 특정 과목 그래프")
            print("2. 모든 과목 평균 비교")
            graph_choice = input("선택 (1-2): ").strip()

            if graph_choice == '1':
                subject = input("과목 입력: ").strip()
                analyzer.draw_graph(subject)
            elif graph_choice == '2':
                analyzer.draw_graph()
            else:
                print("❌ 올바른 선택을 해주세요.")

        elif choice == '4':
            print("\n🎯 퀴즈 풀기")
            subject = input("과목 입력 (국어, 수학, 영어): ").strip()
            year = int(input("학년 입력: ") or "1")
            semester = int(input("학기 입력 (1 또는 2): ") or "1")
            unit = input("단원 입력 (예: 단원1): ").strip()
            analyzer.take_quiz(subject, year, semester, unit)

        elif choice == '5':
            print("\n👋 프로그램을 종료합니다.")
            break

        else:
            print("❌ 올바른 선택을 해주세요.")

if __name__ == "__main__":
    main()
