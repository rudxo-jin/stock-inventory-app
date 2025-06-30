# 재고조사 앱 빠른 참조 가이드

## 🎯 **프로젝트 핵심 정보**
- **앱 이름**: 재고조사 앱 (Stock Inventory App)
- **GitHub**: https://github.com/rudxo-jin/stock-inventory-app.git
- **배포 URL**: https://stock-inventory-app-rudxo-jin.streamlit.app/
- **상태**: ✅ 배포 성공 (2025-01-03 15:20)

## 🏗️ **현재 구조**
```
streamlit_app.py (메인)
├── utils/
│   ├── data_processor.py      # 데이터 처리
│   ├── report_generator.py    # 7개 시트 보고서
│   ├── file_converter.py      # .xls→.xlsx 변환
│   └── ui_components.py       # UI 컴포넌트
├── requirements.txt           # streamlit, pandas, numpy, plotly, openpyxl
├── runtime.txt               # python-3.11.0
└── cache_buster.txt          # 캐시 무효화
```

## 🔧 **기술 스택**
- **Python**: 3.11.0 (안정적 호환성)
- **패키지**: streamlit, pandas, numpy, plotly, openpyxl (미니멀 스택)
- **시스템 패키지**: 없음 (packages.txt 삭제됨)
- **패키지 매니저**: uv (Streamlit Cloud 자동)

## 📊 **주요 기능**
1. **엑셀 업로드** (.xls, .xlsx)
2. **데이터 분석** (재고조사, 재고조정)
3. **7개 시트 보고서**:
   - 재고조사요약
   - 재고차이리스트(+/-)
   - 재고조정리스트(+/-)
4. **시각화** (plotly 차트)
5. **파일 다운로드**

## 🚨 **해결된 핵심 문제**
1. **packages.txt 주석 오류** → 파일 완전 삭제
2. **Python 3.13 호환성** → Python 3.11.0 사용
3. **정규표현식 SyntaxWarning** → 단순 문자열 검색
4. **의존성 충돌** → 미니멀 스택

## 💡 **중요한 학습사항**
- Streamlit Cloud에서 packages.txt 주석(#) 사용 금지
- 미니멀 스택이 복잡한 의존성보다 안정적
- Python 3.11이 3.13보다 호환성 면에서 우수
- 캐시 무효화를 위해 파일 내용 변경 필요

## 🔄 **데이터 플로우**
```
파일 업로드 → 형식 변환 → 데이터 로딩 → 분석 → 보고서 생성 → 다운로드
```

## 📞 **개발자 정보**
- **GitHub 사용자**: rudxo-jin
- **프로젝트 완성도**: 100% (배포 성공)
- **마지막 업데이트**: 2025-01-03

---
**📌 새창 채팅 시 이 파일 먼저 확인하여 맥락 파악하세요!** 