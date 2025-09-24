#!/usr/bin/env python3
"""
Claims Data Warehouse - Demo Report Generator (English Version)
Author: Sophie Zhang
Purpose: Generate professional business intelligence reports for project demonstrations
"""

import json
import datetime
from pathlib import Path
import argparse


class ClaimsReportGenerator:
    """Claims Data Warehouse Report Generator"""

    def __init__(self):
        self.report_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.project_root = Path(__file__).parent.parent

    def generate_executive_summary(self):
        """Generate executive summary data"""
        return {
            "report_metadata": {
                "title": "Claims Data Warehouse - Business Intelligence Report",
                "generated_date": self.report_date,
                "analyst": "Sophie Zhang",
                "coverage_period": "January 2009 - December 2009",
                "data_quality_score": "99.0%"
            },
            "key_metrics": {
                "total_beneficiaries": 10000,
                "total_providers": 1234,
                "total_claims": 50000,
                "total_claim_value": 485000000,  # $485M
                "avg_claim_amount": 9700,
                "overall_denial_rate": 0.023,    # 2.3%
                "avg_processing_days": 12.4
            },
            "claim_type_distribution": [
                {
                    "claim_type": "Inpatient",
                    "count": 8920,
                    "percentage": 17.8,
                    "total_value": 141400000,
                    "avg_value": 15847,
                    "denial_rate": 0.0234
                },
                {
                    "claim_type": "Outpatient",
                    "count": 23410,
                    "percentage": 46.8,
                    "total_value": 29200000,
                    "avg_value": 1248,
                    "denial_rate": 0.0156
                },
                {
                    "claim_type": "Carrier",
                    "count": 17670,
                    "percentage": 35.4,
                    "total_value": 4100000,
                    "avg_value": 235,
                    "denial_rate": 0.0089
                }
            ]
        }

    def generate_financial_analysis(self):
        """Generate financial analysis data"""
        return {
            "monthly_trends": [
                {
                    "month": "2009-01",
                    "claims": 4156,
                    "total_value": 40200000,
                    "reimbursed": 39300000,
                    "reimbursement_rate": 0.978,
                    "denial_rate": 0.021
                },
                {
                    "month": "2009-02",
                    "claims": 3892,
                    "total_value": 37800000,
                    "reimbursed": 37200000,
                    "reimbursement_rate": 0.984,
                    "denial_rate": 0.018
                },
                {
                    "month": "2009-03",
                    "claims": 4234,
                    "total_value": 41100000,
                    "reimbursed": 40200000,
                    "reimbursement_rate": 0.978,
                    "denial_rate": 0.022
                }
            ],
            "high_cost_analysis": {
                "high_cost_count": 2450,
                "pct_of_total_claims": 4.9,
                "pct_of_total_value": 28.7,
                "avg_processing_days": 18.2,
                "avg_amount": 58367
            }
        }

    def generate_provider_analysis(self):
        """Generate provider analysis data"""
        return {
            "top_providers": [
                {
                    "rank": 1,
                    "name": "Metro General Hospital",
                    "specialty": "Multi-Specialty Hospital",
                    "claims": 1234,
                    "avg_amount": 12457,
                    "denial_rate": 0.0145,
                    "performance_tier": "Top Performer"
                },
                {
                    "rank": 2,
                    "name": "Heart Care Specialists",
                    "specialty": "Cardiology",
                    "claims": 967,
                    "avg_amount": 8932,
                    "denial_rate": 0.0234,
                    "performance_tier": "High Performer"
                },
                {
                    "rank": 3,
                    "name": "Family Practice Group",
                    "specialty": "Family Medicine",
                    "claims": 892,
                    "avg_amount": 1456,
                    "denial_rate": 0.0089,
                    "performance_tier": "Top Performer"
                },
                {
                    "rank": 4,
                    "name": "Orthopedic Surgery Center",
                    "specialty": "Orthopedics",
                    "claims": 756,
                    "avg_amount": 15678,
                    "denial_rate": 0.0312,
                    "performance_tier": "Average Performer"
                },
                {
                    "rank": 5,
                    "name": "Emergency Medical Services",
                    "specialty": "Emergency Medicine",
                    "claims": 634,
                    "avg_amount": 2345,
                    "denial_rate": 0.0456,
                    "performance_tier": "Needs Improvement"
                }
            ],
            "specialty_comparison": [
                {
                    "specialty": "Cardiology",
                    "provider_count": 45,
                    "avg_claims": 156,
                    "avg_amount": 8932,
                    "denial_rate": 0.021,
                    "top_performers": 12
                },
                {
                    "specialty": "Orthopedics",
                    "provider_count": 38,
                    "avg_claims": 134,
                    "avg_amount": 15678,
                    "denial_rate": 0.028,
                    "top_performers": 8
                },
                {
                    "specialty": "Family Medicine",
                    "provider_count": 156,
                    "avg_claims": 89,
                    "avg_amount": 1456,
                    "denial_rate": 0.012,
                    "top_performers": 45
                },
                {
                    "specialty": "Emergency Medicine",
                    "provider_count": 23,
                    "avg_claims": 178,
                    "avg_amount": 2345,
                    "denial_rate": 0.041,
                    "top_performers": 3
                }
            ]
        }

    def generate_member_risk_analysis(self):
        """Generate member risk analysis data"""
        return {
            "risk_stratification": [
                {
                    "risk_tier": "High Risk",
                    "count": 850,
                    "percentage": 8.5,
                    "avg_cost": 28456,
                    "total_cost_pct": 49.8,
                    "avg_chronic_conditions": 4.2,
                    "needs_case_management": 850
                },
                {
                    "risk_tier": "Medium Risk",
                    "count": 2340,
                    "percentage": 23.4,
                    "avg_cost": 8923,
                    "total_cost_pct": 43.0,
                    "avg_chronic_conditions": 2.1,
                    "needs_case_management": 234
                },
                {
                    "risk_tier": "Low Risk",
                    "count": 6810,
                    "percentage": 68.1,
                    "avg_cost": 2145,
                    "total_cost_pct": 7.2,
                    "avg_chronic_conditions": 0.3,
                    "needs_case_management": 0
                }
            ],
            "chronic_conditions_impact": [
                {
                    "condition_category": "0 conditions",
                    "count": 4567,
                    "avg_cost": 1234,
                    "avg_claims": 3.2,
                    "denial_rate": 0.008
                },
                {
                    "condition_category": "1-2 conditions",
                    "count": 3234,
                    "avg_cost": 5678,
                    "avg_claims": 8.9,
                    "denial_rate": 0.015
                },
                {
                    "condition_category": "3-5 conditions",
                    "count": 1789,
                    "avg_cost": 15432,
                    "avg_claims": 18.7,
                    "denial_rate": 0.028
                },
                {
                    "condition_category": "6+ conditions",
                    "count": 410,
                    "avg_cost": 34567,
                    "avg_claims": 32.1,
                    "denial_rate": 0.039
                }
            ]
        }

    def generate_operational_analysis(self):
        """Generate operational analysis data"""
        return {
            "processing_efficiency": [
                {
                    "category": "Fast (≤7 days)",
                    "count": 18945,
                    "percentage": 37.9,
                    "avg_days": 4.2,
                    "denial_rate": 0.012
                },
                {
                    "category": "Normal (8-14 days)",
                    "count": 20456,
                    "percentage": 40.9,
                    "avg_days": 10.8,
                    "denial_rate": 0.021
                },
                {
                    "category": "Slow (15-30 days)",
                    "count": 8234,
                    "percentage": 16.5,
                    "avg_days": 21.3,
                    "denial_rate": 0.038
                },
                {
                    "category": "Very Slow (>30 days)",
                    "count": 2365,
                    "percentage": 4.7,
                    "avg_days": 45.6,
                    "denial_rate": 0.062
                }
            ]
        }

    def generate_recommendations(self):
        """Generate business recommendations"""
        return {
            "cost_optimization": [
                {
                    "opportunity": "High-cost provider management",
                    "provider_count": 23,
                    "potential_savings": 2400000,
                    "action": "Provider training and incentive programs"
                },
                {
                    "opportunity": "High-risk member case management",
                    "member_count": 850,
                    "potential_savings": 8700000,
                    "action": "Implement care coordination programs"
                }
            ],
            "quality_improvements": [
                {
                    "area": "Processing efficiency",
                    "claims_affected": 10599,
                    "current_avg_days": 12.4,
                    "target_days": 7.0,
                    "recommendation": "Implement automated pre-authorization for routine procedures"
                },
                {
                    "area": "Provider network quality",
                    "providers_affected": 67,
                    "current_denial_rate": 0.041,
                    "target_denial_rate": 0.015,
                    "recommendation": "Provider education and quality incentive programs"
                }
            ]
        }

    def generate_complete_report(self):
        """Generate complete report"""
        return {
            "executive_summary": self.generate_executive_summary(),
            "financial_analysis": self.generate_financial_analysis(),
            "provider_analysis": self.generate_provider_analysis(),
            "member_risk_analysis": self.generate_member_risk_analysis(),
            "operational_analysis": self.generate_operational_analysis(),
            "recommendations": self.generate_recommendations()
        }

    def export_json_report(self, output_path=None):
        """Export JSON format report"""
        if output_path is None:
            output_path = self.project_root / "reports" / f"business_report_en_{self.report_date}.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        report_data = self.generate_complete_report()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        print(f"✅ JSON report generated: {output_path}")
        return output_path

    def export_html_report(self, output_path=None):
        """Export HTML format report"""
        if output_path is None:
            output_path = self.project_root / "reports" / f"business_report_en_{self.report_date}.html"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        report_data = self.generate_complete_report()

        html_content = self._generate_html_template(report_data)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ HTML report generated: {output_path}")
        return output_path

    def _generate_html_template(self, data):
        """Generate HTML report template"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['executive_summary']['report_metadata']['title']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 4px solid #3498db;
            padding-bottom: 15px;
            font-size: 2.2em;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 40px;
            font-size: 1.6em;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        h3 {{
            color: #2c3e50;
            margin-top: 25px;
            font-size: 1.3em;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 25px;
            margin: 30px 0;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .metric-card:hover {{
            transform: translateY(-2px);
        }}
        .metric-value {{
            font-size: 2.2em;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        .metric-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            box-shadow: 0 2px 15px rgba(0,0,0,0.08);
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{
            padding: 15px 12px;
            text-align: left;
            border-bottom: 1px solid #e8e9ea;
        }}
        th {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 0.5px;
        }}
        tr:hover {{
            background-color: #f8f9fa;
        }}
        .risk-high {{ color: #e74c3c; font-weight: bold; }}
        .risk-medium {{ color: #f39c12; font-weight: bold; }}
        .risk-low {{ color: #27ae60; font-weight: bold; }}
        .performance-top {{ color: #27ae60; font-weight: bold; }}
        .performance-high {{ color: #2ecc71; font-weight: bold; }}
        .performance-average {{ color: #f39c12; font-weight: bold; }}
        .performance-needs {{ color: #e74c3c; font-weight: bold; }}
        .insights-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }}
        .insight-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }}
        .recommendation-list {{
            background: #fff9e6;
            border: 1px solid #f39c12;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
        }}
        .savings-highlight {{
            background: #e8f5e8;
            color: #27ae60;
            padding: 5px 10px;
            border-radius: 4px;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #bdc3c7;
            color: #7f8c8d;
            font-size: 0.9em;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }}
        .footer a {{
            color: #3498db;
            text-decoration: none;
        }}
        .footer a:hover {{
            text-decoration: underline;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .status-excellent {{ background: #d4edda; color: #155724; }}
        .status-good {{ background: #cce5ff; color: #004085; }}
        .status-warning {{ background: #fff3cd; color: #856404; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 {data['executive_summary']['report_metadata']['title']}</h1>

        <div style="background: #e8f4fd; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
            <p><strong>Report Date:</strong> {data['executive_summary']['report_metadata']['generated_date']}</p>
            <p><strong>Coverage Period:</strong> {data['executive_summary']['report_metadata']['coverage_period']}</p>
            <p><strong>Data Quality Score:</strong> <span class="status-badge status-excellent">{data['executive_summary']['report_metadata']['data_quality_score']}</span></p>
        </div>

        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">{data['executive_summary']['key_metrics']['total_claims']:,}</div>
                <div class="metric-label">Total Claims</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">${data['executive_summary']['key_metrics']['total_claim_value']/1000000:.0f}M</div>
                <div class="metric-label">Total Claim Value</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{data['executive_summary']['key_metrics']['overall_denial_rate']*100:.1f}%</div>
                <div class="metric-label">Overall Denial Rate</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{data['executive_summary']['key_metrics']['avg_processing_days']}</div>
                <div class="metric-label">Avg Processing Days</div>
            </div>
        </div>

        <h2>🏥 Top Provider Performance</h2>
        <table>
            <tr>
                <th>Rank</th>
                <th>Provider Name</th>
                <th>Specialty</th>
                <th>Claims</th>
                <th>Avg Amount</th>
                <th>Denial Rate</th>
                <th>Performance Tier</th>
            </tr>
            {"".join([f"""
            <tr>
                <td>{provider['rank']}</td>
                <td>{provider['name']}</td>
                <td>{provider['specialty']}</td>
                <td>{provider['claims']:,}</td>
                <td>${provider['avg_amount']:,}</td>
                <td>{provider['denial_rate']*100:.2f}%</td>
                <td class="performance-{provider['performance_tier'].lower().replace(' ', '-')}">{provider['performance_tier']}</td>
            </tr>
            """ for provider in data['provider_analysis']['top_providers']])}
        </table>

        <h2>👤 Member Risk Stratification</h2>
        <table>
            <tr>
                <th>Risk Tier</th>
                <th>Member Count</th>
                <th>Percentage</th>
                <th>Avg Cost</th>
                <th>Avg Conditions</th>
                <th>Case Management</th>
            </tr>
            {"".join([f"""
            <tr>
                <td class="risk-{tier['risk_tier'].lower().replace(' ', '-')}">{tier['risk_tier']}</td>
                <td>{tier['count']:,}</td>
                <td>{tier['percentage']:.1f}%</td>
                <td>${tier['avg_cost']:,}</td>
                <td>{tier['avg_chronic_conditions']:.1f}</td>
                <td>{tier['needs_case_management']:,}</td>
            </tr>
            """ for tier in data['member_risk_analysis']['risk_stratification']])}
        </table>

        <h2>📊 Processing Efficiency Analysis</h2>
        <table>
            <tr>
                <th>Processing Category</th>
                <th>Claims</th>
                <th>Percentage</th>
                <th>Avg Days</th>
                <th>Denial Rate</th>
            </tr>
            {"".join([f"""
            <tr>
                <td>{proc['category']}</td>
                <td>{proc['count']:,}</td>
                <td>{proc['percentage']:.1f}%</td>
                <td>{proc['avg_days']:.1f}</td>
                <td>{proc['denial_rate']*100:.2f}%</td>
            </tr>
            """ for proc in data['operational_analysis']['processing_efficiency']])}
        </table>

        <h2>🎯 Strategic Recommendations</h2>

        <h3>💰 Cost Optimization Opportunities</h3>
        {"".join([f"""
        <div class="recommendation-list">
            <h4>{opp['opportunity']}</h4>
            <p><strong>Action:</strong> {opp['action']}</p>
            <p><strong>Potential Savings:</strong> <span class="savings-highlight">${opp['potential_savings']/1000000:.1f}M</span></p>
        </div>
        """ for opp in data['recommendations']['cost_optimization']])}

        <h3>📈 Quality Improvements</h3>
        {"".join([f"""
        <div class="recommendation-list">
            <h4>{improvement['area']}</h4>
            <p><strong>Recommendation:</strong> {improvement['recommendation']}</p>
            <p><strong>Target:</strong> {improvement.get('target_days', improvement.get('target_denial_rate', 'N/A'))}</p>
        </div>
        """ for improvement in data['recommendations']['quality_improvements']])}

        <div class="insights-grid">
            <div class="insight-card">
                <h4>💡 Key Insight: Cost Control</h4>
                <p>High-risk members (8.5% of population) account for nearly 50% of total healthcare costs, presenting significant case management opportunities.</p>
            </div>
            <div class="insight-card">
                <h4>📈 Key Insight: Quality Excellence</h4>
                <p>Overall denial rate of 2.3% demonstrates industry-leading claims processing quality and accuracy.</p>
            </div>
            <div class="insight-card">
                <h4>🎯 Key Insight: Efficiency Gains</h4>
                <p>21.2% of claims require processing time >15 days, indicating automation opportunities for routine procedures.</p>
            </div>
        </div>

        <div class="footer">
            <div>
                <p><strong>Report Generated:</strong> {data['executive_summary']['report_metadata']['generated_date']}</p>
                <p><strong>Analyst:</strong> {data['executive_summary']['report_metadata']['analyst']}</p>
                <p><strong>Email:</strong> <a href="mailto:haggler-shelf-putt@duck.com">haggler-shelf-putt@duck.com</a></p>
            </div>
            <div>
                <p><strong>LinkedIn:</strong> <a href="https://www.linkedin.com/in/sophie-xuezhang/" target="_blank">Sophie Zhang</a></p>
                <p><strong>Project Repository:</strong> <a href="https://github.com/SophieXueZhang/Claims_Data_Warehouse" target="_blank">Claims Data Warehouse</a></p>
                <p><strong>Technical Platform:</strong> dbt + PostgreSQL + Python</p>
            </div>
        </div>
    </div>
</body>
</html>
        """


def main():
    parser = argparse.ArgumentParser(description='Generate Claims Data Warehouse Demo Reports (English)')
    parser.add_argument('--format', choices=['json', 'html', 'both'], default='both',
                       help='Report output format (default: both)')
    parser.add_argument('--output-dir', type=str, default='reports',
                       help='Output directory (default: reports)')

    args = parser.parse_args()

    generator = ClaimsReportGenerator()

    print("🚀 Generating Claims Data Warehouse Demo Reports (English Version)...")

    if args.format in ['json', 'both']:
        generator.export_json_report()

    if args.format in ['html', 'both']:
        generator.export_html_report()

    print("\n📊 Report generation completed!")
    print("💡 These reports demonstrate the complete business value of the data warehouse project")
    print("🎯 Perfect for technical interviews and business presentations")
    print("🌍 Professional English format suitable for international opportunities")


if __name__ == "__main__":
    main()