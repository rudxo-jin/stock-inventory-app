# 📦 재고조사 앱

매장 재고 실사와 재고조정을 위한 웹 애플리케이션입니다.

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