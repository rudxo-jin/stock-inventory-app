import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
import os
from typing import Optional, Tuple, Dict

class PartDataProcessor:
    """PART 파일 데이터 처리 클래스"""
    
    def __init__(self):
        self.required_columns = ['제작사 품번', '부품명', '재고', '재고액']
        self.data = None
        self.unit_prices = None
    
    def load_part_file(self, file_path: str) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """
        PART 엑셀 파일을 로드하고 필요한 컬럼을 추출
        
        Returns:
            (성공여부, 메시지, 데이터프레임)
        """
        try:
            # openpyxl 엔진만 사용 (자동 변환된 .xlsx 파일)
            df = pd.read_excel(file_path, engine='openpyxl')
            
            # 필요한 컬럼 존재 확인
            missing_columns = [col for col in self.required_columns if col not in df.columns]
            if missing_columns:
                return False, f"필수 컬럼이 없습니다: {', '.join(missing_columns)}", None
            
            # 필요한 컬럼만 추출
            processed_df = df[self.required_columns].copy()
            
            # 데이터 정리
            processed_df = self._clean_data(processed_df)
            
            # 단가 계산
            processed_df = self._calculate_unit_prices(processed_df)
            
            self.data = processed_df
            
            return True, f"✅ 성공적으로 로드됨 ({len(processed_df):,}개 품목)", processed_df
            
        except Exception as e:
            return False, f"파일 읽기 오류: {str(e)}", None
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """데이터 정리 및 검증"""
        # 결측값 처리
        df = df.dropna(subset=['제작사 품번', '부품명']).copy()  # 추가적인 copy() 호출
        
        # 숫자 컬럼 타입 변환 (pandas 2.x 호환)
        df.loc[:, '재고'] = pd.to_numeric(df['재고'], errors='coerce').fillna(0)
        df.loc[:, '재고액'] = pd.to_numeric(df['재고액'], errors='coerce').fillna(0)
        
        # 음수값 처리 (0으로 변환)
        df.loc[:, '재고'] = df['재고'].clip(lower=0)
        df.loc[:, '재고액'] = df['재고액'].clip(lower=0)
        
        return df
    
    def _calculate_unit_prices(self, df: pd.DataFrame) -> pd.DataFrame:
        """단가 계산 (재고액 ÷ 재고)"""
        # 재고가 0인 경우 단가를 0으로 설정
        df.loc[:, '단가'] = np.where(
            df['재고'] > 0,
            df['재고액'] / df['재고'],
            0
        )
        
        # 단가를 소수점 둘째 자리까지 반올림
        df.loc[:, '단가'] = df['단가'].round(2)
        
        return df
    
    def get_summary_stats(self) -> Dict:
        """데이터 요약 통계 반환"""
        if self.data is None:
            return {}
        
        return {
            'total_items': len(self.data),
            'total_stock': self.data['재고'].sum(),
            'total_stock_value': self.data['재고액'].sum(),
            'avg_unit_price': self.data['단가'].mean(),
            'zero_stock_items': len(self.data[self.data['재고'] == 0]),
            'zero_value_items': len(self.data[self.data['재고액'] == 0])
        }
    
    def create_inventory_template(self) -> pd.DataFrame:
        """실재고 입력용 템플릿 생성 (재고가 있는 품목만, 부품명 오름차순 정렬)"""
        if self.data is None:
            raise ValueError("먼저 PART 파일을 로드해주세요.")
        
        # 재고가 0보다 큰 품목만 필터링
        filtered_data = self.data[self.data['재고'] > 0].copy()
        
        # 부품명 오름차순으로 정렬
        filtered_data = filtered_data.sort_values('부품명', ascending=True)
        
        # 기본 컬럼 복사
        template = filtered_data[['제작사 품번', '부품명', '재고', '재고액', '단가']].copy()
        
        # 실재고 입력용 컬럼 추가 (빈 값으로)
        template['실재고'] = ''
        template['실재고액'] = ''
        template['차이'] = ''
        template['차액'] = ''
        
        # 인덱스 리셋
        template = template.reset_index(drop=True)
        
        return template
    
    def validate_inventory_data(self, df: pd.DataFrame) -> Tuple[bool, str, pd.DataFrame]:
        """업로드된 실재고 데이터 검증 및 계산"""
        try:
            # 필수 컬럼 확인
            required_cols = ['제작사 품번', '부품명', '재고', '재고액', '단가', '실재고', '실재고액', '차이', '차액']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                return False, f"필수 컬럼이 없습니다: {', '.join(missing_cols)}", df
            
            # 데이터 타입 변환
            numeric_cols = ['재고', '재고액', '단가', '실재고', '실재고액', '차이', '차액']
            for col in numeric_cols:
                df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')
            
            # 계산 수행
            df = self._calculate_inventory_values(df)
            
            return True, "✅ 실재고 데이터 처리 완료", df
            
        except Exception as e:
            return False, f"데이터 처리 오류: {str(e)}", df
    
    def _calculate_inventory_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """실재고 관련 값들 자동 계산 (총액 기준 처리 방식)"""
        df = df.copy()
        
        for idx, row in df.iterrows():
            재고 = row['재고']
            재고액 = row['재고액']
            단가 = row['단가']
            실재고 = row['실재고']
            차이 = row['차이']
            
            # 차이값이 입력된 경우 (우선순위)
            if pd.notna(차이) and 차이 != '':
                실재고_계산 = 재고 + 차이
                
                # 총액 기준 처리 방식
                실재고액_계산, 차액_계산 = self._calculate_stock_value_by_total(
                    재고, 재고액, 단가, 실재고_계산
                )
                
                df.at[idx, '실재고'] = 실재고_계산
                df.at[idx, '실재고액'] = 실재고액_계산
                df.at[idx, '차액'] = 차액_계산
                
            # 실재고가 입력된 경우
            elif pd.notna(실재고) and 실재고 != '':
                차이_계산 = 실재고 - 재고
                
                # 총액 기준 처리 방식
                실재고액_계산, 차액_계산 = self._calculate_stock_value_by_total(
                    재고, 재고액, 단가, 실재고
                )
                
                df.at[idx, '실재고액'] = 실재고액_계산
                df.at[idx, '차이'] = 차이_계산
                df.at[idx, '차액'] = 차액_계산
                
            # 아무것도 입력되지 않은 경우: 실재고 = 재고로 설정하고 총액 기준 처리 적용
            else:
                실재고_계산 = 재고  # 실재고 = 재고 (변동 없음)
                차이_계산 = 0       # 차이 = 0
                
                # 총액 기준 처리 방식 적용 (변동수량=0이어도 일관성 유지)
                실재고액_계산, 차액_계산 = self._calculate_stock_value_by_total(
                    재고, 재고액, 단가, 실재고_계산
                )
                
                df.at[idx, '실재고'] = 실재고_계산
                df.at[idx, '실재고액'] = 실재고액_계산
                df.at[idx, '차이'] = 차이_계산
                df.at[idx, '차액'] = 차액_계산
        
        # 정수 타입으로 변환 (원 단위)
        df.loc[:, '실재고액'] = df['실재고액'].round(0).astype(int)
        df.loc[:, '차액'] = df['차액'].round(0).astype(int)
        
        return df
    
    def _calculate_stock_value_by_total(self, 전산재고, 전산재고액, 단가, 실재고):
        """총액 기준 처리 방식으로 실재고액 계산"""
        
        # 변동 수량 계산
        변동수량 = 실재고 - 전산재고
        
        if 변동수량 == 0:
            # 변동이 없는 경우
            실재고액 = 전산재고액
            차액 = 0
            
        elif 변동수량 < 0:
            # 감소의 경우: 감소분 재고액을 차감
            감소수량 = abs(변동수량)
            감소분재고액 = round(감소수량 * 단가, 0)  # 원 단위 반올림
            실재고액 = 전산재고액 - 감소분재고액
            차액 = -감소분재고액
            
        else:
            # 증가의 경우: 증가분 재고액을 추가
            증가수량 = 변동수량
            증가분재고액 = round(증가수량 * 단가, 0)  # 원 단위 반올림
            실재고액 = 전산재고액 + 증가분재고액
            차액 = 증가분재고액
        
        return int(실재고액), int(차액) 