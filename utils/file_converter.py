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
            
            # .xls 파일인 경우 .xlsx로 변환
            if uploaded_file.name.endswith('.xls'):
                converted_path = ExcelFileConverter.convert_xls_to_xlsx(temp_path)
                return converted_path
            else:
                return temp_path
                
        except Exception as e:
            st.error(f"파일 처리 중 오류: {str(e)}")
            return None
    
    @staticmethod
    def convert_xls_to_xlsx(xls_path):
        """XLS 파일을 XLSX로 변환 (크로스 플랫폼 호환)"""
        try:
            # pandas + xlrd를 사용한 변환 (웹앱 배포 호환)
            st.info("📄 .xls 파일을 .xlsx로 변환 중...")
            
            # xlrd 1.2.0을 사용하여 .xls 파일 읽기
            df = pd.read_excel(xls_path, engine='xlrd')
            
            # .xlsx로 저장
            xlsx_path = xls_path.replace('.xls', '.xlsx')
            df.to_excel(xlsx_path, index=False, engine='openpyxl')
            
            st.success("✅ 파일 변환 완료")
            return xlsx_path
            
        except Exception as e:
            st.error(f"파일 변환 중 오류: {str(e)}")
            st.error("💡 .xls 파일 대신 .xlsx 파일을 사용해주세요.")
            return None
    
    @staticmethod
    def cleanup_temp_file(file_path):
        """임시 파일 정리"""
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                
            # .xls에서 변환된 .xlsx 파일도 정리
            if file_path and file_path.endswith('.xlsx'):
                xls_path = file_path.replace('.xlsx', '.xls')
                if os.path.exists(xls_path):
                    os.remove(xls_path)
                    
        except Exception as e:
            # 파일 정리 실패는 치명적이지 않으므로 로그만 출력
            st.warning(f"임시 파일 정리 실패: {str(e)}") 