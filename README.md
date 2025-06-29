# 📦 재고조사 앱

매장 재고 실사와 재고조정을 위한 웹 애플리케이션입니다.

## 🚀 배포 환경

### 요구사항
- Python 3.11.0
- Streamlit Cloud 또는 Heroku 호환
- 메모리: 최소 512MB 권장

### 의존성 버전 (배포 최적화)
```
streamlit==1.28.1
pandas==2.0.3
openpyxl==3.1.2
plotly==5.15.0
numpy==1.24.3
```

## 🔧 배포 문제 해결

### Python 3.13 호환성 문제
**문제**: pandas 2.2.3이 Python 3.13에서 컴파일 오류 발생
**해결**: Python 3.11.0 + pandas 2.0.3 조합으로 안정화

### 파일 처리 최적화
- .xls 파일: 웹 환경에서 지원 안내 메시지 표시
- .xlsx 파일: openpyxl 엔진으로 처리
- 임시 파일: 메모리 기반 처리로 변경

## 📋 주요 기능

### 1단계: PART 파일 분석
- 엑셀 파일 업로드 및 자동 분석
- 재고량, 재고액, 단가 자동 계산
- 데이터 요약 통계 제공

### 2단계: 실재고 템플릿 생성
- 재고가 있는 품목만 필터링
- 부품명 오름차순 정렬
- 실재고 입력용 템플릿 다운로드

### 3단계: 실재고 데이터 처리
- 실재고 또는 차이값 입력 지원
- 자동 계산 (실재고액, 차액)
- 데이터 검증 및 오류 처리

### 4단계: 재고조정 적용
- 날짜 범위 필터링
- 제작사품번 기준 매칭
- 재고조정 영향 분석

### 5단계: 결과보고서 생성
- 점포 정보 입력
- 카드형 요약 보고서
- 엑셀 보고서 다운로드

## 🎨 UI/UX 특징

### 진행 단계 표시
- 사이드바 진행률 표시
- 단계별 완료 상태 확인

### 카드형 보고서
- 4개 섹션별 카드 구성
- 색상 코딩 (양수/음수/합계)
- 반응형 레이아웃

### 사용자 경험
- 직관적인 탭 구조
- 실시간 데이터 검증
- 상세한 안내 메시지

## 🏗️ 아키텍처

### 모듈 구조
```
├── app.py                      # 메인 애플리케이션
├── utils/
│   ├── data_processor.py       # PART 파일 처리
│   ├── adjustment_processor.py # 재고조정 처리
│   ├── report_generator.py     # 보고서 생성
│   ├── file_converter.py       # 파일 변환
│   └── ui_components.py        # UI 컴포넌트
├── requirements.txt            # 의존성 (배포용)
├── runtime.txt                 # Python 버전
├── packages.txt                # 시스템 패키지
└── .streamlit/
    └── config.toml            # Streamlit 설정
```

### 기술 스택
- **Frontend**: Streamlit
- **Backend**: Python, Pandas
- **File Processing**: openpyxl
- **Visualization**: Plotly
- **Deployment**: Streamlit Cloud

## 🚨 배포 시 주의사항

### 1. 버전 호환성
- Python 3.11.0 고정 사용
- pandas 2.0.3 이하 버전 권장
- numpy 1.24.x 시리즈 사용

### 2. 메모리 관리
- 대용량 파일 처리 시 메모리 부족 가능
- 캐시 기능으로 메모리 효율성 향상
- 임시 파일 자동 정리

### 3. 파일 업로드 제한
- 최대 파일 크기: 200MB
- .xls 파일은 .xlsx 변환 필요
- 엑셀 파일만 지원

## 📊 성능 최적화

### 캐시 활용
- `@st.cache_resource`: 프로세서 인스턴스 캐시
- `@st.cache_data`: 계산 결과 캐시
- 세션 상태 관리로 데이터 유지

### 메모리 효율성
- BytesIO 활용한 메모리 기반 파일 처리
- 불필요한 데이터 즉시 정리
- 단계별 데이터 분리 저장

## 🔍 디버깅 정보

배포 환경에서 문제 발생 시:
1. 브라우저 개발자 도구 콘솔 확인
2. Streamlit Cloud 로그 확인
3. 파일 크기 및 형식 검증
4. Python/패키지 버전 호환성 확인

## 📞 지원

