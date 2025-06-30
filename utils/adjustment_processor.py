import pandas as pd
import numpy as np
from datetime import datetime, date
from typing import Optional, Tuple, Dict

class AdjustmentProcessor:
    """재고조정 파일 처리 클래스"""
    
    def __init__(self):
        self.data = None
        self.filtered_data = None
    
    def load_adjustment_file(self, file_path: str) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """재고조정 엑셀 파일을 로드"""
        try:
            # openpyxl 엔진만 사용 (자동 변환된 .xlsx 파일)
            df = pd.read_excel(file_path, engine='openpyxl')
            
            # 기본 검증
            if len(df) == 0:
                return False, "파일에 데이터가 없습니다.", None
            
            if len(df.columns) < 5:
                return False, f"컬럼이 부족합니다. 필요: 5개, 현재: {len(df.columns)}개", None
            
            # 컬럼명 표준화
            df.columns = ['일자', '수량변경', '제작사품번', '부품명', '수량']
            
            # 데이터 정리
            df = self._clean_data(df)
            
            if len(df) == 0:
                return False, "유효한 데이터가 없습니다.", None
            
            self.data = df
            
            # 날짜 범위 정보
            try:
                min_date = df['일자'].min().strftime('%Y-%m-%d')
                max_date = df['일자'].max().strftime('%Y-%m-%d')
                date_info = f"({min_date} ~ {max_date})"
            except:
                date_info = ""
            
            return True, f"✅ 재고조정 파일 로드 완료 ({len(df):,}건) {date_info}", df
            
        except Exception as e:
            return False, f"파일 읽기 오류: {str(e)}", None
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """데이터 정리"""
        # 복사본 생성하여 경고 방지
        df = df.copy()
        
        # 필수 컬럼 결측값 제거
        df = df.dropna(subset=['제작사품번'])
        
        # 일자 변환
        df.loc[:, '일자'] = pd.to_datetime(df['일자'], errors='coerce')
        df = df.dropna(subset=['일자'])
        
        # 수량 변환
        df.loc[:, '수량'] = pd.to_numeric(df['수량'], errors='coerce').fillna(0)
        
        # 조정구분 추출
        df.loc[:, '조정구분'] = df['수량변경'].astype(str).apply(self._extract_type)
        
        # 유효한 데이터만 유지
        df = df[(df['수량'] != 0) & (df['조정구분'] != '')]
        
        return df.reset_index(drop=True)
    
    def _extract_type(self, value: str) -> str:
        """+/- 구분 추출"""
        if '+' in value or '증가' in value:
            return '+'
        elif '-' in value or '감소' in value:
            return '-'
        return ''
    
    def filter_by_date_range(self, start_date: date, end_date: date) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """날짜 범위 필터링"""
        if self.data is None:
            return False, "먼저 재고조정 파일을 로드해주세요.", None
        
        mask = (self.data['일자'].dt.date >= start_date) & (self.data['일자'].dt.date <= end_date)
        filtered_df = self.data[mask].copy()
        
        if len(filtered_df) == 0:
            return False, f"선택한 기간에 해당하는 데이터가 없습니다.", None
        
        self.filtered_data = filtered_df
        return True, f"✅ 기간 필터링 완료 ({len(filtered_df):,}건)", filtered_df
    
    def apply_adjustments_to_inventory(self, inventory_df: pd.DataFrame, part_data: pd.DataFrame) -> Tuple[bool, str, pd.DataFrame, Dict]:
        """재고조정을 실재고 데이터에 반영"""
        if self.filtered_data is None:
            return False, "먼저 재고조정 기간을 설정해주세요.", inventory_df, {}
        
        result_df = inventory_df.copy()
        summary = {'total_adjustments': 0, 'positive_adjustments': 0, 'negative_adjustments': 0,
                  'positive_amount': 0, 'negative_amount': 0, 'unmatched_items': []}
        
        # 제작사품번별 재고조정 집계
        adj_grouped = self.filtered_data.groupby(['제작사품번', '조정구분'])['수량'].sum().reset_index()
        
        # 매칭된 품목 수와 매칭 실패 수 추적
        matched_count = 0
        unmatched_count = 0
        
        for _, adj_row in adj_grouped.iterrows():
            part_code = adj_row['제작사품번']
            adj_type = adj_row['조정구분']
            quantity = adj_row['수량']
            
            # 실재고 데이터에서 해당 품목 찾기
            mask = result_df['제작사 품번'] == part_code
            
            if mask.any():
                # 단가는 inventory_df에서 가져오기 (이미 계산되어 있음)
                unit_price = result_df.loc[mask, '단가'].iloc[0]
                adjustment_amount = quantity * unit_price
                
                if adj_type == '+':
                    result_df.loc[mask, '실재고'] += quantity
                    result_df.loc[mask, '실재고액'] += adjustment_amount
                    summary['positive_adjustments'] += 1
                    summary['positive_amount'] += adjustment_amount
                elif adj_type == '-':
                    result_df.loc[mask, '실재고'] -= quantity
                    result_df.loc[mask, '실재고액'] -= adjustment_amount
                    summary['negative_adjustments'] += 1
                    summary['negative_amount'] -= adjustment_amount  # 음수로 저장
                
                # 차이와 차액 재계산
                result_df.loc[mask, '차이'] = result_df.loc[mask, '실재고'] - result_df.loc[mask, '재고']
                result_df.loc[mask, '차액'] = result_df.loc[mask, '실재고액'] - result_df.loc[mask, '재고액']
                
                summary['total_adjustments'] += 1
                matched_count += 1
            else:
                summary['unmatched_items'].append({
                    'part_code': part_code, 'quantity': quantity, 'type': adj_type
                })
                unmatched_count += 1
        
        # 처리 결과 메시지에 상세 정보 포함
        message = f"✅ 재고조정 반영 완료 (매칭: {matched_count}건, 미매칭: {unmatched_count}건)"
        
        # 반올림
        for col in ['실재고', '실재고액', '차이', '차액']:
            if col in result_df.columns:
                result_df.loc[:, col] = result_df[col].round(2)
        
        return True, message, result_df, summary
    
    def get_adjustment_summary(self) -> Dict:
        """재고조정 요약 통계"""
        if self.filtered_data is None:
            return {}
        
        positive_data = self.filtered_data[self.filtered_data['조정구분'] == '+']
        negative_data = self.filtered_data[self.filtered_data['조정구분'] == '-']
        
        return {
            'total_records': len(self.filtered_data),
            'positive_records': len(positive_data),
            'negative_records': len(negative_data),
            'positive_quantity': positive_data['수량'].sum(),
            'negative_quantity': negative_data['수량'].sum(),
            'unique_parts': self.filtered_data['제작사품번'].nunique(),
            'date_range': {
                'start': self.filtered_data['일자'].min().strftime('%Y-%m-%d'),
                'end': self.filtered_data['일자'].max().strftime('%Y-%m-%d')
            }
        }
    
    def get_filtered_data(self) -> Optional[pd.DataFrame]:
        """필터링된 재고조정 데이터 반환"""
        return self.filtered_data 