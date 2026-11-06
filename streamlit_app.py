import streamlit as st
import json
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from typing import Dict, List, Optional

st.set_page_config(
    page_title="📚 성적 분석 프로그램",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    font_path = 'C:\\Windows\\Fonts\\malgun.ttf'
    if os.path.exists(font_path):
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
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_grades(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.grades, f, ensure_ascii=False, indent=2)

    def load_quiz_db(self) -> Dict:
        return {
            '국어': {
                (11, 1): {'단원1': ['한글의 자음과 모음은?', '다음 중 맞은 문장은?'],
                          '단원2': ['문법의 기본은?', '품사는 몇 가지인가?']},
                (11, 2): {'단원1': ['한국 문학의 시작은?', '고전 문학이란?'],
                          '단원2': ['현대 문학의 특징은?', '시와 소설의 차이는?']},
                (21, 1): {'단원1': ['소설의 구성 요소는?', '인물의 성격 분석은?'],
                          '단원2': ['시의 표현 기법은?', '운율이란?']},
                (21, 2): {'단원1': ['수필의 특징은?', '정보 전달 방식은?'],
                          '단원2': ['비유 표현이란?', '문학사의 시대별 특징은?']},
                (31, 1): {'단원1': ['고전 시가의 특징은?', '현대 시의 특징은?'],
                          '단원2': ['소설 분석법은?', '인물 심리 파악 방법은?']},
                (31, 2): {'단원1': ['문법 종합 문제', '문장 구조 분석 방법'],
                          '단원2': ['글쓰기 기법은?', '작문 평가 기준은?']},
            },
            '수학': {
                (11, 1): {'단원1': ['1+1은?', '2×3은?'],
                          '단원2': ['10÷2는?', '5의 제곱은?']},
                (11, 2): {'단원1': ['제곱근 4는?', '방정식이란?'],
                          '단원2': ['함수의 정의는?', '그래프란?']},
                (21, 1): {'단원1': ['x²+5x+6을 인수분해하면?', 'x²-x-12를 인수분해하면?'],
                          '단원2': ['y=x²의 꼭짓점은?', '포물선의 성질은?']},
                (21, 2): {'단원1': ['연립방정식 풀이법', 'x-3>0의 해'],
                          '단원2': ['삼각형의 내각의 합은?', '닮음의 조건은?']},
                (31, 1): {'단원1': ['수열의 정의는?', '1,3,5,7의 다음항은?'],
                          '단원2': ['첫항이 2, 공비가 3인 등비수열의 3항은?', '급수의 합 공식']},
                (31, 2): {'단원1': ['미분의 개념은?', 'y=x²의 도함수는?'],
                          '단원2': ['∫x dx의 부정적분은?', '정적분의 의미는?']},
            },
            '영어': {
                (11, 1): {'단원1': ['Hello의 뜻은?', 'Good morning의 뜻은?'],
                          '단원2': ['알파벳은 몇 개인가?', 'A-B-C의 발음은?']},
                (11, 2): {'단원1': ['I am의 뜻은?', 'You are의 뜻은?'],
                          '단원2': ['현재형이란?', '과거형이란?']},
                (21, 1): {'단원1': ['He goes to school의 동사는?', 'Present perfect란?'],
                          '단원2': ['수동태란?', 'Modal verbs의 종류는?']},
                (21, 2): {'단원1': ['조동사 can의 의미는?', '동명사 형태는?'],
                          '단원2': ['관계사 who의 용법은?', '간접화법이란?']},
                (31, 1): {'단원1': ['복합문과 복문의 차이는?', 'If I were you...는?'],
                          '단원2': ['관용구 표현 예시는?', '작문의 기본 기법은?']},
                (31, 2): {'단원1': ['영문법 전체 복습 문제', '논문 읽기 기법'],
                          '단원2': ['토론에서 의견 제시 표현', 'PPT 프레젠테이션 영어']},
            }
        }

    def add_grade(self, subject: str, score: float, semester_year: int = 1, semester_num: int = 1):
        if subject not in self.grades:
            self.grades[subject] = []
        self.grades[subject].append({
            'score': score,
            'year': semester_year,
            'semester': semester_num
        })
        self.save_grades()
        return True

    def get_average(self, subject: Optional[str] = None) -> float:
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

    def get_all_grades_list(self, subject: Optional[str] = None) -> List:
        if subject:
            if subject not in self.grades:
                return []
            return self.grades[subject]
        else:
            all_grades = []
            for subj, grades_list in self.grades.items():
                for grade in grades_list:
                    all_grades.append({'subject': subj, **grade})
            return all_grades

    def delete_grade(self, subject: str, index: int):
        if subject in self.grades and 0 <= index < len(self.grades[subject]):
            self.grades[subject].pop(index)
            self.save_grades()
            return True
        return False

    def draw_graph(self, subject: Optional[str] = None):
        if not self.grades:
            return None

        if subject:
            if subject not in self.grades:
                return None
            scores = [g['score'] for g in self.grades[subject]]
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(range(1, len(scores) + 1), scores, marker='o', linewidth=2.5, markersize=8, label=subject, color='#4ECDC4')
            ax.axhline(y=self.get_average(subject), color='r', linestyle='--', label=f'평균: {self.get_average(subject):.2f}')
            ax.set_title(f'{subject} 성적 추이', fontsize=14, fontweight='bold')
            ax.set_xlabel('입력 순서', fontsize=12)
            ax.set_ylabel('성적 (점)', fontsize=12)
            ax.grid(True, alpha=0.3)
            ax.legend()
            plt.tight_layout()
            return fig
        else:
            subjects = list(self.grades.keys())
            averages = [self.get_average(s) for s in subjects]
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(subjects, averages, marker='o', linewidth=2.5, markersize=10, label='평균 성적', color='#4ECDC4')
            for i, (subject, avg) in enumerate(zip(subjects, averages)):
                ax.text(i, avg + 2, f'{avg:.1f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
            ax.set_title('과목별 평균 성적', fontsize=14, fontweight='bold')
            ax.set_ylabel('평균 성적 (점)', fontsize=12)
            ax.set_ylim(0, 105)
            ax.grid(True, alpha=0.3, axis='y')
            ax.legend()
            plt.tight_layout()
            return fig

if 'analyzer' not in st.session_state:
    st.session_state.analyzer = GradeAnalyzer()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'username' not in st.session_state:
    st.session_state.username = ""

analyzer = st.session_state.analyzer

if not st.session_state.logged_in:
    st.title("📚 성적 분석 프로그램")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("👤 로그인")
        username = st.text_input("이름을 입력하세요", placeholder="예: 김철수")
        if st.button("🚀 로그인", use_container_width=True):
            if username.strip():
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                st.rerun()
            else:
                st.error("❌ 이름을 입력해주세요!")
    st.markdown("---")
    st.info("💡 이름을 입력하고 로그인하여 성적을 관리하세요!")
else:
    st.sidebar.title("👤 사용자 정보")
    st.sidebar.write(f"**{st.session_state.username}**님 로그인 중")
    if st.sidebar.button("🚪 로그아웃", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    st.sidebar.divider()

    st.sidebar.title("🎯 메뉴")
    menu = st.sidebar.radio("원하는 기능을 선택하세요",
        ["📊 대시보드", "📝 성적 입력", "📈 성적 조회", "📉 그래프 보기", "🎯 퀴즈 풀기", "⚙️ 설정"])

    st.title("📚 성적 분석 프로그램")
    st.markdown(f"**{st.session_state.username}**님, 환영합니다! 📊")

    if menu == "📊 대시보드":
        st.header("대시보드")
        if not analyzer.grades:
            st.info("📌 아직 입력된 성적이 없습니다. '성적 입력' 메뉴에서 성적을 추가해주세요.")
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                overall_avg = analyzer.get_average()
                st.metric("📊 전체 평균", f"{overall_avg:.2f}점", delta=None)
            with col2:
                total_grades = sum(len(grades) for grades in analyzer.grades.values())
                st.metric("📝 입력된 성적 수", f"{total_grades}개", delta=None)
            with col3:
                subject_count = len(analyzer.grades)
                st.metric("📚 과목 수", f"{subject_count}개", delta=None)
            st.divider()
            st.subheader("과목별 평균")
            col1, col2 = st.columns(2)
            with col1:
                for subject in analyzer.grades:
                    avg = analyzer.get_average(subject)
                    count = len(analyzer.grades[subject])
                    st.write(f"**{subject}**: {avg:.2f}점 ({count}개 성적)")
            with col2:
                fig = analyzer.draw_graph()
                if fig:
                    st.pyplot(fig)
                plt.close('all')

    elif menu == "📝 성적 입력":
        st.header("성적 입력")
        col1, col2, col3 = st.columns(3)
        with col1:
            school_type = st.selectbox("학교 선택", ["초등학교", "중학교", "고등학교"], key="input_school")
        with col2:
            year = st.selectbox("학년 선택", [1, 2, 3], key="input_year")
        with col3:
            semester = st.selectbox("학기 선택", [1, 2], key="input_semester")

        school_map = {"초등학교": 1, "중학교": 2, "고등학교": 3}
        year_code = school_map[school_type] * 10 + year

        st.divider()
        st.subheader(f"📚 {school_type} {year}학년 {semester}학기 단원")

        units_by_subject = {}
        for subject, quiz_data in analyzer.quiz_db.items():
            if (year_code, semester) in quiz_data:
                units_by_subject[subject] = list(quiz_data[(year_code, semester)].keys())

        if units_by_subject:
            for subject, units in units_by_subject.items():
                st.write(f"**{subject}**")
                cols = st.columns(len(units))
                for i, unit in enumerate(units):
                    with cols[i]:
                        if st.button(f"📖 {unit}", use_container_width=True, key=f"unit_{subject}_{unit}"):
                            st.session_state.selected_unit = (subject, unit)
                            st.session_state.selected_year = year_code
                            st.session_state.selected_semester = semester
            st.divider()

            if 'selected_unit' in st.session_state:
                subject, unit = st.session_state.selected_unit
                year_selected = st.session_state.selected_year
                semester_selected = st.session_state.selected_semester
                school_reverse = {1: "초등학교", 2: "중학교", 3: "고등학교"}
                school_name = school_reverse[year_selected // 10]
                grade_num = year_selected % 10

                st.subheader(f"✏️ {subject} - {unit} 성적 입력")
                st.info(f"{school_name} {grade_num}학년 {semester_selected}학기")
                score = st.slider("성적 입력 (0-100)", 0, 100, 50, key="input_score")

                if st.button("✅ 성적 저장", use_container_width=True):
                    analyzer.add_grade(subject, score, year_selected, semester_selected)
                    st.success(f"✅ {subject} {unit} 성적 {score}점이 저장되었습니다!")
                    st.session_state.selected_unit = None
        else:
            st.info(f"📌 {school_type} {year}학년 {semester}학기에 등록된 단원이 없습니다.")

    elif menu == "📈 성적 조회":
        st.header("성적 조회")
        if not analyzer.grades:
            st.info("📌 입력된 성적이 없습니다.")
        else:
            st.subheader("📊 과목별 평균")
            for subject in analyzer.grades:
                avg = analyzer.get_average(subject)
                count = len(analyzer.grades[subject])
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{subject}**")
                with col2:
                    st.metric("평균", f"{avg:.2f}점")
                with col3:
                    st.metric("개수", f"{count}개")
            st.divider()

            st.subheader("📝 상세 성적 목록")
            subject_filter = st.selectbox("과목 선택", ["모든 과목 보기"] + list(analyzer.grades.keys()))
            if subject_filter == "모든 과목 보기":
                grades_list = analyzer.get_all_grades_list()
            else:
                grades_list = analyzer.get_all_grades_list(subject_filter)

            for i, grade in enumerate(grades_list):
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                with col1:
                    st.write(f"**{grade.get('subject', subject_filter)}**")
                with col2:
                    st.write(f"성적: {grade['score']}점")
                with col3:
                    st.write(f"{grade['year']}학년")
                with col4:
                    st.write(f"{grade['semester']}학기")
                with col5:
                    if st.button("🗑️", key=f"delete_{i}"):
                        if analyzer.delete_grade(grade.get('subject', subject_filter), i):
                            st.rerun()

    elif menu == "📉 그래프 보기":
        st.header("그래프 보기")
        if not analyzer.grades:
            st.info("📌 그래프를 그릴 성적이 없습니다.")
        else:
            graph_type = st.radio("그래프 종류 선택", ["모든 과목 평균 비교", "특정 과목 성적 추이"])
            if graph_type == "모든 과목 평균 비교":
                st.subheader("모든 과목 평균 비교")
                fig = analyzer.draw_graph()
                if fig:
                    st.pyplot(fig)
                    plt.close('all')
            else:
                subject = st.selectbox("과목 선택", list(analyzer.grades.keys()))
                st.subheader(f"{subject} 성적 추이")
                fig = analyzer.draw_graph(subject)
                if fig:
                    st.pyplot(fig)
                    plt.close('all')

    elif menu == "🎯 퀴즈 풀기":
        st.header("퀴즈 풀기")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            subject = st.selectbox("과목 선택", list(analyzer.quiz_db.keys()))

        if subject in analyzer.quiz_db:
            available_years = list(analyzer.quiz_db[subject].keys())
            school_types = list(set([y[0] // 10 for y in available_years]))
            school_map_reverse = {1: "초등학교", 2: "중학교", 3: "고등학교"}

            with col2:
                school_code = st.selectbox("학교", sorted(school_types), format_func=lambda x: school_map_reverse[x])
            with col3:
                available_grades = sorted(list(set([y[0] % 10 for y in available_years if y[0] // 10 == school_code])))
                grade = st.selectbox("학년", available_grades, format_func=lambda x: f"{x}학년")

            year = school_code * 10 + grade
            with col4:
                semester = st.selectbox("학기 선택", [s[1] for s in available_years if s[0] == year], format_func=lambda x: f"{x}학기")

            available_units = list(analyzer.quiz_db[subject][(year, semester)].keys())
            unit = st.selectbox("단원 선택", available_units)

            st.divider()
            questions = analyzer.quiz_db[subject][(year, semester)][unit]
            st.subheader(f"🎯 {subject} {year}학년 {semester}학기 {unit} 퀴즈")
            st.write(f"총 {len(questions)}문제")

            correct = 0
            for i, question in enumerate(questions, 1):
                st.write(f"**문제 {i}: {question}**")
                answer = st.text_input(f"답변 {i}", key=f"answer_{i}")
                if answer.strip():
                    correct += 1

            if st.button("퀴즈 제출", use_container_width=True):
                score = (correct / len(questions)) * 100
                st.success(f"✅ 퀴즈 완료! {correct}/{len(questions)} ({score:.1f}점)")

    elif menu == "⚙️ 설정":
        st.header("설정")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 데이터 관리")
            if st.button("🔄 모든 데이터 초기화", use_container_width=True, key="reset_btn"):
                analyzer.grades = {}
                analyzer.save_grades()
                st.success("✅ 모든 데이터가 초기화되었습니다!")
                st.rerun()

        with col2:
            st.subheader("📥 데이터 다운로드")
            if analyzer.grades:
                json_str = json.dumps(analyzer.grades, ensure_ascii=False, indent=2)
                st.download_button("📥 성적 데이터 다운로드 (JSON)", data=json_str, file_name="grades.json", mime="application/json", use_container_width=True)
            else:
                st.info("📌 다운로드할 데이터가 없습니다.")

        st.divider()
        st.info("💡 Tip: 이 프로그램은 당신의 성적을 추적하고 분석하는데 도움을 줍니다!")

    st.sidebar.divider()
    st.sidebar.info("📚 성적 분석 프로그램 v1.0")
