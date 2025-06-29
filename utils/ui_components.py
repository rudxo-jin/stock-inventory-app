import streamlit as st
from datetime import date


class UIComponents:
    """UI 컴포넌트와 스타일을 관리하는 클래스"""
    
    @staticmethod
    def get_card_styles():
        """카드 스타일 CSS를 반환"""
        return """
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
        """
    
    @staticmethod
    def render_store_info_form():
        """점포 정보 입력 폼을 렌더링"""
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
            
            # 폼이 제출되었을 때만 store_info 반환
            if generate_report:
                return {
                    'store_name': store_name,
                    'survey_date': survey_date.strftime('%Y년 %m월 %d일'),
                    'survey_method': survey_method,
                    'survey_staff': survey_staff
                }
            else:
                return None
    
    @staticmethod
    def render_store_info_card(store_info):
        """점포 정보 카드를 렌더링"""
        return f"""
        <div class="card-container">
            <div class="section-card">
                <div class="section-title">🏪 점포 정보</div>
                <table class="metric-table">
                    <tr class="metric-row">
                        <td class="metric-label">점포명</td>
                        <td class="metric-value">{store_info['store_name']}</td>
                    </tr>
                    <tr class="metric-row">
                        <td class="metric-label">조사일시</td>
                        <td class="metric-value">{store_info['survey_date']}</td>
                    </tr>
                    <tr class="metric-row">
                        <td class="metric-label">조사방식</td>
                        <td class="metric-value">{store_info['survey_method']}</td>
                    </tr>
                    <tr class="metric-row">
                        <td class="metric-label">조사인원</td>
                        <td class="metric-value">{store_info['survey_staff']}</td>
                    </tr>
                </table>
            </div>
        </div>
        """
    
    @staticmethod
    def render_inventory_comparison_card(inv_comp):
        """전산재고 vs 실재고 카드를 렌더링"""
        return f"""
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
        """
    
    @staticmethod
    def render_adjustment_impact_card(adj_imp):
        """재고조정 영향 카드를 렌더링"""
        return f"""
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
        """
    
    @staticmethod
    def render_total_impact_card(total_imp):
        """총 재고차액 카드를 렌더링"""
        return f"""
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
        """
    
    @staticmethod
    def show_progress_sidebar():
        """사이드바에 진행 단계를 표시"""
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
    
    @staticmethod
    def render_report_cards(report_data):
        """전체 보고서 카드들을 렌더링"""
        # CSS 스타일 적용
        st.markdown(UIComponents.get_card_styles(), unsafe_allow_html=True)
        
        # 1. 점포 정보 카드
        st.markdown(UIComponents.render_store_info_card(report_data['store_info']), unsafe_allow_html=True)
        
        # 구분선
        st.markdown("---")
        
        # 2. 전산재고 vs 실재고 카드
        st.markdown(UIComponents.render_inventory_comparison_card(report_data['inventory_comparison']), unsafe_allow_html=True)
        
        # 3. 재고조정 영향 카드
        st.markdown(UIComponents.render_adjustment_impact_card(report_data['adjustment_impact']), unsafe_allow_html=True)
        
        # 4. 총 재고차액 카드
        st.markdown(UIComponents.render_total_impact_card(report_data['total_impact']), unsafe_allow_html=True) 