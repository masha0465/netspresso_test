"""
유틸리티 함수들
"""

import os
import json
import logging
from datetime import datetime

def setup_logging():
    """로깅 설정"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('netspresso_test.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def ensure_dir(directory):
    """디렉토리 존재 확인 및 생성"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    return False

def save_test_result(result, output_path):
    """테스트 결과를 JSON 파일로 저장"""
    ensure_dir(os.path.dirname(output_path))
    
    result_data = {
        'timestamp': datetime.now().isoformat(),
        'result': result
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)

def load_test_result(file_path):
    """저장된 테스트 결과 로드"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"JSON 파일 읽기 실패: {e}")
        return None

def format_file_size(size_bytes):
    """파일 크기를 읽기 쉬운 형태로 변환"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def get_model_info(model_path):
    """모델 파일 정보 수집"""
    if not os.path.exists(model_path):
        return {"error": "파일이 존재하지 않음"}
    
    file_size = os.path.getsize(model_path)
    file_ext = os.path.splitext(model_path)[1]
    
    return {
        "path": model_path,
        "size": file_size,
        "size_readable": format_file_size(file_size),
        "extension": file_ext,
        "exists": True
    }

class TestResultCollector:
    """테스트 결과 수집 및 정리"""
    
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
    
    def add_result(self, test_name, success, details=None):
        """테스트 결과 추가"""
        result = {
            'test_name': test_name,
            'success': success,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        self.results.append(result)
    
    def get_summary(self):
        """테스트 요약 정보 반환"""
        total = len(self.results)
        success = sum(1 for r in self.results if r['success'])
        failed = total - success
        
        return {
            'total_tests': total,
            'success_count': success,
            'failed_count': failed,
            'success_rate': (success / total * 100) if total > 0 else 0,
            'test_duration': (datetime.now() - self.start_time).total_seconds(),
            'results': self.results
        }
    
    def save_summary(self, output_path):
        """요약 결과를 파일로 저장"""
        summary = self.get_summary()
        save_test_result(summary, output_path)
        return summary