배포 관련 문제 발생 시 다음 정보 제공:
- 오류 메시지 전문
- 업로드한 파일 정보
- 브라우저 및 OS 정보
- 수행한 단계별 상세 내용

## 🚀 주요 기능

- **PART 파일 분석**: 제작사품번, 부품명, 재고, 재고액 데이터 처리
- **실재고 템플릿 생성**: 재고조사용 엑셀 템플릿 자동 생성
- **실재고 데이터 처리**: 차이값 우선 처리, 자동 계산
- **재고조정 적용**: 날짜 범위 필터링, 제작사품번 매칭
- **다중 시트 보고서**: 5개 시트로 구성된 상세 엑셀 보고서

## 📊 엑셀 보고서 구성

1. **재고조사요약**: 전체 요약 보고서
2. **재고차이리스트(-)**: 재고 감소 품목 상세
3. **재고차이리스트(+)**: 재고 증가 품목 상세  
4. **재고조정리스트(+)**: 재고 증가 조정 내역
5. **재고조정리스트(-)**: 재고 감소 조정 내역

## 🛠️ 설치 및 실행

### 🌐 웹앱 사용 (권장)

배포된 웹앱에서 바로 사용하세요:
- **URL**: [배포 후 링크 업데이트 예정]
- **지원 파일**: .xlsx 파일만 지원
- **변환 필요**: .xls 파일은 Excel에서 .xlsx로 저장 후 업로드

### 💻 로컬 환경 (Windows)

```bash
# 저장소 클론
git clone <repository-url>
cd stock_app

# 의존성 설치
pip install -r requirements.txt

# 로컬에서 .xls 지원 원할 시 (선택사항)
pip install xlrd==1.2.0

# 앱 실행
streamlit run app.py
```

### 🚀 Streamlit Cloud 배포

1. GitHub 저장소 연결
2. `app.py` 메인 파일 지정
3. `requirements.txt` 자동 인식
4. 배포 완료

## 📁 파일 지원

### 로컬 환경
- ✅ `.xlsx` 파일 (권장)
- ✅ `.xls` 파일 (자동 변환)

### 웹앱 환경  
- ✅ `.xlsx` 파일만 지원
- ❌ `.xls` 파일 (수동 변환 필요)

## 🔧 .xls 파일 변환 방법

웹앱에서 .xls 파일을 사용하려면:

1. **Excel에서 변환**:
   - 파일 열기 → '다른 이름으로 저장' → '.xlsx' 형식 선택

2. **Google Sheets에서 변환**:
   - 파일 업로드 → '파일' → '다운로드' → '.xlsx' 선택

## 📂 프로젝트 구조

```
stock_app/
├── app.py                 # 메인 애플리케이션
├── requirements.txt       # 웹앱 배포용 의존성
├── requirements-local.txt # 로컬 개발용 의존성
├── utils/
│   ├── data_processor.py       # PART 파일 처리
│   ├── adjustment_processor.py # 재고조정 처리
│   ├── file_converter.py       # 파일 변환
│   ├── report_generator.py     # 보고서 생성
│   └── ui_components.py        # UI 컴포넌트
├── templates/             # 생성된 템플릿 저장
├── uploads/              # 업로드 파일 임시 저장
└── outputs/              # 출력 파일 저장
```

## 🌐 배포 플랫폼 호환성

- ✅ **Streamlit Cloud**: 100% 호환
- ✅ **Heroku**: 100% 호환
- ✅ **AWS Lambda/ECS**: 100% 호환
- ✅ **Google Cloud Run**: 100% 호환
- ✅ **Azure Container Instances**: 100% 호환

## 💡 사용 팁

1. **PART 파일**: 제작사품번, 부품명, 재고, 재고액 컬럼 필수
2. **실재고 입력**: 차이값 입력 시 우선 적용
3. **재고조정**: 날짜 범위 설정으로 필터링 가능
4. **보고서**: 모든 시트에 합계 자동 계산

## 🔍 문제 해결

### xlrd 오류 (로컬 환경)
```bash
pip install xlrd==1.2.0
```

### .xls 파일 지원 안됨 (웹앱)
- .xlsx 파일로 변환 후 사용

### pandas 버전 충돌
```bash
pip install pandas==1.5.3
```

## 📝 라이선스

MIT License

## 👨‍💻 개발자

Claude AI Assistant 