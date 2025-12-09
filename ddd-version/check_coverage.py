"""
測試覆蓋率檢查腳本
"""
import subprocess
import sys
import os
from datetime import datetime

def run_coverage():
    """執行覆蓋率測試"""
    print("=" * 60)
    print("執行測試覆蓋率分析...")
    print("=" * 60)
    
    # 執行 pytest 並產生覆蓋率報告
    result = subprocess.run([
        sys.executable, '-m', 'pytest',
        'tests/test_api_compliance.py',
        '--cov=src',
        '--cov-report=term',
        '--cov-report=html',
        '-v'
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    print("\n" + "=" * 60)
    print("✅ 覆蓋率報告已產生")
    print("詳細報告位置：htmlcov/index.html")
    print("=" * 60)
    
    # 提取覆蓋率數據
    output = result.stdout
    if "TOTAL" in output:
        # 解析覆蓋率
        for line in output.split('\n'):
            if 'TOTAL' in line:
                parts = line.split()
                if len(parts) >= 4:
                    coverage = parts[-1].replace('%', '')
                    print(f"\n📊 總覆蓋率: {coverage}%")
                    
                    # 建議記錄到 CSV
                    today = datetime.now().strftime('%Y-%m-%d')
                    print(f"\n請記錄到 test_coverage.csv：")
                    print(f"DDD,{today},{coverage},,100,{count_tests()},")
    
    return result.returncode

def count_tests():
    """計算測試數量"""
    result = subprocess.run([
        sys.executable, '-m', 'pytest',
        'tests/test_api_compliance.py',
        '--collect-only', '-q'
    ], capture_output=True, text=True)
    
    output = result.stdout
    for line in output.split('\n'):
        if 'test' in line.lower():
            # 計算測試數量
            pass
    
    # 簡單計算：找 "def test_" 的數量
    with open('test/test_api_compliance.py', 'r', encoding='utf-8') as f:
        content = f.read()
        count = content.count('def test_')
    
    return count

if __name__ == "__main__":
    exit_code = run_coverage()
    sys.exit(exit_code)