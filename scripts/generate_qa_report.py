"""
QA 리포트 생성 스크립트
"""

import os
import json
from datetime import datetime
import glob
import sys

# 상위 디렉토리의 src 모듈 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from utils import TestResultCollector, load_test_result, format_file_size

def collect_test_results():
    """테스트 결과 파일들을 수집하여 종합 리포트 생성"""
    
    collector = TestResultCollector()
    
    # 결과 폴더에서 JSON 파일들 찾기
    result_files = glob.glob('./results/**/*.json', recursive=True)
    
    for result_file in result_files:
        test_data = load_test_result(result_file)
        if test_data and 'result' in test_data:
            result = test_data['result']
            test_name = os.path.basename(result_file).replace('.json', '')
            
            collector.add_result(
                test_name=test_name,
                success=result.get('success', False),
                details=result
            )
    
    return collector

def generate_markdown_report(collector):
    """마크다운 형태의 QA 리포트 생성"""
    
    summary = collector.get_summary()
    
    report = f"""# NetsPresso QA 테스트 리포트

**생성 시각**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**테스트 소요시간**: {summary['test_duration']:.1f}초

## 테스트 결과 요약

- **전체 테스트**: {summary['total_tests']}개
- **성공**: {summary['success_count']}개
- **실패**: {summary['failed_count']}개
- **성공률**: {summary['success_rate']:.1f}%

## 상세 결과

"""
    
    for result in summary['results']:
        status_emoji = "✅" if result['success'] else "❌"
        report += f"### {status_emoji} {result['test_name']}\n"
        report += f"- **실행 시간**: {result['timestamp']}\n"
        report += f"- **결과**: {'성공' if result['success'] else '실패'}\n"
        
        if result['details']:
            if 'error' in result['details'] and result['details']['error']:
                report += f"- **에러**: {result['details']['error']}\n"
            if 'compressed_path' in result['details'] and result['details']['compressed_path']:
                report += f"- **압축 결과**: {result['details']['compressed_path']}\n"
        
        report += "\n"
    
    # QA 관점에서의 발견사항 추가
    report += """## QA 관점 발견사항

### 발견된 이슈들
"""
    
    failed_tests = [r for r in summary['results'] if not r['success']]
    if failed_tests:
        report += "\n"
        for test in failed_tests:
            if 'yolo' in test['test_name'].lower():
                report += "- YOLOv8 모델 압축 시 NotValidFrameworkException 발생\n"
            elif 'error' in test['test_name'].lower():
                report += "- 에러 처리 관련 개선 필요 사항 발견\n"
    
    report += """
### 권장 개선사항
- 복잡한 모델에 대한 제약사항을 문서에 명시
- 에러 메시지 개선으로 사용자 가이드 향상
- Python SDK와 웹 인터페이스 간 기능 차이 명시
- 모델 업로드 전 호환성 사전 검증 기능 추가

---
*이 리포트는 자동으로 생성되었습니다.*
"""
    
    return report

def main():
    """메인 실행 함수"""
    print("QA 리포트 생성 중...")
    
    # 결과 수집
    collector = collect_test_results()
    
    if not collector.results:
        print("테스트 결과를 찾을 수 없습니다.")
        return
    
    # 마크다운 리포트 생성
    report = generate_markdown_report(collector)
    
    # 리포트 저장
    os.makedirs('./results/reports', exist_ok=True)
    report_path = f"./results/reports/qa_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 최신 리포트로 복사
    with open('./results/qa_summary_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"QA 리포트 생성 완료: {report_path}")
    print("요약 리포트: ./results/qa_summary_report.md")
    
    # 요약 정보 출력
    summary = collector.get_summary()
    print(f"\n테스트 요약:")
    print(f"- 성공: {summary['success_count']}/{summary['total_tests']}")
    print(f"- 성공률: {summary['success_rate']:.1f}%")

if __name__ == "__main__":
    main()