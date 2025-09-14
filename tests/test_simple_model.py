```python
import pytest
import torch
import torch.fx
import os
from src.netspresso_client import NetsPresssoQAClient
from src.model_tests import create_simple_test_model

class TestSimpleModel:
    
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
    
    def test_basic_compression_workflow(self, client, simple_model_path):
        """기본 압축 워크플로우 테스트"""
        
        output_dir = "./results/test_simple_compression"
        result = client.test_simple_compression(simple_model_path, output_dir)
        
        # QA 관점에서의 검증 포인트
        assert result is not None, "결과가 반환되어야 함"
        assert 'success' in result, "성공 여부가 명시되어야 함"
        assert 'status' in result, "상태 정보가 포함되어야 함"
        
        if result['success']:
            assert result['status'] == 'completed', "성공 시 상태는 completed여야 함"
            assert result['compressed_path'] is not None, "압축 파일 경로가 제공되어야 함"
            assert os.path.exists(result['compressed_path']), "압축 파일이 실제로 생성되어야 함"
        else:
            assert result['error'] is not None, "실패 시 에러 메시지가 제공되어야 함"
            assert len(result['error']) > 0, "에러 메시지는 비어있지 않아야 함"
    
    def test_compression_performance(self, client, simple_model_path):
        """압축 성능 테스트"""
        
        import time
        
        start_time = time.time()
        result = client.test_simple_compression(simple_model_path, "./results/test_performance")
        end_time = time.time()
        
        compression_time = end_time - start_time
        
        # QA 관점: 성능 기준 검증
        assert compression_time < 120, f"압축 시간이 2분을 초과함: {compression_time:.2f}초"
        
        if result['success'] and result['compressed_path']:
            original_size = os.path.getsize(simple_model_path)
            compressed_size = os.path.getsize(result['compressed_path'])
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            assert compression_ratio > 10, f"압축률이 10% 미만: {compression_ratio:.1f}%"