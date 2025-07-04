# 📋 재고조사 앱 사용자 매뉴얼

## 🎯 **앱 개요**

**재고조사 앱**은 매장의 재고 실사와 재고조정을 효율적으로 처리하기 위한 웹 애플리케이션입니다.

### **주요 기능**
- 📊 PART 파일 분석 및 요약
- 📝 실재고 조사용 템플릿 생성
- 🔍 실재고 데이터 처리 및 분석
- ⚖️ 재고조정 내역 적용
- 📈 종합 보고서 생성 (엑셀 7개 시트)

### **사용 대상**
- 매장 담당자 
- 본사 운영부

---

## 🌐 **1. 앱 접속하기**

### **접속 주소**
```
https://stock-inven.streamlit.app/
```

### **접속 방법**
1. 웹 브라우저를 열어주세요 (Chrome, Edge, Firefox 등)
2. 위 주소를 주소창에 입력하거나 복사해서 붙여넣기
3. Enter 키를 누르면 앱이 로딩됩니다 (약 8초 소요)

### **화면 구성**
- 상단: 앱 제목과 설명
- 좌측: 5개 탭 메뉴
- 우측: 진행 상황 사이드바
- 메인: 선택한 탭의 작업 화면

---

## 📊 **2. Tab 1: PART 파일 분석**

### **목적**
매장의 전산재고 데이터(PART 파일)를 업로드하고 분석합니다.

### **준비물**
- PART 파일 (엑셀 형식: .xlsx 또는 .xls)
- 파일에는 다음 컬럼들이 포함되어야 합니다:
  - 제품명, 제작사품번, 단가, 재고수량, 재고액 등

### **사용 방법**

#### **STEP 1: 파일 업로드**
1. "PART 파일을 업로드하세요" 영역을 클릭
2. 컴퓨터에서 PART 파일을 선택
3. 파일이 업로드되면 자동으로 분석 시작

#### **STEP 2: 데이터 확인**
업로드가 완료되면 다음 정보가 표시됩니다:

**📋 요약 정보**
- 총 품목 수: 예) 14,253개
- 총 재고액: 예) 1,234,567,890원
- 평균 단가: 예) 12,345원
- 재고 있는 품목: 예) 8,954개
- 재고 없는 품목: 예) 5,299개

**📊 데이터 미리보기**
- 상위 10개 품목의 상세 정보 표시
- 컬럼명과 데이터 형식 확인 가능

### **주의사항**
- 파일 크기는 50MB 이하로 제한
- .xls 파일은 자동으로 .xlsx로 변환됩니다
- 필수 컬럼이 없으면 오류 메시지가 표시됩니다

---

## 📝 **3. Tab 2: 실재고 템플릿 생성**

### **목적**
재고조사를 위한 엑셀 템플릿을 다운로드합니다.

### **사용 방법**

#### **STEP 1: 템플릿 다운로드**
1. Tab 1에서 PART 파일을 먼저 업로드해야 합니다
2. "📥 실재고 템플릿 다운로드" 버튼 클릭
3. 브라우저 다운로드 폴더에 파일 저장됨

#### **STEP 2: 템플릿 내용 확인**
다운로드된 파일에는 다음이 포함됩니다:
- **제품명**: PART 파일의 제품명
- **제작사품번**: 고유 식별 번호
- **전산재고**: 현재 시스템 재고수량
- **차이값**: 실재고 - 전산재고 (입력란)
- **실재고**: 실제 조사한 재고수량 (입력란)

#### **STEP 3: 재고조사 수행**
1. 템플릿을 매장으로 가져가기
2. 실제 재고를 세면서 다음 중 **하나만** 입력:
   - **차이값**: 실재고와 전산재고의 차이
   - **실재고**: 실제 센 재고수량

### **입력 방법 예시**

**방법 1: 차이값 입력 (권장)**
```
전산재고: 100개
실제재고: 95개
→ 차이값: -5 (5개 부족)
```

**방법 2: 실재고 입력**
```
전산재고: 100개
실제재고: 95개
→ 실재고: 95
```

### **💡 팁**
- 재고가 0인 품목은 템플릿에서 자동 제외됩니다
- 차이값 입력이 더 빠르고 정확합니다
- 두 값을 모두 입력하면 차이값이 우선 적용됩니다

---

