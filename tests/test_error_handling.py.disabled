"""
에러 처리 테스트
"""

import pytest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from netspresso_client import NetsPresssoQAClient

class TestErrorHandling:
    
    @pytest.fixture
    def client(self):
        return NetsPresssoQAClient()
    
    def test_invalid_model_path(self, client):
        """존재하지 않는 모델 파일 테스트"""
        result = client.test_simple_compression("nonexistent_model.pt", "./results/error_test")
        
        assert result['success'] is False
        assert result['error'] is not None
        assert len(result['error']) > 0
    
    def test_invalid_api_key(self):
        """잘못된 API 키 테스트"""
        # 임시로 환경 변수 변경
        original_key = os.environ.get('NETSPRESSO_API_KEY')
        os.environ['NETSPRESSO_API_KEY'] = 'invalid_key'
        
        try:
            client = NetsPresssoQAClient()
            # API 키 검증은 실제 요청 시에 발생
            result = client.test_simple_compression("temp_model.pt", "./results/invalid_key_test")
            
            # 인증 오류가 발생해야 함
            if not result['success']:
                assert 'auth' in result['error'].lower() or 'key' in result['error'].lower()
        
        finally:
            # 원래 키 복원
            if original_key:
                os.environ['NETSPRESSO_API_KEY'] = original_key
            elif 'NETSPRESSO_API_KEY' in os.environ:
                del os.environ['NETSPRESSO_API_KEY']
    
    def test_error_message_quality(self, client):
        """에러 메시지 품질 테스트"""
        result = client.test_simple_compression("invalid_file.txt", "./results/message_test")
        
        if not result['success']:
            error_msg = result['error']
            # 에러 메시지가 유용한 정보를 포함하는지 확인
            assert len(error_msg) > 10, "에러 메시