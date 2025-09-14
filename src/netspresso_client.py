"""
NetsPresso QA 테스트용 클라이언트
"""

import os
from netspresso import NetsPresso
import torch
import torch.fx

class NetsPresssoQAClient:
    """QA 테스트용 NetsPresso 클라이언트"""
    
    def __init__(self):
        api_key = os.getenv('NETSPRESSO_API_KEY', 'np-rlKs4kiEU5n27qLmtFySjD1pAX79IENd')
        self.netspresso = NetsPresso(api_key=api_key)
        self.compressor = self.netspresso.compressor_v2()
    
    def test_simple_compression(self, model_path, output_dir):
        """간단한 모델 압축 테스트"""
        try:
            result = self.compressor.automatic_compression(
                input_model_path=model_path,
                output_dir=output_dir,
                input_shapes=[{"batch": 1, "channel": 3, "dimension": [224, 224]}],
                compression_ratio=0.5
            )
            return {
                'success': True,
                'status': result.status,
                'compressed_path': getattr(result, 'compressed_model_path', None),
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'status': 'error',
                'compressed_path': None,
                'error': str(e)
            }

def create_simple_test_model():
    """간단한 테스트용 CNN 모델"""
    class SimpleCNN(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = torch.nn.Conv2d(3, 16, 3, padding=1)
            self.conv2 = torch.nn.Conv2d(16, 32, 3, padding=1)
            self.pool = torch.nn.AdaptiveAvgPool2d((1, 1))
            self.fc = torch.nn.Linear(32, 10)
        
        def forward(self, x):
            x = torch.relu(self.conv1(x))
            x = torch.relu(self.conv2(x))
            x = self.pool(x)
            x = torch.flatten(x, 1)
            return self.fc(x)
    
    return SimpleCNN()

if __name__ == "__main__":
    # 기본 테스트
    client = NetsPresssoQAClient()
    
    # 간단한 모델 생성 및 테스트
    model = create_simple_test_model()
    fx_model = torch.fx.symbolic_trace(model)
    
    # 임시 저장
    torch.save(fx_model, "temp_simple_model.pt")
    
    # 압축 테스트
    result = client.test_simple_compression("temp_simple_model.pt", "./results/test")
    print(f"테스트 결과: {result}")