## 🔍 **4. Tab 3: 실재고 데이터 처리**

### **목적**
작성된 실재고 조사 결과를 업로드하고 분석합니다.

### **준비물**
- 작성 완료된 실재고 조사 템플릿

### **사용 방법**

#### **STEP 1: 실재고 파일 업로드**
1. "실재고 파일을 업로드하세요" 영역 클릭
2. 작성된 템플릿 파일 선택
3. 파일 업로드 및 자동 분석 시작

#### **STEP 2: 처리 결과 확인**
업로드가 완료되면 다음 정보가 표시됩니다:

**📊 처리 요약**
- 총 처리 품목: 예) 8,954개
- 차이값 입력: 예) 5,234개
- 실재고 입력: 예) 3,720개
- 재고 증가: 예) 2,145개 (+1,234,567원)
- 재고 감소: 예) 3,089개 (-2,345,678원)

**📋 데이터 미리보기**
- 처리된 재고 데이터 상위 10개 표시
- 각 품목별 차이값과 재고액 변동 확인

#### **STEP 3: 완성된 실재고 파일 다운로드**
데이터 처리가 완료되면 자동으로 다운로드 기능이 활성화됩니다:

**📥 다운로드 기능**
- **다운로드 버튼**: "📊 완성된 실재고 파일 다운로드" 버튼 클릭
- **파일 형태**: 엑셀 (.xlsx) 파일
- **파일명**: 완성된_실재고데이터_20250103_1430.xlsx (날짜시간 자동 생성)

**📋 다운로드 파일 내용**
- 원본 데이터 + 계산된 모든 값 포함
- 차이값, 실재고, 재고액 변동 등 모든 컬럼
- 시각적 스타일 적용:
  - 헤더: 진한 네이비 배경
  - 양수 값: 연한 녹색 배경
  - 음수 값: 연한 빨간색 배경
  - 컬럼 너비 자동 조정

### **데이터 처리 로직 (총액 기준 처리 방식)**
1. **차이값 우선**: 차이값이 있으면 우선 사용
2. **실재고 계산**: 차이값이 없으면 실재고에서 차이값 계산
3. **총액 기준 재고액 계산** (소수점 오차 제거):
   - **감소의 경우**: 실재고액 = 전산재고액 - (감소수량 × 단가)
   - **증가의 경우**: 실재고액 = 전산재고액 + (증가수량 × 단가)
   - **변동분 재고액**: 원 단위로 반올림하여 정수 처리
4. **검증**: 비정상적인 값이 있으면 경고 표시

### **💡 총액 기준 처리 방식의 장점**
- **정확성**: 소수점 오차 없는 정확한 재고액 계산
- **실무성**: 전체 재고 흐름 기준으로 처리하여 이해하기 쉬움
- **일관성**: 모든 재고액이 원 단위 정수로 통일

---

## ⚖️ **5. Tab 4: 재고조정 적용**

### **목적**
과거 재고조정 내역을 현재 재고에 반영하여 정확한 재고차이를 계산합니다.

### **준비물**
- 재고조정 파일 (엑셀 형식)
- 파일에는 다음 컬럼들이 포함되어야 합니다:
  - 작업일자, 제작사품번, 수량변경, 변경사유 등

### **사용 방법**

#### **STEP 1: 재고조정 파일 업로드**
1. "재고조정 파일 선택" 영역 클릭
2. 재고조정 엑셀 파일 선택 업로드
3. 파일 업로드 완료 후 데이터 미리보기 표시

#### **STEP 2: 적용 기간 설정 (개선된 UI)**
업로드가 완료되면 **깔끔한 2컬럼 레이아웃**의 날짜 설정 화면이 표시됩니다:

**📌 기간 설정 가이드**
> "기본적으로 최근 6개월 기간이 설정됩니다. 필요에 따라 조정하세요."

**🗓️ 날짜 선택 (2컬럼 나란히 배치)**
```
📅 시작일          |  🗓️ 종료일
2024-06-30        |  2024-12-30
(6개월 전 자동)    |  (오늘 자동)
```

**📊 실시간 피드백**
선택한 기간이 즉시 표시됩니다:
> "📊 선택된 기간: 2024-06-30 ~ 2024-12-30 (184일)"

