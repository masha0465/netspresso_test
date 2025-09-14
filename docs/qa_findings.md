# QA 관점에서의 발견사항

## 발견된 주요 이슈들

### 이슈 #1: YOLOv8 ONNX 모델 업로드 실패
**심각도**: High
**재현율**: 100%

**재현 절차**:
1. NetsPresso Python SDK 설치 및 API 키 설정
2. YOLOv8 ONNX 모델 준비
3. automatic_compression() 메서드 호출
4. NotValidFrameworkException 에러 발생

**실제 결과**: 모델 업로드는 성공하나 압축 실패
**기대 결과**: 문서에 명시된 대로 ONNX 모델 압축 성공

### 이슈 #2: Python SDK vs 웹 인터페이스 지원 범위 차이
**심각도**: Major
**카테고리**: 문서 개선

**문제**: 웹 인터페이스는 "GraphModule 또는 ONNX" 지원이지만, Python SDK는 실제로 torch.fx.GraphModule만 지원. 이 차이가 문서에 명시되지 않음.

## 사용성 개선 제안

1. **사전 호환성 검증**: 업로드 전 모델 지원 여부 확인 기능
2. **구체적 에러 메시지**: 실패 원인과 해결 방법 안내
3. **단계별 가이드**: 모델 변환 과정 상세 설명
4. **인터페이스별 차이점 명시**: Python SDK와 웹 UI의 기능 차이 문서화