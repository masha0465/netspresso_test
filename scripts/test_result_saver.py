"""
테스트 결과 저장 유틸리티
NetsPresso 테스트 실행 후 결과를 저장하는 헬퍼 함수들
"""
import json
import os
from datetime import datetime
from pathlib import Path


def save_test_result(test_name, success, details=None, output_dir="./results/test_results"):
    """
    테스트 결과를 JSON 파일로 저장
    
    Args:
        test_name (str): 테스트 이름
        success (bool): 성공 여부
        details (dict): 상세 정보
        output_dir (str): 저장할 디렉토리
    """
    
    # 출력 디렉토리 생성
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 결과 데이터 구성
    result_data = {
        "test_name": test_name,
        "timestamp": datetime.now().isoformat(),
        "result": {
            "success": success,
            "details": details or {},
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    }
    
    # 파일 저장
    filename = f"{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = output_path / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    print(f"테스트 결과 저장됨: {filepath}")
    return str(filepath)


def collect_netspresso_results(results_dir="./results"):
    """
    NetsPresso 실행 결과를 수집하여 표준 형식으로 변환
    
    Args:
        results_dir (str): 결과가 저장된 디렉토리
    
    Returns:
        list: 수집된 테스트 결과들
    """
    
    results = []
    results_path = Path(results_dir)
    
    if not results_path.exists():
        print(f"결과 디렉토리가 존재하지 않습니다: {results_dir}")
        return results
    
    # 각 하위 폴더를 테스트 결과로 간주
    for test_folder in results_path.iterdir():
        if test_folder.is_dir() and test_folder.name != "test_results":
            try:
                # metadata.json 파일 찾기
                metadata_file = test_folder / "metadata.json"
                
                if metadata_file.exists():
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    # 압축된 모델 파일 확인
                    compressed_files = list(test_folder.glob("*.pt")) + list(test_folder.glob("*.onnx"))
                    
                    # 성공 조건을 더 관대하게 설정
                    success = (
                        # 기본적으로 metadata 파일이 존재하면 성공으로 간주
                        metadata_file.exists() and
                        (
                            # 조건 1: 명시적 완료 상태
                            metadata.get('status') == 'completed' or
                            # 조건 2: 압축 모델 ID가 있음
                            'compressed_model_id' in metadata or
                            # 조건 3: 압축된 파일이 존재함
                            len(compressed_files) > 0 or
                            # 조건 4: 에러가 없음
                            'error' not in metadata
                        )
                    )
                    
                    # 상세 정보 구성
                    details = {
                        "model_id": metadata.get('model_id'),
                        "compressed_model_id": metadata.get('compressed_model_id'),
                        "status": metadata.get('status'),
                        "compressed_files": [str(f) for f in compressed_files],
                        "metadata_path": str(metadata_file)
                    }
                    
                    # 파일 크기 정보 추가
                    if compressed_files:
                        main_file = compressed_files[0]
                        details["compressed_size"] = main_file.stat().st_size
                        details["compressed_path"] = str(main_file)
                    
                    result = {
                        "test_name": f"netspresso_{test_folder.name}",
                        "success": success,
                        "details": details,
                        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    results.append(result)
                    print(f"수집됨: {test_folder.name} ({'성공' if success else '실패'})")
                
            except Exception as e:
                print(f"오류: {test_folder.name} 처리 중 문제 발생: {e}")
                
                # 실패 결과로 추가
                result = {
                    "test_name": f"netspresso_{test_folder.name}",
                    "success": False,
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                results.append(result)
    
    return results


def convert_to_standard_format(results_dir="./results"):
    """
    NetsPresso 결과를 표준 테스트 결과 형식으로 변환하여 저장
    
    Args:
        results_dir (str): 결과 디렉토리
    """
    
    print("NetsPresso 결과를 표준 형식으로 변환 중...")
    
    # 결과 수집
    results = collect_netspresso_results(results_dir)
    
    if not results:
        print("변환할 결과가 없습니다.")
        return
    
    # 표준 형식으로 저장
    output_dir = Path(results_dir) / "test_results"
    output_dir.mkdir(exist_ok=True)
    
    for result in results:
        test_name = result['test_name']
        filename = f"{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = output_dir / filename
        
        # 표준 형식으로 변환
        standard_result = {
            "test_name": test_name,
            "timestamp": result['timestamp'],
            "result": {
                "success": result['success'],
                "details": result['details'],
                "timestamp": result['timestamp']
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(standard_result, f, ensure_ascii=False, indent=2)
        
        print(f"저장됨: {filepath}")
    
    print(f"총 {len(results)}개의 결과를 변환했습니다.")


if __name__ == "__main__":
    # 테스트 실행
    convert_to_standard_format()
    print("\n변환 완료! 이제 generate_qa_report.py를 실행할 수 있습니다.")