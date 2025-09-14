# NetsPresso 사용 경험 포트폴리오
**YOLOv8 모델 압축을 통한 제품 이해**

## 프로젝트 배경

10년차 QA 엔지니어로서 Nota AI의 NetsPresso에 관심이 생겨서 직접 사용해보게 되었습니다. YOLOv8 모델 압축이라는 실제 사용 케이스로 제품을 테스트해보면서 어떤 부분들을 개선할 수 있을지 생각해봤습니다.

**목표**: NetsPresso 사용해보고 QA 관점에서 피드백 정리  
**기간**: 2025년 9월  
**테스트 방식**: 실제 사용자처럼 문서 보고 따라하기

## 사용해본 내용

### 1. 제품 기능 탐구
- NetsPresso Python SDK를 활용한 모델 압축 프로세스 테스트
- YOLOv8 ONNX 모델(167MB)을 압축 대상으로 선정
- API 사용법 학습 및 실제 적용

### 2. 발견한 사용자 경험 이슈

**문제 상황**: 
- 공식 문서에서는 ONNX와 YOLOv8 지원을 명시
- 실제 테스트 시 `NotValidFrameworkException` 오류 발생
- 모델 업로드는 성공하나 압축 단계에서 실패

**QA 관점에서의 분석**:
- 문서와 실제 구현 간 차이 존재
- 에러 메시지가 구체적이지 않아 사용자가 해결방법 파악 어려움
- Python SDK의 제약사항이 명확히 문서화되지 않음

## 결과

- **간단한 모델**: 84KB → 압축 성공
- **YOLO 호환 모델**: 6.4MB → 압축 성공  
- **원본 YOLOv8**: 167MB → 압축 실패

## 상세 분석

📋 **[테스트 이슈 리스트.pdf](./docs/NetsPresso 이슈 리스트_김선아.pdf)**
- 발견된 이슈들과 개선 제안사항 정리

## 실행 방법
```bash
# 환경 설정
pip install -r requirements.txt

# 기본 테스트 실행
python src/netspresso_client.py

# 리포트 생성
python scripts/generate_qa_report.py