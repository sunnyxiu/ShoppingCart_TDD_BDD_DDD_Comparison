#!/usr/bin/env python3
"""
從 CSV 檔案生成比較圖表

使用方式：
    python generate_charts.py
    python generate_charts.py --chart development_time
    python generate_charts.py --chart coverage
    python generate_charts.py --chart all

需要安裝：
    pip install pandas matplotlib seaborn --break-system-packages
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import sys
from pathlib import Path

# 設定中文字體（避免中文顯示問題）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 設定 seaborn 樣式
sns.set_style("whitegrid")
sns.set_palette("husl")


class ChartGenerator:
    """圖表生成器"""
    
    def __init__(self):
        """初始化"""
        self.metrics_dir = Path("../comparison/metrics")
        self.output_dir = Path("../comparison/analysis/charts")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
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
    
    def plot_development_time(self):
        """繪製開發時間比較圖"""
        print("\n📊 生成開發時間比較圖...")
        
        df = self.load_data("development_time.csv")
        if df is None or df.empty:
            print("⚠️  沒有開發時間資料")
            return
        
        # 移除空白行
        df = df.dropna(subset=['耗時(分鐘)'])
        
        if df.empty:
            print("⚠️  沒有有效的開發時間資料")
            return
        
        # 1. 總開發時間比較
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 按版本分組計算總時間
        total_time = df.groupby('版本')['耗時(分鐘)'].sum().sort_values(ascending=False)
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        total_time.plot(kind='bar', ax=ax1, color=colors, alpha=0.8)
        ax1.set_title('總開發時間比較', fontsize=16, fontweight='bold', pad=20)
        ax1.set_xlabel('版本', fontsize=12)
        ax1.set_ylabel('時間 (分鐘)', fontsize=12)
        ax1.tick_params(axis='x', rotation=0)
        ax1.grid(axis='y', alpha=0.3)
        
        # 在柱狀圖上顯示數值
        for i, v in enumerate(total_time):
            ax1.text(i, v + 10, f'{int(v)}', ha='center', va='bottom', fontweight='bold')
        
        # 2. 各功能開發時間分布
        pivot_data = df.pivot_table(values='耗時(分鐘)', index='功能', columns='版本', aggfunc='sum')
        pivot_data.plot(kind='bar', ax=ax2, width=0.8)
        ax2.set_title('各功能開發時間分布', fontsize=16, fontweight='bold', pad=20)
        ax2.set_xlabel('功能', fontsize=12)
        ax2.set_ylabel('時間 (分鐘)', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        ax2.legend(title='版本', loc='upper right')
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = self.output_dir / "development_time_chart.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ 開發時間圖表已儲存：{output_path}")
    
    def plot_code_coverage(self):
        """繪製測試覆蓋率比較圖"""
        print("\n📊 生成測試覆蓋率比較圖...")
        
        df = self.load_data("test_coverage.csv")
        if df is None or df.empty:
            print("⚠️  沒有測試覆蓋率資料")
            return
        
        # 移除空白行
        df = df.dropna(subset=['行覆蓋率(%)'])
        
        if df.empty:
            print("⚠️  沒有有效的測試覆蓋率資料")
            return
        
        # 取每個版本的最新覆蓋率
        latest = df.groupby('版本').last()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 1. 最終覆蓋率比較
        coverage_types = ['行覆蓋率(%)', '分支覆蓋率(%)', '函數覆蓋率(%)']
        x = range(len(latest.index))
        width = 0.25
        
        for i, cov_type in enumerate(coverage_types):
            if cov_type in latest.columns:
                values = latest[cov_type].values
                ax1.bar([p + width * i for p in x], values, width, 
                       label=cov_type.replace('覆蓋率(%)', ''), alpha=0.8)
        
        ax1.set_title('最終測試覆蓋率比較', fontsize=16, fontweight='bold', pad=20)
        ax1.set_xlabel('版本', fontsize=12)
        ax1.set_ylabel('覆蓋率 (%)', fontsize=12)
        ax1.set_xticks([p + width for p in x])
        ax1.set_xticklabels(latest.index)
        ax1.set_ylim(0, 100)
        ax1.legend(loc='upper right')
        ax1.grid(axis='y', alpha=0.3)
        
        # 2. 覆蓋率變化趨勢
        for version in df['版本'].unique():
            version_data = df[df['版本'] == version].sort_values('日期')
            if not version_data.empty and '行覆蓋率(%)' in version_data.columns:
                ax2.plot(range(len(version_data)), version_data['行覆蓋率(%)'], 
                        marker='o', label=version, linewidth=2, markersize=8)
        
        ax2.set_title('測試覆蓋率變化趨勢', fontsize=16, fontweight='bold', pad=20)
        ax2.set_xlabel('時間點', fontsize=12)
        ax2.set_ylabel('行覆蓋率 (%)', fontsize=12)
        ax2.set_ylim(0, 100)
        ax2.legend(loc='lower right')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_path = self.output_dir / "code_coverage_chart.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ 測試覆蓋率圖表已儲存：{output_path}")
    
    def plot_code_complexity(self):
        """繪製程式碼複雜度比較圖"""
        print("\n📊 生成程式碼複雜度比較圖...")
        
        df = self.load_data("code_metrics.csv")
        if df is None or df.empty:
            print("⚠️  沒有程式碼指標資料")
            return
        
        # 移除空白行
        df = df.dropna(subset=['程式碼行數'])
        
        if df.empty:
            print("⚠️  沒有有效的程式碼指標資料")
            return
        
        # 取最新的指標
        latest = df.groupby('版本').last()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. 程式碼行數比較
        if '程式碼行數' in latest.columns and '測試行數' in latest.columns:
            metrics = latest[['程式碼行數', '測試行數']]
            metrics.plot(kind='bar', ax=ax1, width=0.8, alpha=0.8)
            ax1.set_title('程式碼與測試行數比較', fontsize=14, fontweight='bold')
            ax1.set_xlabel('版本', fontsize=12)
            ax1.set_ylabel('行數', fontsize=12)
            ax1.tick_params(axis='x', rotation=0)
            ax1.legend(['程式碼', '測試'])
            ax1.grid(axis='y', alpha=0.3)
        
        # 2. 圈複雜度比較
        if '圈複雜度' in latest.columns:
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
            latest['圈複雜度'].plot(kind='bar', ax=ax2, color=colors, alpha=0.8)
            ax2.set_title('平均圈複雜度比較', fontsize=14, fontweight='bold')
            ax2.set_xlabel('版本', fontsize=12)
            ax2.set_ylabel('複雜度', fontsize=12)
            ax2.tick_params(axis='x', rotation=0)
            ax2.grid(axis='y', alpha=0.3)
            ax2.axhline(y=10, color='r', linestyle='--', alpha=0.5, label='警戒線')
            ax2.legend()
        
        # 3. 函數數量比較
        if '函數數量' in latest.columns:
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
            latest['函數數量'].plot(kind='bar', ax=ax3, color=colors, alpha=0.8)
            ax3.set_title('函數數量比較', fontsize=14, fontweight='bold')
            ax3.set_xlabel('版本', fontsize=12)
            ax3.set_ylabel('數量', fontsize=12)
            ax3.tick_params(axis='x', rotation=0)
            ax3.grid(axis='y', alpha=0.3)
        
        # 4. 測試與程式碼比例
        if '程式碼行數' in latest.columns and '測試行數' in latest.columns:
            ratio = (latest['測試行數'] / latest['程式碼行數']).fillna(0)
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
            ratio.plot(kind='bar', ax=ax4, color=colors, alpha=0.8)
            ax4.set_title('測試/程式碼比例', fontsize=14, fontweight='bold')
            ax4.set_xlabel('版本', fontsize=12)
            ax4.set_ylabel('比例', fontsize=12)
            ax4.tick_params(axis='x', rotation=0)
            ax4.grid(axis='y', alpha=0.3)
            ax4.axhline(y=1.0, color='g', linestyle='--', alpha=0.5, label='理想比例')
            ax4.legend()
        
        plt.tight_layout()
        output_path = self.output_dir / "complexity_comparison.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ 程式碼複雜度圖表已儲存：{output_path}")
    
    def plot_bug_statistics(self):
        """繪製 Bug 統計圖"""
        print("\n📊 生成 Bug 統計圖...")
        
        df = self.load_data("bug_tracking.csv")
        if df is None or df.empty:
            print("⚠️  沒有 Bug 追蹤資料")
            return
        
        # 移除空白行
        df = df.dropna(subset=['發現日期'])
        
        if df.empty:
            print("⚠️  沒有有效的 Bug 資料")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Bug 總數比較
        bug_count = df.groupby('版本').size()
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        bug_count.plot(kind='bar', ax=ax1, color=colors, alpha=0.8)
        ax1.set_title('Bug 總數比較', fontsize=14, fontweight='bold')
        ax1.set_xlabel('版本', fontsize=12)
        ax1.set_ylabel('數量', fontsize=12)
        ax1.tick_params(axis='x', rotation=0)
        ax1.grid(axis='y', alpha=0.3)
        
        # 在柱狀圖上顯示數值
        for i, v in enumerate(bug_count):
            ax1.text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')
        
        # 2. Bug 嚴重性分布
        if '嚴重性' in df.columns:
            severity_data = pd.crosstab(df['版本'], df['嚴重性'])
            severity_data.plot(kind='bar', ax=ax2, stacked=True, alpha=0.8)
            ax2.set_title('Bug 嚴重性分布', fontsize=14, fontweight='bold')
            ax2.set_xlabel('版本', fontsize=12)
            ax2.set_ylabel('數量', fontsize=12)
            ax2.tick_params(axis='x', rotation=0)
            ax2.legend(title='嚴重性')
            ax2.grid(axis='y', alpha=0.3)
        
        # 3. Bug 發現階段分布
        if '發現階段' in df.columns:
            stage_data = pd.crosstab(df['版本'], df['發現階段'])
            stage_data.plot(kind='bar', ax=ax3, alpha=0.8)
            ax3.set_title('Bug 發現階段分布', fontsize=14, fontweight='bold')
            ax3.set_xlabel('版本', fontsize=12)
            ax3.set_ylabel('數量', fontsize=12)
            ax3.tick_params(axis='x', rotation=0)
            ax3.legend(title='發現階段')
            ax3.grid(axis='y', alpha=0.3)
        
        # 4. 平均修復時間
        if '修復時間(分鐘)' in df.columns:
            avg_fix_time = df.groupby('版本')['修復時間(分鐘)'].mean()
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
            avg_fix_time.plot(kind='bar', ax=ax4, color=colors, alpha=0.8)
            ax4.set_title('平均 Bug 修復時間', fontsize=14, fontweight='bold')
            ax4.set_xlabel('版本', fontsize=12)
            ax4.set_ylabel('時間 (分鐘)', fontsize=12)
            ax4.tick_params(axis='x', rotation=0)
            ax4.grid(axis='y', alpha=0.3)
            
            # 顯示數值
            for i, v in enumerate(avg_fix_time):
                if not pd.isna(v):
                    ax4.text(i, v + 1, f'{v:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        output_path = self.output_dir / "bug_statistics.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Bug 統計圖表已儲存：{output_path}")
    
    def generate_all_charts(self):
        """生成所有圖表"""
        print("\n" + "="*50)
        print("📊 開始生成所有比較圖表")
        print("="*50)
        
        self.plot_development_time()
        self.plot_code_coverage()
        self.plot_code_complexity()
        self.plot_bug_statistics()
        
        print("\n" + "="*50)
        print("✅ 所有圖表生成完成！")
        print(f"📁 圖表位置：{self.output_dir}")
        print("="*50 + "\n")


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description='生成比較圖表',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
    python generate_charts.py                    # 生成所有圖表
    python generate_charts.py --chart all        # 生成所有圖表
    python generate_charts.py --chart time       # 只生成開發時間圖表
    python generate_charts.py --chart coverage   # 只生成測試覆蓋率圖表
    python generate_charts.py --chart complexity # 只生成複雜度圖表
    python generate_charts.py --chart bug        # 只生成 Bug 統計圖表
        """
    )
    
    parser.add_argument(
        '--chart',
        choices=['all', 'time', 'coverage', 'complexity', 'bug'],
        default='all',
        help='指定要生成的圖表類型'
    )
    
    args = parser.parse_args()
    
    try:
        generator = ChartGenerator()
        
        if args.chart == 'all':
            generator.generate_all_charts()
        elif args.chart == 'time':
            generator.plot_development_time()
        elif args.chart == 'coverage':
            generator.plot_code_coverage()
        elif args.chart == 'complexity':
            generator.plot_code_complexity()
        elif args.chart == 'bug':
            generator.plot_bug_statistics()
        
    except Exception as e:
        print(f"\n❌ 生成圖表時發生錯誤：{e}")
        sys.exit(1)


if __name__ == '__main__':
    main()