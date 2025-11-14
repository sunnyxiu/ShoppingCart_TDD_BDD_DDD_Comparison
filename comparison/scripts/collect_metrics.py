#!/usr/bin/env python3
"""
自動收集程式碼指標的腳本

使用方式：
    python collect_metrics.py --version tdd
    python collect_metrics.py --version bdd
    python collect_metrics.py --version ddd
    python collect_metrics.py --all  # 收集所有版本

需要安裝的工具：
    pip install radon --break-system-packages
    
可選安裝（用於更詳細的分析）：
    # Ubuntu/Debian
    sudo apt-get install cloc
    
    # macOS
    brew install cloc
"""

import subprocess
import csv
import os
import sys
from datetime import datetime
from pathlib import Path
import argparse


class MetricsCollector:
    """程式碼指標收集器"""
    
    def __init__(self, version_name):
        """
        初始化
        
        Args:
            version_name: 版本名稱 (tdd, bdd, ddd)
        """
        self.version = version_name.upper()
        self.version_path = f"../{version_name}-version/src"
        self.metrics_file = "../comparison/metrics/code_metrics.csv"
        
    def count_lines(self):
        """計算程式碼行數"""
        try:
            # 嘗試使用 cloc（更準確）
            result = subprocess.run(
                ['cloc', self.version_path, '--csv', '--quiet'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'Python' in line:
                        parts = line.split(',')
                        return int(parts[4])  # code lines
            
            # 如果 cloc 失敗，使用簡單計數
            return self._count_lines_simple()
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # cloc 不存在，使用簡單計數
            return self._count_lines_simple()
    
    def _count_lines_simple(self):
        """簡單的行數計算（備用方案）"""
        total_lines = 0
        src_path = Path(self.version_path)
        
        if not src_path.exists():
            print(f"⚠️  警告：{self.version_path} 不存在")
            return 0
        
        for py_file in src_path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # 排除空行和註解
                    code_lines = [
                        line for line in lines 
                        if line.strip() and not line.strip().startswith('#')
                    ]
                    total_lines += len(code_lines)
            except Exception as e:
                print(f"⚠️  讀取 {py_file} 時發生錯誤: {e}")
        
        return total_lines
    
    def count_test_lines(self):
        """計算測試程式碼行數"""
        version_lower = self.version.lower()
        
        # 根據不同版本使用不同的測試目錄
        if version_lower == 'tdd':
            test_path = f"../{version_lower}-version/tests"
        elif version_lower == 'bdd':
            test_path = f"../{version_lower}-version/features"
        else:  # ddd
            test_path = f"../{version_lower}-version/tests"
        
        try:
            result = subprocess.run(
                ['cloc', test_path, '--csv', '--quiet'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'Python' in line or 'Gherkin' in line:
                        parts = line.split(',')
                        return int(parts[4])
            
            return self._count_test_lines_simple(test_path)
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return self._count_test_lines_simple(test_path)
    
    def _count_test_lines_simple(self, test_path):
        """簡單的測試行數計算（備用方案）"""
        total_lines = 0
        path = Path(test_path)
        
        if not path.exists():
            print(f"⚠️  警告：{test_path} 不存在")
            return 0
        
        # 計算 .py 和 .feature 檔案
        for ext in ['*.py', '*.feature']:
            for file in path.rglob(ext):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        code_lines = [
                            line for line in lines 
                            if line.strip() and not line.strip().startswith('#')
                        ]
                        total_lines += len(code_lines)
                except Exception as e:
                    print(f"⚠️  讀取 {file} 時發生錯誤: {e}")
        
        return total_lines
    
    def count_doc_lines(self):
        """計算文件行數"""
        version_lower = self.version.lower()
        doc_path = f"../{version_lower}-version/docs"
        
        if not Path(doc_path).exists():
            return 0
        
        total_lines = 0
        for md_file in Path(doc_path).rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # 計算非空行
                    doc_lines = [line for line in lines if line.strip()]
                    total_lines += len(doc_lines)
            except Exception as e:
                print(f"⚠️  讀取 {md_file} 時發生錯誤: {e}")
        
        return total_lines
    
    def calculate_complexity(self):
        """計算平均圈複雜度"""
        try:
            result = subprocess.run(
                ['radon', 'cc', self.version_path, '-a', '-s'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                output = result.stdout
                # 解析平均複雜度
                for line in output.split('\n'):
                    if 'Average complexity' in line:
                        # 格式: "Average complexity: A (2.5)"
                        parts = line.split('(')
                        if len(parts) > 1:
                            complexity = parts[1].split(')')[0]
                            return float(complexity)
            
            return 0.0
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"⚠️  警告：無法執行 radon，請安裝：pip install radon")
            return 0.0
    
    def count_functions(self):
        """計算函數數量"""
        total_functions = 0
        src_path = Path(self.version_path)
        
        if not src_path.exists():
            return 0
        
        for py_file in src_path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 簡單計算 def 關鍵字數量
                    total_functions += content.count('\ndef ')
                    # 加上可能在檔案開頭的函數
                    if content.strip().startswith('def '):
                        total_functions += 1
            except Exception as e:
                print(f"⚠️  讀取 {py_file} 時發生錯誤: {e}")
        
        return total_functions
    
    def collect_all_metrics(self):
        """收集所有指標"""
        print(f"\n📊 開始收集 {self.version} 版本的程式碼指標...")
        
        metrics = {
            '版本': self.version,
            '日期': datetime.now().strftime('%Y-%m-%d'),
            '程式碼行數': self.count_lines(),
            '測試行數': self.count_test_lines(),
            '文件行數': self.count_doc_lines(),
            '圈複雜度': round(self.calculate_complexity(), 2),
            '重複程度(%)': 0,  # 需要手動填寫或使用專門工具
            '函數數量': self.count_functions(),
            '備註': ''
        }
        
        return metrics
    
    def save_to_csv(self, metrics):
        """儲存到 CSV 檔案"""
        csv_path = Path(self.metrics_file)
        
        # 確保目錄存在
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 檢查檔案是否存在
        file_exists = csv_path.exists()
        
        # 寫入 CSV
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            fieldnames = ['版本', '日期', '程式碼行數', '測試行數', '文件行數', 
                         '圈複雜度', '重複程度(%)', '函數數量', '備註']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # 如果是新檔案，寫入標題
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(metrics)
        
        print(f"✅ {self.version} 指標已儲存到 {self.metrics_file}")
    
    def display_metrics(self, metrics):
        """顯示收集到的指標"""
        print(f"\n{'='*50}")
        print(f"📊 {self.version} 版本程式碼指標")
        print(f"{'='*50}")
        print(f"📅 日期：{metrics['日期']}")
        print(f"📝 程式碼行數：{metrics['程式碼行數']}")
        print(f"🧪 測試行數：{metrics['測試行數']}")
        print(f"📖 文件行數：{metrics['文件行數']}")
        print(f"🔄 圈複雜度：{metrics['圈複雜度']}")
        print(f"🔢 函數數量：{metrics['函數數量']}")
        print(f"{'='*50}\n")


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description='收集程式碼指標',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
    python collect_metrics.py --version tdd
    python collect_metrics.py --version bdd
    python collect_metrics.py --version ddd
    python collect_metrics.py --all
        """
    )
    
    parser.add_argument(
        '--version',
        choices=['tdd', 'bdd', 'ddd'],
        help='指定要收集的版本'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='收集所有版本的指標'
    )
    
    args = parser.parse_args()
    
    # 檢查參數
    if not args.version and not args.all:
        parser.print_help()
        sys.exit(1)
    
    # 決定要收集哪些版本
    versions = ['tdd', 'bdd', 'ddd'] if args.all else [args.version]
    
    # 收集指標
    for version in versions:
        try:
            collector = MetricsCollector(version)
            metrics = collector.collect_all_metrics()
            collector.display_metrics(metrics)
            collector.save_to_csv(metrics)
        except Exception as e:
            print(f"❌ 收集 {version.upper()} 指標時發生錯誤：{e}")
            continue
    
    print("\n✅ 所有指標收集完成！")


if __name__ == '__main__':
    main()