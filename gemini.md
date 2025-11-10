# Gemini Side Project Log

## Project Goal: MBTI-like Psychological Test Web Application

**Date:** 2025년 11월 10일 월요일

**Current Status:**
사용자 요청에 따라 "분석 및 모델링"에 중점을 둔 웹 애플리케이션으로, MBTI와 같은 새로운 심리 검사 웹 애플리케이션을 기획하고 개발하기로 결정. 모든 작업 내용은 이 `gemini.md` 파일에 기록될 예정.

**Project Concept: 데이터 기반 워크 스타일 및 게임 추천 탐색기 (Data-Driven Work Style & Game Recommender)**
*   **핵심 아이디어:** 사용자의 성격/워크 스타일을 분석하여, 그에 가장 잘 어울리는 게임 장르 또는 특정 게임을 추천해 주는 심리 검사 웹 애플리케이션.
*   **주요 기능:** 인터랙티브 설문지, 개인화된 결과 대시보드 (추천 게임 포함), 결과 시각화.
*   **"분석 및 모델링" 요소 강화:**
    *   **데이터 기반 프로필 생성 (클러스터링):** 사용자의 수치형 설문 응답 데이터를 기반으로 K-Means와 같은 비지도 학습(Unsupervised Learning) 알고리즘을 적용하여 워크 스타일 프로필을 데이터 기반으로 도출. 각 클러스터의 특징을 분석하여 프로필 정의.
    *   **게임 추천 시스템:** 도출된 프로필에 따라 적절한 게임 장르 또는 특정 게임을 추천. 초기에는 규칙 기반 매핑, 향후 고급 추천 모델로 발전 가능.
    *   **예측 모델링 (향후 확장):** 외부 목표 변수(예: 팀 성과, 직무 만족도) 수집 시 지도 학습 모델을 통한 예측 기능 추가.

**PoC Planning Steps:**

1.  **핵심 컨셉 및 범위:** 사용자의 성격/워크 스타일을 분석하여, 그에 가장 잘 어울리는 게임 장르 또는 특정 게임을 추천해 주는 심리 검사 웹 애플리케이션.
2.  **질문지 설계:**
    *   총 15개의 질문.
    *   5점 리커트 척도.
    *   5가지 테마: 의사결정 및 문제 해결 방식, 대인 관계 및 협업 선호도, 도전 및 위험 감수 성향, 정보 처리 및 집중 방식, 학습 및 탐구 동기.
3.  **데이터 시뮬레이션/수집 전략:**
    *   **가상 데이터 생성:** 3~5개의 '원형(Archetypal)' 프로필을 정의하고, 각 원형에 대한 15개 질문의 평균 응답 점수를 설정. 여기에 노이즈를 추가하여 각 원형별로 50~100명의 가상 사용자를 생성 (총 200~500명).
    *   **게임 데이터 확보:** Free-To-Play Games Database API (FreeToGame.com)를 사용하여 100개 이상의 게임 목록과 장르, 태그 정보를 확보.
4.  **클러스터링 모델 선정 및 학습:**
    *   **알고리즘:** K-Means.
    *   **클러스터 수 (k):** 가상 데이터의 원형 프로필 수에 맞춰 3~5개로 초기 설정.
    *   **학습:** 가상 데이터로 K-Means 모델 학습 후, `joblib` 또는 `pickle`을 사용하여 모델 저장 및 백엔드 로드.
5.  **결과 해석 및 표현 방식:**
    *   **프로필 명명 및 설명:** 각 클러스터에 설득력 있는 이름과 상세 설명(강점, 약점, 상호작용 방식) 부여.
    *   **게임 추천 매핑:** 각 프로필에 어울리는 게임 장르/특정 게임 1~3개 선정 및 추천 이유 설명.
    *   **시각적 결과 표현:** 할당된 프로필, 추천 게임 목록, 사용자 응답과 클러스터 평균 비교 레이더 차트, 핵심 특징 요약.
6.  **기술 스택 및 아키텍처:**
    *   **프론트엔드:** React (TypeScript), Tailwind CSS, Chart.js/Recharts.
    *   **백엔드:** Python (FastAPI), Scikit-learn, Pandas/Numpy, PostgreSQL, SQLAlchemy, joblib/pickle.
    *   **외부 API:** Free-To-Play Games Database API.

**개발 로드맵:**

1.  **프로젝트 초기 설정 및 환경 구성 (현재 진행 중):**
    *   Initialize project structure (frontend, backend folders).
    *   Set up virtual environments and install basic dependencies.
    *   Configure Git repository.
    *   Database setup (PostgreSQL).
2.  **백엔드 개발 (Data & ML Focus):**
    *   **Data Model Definition:** Define SQLAlchemy models for questions, user responses, game data, clusters, and profile interpretations.
    *   **Game Data Ingestion:** Implement a script to fetch game data from Free-To-Play Games Database API and store it in the database.
    *   **Synthetic Data Generation:** Implement a script to generate the synthetic user response data based on archetypal profiles.
    *   **Clustering Model Training & Persistence:**
        *   Implement the K-Means clustering logic using Scikit-learn.
        *   Train the model on synthetic data.
        *   Save the trained model to a file (`.pkl`).
    *   **Cluster Interpretation & Mapping:** Manually define cluster names, descriptions, and initial game recommendations for each cluster. Store this in the database.
    *   **API Endpoints:**
        *   Endpoint to get all questions.
        *   Endpoint to submit user responses.
        *   Endpoint to get analysis results (profile, game recommendations).
3.  **프론트엔드 개발 (UI Focus):**
    *   **Basic UI Setup:** Create a React app with basic routing.
    *   **Questionnaire Component:** Display the 15 questions with 5-point Likert scale input.
    *   **Result Display Component:**
        *   Show the user's assigned profile name and description.
        *   Display recommended games with explanations.
        *   Implement a radar chart to visualize user responses vs. cluster averages.
    *   **API Integration:** Connect frontend to backend API endpoints.
4.  **테스트 및 개선:**
    *   Unit tests for backend logic (data processing, clustering).
    *   Integration tests for API endpoints.
    *   Frontend component testing.
    *   End-to-end testing of the user flow.
    *   Styling and UI/UX adjustments.

---