import os
import tempfile
import pandas as pd
import streamlit as st


class ExcelFileConverter:
    """엑셀 파일 변환을 담당하는 클래스 (웹앱 배포 호환)"""
    
    @staticmethod
    def process_uploaded_file(uploaded_file):
        """업로드된 파일을 처리하고 필요시 변환"""
        try:
            # 임시 파일로 저장
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # .xls 파일인 경우 처리
            if uploaded_file.name.endswith('.xls'):
                return ExcelFileConverter.handle_xls_file(temp_path)
            else:
                return temp_path
                
        except Exception as e:
            st.error(f"파일 처리 중 오류: {str(e)}")
            return None
    
    @staticmethod
    def handle_xls_file(xls_path):
        """XLS 파일 처리 (웹 환경 호환)"""
        try:
            st.error("❌ .xls 파일은 웹 환경에서 지원되지 않습니다")
            st.error("🌐 **웹앱 환경에서는 .xlsx 파일만 지원됩니다**")
            st.info("💡 **해결 방법:**")
            st.info("1. Excel에서 파일을 열어 '다른 이름으로 저장' → '.xlsx' 형식 선택")
            st.info("2. 또는 Google Sheets에서 열어서 .xlsx로 다운로드")
            st.warning("⚠️ .xlsx 파일로 변환 후 다시 업로드해주세요.")
            
            # 임시 파일 정리
            if os.path.exists(xls_path):
                os.remove(xls_path)
            
            return None
                
        except Exception as e:
            st.error(f"파일 처리 중 오류: {str(e)}")
            return None
    
    @staticmethod
    def cleanup_temp_file(file_path):
        """임시 파일 정리"""
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                    
        except Exception as e:
            # 파일 정리 실패는 치명적이지 않으므로 로그만 출력
            pass  # 웹 환경에서는 조용히 처리 