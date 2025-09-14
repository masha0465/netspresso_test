"""
모델 생성 및 테스트 관련 함수들
"""

import torch
import torch.fx

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

def create_yolo_compatible_model():
    """torch.fx 호환 가능한 YOLO 유사 모델"""
    class YOLOCompatibleModel(torch.nn.Module):
        def __init__(self, num_classes=80):
            super().__init__()
            # Backbone
            self.backbone = torch.nn.Sequential(
                # Block 1
                torch.nn.Conv2d(3, 32, 3, padding=1),
                torch.nn.BatchNorm2d(32),
                torch.nn.ReLU(),
                torch.nn.MaxPool2d(2),
                
                # Block 2
                torch.nn.Conv2d(32, 64, 3, padding=1),
                torch.nn.BatchNorm2d(64),
                torch.nn.ReLU(),
                torch.nn.MaxPool2d(2),
                
                # Block 3
                torch.nn.Conv2d(64, 128, 3, padding=1),
                torch.nn.BatchNorm2d(128),
                torch.nn.ReLU(),
                torch.nn.MaxPool2d(2),
                
                # Block 4
                torch.nn.Conv2d(128, 256, 3, padding=1),
                torch.nn.BatchNorm2d(256),
                torch.nn.ReLU(),
                torch.nn.MaxPool2d(2),
            )
            
            # Detection head
            self.detection_head = torch.nn.Sequential(
                torch.nn.Conv2d(256, 512, 3, padding=1),
                torch.nn.ReLU(),
                torch.nn.Conv2d(512, 5 + num_classes, 1),  # bbox + classes
            )
        
        def forward(self, x):
            features = self.backbone(x)
            detection = self.detection_head(features)
            return detection
    
    return YOLOCompatibleModel()

def save_fx_model(model, path):
    """모델을 torch.fx.GraphModule로 변환 후 저장"""
    try:
        fx_model = torch.fx.symbolic_trace(model)
        torch.save(fx_model, path)
        return True
    except Exception as e:
        print(f"FX 변환 실패: {e}")
        return False

def verify_fx_model(model_path):
    """저장된 모델이 올바른 torch.fx.GraphModule인지 확인"""
    try:
        model = torch.load(model_path, map_location='cpu')
        is_fx = isinstance(model, torch.fx.GraphModule)
        
        if is_fx:
            # 간단한 실행 테스트
            example_input = torch.randn(1, 3, 224, 224)
            with torch.no_grad():
                output = model(example_input)
            return True, f"FX 모델 검증 성공. 출력 형태: {output.shape}"
        else:
            return False, f"torch.fx.GraphModule이 아님: {type(model)}"
    
    except Exception as e:
        return False, f"모델 검증 실패: {e}"