**💡 스마트 기본값**
- **시작일**: 오늘에서 6개월 전으로 자동 설정
- **종료일**: 오늘 날짜로 자동 설정
- **실용적**: 가장 많이 사용하는 기간으로 설정되어 별도 조정 불필요

#### **STEP 3: 재고조정 적용**
날짜 설정 후 "⚖️ 재고조정 적용" 버튼을 클릭하면:

**🔄 처리 과정**
1. 선택된 기간 내 조정 건 필터링
2. 제작사품번 기준 매칭
3. 실재고 데이터에 조정 내역 반영
4. 최종 재고차이 계산

#### **STEP 4: 적용 결과 확인**
적용이 완료되면 다음과 같은 결과가 표시됩니다:

**📊 적용 요약 (4개 메트릭 카드)**
- **필터된 조정 건수**: 예) 456건 (선택된 기간 내)
- **매칭된 조정 건수**: 예) 423건 (실재고와 매칭 성공)
- **(+) 조정액**: 예) +1,234,567원 (증가 조정)
- **(-) 조정액**: 예) -2,345,678원 (감소 조정)

**⚠️ 미매칭 품목 확인**
매칭되지 않은 품목이 있으면 경고가 표시됩니다:
- **미매칭 사유**: 제작사품번 불일치, 품목 없음 등
- **상세 정보**: 접기/펼치기로 미매칭 품목 리스트 확인 가능
- **해결 방법**: 품번 형식 통일 또는 해당 품목 수동 처리

### **💡 재고조정 활용 팁**
- **기간 설정**: 마지막 재고조사 ~ 현재 조사 직전까지
- **데이터 정확성**: 제작사품번 형식을 PART 파일과 동일하게 유지
- **성능 최적화**: 너무 긴 기간보다는 적절한 기간 설정 권장
- **검증**: 미매칭 품목이 많으면 데이터 품질 재검토

---

## 📈 **6. Tab 5: 결과보고서**

### **목적**
모든 분석 결과를 종합하여 최종 보고서를 생성합니다.

### **사용 방법**

#### **STEP 1: 점포 정보 입력**
다음 정보를 입력해주세요:

**📋 필수 정보**
- **점포명**: 예) 강남점
- **조사일시**: 2025-01-03 09:00
- **조사방식**: 전체조사 또는 ABC조사
- **조사인원**: 예) 3명

입력 완료 후 **확인** 버튼 클릭

#### **STEP 2: 보고서 카드 확인**
4개의 요약 카드가 표시됩니다:

**🏪 점포 정보**
- 입력한 점포 정보 요약 표시

**📊 전산재고 vs 실재고**
- 전산재고액: 예) 1,234,567,890원
- 증감액: 예) -12,345,678원
- 최종재고액: 예) 1,222,222,212원
- 차액: 예) -12,345,678원 (적자는 🔴빨간색)

**⚖️ 재고조정 영향**
- 조정액: 예) +2,345,678원
- 차액: 예) +2,345,678원 (흑자는 🟢녹색)

**💰 총 재고차액**
- 총 증감액: 예) -10,000,000원
- 총 차액: 예) -10,000,000원 (🟡노란색 배경)

#### **STEP 3: 엑셀 보고서 다운로드**
1. **📊 엑셀 보고서 생성** 버튼 클릭 (세션 상태 기반으로 안정적 생성)
2. **7개 시트로 구성된 완성형 보고서** 즉시 다운로드

**📋 7개 시트 상세 구성 (논리적 순서)**

**1️⃣ 재고조사요약**
- **내용**: 전체 재고조사 결과 종합 요약
- **포함 정보**: 점포정보, 전산재고 현황, 실재고 현황, 재고조정 영향, 총 재고차액
- **레이아웃**: 보고서 형태의 깔끔한 테이블
- **색상 코딩**: 제목(진한 네이비), 정보(연한 파랑), 금액별 색상 구분

**2️⃣ PART원본데이터**
- **내용**: 업로드한 PART 파일의 전체 원본 데이터
- **정렬 기준**: 재고액 기준 내림차순 (가치 높은 품목 우선)
- **포함 정보**: 제작사품번, 부품명, 재고, 재고액, 단가
- **활용**: 원본 데이터 검증 및 참고 자료

