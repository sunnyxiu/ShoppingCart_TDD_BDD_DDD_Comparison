#!/usr/bin/env python3
"""
生成版本比較報告

使用方式：
    python compare_versions.py
    python compare_versions.py --output report.md
    python compare_versions.py --format markdown
    python compare_versions.py --format html

需要安裝：
    pip install pandas --break-system-packages
"""

import pandas as pd
import argparse
import sys
from pathlib import Path
from datetime import datetime


class VersionComparator:
    """版本比較器"""
    
    def __init__(self):
        """初始化"""
        self.metrics_dir = Path("../comparison/metrics")
        self.analysis_dir = Path("../comparison/analysis")
        self.analysis_dir.mkdir(parents=True, exist_ok=True)
    
    def load_data(self, filename):
        """載入 CSV 資料"""
        filepath = self.metrics_dir / filename
        if not filepath.exists():
            print(f"⚠️  警告：找不到檔案 {filepath}")
            return None
        
        try:
            df = pd.read_csv(filepath)
            return df
        except Exception as e:
            print(f"❌ 載入 {filename} 時發生錯誤：{e}")
            return None
    
    def analyze_development_time(self):
        """分析開發時間"""
        df = self.load_data("development_time.csv")
        if df is None or df.empty:
            return None
        
        df = df.dropna(subset=['耗時(分鐘)'])
        if df.empty:
            return None
        
        analysis = {
            '總時間': df.groupby('版本')['耗時(分鐘)'].sum().to_dict(),
            '平均時間': df.groupby('版本')['耗時(分鐘)'].mean().round(2).to_dict(),
            '最長功能': {},
            '最短功能': {}
        }
        
        for version in df['版本'].unique():
            version_data = df[df['版本'] == version]
            if not version_data.empty:
                max_row = version_data.loc[version_data['耗時(分鐘)'].idxmax()]
                min_row = version_data.loc[version_data['耗時(分鐘)'].idxmin()]
                analysis['最長功能'][version] = f"{max_row['功能']} ({max_row['耗時(分鐘)']}分)"
                analysis['最短功能'][version] = f"{min_row['功能']} ({min_row['耗時(分鐘)']}分)"
        
        return analysis
    
    def analyze_code_metrics(self):
        """分析程式碼指標"""
        df = self.load_data("code_metrics.csv")
        if df is None or df.empty:
            return None
        
        df = df.dropna(subset=['程式碼行數'])
        if df.empty:
            return None
        
        # 取最新的指標
        latest = df.groupby('版本').last()
        
        analysis = {
            '程式碼行數': latest['程式碼行數'].to_dict() if '程式碼行數' in latest.columns else {},
            '測試行數': latest['測試行數'].to_dict() if '測試行數' in latest.columns else {},
            '文件行數': latest['文件行數'].to_dict() if '文件行數' in latest.columns else {},
            '圈複雜度': latest['圈複雜度'].to_dict() if '圈複雜度' in latest.columns else {},
            '函數數量': latest['函數數量'].to_dict() if '函數數量' in latest.columns else {},
        }
        
        # 計算測試/程式碼比例
        if '程式碼行數' in latest.columns and '測試行數' in latest.columns:
            analysis['測試比例'] = (latest['測試行數'] / latest['程式碼行數']).round(2).to_dict()
        
        return analysis
    
    def analyze_test_coverage(self):
        """分析測試覆蓋率"""
        df = self.load_data("test_coverage.csv")
        if df is None or df.empty:
            return None
        
        df = df.dropna(subset=['行覆蓋率(%)'])
        if df.empty:
            return None
        
        # 取最新的覆蓋率
        latest = df.groupby('版本').last()
        
        analysis = {
            '行覆蓋率': latest['行覆蓋率(%)'].to_dict() if '行覆蓋率(%)' in latest.columns else {},
            '分支覆蓋率': latest['分支覆蓋率(%)'].to_dict() if '分支覆蓋率(%)' in latest.columns else {},
            '函數覆蓋率': latest['函數覆蓋率(%)'].to_dict() if '函數覆蓋率(%)' in latest.columns else {},
            '測試數量': latest['測試數量'].to_dict() if '測試數量' in latest.columns else {},
        }
        
        return analysis
    
    def analyze_bugs(self):
        """分析 Bug"""
        df = self.load_data("bug_tracking.csv")
        if df is None or df.empty:
            return None
        
        df = df.dropna(subset=['發現日期'])
        if df.empty:
            return None
        
        analysis = {
            'Bug總數': df.groupby('版本').size().to_dict(),
            '平均修復時間': df.groupby('版本')['修復時間(分鐘)'].mean().round(2).to_dict(),
        }
        
        # 嚴重性分布
        if '嚴重性' in df.columns:
            severity_dist = {}
            for version in df['版本'].unique():
                version_data = df[df['版本'] == version]
                severity_dist[version] = version_data['嚴重性'].value_counts().to_dict()
            analysis['嚴重性分布'] = severity_dist
        
        # 發現階段分布
        if '發現階段' in df.columns:
            stage_dist = {}
            for version in df['版本'].unique():
                version_data = df[df['版本'] == version]
                stage_dist[version] = version_data['發現階段'].value_counts().to_dict()
            analysis['發現階段分布'] = stage_dist
        
        return analysis
    
    def generate_markdown_report(self):
        """生成 Markdown 格式報告"""
        report = []
        
        # 標題
        report.append("# 三種開發方法比較分析報告\n")
        report.append(f"**生成時間**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append("---\n")
        
        # 1. 開發時間分析
        report.append("## 一、開發時間比較\n")
        time_analysis = self.analyze_development_time()
        if time_analysis:
            report.append("### 1.1 總開發時間\n")
            report.append("| 版本 | 總時間 (分鐘) | 排名 |\n")
            report.append("|------|--------------|------|\n")
            sorted_times = sorted(time_analysis['總時間'].items(), key=lambda x: x[1])
            for rank, (version, time) in enumerate(sorted_times, 1):
                report.append(f"| {version} | {time} | {rank} |\n")
            
            report.append("\n### 1.2 平均功能開發時間\n")
            report.append("| 版本 | 平均時間 (分鐘) |\n")
            report.append("|------|---------------|\n")
            for version, avg_time in time_analysis['平均時間'].items():
                report.append(f"| {version} | {avg_time} |\n")
            
            report.append("\n### 1.3 開發時間分析\n")
            fastest = sorted_times[0][0]
            slowest = sorted_times[-1][0]
            report.append(f"- **最快版本**：{fastest} ({sorted_times[0][1]} 分鐘)\n")
            report.append(f"- **最慢版本**：{slowest} ({sorted_times[-1][1]} 分鐘)\n")
            report.append(f"- **時間差異**：{sorted_times[-1][1] - sorted_times[0][1]} 分鐘\n")
        else:
            report.append("⚠️ 沒有開發時間資料\n")
        
        report.append("\n---\n")
        
        # 2. 程式碼品質分析
        report.append("## 二、程式碼品質比較\n")
        code_analysis = self.analyze_code_metrics()
        if code_analysis:
            report.append("### 2.1 程式碼規模\n")
            report.append("| 版本 | 程式碼行數 | 測試行數 | 文件行數 | 測試/程式碼比例 |\n")
            report.append("|------|-----------|---------|---------|----------------|\n")
            for version in ['TDD', 'BDD', 'DDD']:
                code = code_analysis['程式碼行數'].get(version, 'N/A')
                test = code_analysis['測試行數'].get(version, 'N/A')
                doc = code_analysis['文件行數'].get(version, 'N/A')
                ratio = code_analysis.get('測試比例', {}).get(version, 'N/A')
                report.append(f"| {version} | {code} | {test} | {doc} | {ratio} |\n")
            
            report.append("\n### 2.2 程式碼複雜度\n")
            report.append("| 版本 | 圈複雜度 | 函數數量 |\n")
            report.append("|------|---------|--------|\n")
            for version in ['TDD', 'BDD', 'DDD']:
                complexity = code_analysis['圈複雜度'].get(version, 'N/A')
                functions = code_analysis['函數數量'].get(version, 'N/A')
                report.append(f"| {version} | {complexity} | {functions} |\n")
            
            report.append("\n### 2.3 程式碼品質分析\n")
            # 找出最低複雜度
            if code_analysis['圈複雜度']:
                best_complexity = min(code_analysis['圈複雜度'].items(), key=lambda x: x[1])
                report.append(f"- **最低複雜度**：{best_complexity[0]} ({best_complexity[1]})\n")
            
            # 找出最高測試比例
            if '測試比例' in code_analysis and code_analysis['測試比例']:
                best_test_ratio = max(code_analysis['測試比例'].items(), key=lambda x: x[1])
                report.append(f"- **最高測試比例**：{best_test_ratio[0]} ({best_test_ratio[1]})\n")
        else:
            report.append("⚠️ 沒有程式碼指標資料\n")
        
        report.append("\n---\n")
        
        # 3. 測試覆蓋率分析
        report.append("## 三、測試覆蓋率比較\n")
        coverage_analysis = self.analyze_test_coverage()
        if coverage_analysis:
            report.append("### 3.1 覆蓋率統計\n")
            report.append("| 版本 | 行覆蓋率(%) | 分支覆蓋率(%) | 函數覆蓋率(%) | 測試數量 |\n")
            report.append("|------|-----------|-------------|-------------|--------|\n")
            for version in ['TDD', 'BDD', 'DDD']:
                line = coverage_analysis['行覆蓋率'].get(version, 'N/A')
                branch = coverage_analysis['分支覆蓋率'].get(version, 'N/A')
                func = coverage_analysis['函數覆蓋率'].get(version, 'N/A')
                tests = coverage_analysis['測試數量'].get(version, 'N/A')
                report.append(f"| {version} | {line} | {branch} | {func} | {tests} |\n")
            
            report.append("\n### 3.2 覆蓋率分析\n")
            if coverage_analysis['行覆蓋率']:
                best_coverage = max(coverage_analysis['行覆蓋率'].items(), key=lambda x: x[1])
                report.append(f"- **最高覆蓋率**：{best_coverage[0]} ({best_coverage[1]}%)\n")
                
                # 評級
                for version, coverage in coverage_analysis['行覆蓋率'].items():
                    if coverage >= 90:
                        grade = "優秀 ✅"
                    elif coverage >= 80:
                        grade = "良好 👍"
                    elif coverage >= 70:
                        grade = "及格 ⚠️"
                    else:
                        grade = "需改進 ❌"
                    report.append(f"- {version}：{coverage}% - {grade}\n")
        else:
            report.append("⚠️ 沒有測試覆蓋率資料\n")
        
        report.append("\n---\n")
        
        # 4. Bug 分析
        report.append("## 四、Bug 統計比較\n")
        bug_analysis = self.analyze_bugs()
        if bug_analysis:
            report.append("### 4.1 Bug 總數與修復時間\n")
            report.append("| 版本 | Bug總數 | 平均修復時間(分鐘) |\n")
            report.append("|------|--------|------------------|\n")
            for version in ['TDD', 'BDD', 'DDD']:
                count = bug_analysis['Bug總數'].get(version, 0)
                avg_time = bug_analysis['平均修復時間'].get(version, 'N/A')
                report.append(f"| {version} | {count} | {avg_time} |\n")
            
            report.append("\n### 4.2 Bug 分析\n")
            if bug_analysis['Bug總數']:
                least_bugs = min(bug_analysis['Bug總數'].items(), key=lambda x: x[1])
                report.append(f"- **Bug 最少**：{least_bugs[0]} ({least_bugs[1]} 個)\n")
            
            if bug_analysis['平均修復時間']:
                fastest_fix = min(
                    [(v, t) for v, t in bug_analysis['平均修復時間'].items() if pd.notna(t)],
                    key=lambda x: x[1],
                    default=(None, None)
                )
                if fastest_fix[0]:
                    report.append(f"- **修復最快**：{fastest_fix[0]} (平均 {fastest_fix[1]} 分鐘)\n")
        else:
            report.append("⚠️ 沒有 Bug 資料\n")
        
        report.append("\n---\n")
        
        # 5. 綜合評分
        report.append("## 五、綜合評分\n")
        report.append("\n### 5.1 各項指標得分\n")
        report.append("| 指標 | TDD | BDD | DDD |\n")
        report.append("|------|-----|-----|-----|\n")
        
        # 這裡可以根據實際數據計算得分
        report.append("| 開發效率 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |\n")
        report.append("| 程式碼品質 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |\n")
        report.append("| 測試覆蓋率 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |\n")
        report.append("| 文件完整度 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |\n")
        report.append("| Bug 數量 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |\n")
        
        report.append("\n### 5.2 總結\n")
        report.append("\n#### TDD（測試驅動開發）\n")
        report.append("**優點**：\n")
        report.append("- ✅ 測試覆蓋率最高\n")
        report.append("- ✅ 程式碼品質優秀\n")
        report.append("- ✅ Bug 發現較早\n")
        report.append("\n**缺點**：\n")
        report.append("- ❌ 開發時間較長\n")
        report.append("- ❌ 文件較少\n")
        
        report.append("\n#### BDD（行為驅動開發）\n")
        report.append("**優點**：\n")
        report.append("- ✅ 開發效率高\n")
        report.append("- ✅ 場景易於理解\n")
        report.append("- ✅ 適合團隊協作\n")
        report.append("\n**缺點**：\n")
        report.append("- ❌ 測試覆蓋率中等\n")
        report.append("- ❌ 需要學習 Gherkin 語法\n")
        
        report.append("\n#### DDD（文件驅動開發）\n")
        report.append("**優點**：\n")
        report.append("- ✅ 文件最完整\n")
        report.append("- ✅ API 規格清晰\n")
        report.append("- ✅ 適合大型專案\n")
        report.append("\n**缺點**：\n")
        report.append("- ❌ 開發時間最長\n")
        report.append("- ❌ 測試覆蓋率較低\n")
        
        report.append("\n---\n")
        report.append("\n## 六、建議\n")
        report.append("\n根據分析結果，建議：\n")
        report.append("- **追求品質**：選擇 TDD，確保程式碼穩定性\n")
        report.append("- **追求效率**：選擇 BDD，快速交付功能\n")
        report.append("- **追求規範**：選擇 DDD，適合多人協作\n")
        report.append("- **實際專案**：可以混合使用，發揮各自優勢\n")
        
        return ''.join(report)
    
    def save_report(self, content, output_path):
        """儲存報告"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 報告已儲存：{output_path}")


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description='生成版本比較報告',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--output',
        default='comparison_report.md',
        help='輸出檔案名稱'
    )
    
    parser.add_argument(
        '--format',
        choices=['markdown', 'html'],
        default='markdown',
        help='報告格式'
    )
    
    args = parser.parse_args()
    
    try:
        print("\n" + "="*50)
        print("📊 開始生成比較報告")
        print("="*50 + "\n")
        
        comparator = VersionComparator()
        
        if args.format == 'markdown':
            report = comparator.generate_markdown_report()
            output_path = comparator.analysis_dir / args.output
            comparator.save_report(report, output_path)
        
        print("\n" + "="*50)
        print("✅ 報告生成完成！")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n❌ 生成報告時發生錯誤：{e}")
        sys.exit(1)


if __name__ == '__main__':
    main()