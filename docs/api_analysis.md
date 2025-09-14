# NetsPresso API 분석

## Python SDK 분석

### 주요 클래스 및 메서드

#### NetsPresso 클래스
- **초기화**: `NetsPresso(api_key="YOUR_API_KEY")`
- **로그인**: API 키 방식 권장 (이메일/패스워드는 deprecated 예정)

#### Compressor 클래스
- **초기화**: `netspresso.compressor_v2()`
- **주요 메서드**: `automatic_compression()`

### automatic_compression 파라미터 분석
```python
compression_result = compressor.automatic_compression(
    input_model_path="model.pt",           # 필수: 모델 파일 경로
    output_dir="./results/compressed",     # 필수: 출력 디렉토리
    input_shapes=[{                        # 필수: 입력 형태 정의
        "batch": 1,
        "channel": 3,
        "dimension": [224, 224]
    }],
    compression_ratio=0.5                  # 선택: 압축 비율 (기본값)
)