**3️⃣ 전체재고리스트**
- **내용**: 재고조사 후 계산값이 적용된 전체 재고 현황
- **정렬 기준**: 차액 절댓값 기준 내림차순 (차이가 큰 품목 우선)
- **포함 정보**: 제작사품번, 부품명, 단가, 재고, 재고액, 실재고, 실재고액, 차이, 차액
- **활용**: 전체 재고 현황 파악 및 차이 분석

**4️⃣ 재고차이리스트(-)**
- **내용**: 실재고가 전산재고보다 **부족한** 품목들
- **정렬 기준**: 차액 기준 오름차순 (손실 큰 품목 우선)
- **색상**: 연한 빨간색 배경 (손실 표시)
- **활용**: 재고 부족 품목 집중 관리 대상 식별

**5️⃣ 재고차이리스트(+)**
- **내용**: 실재고가 전산재고보다 **초과된** 품목들
- **정렬 기준**: 차액 기준 내림차순 (이익 큰 품목 우선)
- **색상**: 연한 녹색 배경 (이익 표시)
- **활용**: 과잉 재고 원인 분석 및 재고 관리 최적화

**6️⃣ 재고조정리스트(-)**
- **내용**: 재고조정으로 **감소된** 품목들
- **정렬 기준**: 일자순 (시간 순서)
- **포함 정보**: 일자, 구분, 제작사품번, 부품명, 수량, 단가, 금액
- **활용**: 재고 감소 조정 내역 추적 및 검증

**7️⃣ 재고조정리스트(+)**
- **내용**: 재고조정으로 **증가된** 품목들
- **정렬 기준**: 일자순 (시간 순서)
- **포함 정보**: 일자, 구분, 제작사품번, 부품명, 수량, 단가, 금액
- **활용**: 재고 증가 조정 내역 추적 및 검증

### **🎨 고급 스타일링 기능**
- **색상 코딩**: 각 시트별 의미에 맞는 색상 적용
- **테두리 처리**: 모든 셀에 깔끔한 테두리
- **컬럼 너비 자동 조정**: 내용에 맞는 최적 너비
- **폰트 최적화**: 맑은 고딕, 크기별 차등 적용
- **정렬**: 각 시트별 최적 정렬 기준 적용

---

## 🚨 **문제 해결 가이드**

### **파일 업로드 문제**

**❌ "파일을 읽을 수 없습니다"**
- **원인**: 파일 형식이 올바르지 않음
- **해결**: .xlsx 또는 .xls 파일인지 확인

**❌ "필수 컬럼이 없습니다"**
- **원인**: 요구되는 컬럼명이 파일에 없음
- **해결**: 컬럼명을 정확히 맞춰주세요

**❌ "파일이 너무 큽니다"**
- **원인**: 50MB 초과
- **해결**: 불필요한 시트나 데이터 삭제 후 재업로드

### **데이터 처리 문제**

**❌ "매칭되지 않는 품목이 많습니다"**
- **원인**: 제작사품번이 일치하지 않음
- **해결**: PART 파일과 조정 파일의 품번 형식 통일

**❌ "계산 결과가 이상합니다"**
- **원인**: 차이값 또는 실재고 입력 오류
- **해결**: 템플릿 재확인 후 올바른 값 입력

### **보고서 생성 문제**

**❌ "엑셀 다운로드가 안 됩니다"**
- **원인**: 모든 단계를 완료하지 않음
- **해결**: Tab 1~4를 순서대로 완료 후 시도

**❌ "보고서 카드가 표시되지 않습니다"**
- **원인**: 점포 정보 미입력
- **해결**: 점포 정보를 모두 입력하고 확인 버튼 클릭

---

## ❓ **자주 묻는 질문 (FAQ)**

### **Q1. 어떤 순서로 사용해야 하나요?**
**A:** 반드시 다음 순서를 지켜주세요:
1. Tab 1: PART 파일 업로드
2. Tab 2: 템플릿 다운로드
3. (오프라인) 재고조사 실시
4. Tab 3: 실재고 데이터 업로드
5. Tab 4: 재고조정 적용 (선택사항)
6. Tab 5: 최종 보고서 생성

### **Q2. 재고조정을 꼭 해야 하나요?**
**A:** 아니오. 재고조정은 선택사항입니다.
- 과거 조정 내역이 있으면 더 정확한 결과를 얻을 수 있습니다
- 조정 내역이 없어도 기본 재고차이 분석은 가능합니다

