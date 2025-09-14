"""
YOLO 모델 호환성 테스트
"""

import pytest
import torch
import torch.fx
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from netspresso_client import NetsPresssoQAClient

class TestYOLOCompatibility:
    
    @pytest.fixture
    def client(self):
        return NetsPresssoQAClient()
    
    def create_yolo_compatible_model(self):
        """torch.fx 호환 가능한 YOLO 유사 모델"""
        class YOLOLikeModel(torch.nn.Module):
            def __init__(self):
                super().__init__()
                # 단순화된 YOLO 구조
                self.backbone = torch.nn.Sequential(
                    torch.nn.Conv2d(3, 32, 3, padding=1),
                    torch.nn.ReLU(),
                    torch.nn.MaxPool2d(2),
                    torch.nn.Conv2d(32, 64, 3, padding=1),
                    torch.nn.ReLU(),
                    torch.nn.MaxPool2d(2),
                    torch.nn.Conv2d(64, 128, 3, padding=1),
                    torch.nn.ReLU(),
                )
                self.head = torch.nn.Conv2d(128, 85, 1)  # 85 = 5 + 80 classes
            
            def forward(self, x):
                x = self.backbone(x)
                return self.head(x)
        
        return YOLOLikeModel()
    
    def test_yolo_like_model_creation(self):
        """YOLO 호환 모델 생성 테스트"""
        model = self.create_yolo_compatible_model()
        assert model is not None
        
        # torch.fx 변환 가능성 테스트
        try:
            fx_model = torch.fx.symbolic_trace(model)
            assert isinstance(fx_model, torch.fx.GraphModule)
        except Exception as e:
            pytest.fail(f"torch.fx 변환 실패: {e}")
    
    @pytest.mark.xfail(reason="실제 YOLOv8 ONNX는 NetsPresso Python SDK에서 실패 예상")
    def test_actual_yolo_compression_failure(self, client):
        """실제 YOLOv8 압축 실패 케이스 테스트"""
        # 이 테스트는 실패할 것으로 예상됨 (문서화 목적)
        result = client.test_yolo_compression("yolov8l.onnx", "./results/yolo_fail_test")
        assert result['success'] is False
        assert "NotValidFrameworkException" in result['error']

if __name__ == "__main__":
    test = TestYOLOCompatibility()
    test.test_yolo_like_model_creation()
    print("YOLO 호환성 테스트 완료")