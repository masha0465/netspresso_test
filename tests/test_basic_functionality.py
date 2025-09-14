"""
NetsPresso 기본 기능 테스트
"""

import pytest
import torch
import torch.fx
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from netspresso_client import NetsPresssoQAClient, create_simple_test_model

class TestBasicFunctionality:
    
    @pytest.fixture
    def client(self):
        return NetsPresssoQAClient()
    
    @pytest.fixture
    def simple_model_path(self, tmp_path):
        """간단한 테스트 모델 생성"""
        model = create_simple_test_model()
        fx_model = torch.fx.symbolic_trace(model)
        model_path = tmp_path / "simple_test_model.pt"
        torch.save(fx_model, model_path)
        return str(model_path)
    
    def test_client_initialization(self, client):
        """클라이언트 초기화 테스트"""
        assert client.netspresso is not None
        assert client.compressor is not None
    
    def test_simple_model_compression(self, client, simple_model_path):
        """간단한 모델 압축 테스트"""
        output_dir = "./results/test_simple_compression"
        result = client.test_simple_compression(simple_model_path, output_dir)
        
        # QA 관점에서의 검증
        assert result is not None, "결과가 반환되어야 함"
        assert 'success' in result, "성공 여부가 명시되어야 함"
        assert 'status' in result, "상태 정보가 포함되어야 함"
        
        if result['success']:
            assert result['status'] == 'completed', "성공 시 상태는 completed여야 함"
        else:
            assert result['error'] is not None, "실패 시 에러 메시지가 제공되어야 함"

if __name__ == "__main__":
    # 직접 실행 시 간단한 테스트
    client = NetsPresssoQAClient()
    model = create_simple_test_model()
    fx_model = torch.fx.symbolic_trace(model)
    torch.save(fx_model, "temp_test_model.pt")
    
    result = client.test_simple_compression("temp_test_model.pt", "./results/manual_test")
    print(f"수동 테스트 결과: {result}")