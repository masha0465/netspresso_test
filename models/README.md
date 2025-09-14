# 테스트 모델들

이 폴더에는 NetsPresso 테스트에 사용된 모델들이 저장됩니다.

## 사용된 모델들

### 1. 간단한 CNN 모델
- **파일명**: simple_test_model.pt
- **크기**: 약 84KB
- **구조**: Conv2d → Conv2d → AdaptiveAvgPool2d → Linear
- **용도**: NetsPresso 기본 기능 검증
- **결과**: 압축 성공

### 2. YOLO 호환 모델
- **파일명**: yolo_like_model.pt  
- **크기**: 약 6.4MB
- **구조**: YOLO 유사 구조이지만 torch.fx 호환 가능하게 단순화
- **용도**: 복잡한 모델에서의 압축 가능성 검증
- **결과**: 압축 성공

### 3. YOLOv8 ONNX (테스트 실패)
- **파일명**: yolov8l.onnx
- **크기**: 167MB
- **용도**: 실제 사용 케이스 테스트
- **결과**: NotValidFrameworkException 발생

## 주의사항

- 대용량 모델 파일들은 .gitignore에 의해 Git에서 제외됩니다
- 실제 모델 파일들은 로컬에서만 사용하고 저장소에는 올리지 않습니다