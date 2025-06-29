import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import sys

# utils 모듈 import
from utils.data_processor import PartDataProcessor
from utils.adjustment_processor import AdjustmentProcessor
from utils.file_converter import ExcelFileConverter
from utils.report_generator import ReportGenerator

# 페이지 설정
st.set_page_config(
    page_title="재고조사 앱",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바에 진행 단계 표시
def show_progress_sidebar():
    st.sidebar.title("📋 진행 단계")
    
    steps = [
        "1️⃣ PART 파일 업로드",
        "2️⃣ 실재고 템플릿 다운로드", 
        "3️⃣ 실재고 데이터 업로드",
        "4️⃣ 재고조정 파일 업로드",
        "5️⃣ 결과보고서 생성"
    ]
    
    current_step = st.session_state.get('step', 1)
    
    for i, step in enumerate(steps, 1):
        if i < current_step:
            st.sidebar.success(f"✅ {step}")
        elif i == current_step:
            st.sidebar.info(f"🔄 {step}")
        else:
            st.sidebar.write(f"⏳ {step}")

# 메인 함수
def main():
    st.title("📦 재고조사 앱")
    st.markdown("---")
    
    # 사이드바 진행 단계 표시
    show_progress_sidebar()
    
    # 세션 상태 초기화
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'part_data' not in st.session_state:
        st.session_state.part_data = None
    if 'part_processor' not in st.session_state:
        st.session_state.part_processor = PartDataProcessor()
    if 'adjustment_processor' not in st.session_state:
        st.session_state.adjustment_processor = AdjustmentProcessor()
    if 'report_generator' not in st.session_state:
        st.session_state.report_generator = ReportGenerator()
    if 'inventory_data' not in st.session_state:
        st.session_state.inventory_data = None
    if 'adjustment_data' not in st.session_state:
        st.session_state.adjustment_data = None
    if 'final_data' not in st.session_state:
        st.session_state.final_data = None
    if 'adjustment_summary' not in st.session_state:
        st.session_state.adjustment_summary = None
    
    # 탭 생성
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1️⃣ PART 파일", 
        "2️⃣ 실재고 템플릿", 
        "3️⃣ 실재고 입력", 
        "4️⃣ 재고조정", 
        "5️⃣ 결과보고서"
    ])
    
    with tab1:
        st.header("📁 PART 파일 업로드")
        st.write("PART로 시작하는 엑셀 파일을 업로드해주세요.")
        
        uploaded_file = st.file_uploader(
            "PART 파일 선택",
            type=['xlsx', 'xls'],
            key="part_file"
        )
        
        if uploaded_file is not None:
            try:
                # 파일 자동 변환 처리
                converted_file_path = ExcelFileConverter.process_uploaded_file(uploaded_file)
                
                if converted_file_path:
                    st.success(f"✅ 파일 업로드 완료: {uploaded_file.name}")
                    
                    # 데이터 분석 버튼
                    if st.button("📊 데이터 분석하기", type="primary"):
                        with st.spinner("📊 PART 파일을 분석 중입니다..."):
                            success, message, data = st.session_state.part_processor.load_part_file(converted_file_path)
                            
                            if success:
                                st.session_state.part_data = data
                                st.session_state.step = 2
                                st.success(message)
                                
                                # 임시 파일 정리
                                ExcelFileConverter.cleanup_temp_file(converted_file_path)
                                st.rerun()
                            else:
                                st.error(message)
                                # 임시 파일 정리
                                ExcelFileConverter.cleanup_temp_file(converted_file_path)
                else:
                    st.error("❌ 파일 처리 실패")
                            
            except Exception as e:
                st.error(f"❌ 파일 업로드 오류: {str(e)}")
        
        # 분석 결과 표시
        if st.session_state.part_data is not None:
            st.markdown("### 📊 분석 결과")
            
            # 요약 통계
            stats = st.session_state.part_processor.get_summary_stats()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("총 품목 수", f"{stats['total_items']:,}개")
                st.metric("재고 없는 품목", f"{stats['zero_stock_items']:,}개")
            with col2:
                st.metric("총 재고량", f"{stats['total_stock']:,.0f}")
                st.metric("평균 단가", f"{stats['avg_unit_price']:,.0f}원")
            with col3:
                st.metric("총 재고액", f"{stats['total_stock_value']:,.0f}원")
                st.metric("재고액 없는 품목", f"{stats['zero_value_items']:,}개")
            
            # 데이터 미리보기
            st.markdown("### 📋 데이터 미리보기")
            st.dataframe(
                st.session_state.part_data.head(10),
                use_container_width=True
            )
    
    with tab2:
        st.header("📋 실재고 입력 템플릿")
        if st.session_state.step >= 2 and st.session_state.part_data is not None:
            st.write("PART 파일 분석이 완료되었습니다. 실재고 입력용 템플릿을 다운로드하세요.")
            
            # 템플릿 생성 및 다운로드
            if st.button("📥 템플릿 생성", type="primary"):
                try:
                    template = st.session_state.part_processor.create_inventory_template()
                    
                    # 엑셀 파일로 저장
                    template_path = os.path.join("templates", "실재고입력템플릿.xlsx")
                    template.to_excel(template_path, index=False, engine='openpyxl')
                    
                    st.success("✅ 템플릿이 생성되었습니다!")
                    
                    # 파일 다운로드 버튼
                    with open(template_path, "rb") as file:
                        st.download_button(
                            label="📥 템플릿 다운로드",
                            data=file,
                            file_name="실재고입력템플릿.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    
                    # 템플릿 미리보기
                    st.markdown("### 📋 템플릿 미리보기")
                    st.dataframe(template.head(10), use_container_width=True)
                    
                    # 템플릿 정보 표시
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("템플릿 품목 수", f"{len(template):,}개")
                    with col2:
                        excluded_count = len(st.session_state.part_data) - len(template)
                        st.metric("제외된 품목 수", f"{excluded_count:,}개 (재고 없음)")
                    
                    # 사용 안내
                    st.markdown("### 📝 사용 안내")
                    st.info("""
                    **실재고 입력 방법:**
                    - **실재고** 컬럼에 실제 재고량을 입력하거나
                    - **차이** 컬럼에 차이값을 입력하세요 (예: -5, +10)
                    - 둘 다 입력된 경우 **차이값이 우선**됩니다
                    - 입력하지 않은 품목은 기존 재고로 유지됩니다
                    - **재고가 없는 품목은 템플릿에서 제외**되었습니다
                    """)
                    
                    st.session_state.step = 3
                    
                except Exception as e:
                    st.error(f"❌ 템플릿 생성 오류: {str(e)}")
        else:
            st.warning("⚠️ 먼저 PART 파일을 업로드하고 분석해주세요.")
    
    with tab3:
        st.header("📝 실재고 데이터 입력")
        if st.session_state.step >= 3:
            st.write("작성된 실재고 데이터를 업로드해주세요.")
            
            uploaded_inventory = st.file_uploader(
                "실재고 파일 선택",
                type=['xlsx', 'xls'],
                key="inventory_file"
            )
            
            if uploaded_inventory is not None:
                try:
                    # 파일 자동 변환 처리
                    converted_file_path = ExcelFileConverter.process_uploaded_file(uploaded_inventory)
                    
                    if converted_file_path:
                        # 파일 읽기
                        inventory_df = pd.read_excel(converted_file_path, engine='openpyxl')
                        
                        # 임시 파일 정리
                        ExcelFileConverter.cleanup_temp_file(converted_file_path)
                        
                        # 데이터 검증 및 계산
                        success, message, processed_data = st.session_state.part_processor.validate_inventory_data(inventory_df)
                    else:
                        st.error("❌ 파일 처리 실패")
                        return
                    
                    if success:
                        st.session_state.inventory_data = processed_data
                        st.success(message)
                        
                        # 처리 결과 표시
                        st.markdown("### 📊 처리 결과")
                        
                        # 차이 요약
                        positive_diff = processed_data[processed_data['차이'] > 0]
                        negative_diff = processed_data[processed_data['차이'] < 0]
                        zero_diff = processed_data[processed_data['차이'] == 0]
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("재고 증가 품목", f"{len(positive_diff):,}개")
                            st.metric("증가 재고액", f"{positive_diff['차액'].sum():,.0f}원")
                        with col2:
                            st.metric("재고 감소 품목", f"{len(negative_diff):,}개") 
                            st.metric("감소 재고액", f"{negative_diff['차액'].sum():,.0f}원")
                        with col3:
                            st.metric("변동 없는 품목", f"{len(zero_diff):,}개")
                            st.metric("총 차액", f"{processed_data['차액'].sum():,.0f}원")
                        
                        # 데이터 미리보기
                        st.markdown("### 📋 처리된 데이터")
                        st.dataframe(processed_data.head(10), use_container_width=True)
                        
                        st.session_state.step = 4
                        
                    else:
                        st.error(message)
                        
                except Exception as e:
                    st.error(f"❌ 파일 처리 오류: {str(e)}")
        else:
            st.warning("⚠️ 먼저 이전 단계를 완료해주세요.")
    
    with tab4:
        st.header("⚖️ 재고조정 처리")
        if st.session_state.step >= 4 and st.session_state.inventory_data is not None:
            st.write("재고조정 파일을 업로드하고 기간을 설정해주세요.")
            
            # 재고조정 파일 업로드
            uploaded_adjustment = st.file_uploader(
                "재고조정 파일 선택",
                type=['xlsx', 'xls'],
                key="adjustment_file"
            )
            
            if uploaded_adjustment is not None:
                try:
                    # 파일 자동 변환 처리
                    converted_file_path = ExcelFileConverter.process_uploaded_file(uploaded_adjustment)
                    
                    if converted_file_path:
                        # 재고조정 파일 로드
                        success, message, adj_data = st.session_state.adjustment_processor.load_adjustment_file(converted_file_path)
                        
                        # 임시 파일 정리
                        ExcelFileConverter.cleanup_temp_file(converted_file_path)
                    else:
                        st.error("❌ 파일 처리 실패")
                        return
                    
                    if success:
                        st.session_state.adjustment_data = adj_data
                        st.success(message)
                        
                        # 재고조정 데이터 미리보기
                        st.markdown("### 📋 재고조정 데이터 미리보기")
                        st.dataframe(adj_data.head(10), use_container_width=True)
                        
                        # 날짜 범위 설정
                        st.markdown("### 📅 재고조정 기간 설정")
                        
                        # 날짜 범위 초기값 설정
                        min_date = adj_data['일자'].min().date()
                        max_date = adj_data['일자'].max().date()
                        
                        # 데이터 날짜 범위 정보 표시
                        st.info(f"📊 데이터 날짜 범위: {min_date} ~ {max_date}")
                        
                        # 폼으로 묶어서 한번에 처리
                        with st.form("adjustment_form"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                start_date = st.date_input(
                                    "시작일",
                                    value=min_date,
                                    min_value=min_date,
                                    max_value=date(max_date.year + 1, 12, 31),
                                    format="YYYY-MM-DD"
                                )
                            
                            with col2:
                                end_date = st.date_input(
                                    "종료일", 
                                    value=max_date,
                                    min_value=min_date,
                                    max_value=date(max_date.year + 1, 12, 31),
                                    format="YYYY-MM-DD"
                                )
                            
                            # 재고조정 적용 버튼 (하나로 통합)
                            apply_submitted = st.form_submit_button("📊 재고조정 적용", type="primary")
                        
                        # 재고조정 적용 처리
                        if apply_submitted:
                            # 날짜 유효성 검증
                            if start_date > end_date:
                                st.error("⚠️ 시작일이 종료일보다 늦을 수 없습니다.")
                            else:
                                # 선택된 날짜가 데이터 범위를 벗어나는 경우 경고
                                if start_date < min_date or end_date > max_date:
                                    st.warning(f"⚠️ 선택된 기간이 데이터 범위({min_date} ~ {max_date})를 벗어납니다.")
                                
                                st.info(f"🔄 적용 기간: {start_date} ~ {end_date}")
                                
                                # 날짜 범위 필터링
                                filter_success, filter_message, filtered_data = st.session_state.adjustment_processor.filter_by_date_range(start_date, end_date)
                            
                            if filter_success:
                                st.success(filter_message)
                                
                                # 재고조정 적용
                                apply_success, apply_message, final_data, adj_summary = st.session_state.adjustment_processor.apply_adjustments_to_inventory(
                                    st.session_state.inventory_data,
                                    st.session_state.part_data
                                )
                                
                                if apply_success:
                                    st.session_state.final_data = final_data
                                    st.session_state.adjustment_summary = adj_summary
                                    st.success(apply_message)
                                    
                                    # 재고조정 요약 표시
                                    st.markdown("### 📊 재고조정 적용 결과")
                                    
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.metric("적용된 조정건수", f"{adj_summary['total_adjustments']:,}건")
                                        st.metric("증가 조정", f"{adj_summary['positive_adjustments']:,}건")
                                    with col2:
                                        st.metric("감소 조정", f"{adj_summary['negative_adjustments']:,}건")
                                        st.metric("증가 재고액", f"{adj_summary['positive_amount']:,.0f}원")
                                    with col3:
                                        st.metric("감소 재고액", f"{adj_summary['negative_amount']:,.0f}원")
                                        st.metric("순 조정액", f"{adj_summary['positive_amount'] - adj_summary['negative_amount']:,.0f}원")
                                    
                                    # 매칭되지 않은 품목 표시
                                    if adj_summary['unmatched_items']:
                                        st.warning(f"⚠️ {len(adj_summary['unmatched_items'])}개 품목이 실재고 데이터와 매칭되지 않았습니다.")
                                        
                                        unmatched_df = pd.DataFrame(adj_summary['unmatched_items'])
                                        st.dataframe(unmatched_df, use_container_width=True)
                                    
                                    # 최종 데이터 미리보기
                                    st.markdown("### 📋 최종 재고 데이터")
                                    st.dataframe(final_data.head(10), use_container_width=True)
                                    
                                    st.session_state.step = 5
                                    
                                else:
                                    st.error(apply_message)
                            else:
                                st.error(filter_message)
                        
                    else:
                        st.error(message)
                        
                except Exception as e:
                    st.error(f"❌ 파일 처리 오류: {str(e)}")
            
            # 재고조정 요약 통계 (파일 로드 후)
            if st.session_state.adjustment_data is not None:
                summary = st.session_state.adjustment_processor.get_adjustment_summary()
                if summary:
                    st.markdown("### 📊 재고조정 파일 요약")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("총 조정건수", f"{summary['total_records']:,}건")
                        st.metric("증가 건수", f"{summary['positive_records']:,}건")
                    with col2:
                        st.metric("감소 건수", f"{summary['negative_records']:,}건")
                        st.metric("대상 품목 수", f"{summary['unique_parts']:,}개")
                    with col3:
                        st.metric("증가 수량", f"{summary['positive_quantity']:,.0f}")
                        st.metric("감소 수량", f"{summary['negative_quantity']:,.0f}")
        else:
            st.warning("⚠️ 먼저 이전 단계를 완료해주세요.")
    
    with tab5:
        st.header("📊 결과보고서")
        
        # 디버깅 정보 항상 표시
        st.write(f"🔍 현재 step: {st.session_state.get('step', 'None')}")
        st.write(f"🔍 final_data 상태: {'있음' if st.session_state.get('final_data') is not None else '없음'}")
        
        # 조건을 더 유연하게 변경
        if (st.session_state.get('step', 0) >= 3 and 
            st.session_state.get('inventory_data') is not None):
            st.write("최종 재고조사 결과보고서를 생성합니다.")
            
            # 점포 정보 입력 폼
            st.markdown("### 🏪 점포 정보 입력")
            
            with st.form("store_info_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    store_name = st.text_input(
                        "점포명", 
                        value="고양점",
                        placeholder="예: 고양점"
                    )
                    survey_method = st.selectbox(
                        "조사방식",
                        ["전수조사", "표본조사"],
                        index=0
                    )
                
                with col2:
                    survey_date = st.date_input(
                        "재고조사일시",
                        value=date.today(),
                        help="재고조사를 실시한 날짜를 선택하세요"
                    )
                    survey_staff = st.text_input(
                        "조사인원",
                        value="",
                        placeholder="조사에 참석한 직원명 표기",
                        help="예: 김영길 외 5명"
                    )
                
                # 보고서 생성 버튼
                generate_report = st.form_submit_button("📋 보고서 생성", type="primary")
            
            # 보고서 생성 처리
            if generate_report:
                # 날짜 형식 변환
                survey_date_str = survey_date.strftime('%Y년 %m월 %d일')
                
                store_info = {
                    'store_name': store_name,
                    'survey_date': survey_date_str,
                    'survey_method': survey_method,
                    'survey_staff': survey_staff
                }
                
                # final_data가 없으면 inventory_data로 대체
                final_data_to_use = st.session_state.get('final_data')
                if final_data_to_use is None:
                    final_data_to_use = st.session_state.get('inventory_data')
                    st.info("📝 재고조정 데이터가 없어 실재고 데이터를 사용합니다.")
                
                # adjustment_summary가 없으면 빈 값으로 생성
                adjustment_summary_to_use = st.session_state.get('adjustment_summary')
                if adjustment_summary_to_use is None:
                    adjustment_summary_to_use = {
                        'total_adjustments': 0,
                        'positive_adjustments': 0,
                        'negative_adjustments': 0,
                        'positive_amount': 0,
                        'negative_amount': 0,
                        'unmatched_items': []
                    }
                    st.info("📝 재고조정 요약이 없어 기본값을 사용합니다.")
                
                # 보고서 데이터 생성
                try:
                    report_data = st.session_state.report_generator.generate_report_data(
                        st.session_state.part_data,
                        st.session_state.inventory_data,
                        final_data_to_use,
                        adjustment_summary_to_use,
                        store_info
                    )
                    
                    st.success("✅ 보고서 데이터 생성 완료!")
                    
                    # 요약 통계 표시
                    stats = st.session_state.report_generator.get_summary_stats()
                    
                    # 점포 정보 카드
                    st.markdown(f"""
                    <div class="card-container">
                        <div class="section-card">
                            <div class="section-title">🏪 점포 정보</div>
                            <table class="metric-table">
                                <tr class="metric-row">
                                    <td class="metric-label">점포명</td>
                                    <td class="metric-value">{store_name}</td>
                                </tr>
                                <tr class="metric-row">
                                    <td class="metric-label">조사일시</td>
                                    <td class="metric-value">{survey_date_str}</td>
                                </tr>
                                <tr class="metric-row">
                                    <td class="metric-label">조사방식</td>
                                    <td class="metric-value">{survey_method}</td>
                                </tr>
                                <tr class="metric-row">
                                    <td class="metric-label">조사인원</td>
                                    <td class="metric-value">{survey_staff}</td>
                                </tr>
                            </table>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # 섹션별 카드 스타일 CSS
                    st.markdown("""
                    <style>
                    .card-container {
                        display: flex;
                        justify-content: center;
                        margin: 0.5rem 0;
                    }
                    .section-card {
                        background-color: #ffffff;
                        padding: 1rem;
                        border-radius: 12px;
                        border: 1px solid #e0e0e0;
                        margin: 0.3rem 0;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        max-width: 600px;
                        width: 100%;
                    }
                    .section-title {
                        font-size: 1.2rem;
                        font-weight: bold;
                        color: #333;
                        margin-bottom: 0.8rem;
                        padding-bottom: 0.3rem;
                        border-bottom: 2px solid #f0f0f0;
                        text-align: center;
                    }
                    .metric-table {
                        width: 100%;
                        border-collapse: collapse;
                        max-width: 500px;
                        margin: 0 auto;
                    }
                    .metric-row {
                        border-bottom: 1px solid #f5f5f5;
                    }
                    .metric-row:last-child {
                        border-bottom: none;
                    }
                    .metric-label {
                        padding: 0.5rem 1rem;
                        font-size: 1rem;
                        color: #555;
                        width: 50%;
                        text-align: left;
                    }
                    .metric-value {
                        padding: 0.5rem 1rem;
                        font-size: 1.1rem;
                        font-weight: bold;
                        text-align: right;
                        width: 50%;
                    }
                    .positive-value {
                        color: #28a745;
                    }
                    .negative-value {
                        color: #dc3545;
                    }
                    .total-value {
                        color: #ffc107;
                        background-color: #fffef8;
                        padding: 0.6rem 1rem;
                        border-radius: 6px;
                    }
                    .total-label {
                        background-color: #fffef8;
                        padding: 0.6rem 1rem;
                        border-radius: 6px;
                        font-weight: bold;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # 1. 전산재고 vs 실재고 섹션
                    inv_comp = stats['inventory_comparison']
                    st.markdown(f"""
                    <div class="card-container">
                        <div class="section-card">
                            <div class="section-title">📊 전산재고 vs 실재고</div>
                            <table class="metric-table">
                                <tr class="metric-row">
                                    <td class="metric-label">전산재고액</td>
                                    <td class="metric-value">{inv_comp['computer_stock_value']:,.0f}원</td>
                                </tr>
                                <tr class="metric-row">
                                    <td class="metric-label">(+) 실재고액</td>
                                    <td class="metric-value positive-value">+{inv_comp['positive_amount']:,.0f}원</td>
                                </tr>
                                <tr class="metric-row">
                                    <td class="metric-label">(-) 실재고액</td>
                                    <td class="metric-value negative-value">-{inv_comp['negative_amount']:,.0f}원</td>
                                </tr>
                                <tr class="metric-row">
                                    <td class="metric-label">최종재고액</td>
                                    <td class="metric-value">{inv_comp['final_stock_value']:,.0f}원</td>
                                </tr>
                                <tr class="metric-row">
                                    <td class="metric-label total-label">차액</td>
                                    <td class="metric-value total-value">{inv_comp['difference']:+,.0f}원</td>
                                </tr>
                            </table>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 2. 재고조정 영향 섹션
                    adj_imp = stats['adjustment_impact']
                    st.markdown(f"""
                    <div class="card-container">
                        <div class="section-card">
                            <div class="section-title">⚖️ 재고조정 영향</div>
                            <table class="metric-table">
                                <tr class="metric-row">
                                    <td class="metric-label">(+) 재고조정액</td>
                                    <td class="metric-value positive-value">+{adj_imp['positive_adjustment']:,.0f}원</td>
                                </tr>
                                <tr class="metric-row">
                                    <td class="metric-label">(-) 재고조정액</td>
                                    <td class="metric-value negative-value">-{adj_imp['negative_adjustment']:,.0f}원</td>
                                </tr>
                                <tr class="metric-row">
                                    <td class="metric-label total-label">재고조정 차액</td>
                                    <td class="metric-value total-value">{adj_imp['adjustment_difference']:+,.0f}원</td>
                                </tr>
                            </table>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 3. 총 재고차액 섹션
                    total_imp = stats['total_impact']
                    st.markdown(f"""
                    <div class="card-container">
                        <div class="section-card">
                            <div class="section-title">💰 총 재고차액</div>
                            <table class="metric-table">
                                <tr class="metric-row">
                                    <td class="metric-label">(+) 총재고차액</td>
                                    <td class="metric-value positive-value">+{total_imp['total_positive']:,.0f}원</td>
                                </tr>
                                <tr class="metric-row">
                                    <td class="metric-label">(-) 총재고차액</td>
                                    <td class="metric-value negative-value">-{total_imp['total_negative']:,.0f}원</td>
                                </tr>
                                <tr class="metric-row">
                                    <td class="metric-label total-label">총재고차액 계</td>
                                    <td class="metric-value total-value">{total_imp['total_difference']:+,.0f}원</td>
                                </tr>
                            </table>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 엑셀 다운로드 버튼
                    st.markdown("### 📥 보고서 다운로드")
                    
                    try:
                        # 엑셀 파일 생성 (메모리에서)
                        excel_data = st.session_state.report_generator.create_excel_report()
                        
                        # 파일명 생성
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"매장재고조사보고서_{timestamp}.xlsx"
                        
                        # 다운로드 버튼
                        st.download_button(
                            label="📥 엑셀 보고서 다운로드",
                            data=excel_data,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            type="primary",
                            key="download_excel_report"  # 고유 키 추가로 상태 유지
                        )
                        
                        st.success("✅ 엑셀 보고서가 준비되었습니다! 위 버튼을 클릭하여 다운로드하세요.")
                        st.info("💡 다운로드 후에도 현재 화면이 유지됩니다.")
                        
                    except Exception as e:
                        st.error(f"❌ 엑셀 생성 오류: {str(e)}")
                        st.write(f"오류 상세: {type(e).__name__}: {str(e)}")
                    
                except Exception as e:
                    st.error(f"❌ 보고서 생성 오류: {str(e)}")
        
        else:
            st.warning("⚠️ 먼저 이전 단계를 완료해주세요.")
            
            # 디버깅 정보 표시
            with st.expander("🔍 현재 상태 확인"):
                st.write(f"현재 단계: {st.session_state.get('step', 'None')}")
                st.write(f"PART 데이터: {'있음' if st.session_state.get('part_data') is not None else '없음'}")
                st.write(f"실재고 데이터: {'있음' if st.session_state.get('inventory_data') is not None else '없음'}")
                st.write(f"재고조정 데이터: {'있음' if st.session_state.get('adjustment_data') is not None else '없음'}")
                st.write(f"최종 데이터: {'있음' if st.session_state.get('final_data') is not None else '없음'}")
                st.write(f"재고조정 요약: {'있음' if st.session_state.get('adjustment_summary') is not None else '없음'}")
                
                # 강제로 보고서 생성 버튼 추가
                st.markdown("---")
                st.info("💡 현재 데이터로 보고서를 생성할 수 있습니다.")
                
                if st.button("🚀 강제 보고서 생성", type="primary", key="force_report"):
                    # 현재 데이터로 보고서 생성
                    if st.session_state.get('inventory_data') is not None:
                        st.session_state.final_data = st.session_state.inventory_data.copy()
                        
                    if st.session_state.get('adjustment_summary') is None:
                        st.session_state.adjustment_summary = {
                            'total_adjustments': 0,
                            'positive_adjustments': 0,
                            'negative_adjustments': 0,
                            'positive_amount': 0,
                            'negative_amount': 0,
                            'unmatched_items': []
                        }
                    
                    st.session_state.step = 5
                    st.success("✅ 보고서 데이터가 준비되었습니다!")
                    st.rerun()

    # 푸터
    st.markdown("---")
    st.markdown("**재고조사 앱 v1.0** | 개발: Claude AI Assistant")

if __name__ == "__main__":
    main() 