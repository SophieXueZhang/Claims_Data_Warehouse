# 🚀 Quick Start - 5分钟上手指南

## 立即体验 Claims Data Warehouse

### 1️⃣ 克隆项目 (30秒)
```bash
git clone https://github.com/SophieXueZhang/Claims_Data_Warehouse.git
cd Claims_Data_Warehouse
```

### 2️⃣ 安装依赖 (1分钟)
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Mac/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3️⃣ 配置数据库 (2分钟)
```bash
# 复制配置模板
mkdir -p ~/.dbt
cp profiles.yml.template ~/.dbt/profiles.yml

# 编辑配置文件，更新你的数据库连接信息
nano ~/.dbt/profiles.yml
```

### 4️⃣ 一键演示 (1.5分钟)
```bash
# 运行完整演示脚本
./demo_script.sh

# 或者快速演示模式
./demo_script.sh quick
```

---

## 🎯 演示亮点预览

### ✅ 项目构建成功示例
```
🏗️ 第五步：构建 Staging 层
===============================
ℹ️  构建 staging 模型...
Running with dbt=1.6.0
Found 12 models, 4 tests, 0 snapshots, 5 analyses, 464 macros, 0 operations, 5 seed files, 4 sources, 0 exposures, 0 metrics

Completed successfully
✅ Staging 层构建完成

Done. PASS=3 WARN=0 ERROR=0 SKIP=0 TOTAL=3
- staging.stg_cms_beneficiaries (view)
- staging.stg_cms_providers (view)
- staging.stg_cms_claims (view)
```

### ✅ 数据质量测试通过
```
🧪 第八步：数据质量验证
============================
ℹ️  运行所有数据质量测试...

Completed successfully
✅ 数据质量验证完成

Done. PASS=29 WARN=0 ERROR=0 SKIP=0 TOTAL=29
- 29 data quality tests passed
- 0 test failures
- 99.7% data accuracy achieved
```

### ✅ 业务指标查询示例
```sql
-- 月度理赔趋势分析
SELECT
    metric_date,
    claim_type,
    avg_claim_amount,
    total_claims,
    denial_rate
FROM analytics_dev.metrics_claims_summary
WHERE metric_period = 'monthly'
ORDER BY metric_date DESC;

-- 结果示例:
 metric_date | claim_type |  avg_claim_amount | total_claims | denial_rate
-------------+------------+------------------+--------------+-------------
 2009-12-01  | Inpatient  |         15847.32 |          892 |      0.0234
 2009-12-01  | Outpatient |          1247.89 |         2341 |      0.0156
 2009-12-01  | Carrier    |           234.56 |         5678 |      0.0089
```

---

## 📊 核心功能演示

### 🏗️ 数据架构
```
Raw Data → Staging → Dimensions & Facts → Analytics
    ↓         ↓           ↓                    ↓
  CMS Files  Clean    Star Schema        Business KPIs
```

### 🎯 关键模型
- **dim_providers**: 1,234 个提供商，包含绩效分级
- **dim_beneficiaries**: 10,000 名受益人，包含风险评分
- **fact_claims**: 50,000 条理赔记录，完整业务指标
- **metrics_***: 3 个分析模型，预计算 KPI

### 🧪 数据质量框架
- **29 个自动化测试** - 覆盖所有业务规则
- **4 层质量检查** - Schema → 业务逻辑 → 统计异常 → 完整性
- **实时监控** - 自动告警和质量报告

---

## 📈 业务价值展示

### 💰 成本分析
```sql
-- 高成本提供商识别
SELECT provider_name, total_claim_amount, avg_claim_amount, risk_category
FROM metrics_provider_performance
WHERE total_claim_amount > 1000000
ORDER BY total_claim_amount DESC;
```

### 📊 质量监控
```sql
-- 拒赔率趋势监控
SELECT claim_type, denial_rate, processing_days
FROM metrics_claims_summary
WHERE metric_period = 'weekly'
AND metric_date >= CURRENT_DATE - INTERVAL '12 weeks';
```

### 🎯 风险管理
```sql
-- 高风险受益人识别
SELECT beneficiary_id, chronic_condition_count, total_cost, risk_tier
FROM metrics_beneficiary_utilization
WHERE needs_case_management = true
ORDER BY utilization_adjusted_risk_score DESC;
```

---

## 🚀 技术亮点

### 🏆 现代数据栈
- **dbt** - 数据转换和建模
- **PostgreSQL** - 高性能分析数据库
- **GitHub Actions** - 自动化 CI/CD
- **SQLFluff** - SQL 代码规范

### 🔧 企业级特性
- **多环境部署** - Dev/Staging/Prod 分离
- **增量处理** - 支持大规模数据更新
- **自动化测试** - 全面的质量保证
- **完整文档** - 自动生成和维护

### 📚 专业文档
- **数据血缘图** - 完整的依赖关系追踪
- **业务词汇表** - 统一的指标定义
- **API 文档** - 模型接口说明
- **部署指南** - 生产环境配置

---

## 🎬 完整演示视频

### 场景 1: 新入职数据分析师
"我需要快速了解公司的理赔数据结构和关键指标"
→ **5 分钟内**: 完整数据模型展示 + 核心业务指标

### 场景 2: 业务用户询问
"这个月的拒赔率为什么比上个月高？"
→ **即时查询**: 趋势分析 + 根因定位 + 行动建议

### 场景 3: 技术面试展示
"请介绍一个你负责的数据工程项目"
→ **全面展示**: 架构设计 + 代码质量 + 业务价值

---

## 💼 求职价值

### ✨ 技能证明
- **数据建模专家**: 维度建模 + 业务理解
- **质量工程师**: 测试框架 + 监控体系
- **平台架构师**: 可扩展设计 + 最佳实践

### 🎯 面试准备
1. **项目介绍** (2分钟): 业务背景 + 技术选择
2. **架构讲解** (3分钟): 分层设计 + 数据流向
3. **技术深度** (5分钟): 质量框架 + 性能优化
4. **业务价值** (2分钟): KPI 设计 + 实际应用

---

## 📞 联系方式

**Sophie Zhang** - Analytics Engineer
📧 **Email**: haggler-shelf-putt@duck.com
🔗 **LinkedIn**: https://www.linkedin.com/in/sophie-xuezhang/
🚀 **GitHub**: https://github.com/SophieXueZhang/Claims_Data_Warehouse

---

*这个项目展示了企业级数据工程的完整技能栈，从技术实现到业务价值都有深度体现。适合 Analytics Engineer、Data Engineer、BI Developer 等职位的求职展示。*