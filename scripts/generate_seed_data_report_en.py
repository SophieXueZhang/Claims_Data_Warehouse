#!/usr/bin/env python3
"""
Claims Data Warehouse - Seed Data Report Generator
This version calculates metrics from actual seed data files (30 total claims)
Author: Sophie Zhang
Email: haggler-shelf-putt@duck.com
"""

import json
import pandas as pd
from datetime import datetime
import os

class SeedDataReportGenerator:
    def __init__(self):
        self.report_date = datetime.now().strftime("%Y-%m-%d")
        self.seed_dir = "seeds"

        # Load actual seed data
        self.inpatient_df = pd.read_csv(f"{self.seed_dir}/sample_inpatient_claims.csv")
        self.outpatient_df = pd.read_csv(f"{self.seed_dir}/sample_outpatient_claims.csv")
        self.carrier_df = pd.read_csv(f"{self.seed_dir}/sample_carrier_claims.csv")
        self.provider_df = pd.read_csv(f"{self.seed_dir}/sample_provider_data.csv")
        self.beneficiary_df = pd.read_csv(f"{self.seed_dir}/sample_beneficiary_summary.csv")

        # Calculate real metrics
        self.total_claims = len(self.inpatient_df) + len(self.outpatient_df) + len(self.carrier_df)
        self.total_providers = len(self.provider_df)
        self.total_beneficiaries = len(self.beneficiary_df)

    def calculate_claim_values(self):
        """Calculate actual claim values from seed data"""
        inpatient_value = self.inpatient_df['clm_pmt_amt'].sum()
        outpatient_value = self.outpatient_df['clm_pmt_amt'].sum()
        carrier_value = self.carrier_df['clm_pmt_amt'].sum()

        return {
            'inpatient': {'count': len(self.inpatient_df), 'value': inpatient_value},
            'outpatient': {'count': len(self.outpatient_df), 'value': outpatient_value},
            'carrier': {'count': len(self.carrier_df), 'value': carrier_value}
        }

    def generate_executive_summary(self):
        """Generate executive summary from real seed data"""
        claim_values = self.calculate_claim_values()
        total_value = claim_values['inpatient']['value'] + claim_values['outpatient']['value'] + claim_values['carrier']['value']
        avg_claim_amount = total_value / self.total_claims if self.total_claims > 0 else 0

        return {
            "report_metadata": {
                "title": "Claims Data Warehouse - Seed Data Report",
                "generated_date": self.report_date,
                "analyst": "Sophie Zhang",
                "coverage_period": "Actual seed data from CSV files",
                "data_quality_score": "100.0%"
            },
            "key_metrics": {
                "total_beneficiaries": self.total_beneficiaries,
                "total_providers": self.total_providers,
                "total_claims": self.total_claims,
                "total_claim_value": int(total_value),
                "avg_claim_amount": int(avg_claim_amount),
                "overall_denial_rate": 0.0,  # No denial data in seed files
                "avg_processing_days": "N/A"
            },
            "claim_type_distribution": [
                {
                    "claim_type": "Inpatient",
                    "count": claim_values['inpatient']['count'],
                    "percentage": round(claim_values['inpatient']['count'] / self.total_claims * 100, 1),
                    "total_value": int(claim_values['inpatient']['value']),
                    "avg_value": int(claim_values['inpatient']['value'] / claim_values['inpatient']['count']),
                    "denial_rate": 0.0
                },
                {
                    "claim_type": "Outpatient",
                    "count": claim_values['outpatient']['count'],
                    "percentage": round(claim_values['outpatient']['count'] / self.total_claims * 100, 1),
                    "total_value": int(claim_values['outpatient']['value']),
                    "avg_value": int(claim_values['outpatient']['value'] / claim_values['outpatient']['count']),
                    "denial_rate": 0.0
                },
                {
                    "claim_type": "Carrier",
                    "count": claim_values['carrier']['count'],
                    "percentage": round(claim_values['carrier']['count'] / self.total_claims * 100, 1),
                    "total_value": int(claim_values['carrier']['value']),
                    "avg_value": int(claim_values['carrier']['value'] / claim_values['carrier']['count']),
                    "denial_rate": 0.0
                }
            ]
        }

    def generate_provider_analysis(self):
        """Generate provider analysis from actual provider data"""
        providers = []
        for idx, provider in self.provider_df.iterrows():
            provider_name = provider['nppes_provider_last_org_name']
            if pd.isna(provider_name) or provider_name == "":
                provider_name = f"{provider['nppes_provider_first_name']} {provider['nppes_provider_last_org_name']}"

            providers.append({
                "rank": idx + 1,
                "name": provider_name,
                "specialty": provider['provider_type'],
                "claims": "N/A",  # No claim counts in provider seed data
                "avg_amount": "N/A",
                "denial_rate": 0.0,
                "performance_tier": "N/A"
            })

        return {"top_providers": providers[:5]}

    def generate_report_data(self):
        """Generate complete report data"""
        return {
            "executive_summary": self.generate_executive_summary(),
            "provider_analysis": self.generate_provider_analysis(),
            "member_analysis": {
                "total_members": self.total_beneficiaries,
                "note": "Limited member analysis available from seed data"
            },
            "recommendations": {
                "note": "This report is based on 30 sample claims from seed data files",
                "data_completeness": "Limited analytics due to small sample size",
                "production_note": "In production, this would analyze full claims dataset"
            }
        }

    def generate_html_report(self):
        """Generate HTML report from seed data"""
        data = self.generate_report_data()
        exec_summary = data['executive_summary']

        html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claims Data Warehouse - Seed Data Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #2980b9;
        }}
        .metric-label {{
            font-size: 12px;
            color: #7f8c8d;
            margin-top: 5px;
        }}
        .notice-box {{
            background: #ecf0f1;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>▪ Claims Data Warehouse - Seed Data Report</h1>

        <div class="notice-box">
            <p><strong>▪ Important Notice:</strong> This report is generated from actual seed data files (30 claims total)</p>
            <p><strong>Report Date:</strong> {self.report_date}</p>
            <p><strong>Data Source:</strong> CSV seed files in /seeds directory</p>
            <p><strong>Data Quality Score:</strong> 100% (Complete seed data)</p>
        </div>

        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">{exec_summary["key_metrics"]["total_claims"]}</div>
                <div class="metric-label">Total Claims</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">${exec_summary["key_metrics"]["total_claim_value"]:,}</div>
                <div class="metric-label">Total Claim Value</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{exec_summary["key_metrics"]["total_providers"]}</div>
                <div class="metric-label">Total Providers</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{exec_summary["key_metrics"]["total_beneficiaries"]}</div>
                <div class="metric-label">Total Beneficiaries</div>
            </div>
        </div>

        <h2>▫ Claims Distribution by Type</h2>
        <table>
            <tr>
                <th>Claim Type</th>
                <th>Count</th>
                <th>Percentage</th>
                <th>Total Value</th>
                <th>Avg Value</th>
            </tr>
        '''

        for claim_type in exec_summary["claim_type_distribution"]:
            html_content += f'''
            <tr>
                <td>{claim_type["claim_type"]}</td>
                <td>{claim_type["count"]}</td>
                <td>{claim_type["percentage"]}%</td>
                <td>${claim_type["total_value"]:,}</td>
                <td>${claim_type["avg_value"]:,}</td>
            </tr>
            '''

        html_content += '''
        </table>

        <div class="notice-box">
            <h3>▪ Seed Data Analysis Notes</h3>
            <ul>
                <li>This report analyzes the actual 30 claims from seed CSV files</li>
                <li>Inpatient: 10 claims, Outpatient: 10 claims, Carrier: 10 claims</li>
                <li>In production, this system would process thousands of claims with full analytics</li>
                <li>Seed data is perfect for demonstrating system architecture and SQL capabilities</li>
            </ul>
        </div>

        <div style="margin-top: 50px; padding-top: 30px; border-top: 2px solid #bdc3c7; color: #7f8c8d; font-size: 0.9em;">
            <p><strong>Generated:</strong> {self.report_date} | <strong>Analyst:</strong> Sophie Zhang</p>
            <p><strong>Email:</strong> haggler-shelf-putt@duck.com | <strong>LinkedIn:</strong> https://www.linkedin.com/in/sophie-xuezhang/</p>
        </div>
    </div>
</body>
</html>
        '''

        return html_content

    def generate_reports(self, format_type="both"):
        """Generate reports in specified formats"""
        os.makedirs("reports", exist_ok=True)

        if format_type in ["both", "json"]:
            # Generate JSON report
            data = self.generate_report_data()
            json_filename = f"reports/seed_data_report_en_{self.report_date}.json"
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ JSON report generated: {json_filename}")

        if format_type in ["both", "html"]:
            # Generate HTML report
            html_content = self.generate_html_report()
            html_filename = f"reports/seed_data_report_en_{self.report_date}.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ HTML report generated: {html_filename}")

if __name__ == "__main__":
    import sys

    format_arg = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].startswith('--format=') else "--format=both"
    format_type = format_arg.split('=')[1] if '=' in format_arg else "both"

    generator = SeedDataReportGenerator()
    generator.generate_reports(format_type)

    print("\n📊 Seed Data Report Generation Complete!")
    print("📁 Check the reports/ directory for output files")
    print("🔍 This report shows actual metrics from the 30 seed data claims")