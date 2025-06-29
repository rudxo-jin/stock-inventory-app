import os
import tempfile
import win32com.client as win32
from pathlib import Path
import streamlit as st

class ExcelFileConverter:
    """엑셀 파일 자동 변환 클래스"""
    
    @staticmethod
    def convert_xls_to_xlsx(file_path):
        """
        .xls 파일을 .xlsx로 변환
        
        Args:
            file_path (str): 변환할 .xls 파일 경로
            
        Returns:
            str: 변환된 .xlsx 파일 경로
        """
        try:
            # Excel 애플리케이션 시작
            excel = win32.Dispatch('Excel.Application')
            excel.Visible = False
            excel.DisplayAlerts = False
            
            # 파일 열기
            workbook = excel.Workbooks.Open(file_path)
            
            # .xlsx 확장자로 새 파일명 생성
            xlsx_path = file_path.replace('.xls', '.xlsx')
            
            # .xlsx 형식으로 저장 (FileFormat=51은 xlsx)
            workbook.SaveAs(xlsx_path, FileFormat=51)
            
            # 워크북 닫기
            workbook.Close()
            excel.Quit()
            
            return xlsx_path
            
        except Exception as e:
            st.error(f"파일 변환 중 오류 발생: {str(e)}")
            # Excel 프로세스 정리
            try:
                excel.Quit()
            except:
                pass
            return None
    
    @staticmethod
    def process_uploaded_file(uploaded_file):
        """
        업로드된 파일을 처리하여 .xlsx 형식으로 변환
        
        Args:
            uploaded_file: Streamlit 업로드 파일 객체
            
        Returns:
            str: 처리된 파일 경로
        """
        if uploaded_file is None:
            return None
            
        # 임시 디렉토리에 파일 저장
        temp_dir = tempfile.mkdtemp()
        file_extension = Path(uploaded_file.name).suffix.lower()
        
        # 원본 파일 저장
        temp_file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        # .xls 파일인 경우 변환
        if file_extension == '.xls':
            st.info("🔄 .xls 파일을 .xlsx로 변환 중...")
            converted_path = ExcelFileConverter.convert_xls_to_xlsx(temp_file_path)
            if converted_path:
                st.success("✅ 파일 변환 완료!")
                return converted_path
            else:
                st.error("❌ 파일 변환 실패")
                return None
        
        # .xlsx 파일인 경우 그대로 반환
        elif file_extension == '.xlsx':
            return temp_file_path
        
        else:
            st.error(f"지원하지 않는 파일 형식입니다: {file_extension}")
            return None
    
    @staticmethod
    def cleanup_temp_file(file_path):
        """임시 파일 정리"""
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                # 디렉토리도 비어있으면 삭제
                temp_dir = os.path.dirname(file_path)
                if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                    os.rmdir(temp_dir)
        except Exception as e:
            pass  # 임시 파일 정리 실패는 무시 