### **Q3. 데이터가 사라지면 어떻게 하나요?**
**A:** 웹 브라우저를 새로고침하면 데이터가 초기화됩니다.
- 처음부터 다시 업로드해야 합니다
- 중간에 브라우저를 닫지 마세요
- 모든 작업을 연속으로 진행하세요

### **Q4. 엑셀 파일이 깨져서 나옵니다**
**A:** 다음을 확인해주세요:
- 브라우저가 최신 버전인지 확인
- 다른 브라우저에서 시도
- 인터넷 연결 상태 확인

### **Q5. 대용량 파일 처리 시간이 오래 걸립니다**
**A:** 다음과 같이 최적화할 수 있습니다:
- 불필요한 컬럼 제거
- 빈 행 삭제
- 여러 시트가 있으면 필요한 시트만 남기기

### **Q6. 모바일에서도 사용할 수 있나요?**
**A:** 가능하지만 권장하지 않습니다:
- 화면이 작아 사용이 불편할 수 있습니다
- 파일 업로드/다운로드가 제한적일 수 있습니다
- PC 또는 태블릿 사용을 권장합니다

### **Q7. Tab 3에서 다운로드한 파일은 어떻게 활용하나요?**
**A:** 다운로드한 완성된 실재고 파일은 다음과 같이 활용할 수 있습니다:
- **백업용**: 계산이 완료된 완전한 실재고 데이터 보관
- **검토용**: 각 품목별 차이값과 재고액 변동 상세 확인
- **보고용**: 상급자나 본사에 상세 데이터 제출
- **분석용**: 추가적인 데이터 분석이나 차트 생성에 활용
- **참고용**: 다음 재고조사 시 비교 기준 데이터로 사용

### **Q8. 총액 기준 처리 방식이란 무엇인가요?**
**A:** 소수점 오차를 제거하기 위한 새로운 계산 방식입니다:

**📊 계산 방식 비교**
```
예시: 전산재고 3개, 전산재고액 10,000원, 실재고 2개

기존 방식:
단가 = 10,000 ÷ 3 = 3,333.33원
실재고액 = 2 × 3,333.33 = 6,666.66원 (소수점 오차)

총액 방식:
감소수량 = 3 - 2 = 1개
감소분재고액 = 1 × 3,333.33 = 3,333원 (반올림)
실재고액 = 10,000 - 3,333 = 6,667원 (정확)
```

**✅ 장점**
- **정확성**: 소수점 오차 완전 제거
- **실무성**: 재고 흐름 추적이 명확
- **일관성**: 모든 금액이 원 단위 정수

---

## 📞 **지원 및 도움**

### **기술 지원**
- 앱 사용 중 문제가 발생하면 다음을 확인해주세요:
  1. 인터넷 연결 상태
  2. 브라우저 최신 버전 여부
  3. 파일 형식 및 크기

### **데이터 백업**
- 중요한 데이터는 항상 별도 백업 보관
- 원본 파일은 수정하지 말고 복사본 사용
- 최종 보고서는 즉시 다운로드하여 저장

### **보안 주의사항**
- 민감한 재고 정보이므로 공용 컴퓨터 사용 지양
- 작업 완료 후 브라우저 탭 닫기
- 파일은 안전한 장소에 보관

---

## 🎯 **사용 팁**

### **효율적인 작업을 위한 팁**

**📋 사전 준비**
- 모든 파일을 한 폴더에 정리
- 파일명을 알기 쉽게 변경 (예: PART_2025-01-03.xlsx)
- 안정적인 인터넷 환경에서 작업

**⚡ 빠른 작업**
- 여러 탭을 동시에 열지 말고 순서대로 진행
- 큰 파일은 필요한 데이터만 남기고 경량화
- 재고조사는 차이값 입력 방식 사용

**🔍 정확한 결과**
- 제작사품번 형식을 통일
- 숫자 데이터에 쉼표나 특수문자 사용 금지
- 빈 셀은 비워두거나 0으로 입력

**💾 데이터 관리**
- 중간 결과물도 수시로 저장
- 최종 보고서는 여러 형태로 백업
- 작업 날짜를 파일명에 포함

---

**📞 이 매뉴얼로 해결되지 않는 문제가 있으시면, 시스템 관리자에게 문의해주세요.**

**🎉 재고조사 앱을 활용하여 효율적인 재고 관리를 해보세요!** 