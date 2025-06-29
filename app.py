import streamlit as st
import pandas as pd
import os
from datetime import datetime, date

# utils 모듈 import
from utils.data_processor import PartDataProcessor
from utils.adjustment_processor import AdjustmentProcessor
from utils.file_converter import ExcelFileConverter
from utils.report_generator import ReportGenerator
from utils.ui_components import UIComponents

# 페이지 설정 (배포 최적화)
st.set_page_config(
    page_title="재고조사 앱",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 배포 환경 체크
@st.cache_data
def is_cloud_environment():
    """클라우드 배포 환경인지 확인"""
    return os.getenv('STREAMLIT_SHARING_MODE') is not None or os.getenv('DYNO') is not None

# 캐시된 프로세서 초기화 (배포 최적화)
@st.cache_resource
def get_processors():
    """프로세서 인스턴스들을 캐시하여 메모리 효율성 향상"""
    try:
        return {
            'part_processor': PartDataProcessor(),
            'adjustment_processor': AdjustmentProcessor(),
            'report_generator': ReportGenerator()
        }
    except Exception as e:
        st.error(f"프로세서 초기화 오류: {str(e)}")
        return None

# 메인 함수
def main():
    st.title("📦 재고조사 앱")
    st.markdown("---")
    
    # 사이드바 진행 단계 표시
    UIComponents.show_progress_sidebar()
    
    # 캐시된 프로세서 가져오기
    processors = get_processors()
    
    # 세션 상태 초기화
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'part_data' not in st.session_state:
        st.session_state.part_data = None
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
                            success, message, data = processors['part_processor'].load_part_file(converted_file_path)
                            
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
            stats = processors['part_processor'].get_summary_stats()
            
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
                    template = processors['part_processor'].create_inventory_template()
                    
                    # 메모리에서 엑셀 파일 생성 (웹 배포 호환)
                    from io import BytesIO
                    buffer = BytesIO()
                    template.to_excel(buffer, index=False, engine='openpyxl')
                    buffer.seek(0)
                    
                    st.success("✅ 템플릿이 생성되었습니다!")
                    
                    # 파일 다운로드 버튼
                    st.download_button(
                        label="📥 템플릿 다운로드",
                        data=buffer.getvalue(),
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
                        
                        # 데이터 검증 및 계산
                        success, message, processed_data = processors['part_processor'].validate_inventory_data(inventory_df)
                        
                        if success:
                            st.session_state.inventory_data = processed_data
                            st.session_state.step = 4
                            st.success(message)
                            
                            # 처리 결과 미리보기
                            st.markdown("### 📊 처리 결과")
                            
                            # 요약 통계
                            total_items = len(processed_data)
                            changed_items = len(processed_data[processed_data['차이'] != 0])
                            positive_diff = processed_data[processed_data['차이'] > 0]['차이'].sum()
                            negative_diff = processed_data[processed_data['차이'] < 0]['차이'].sum()
                            total_diff_value = processed_data['차액'].sum()
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("총 품목 수", f"{total_items:,}개")
                                st.metric("변경된 품목", f"{changed_items:,}개")
                            with col2:
                                st.metric("증가 수량", f"{positive_diff:,.0f}")
                                st.metric("감소 수량", f"{negative_diff:,.0f}")
                            with col3:
                                st.metric("총 차액", f"{total_diff_value:,.0f}원")
                            
                            # 데이터 미리보기
                            st.markdown("### 📋 데이터 미리보기")
                            st.dataframe(processed_data.head(10), use_container_width=True)
                            
                        else:
                            st.error(message)
                        
                        # 임시 파일 정리
                        ExcelFileConverter.cleanup_temp_file(converted_file_path)
                    else:
                        st.error("❌ 파일 처리 실패")
                        
                except Exception as e:
                    st.error(f"❌ 파일 처리 오류: {str(e)}")
        else:
            st.warning("⚠️ 먼저 이전 단계를 완료해주세요.")
    
    with tab4:
        st.header("⚖️ 재고조정 적용")
        st.write("재고조정 파일을 업로드하고 기간을 설정하여 적용할 수 있습니다. (선택사항)")
        
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
                    st.success(f"✅ 파일 업로드 완료: {uploaded_adjustment.name}")
                    
                    # 재고조정 파일 로드
                    success, message, adj_data = processors['adjustment_processor'].load_adjustment_file(converted_file_path)
                    
                    if success:
                        st.session_state.adjustment_data = adj_data
                        st.success(message)
                        
                        # 데이터 미리보기
                        st.markdown("### 📋 재고조정 데이터 미리보기")
                        st.dataframe(adj_data.head(10), use_container_width=True)
                        
                        # 날짜 범위 설정
                        st.markdown("### 📅 적용 기간 설정")
                        
                        # 폼으로 날짜 입력과 적용 버튼을 함께 처리
                        with st.form("adjustment_form"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # 기본값을 조정 데이터의 최소/최대 날짜로 설정
                                min_date = adj_data['일자'].min().date() if not adj_data.empty else date.today()
                                max_date = adj_data['일자'].max().date() if not adj_data.empty else date.today()
                                
                                start_date = st.date_input(
                                    "시작일",
                                    value=min_date,
                                    min_value=date(1900, 1, 1),
                                    max_value=date(2100, 12, 31)
                                )
                            
                            with col2:
                                end_date = st.date_input(
                                    "종료일",
                                    value=max_date,
                                    min_value=date(1900, 1, 1),
                                    max_value=date(2100, 12, 31)
                                )
                            
                            # 재고조정 적용 버튼
                            apply_adjustment = st.form_submit_button("⚖️ 재고조정 적용", type="primary")
                        
                        if apply_adjustment:
                            if start_date <= end_date:
                                with st.spinner("⚖️ 재고조정을 적용 중입니다..."):
                                    # 날짜 범위로 필터링
                                    filter_success, filter_message, filtered_data = processors['adjustment_processor'].filter_by_date_range(start_date, end_date)
                                    
                                    if filter_success and st.session_state.inventory_data is not None:
                                        # 실재고 데이터에 재고조정 적용
                                        apply_success, apply_message, final_data, adj_summary = processors['adjustment_processor'].apply_adjustments_to_inventory(
                                            st.session_state.inventory_data, filtered_data
                                        )
                                        
                                        if apply_success:
                                            st.session_state.final_data = final_data
                                            st.session_state.adjustment_summary = adj_summary
                                            st.session_state.step = max(st.session_state.step, 4)
                                            st.success(apply_message)
                                            
                                            # 적용 결과 표시
                                            st.markdown("### 📊 재고조정 적용 결과")
                                            
                                            col1, col2, col3 = st.columns(3)
                                            with col1:
                                                st.metric("적용된 조정 건수", f"{len(filtered_data):,}건")
                                            with col2:
                                                total_adj_qty = filtered_data['수량'].sum()
                                                st.metric("총 조정 수량", f"{total_adj_qty:,.0f}")
                                            with col3:
                                                # 조정액 계산 (단가 * 수량)
                                                total_adj_value = (filtered_data['수량'] * filtered_data.get('단가', 0)).sum() if '단가' in filtered_data.columns else 0
                                                st.metric("총 조정액", f"{total_adj_value:,.0f}원")
                                            
                                            st.rerun()
                                        else:
                                            st.error(apply_message)
                                    elif not filter_success:
                                        st.error(filter_message)
                                    else:
                                        st.warning("⚠️ 먼저 실재고 데이터를 입력해주세요.")
                            else:
                                st.error("❌ 시작일이 종료일보다 늦을 수 없습니다.")
                    else:
                        st.error(message)
                    
                    # 임시 파일 정리
                    ExcelFileConverter.cleanup_temp_file(converted_file_path)
                else:
                    st.error("❌ 파일 처리 실패")
                    
            except Exception as e:
                st.error(f"❌ 파일 처리 오류: {str(e)}")
        
        # 재고조정 요약 정보 표시 (적용된 경우에만)
        if st.session_state.adjustment_summary is not None:
            st.markdown("### 📋 재고조정 요약")
            summary = processors['adjustment_processor'].get_adjustment_summary()
            
            if summary:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("(+) 조정 건수", f"{summary.get('positive_count', 0):,}건")
                    st.metric("(+) 조정 수량", f"{summary.get('positive_qty', 0):,.0f}")
                with col2:
                    st.metric("(-) 조정 건수", f"{summary.get('negative_count', 0):,}건")
                    st.metric("(-) 조정 수량", f"{abs(summary.get('negative_qty', 0)):,.0f}")
    
    with tab5:
        st.header("📊 결과보고서")
        
        # 조건 확인 (step >= 3이고 inventory_data가 있으면 OK)
        if st.session_state.step >= 3 and st.session_state.inventory_data is not None:
            # 점포 정보 입력
            store_info = UIComponents.render_store_info_form()
            
            if store_info:
                # final_data가 없으면 inventory_data 사용
                report_data_source = st.session_state.final_data if st.session_state.final_data is not None else st.session_state.inventory_data
                
                # 재고조정 데이터 설정
                filtered_adj_data = getattr(processors['adjustment_processor'], 'filtered_data', None)
                if filtered_adj_data is not None:
                    processors['report_generator'].set_adjustment_data(filtered_adj_data)
                elif st.session_state.adjustment_data is not None:
                    processors['report_generator'].set_adjustment_data(st.session_state.adjustment_data)
                
                report_data = processors['report_generator'].generate_report_data(
                    inventory_data=report_data_source,
                    store_info=store_info
                )
                
                if report_data:
                    # 보고서 카드 표시
                    UIComponents.render_report_cards(report_data)
                    
                    # 요약 통계
                    stats = processors['report_generator'].get_summary_stats()
                    
                    # 엑셀 보고서 다운로드
                    st.markdown("### 📥 보고서 다운로드")
                    
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if st.button("📊 엑셀 보고서 생성", type="primary"):
                            try:
                                with st.spinner("📊 엑셀 보고서를 생성 중입니다..."):
                                    excel_data = processors['report_generator'].create_excel_report()
                                    
                                    if excel_data:
                                        st.success("✅ 엑셀 보고서가 생성되었습니다!")
                                        
                                        # 파일 다운로드 버튼
                                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                        filename = f"재고조사보고서_{timestamp}.xlsx"
                                        
                                        st.download_button(
                                            label="📥 보고서 다운로드",
                                            data=excel_data,
                                            file_name=filename,
                                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                        )
                                    else:
                                        st.error("❌ 엑셀 보고서 생성 실패")
                            except Exception as e:
                                st.error(f"❌ 보고서 생성 오류: {str(e)}")
                    
                    with col2:
                        st.info("📋 **보고서 구성**: 요약보고서, 재고차이리스트, 재고조정리스트 (3개 시트)")
                else:
                    st.error("❌ 보고서 데이터 생성 실패")
        else:
            st.warning("⚠️ 먼저 이전 단계를 완료해주세요.")
            
            # 디버깅 정보 (개발용)
            if st.checkbox("🔧 디버깅 정보 표시"):
                st.write(f"현재 단계: {st.session_state.step}")
                st.write(f"PART 데이터: {'있음' if st.session_state.part_data is not None else '없음'}")
                st.write(f"실재고 데이터: {'있음' if st.session_state.inventory_data is not None else '없음'}")
                st.write(f"최종 데이터: {'있음' if st.session_state.final_data is not None else '없음'}")
                
                # 강제 보고서 생성 (개발/테스트용)
                if st.session_state.inventory_data is not None:
                    if st.button("🔧 강제 보고서 생성 (테스트용)"):
                        st.session_state.step = 5
                        st.rerun()

if __name__ == "__main__":
    main() 