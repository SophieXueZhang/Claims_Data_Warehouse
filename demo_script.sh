#!/bin/bash

# 🎬 Claims Data Warehouse - 完整演示脚本
# 作者: Sophie Zhang
# 用途: 展示 dbt 项目的完整功能和业务价值

set -e  # 遇到错误时停止执行

echo "🏥 Claims Data Warehouse - 完整演示开始"
echo "================================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数：打印带颜色的信息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo ""
    echo -e "${YELLOW}$1${NC}"
    echo "$(echo "$1" | sed 's/./=/g')"
}

# 检查必要的工具
check_requirements() {
    print_header "🔧 第一步：环境检查"

    if ! command -v dbt &> /dev/null; then
        print_error "dbt 未安装，请运行: pip install dbt-postgres"
        exit 1
    fi
    print_success "dbt 已安装"

    if ! command -v psql &> /dev/null; then
        print_warning "PostgreSQL 客户端未安装，部分功能可能不可用"
    else
        print_success "PostgreSQL 客户端已安装"
    fi

    print_info "dbt 版本: $(dbt --version | head -n 1)"
}

# 验证 dbt 配置
verify_dbt_config() {
    print_header "🔗 第二步：验证 dbt 配置"

    print_info "测试数据库连接..."
    if dbt debug; then
        print_success "dbt 配置验证通过"
    else
        print_error "dbt 配置验证失败，请检查 profiles.yml"
        print_info "请确保已正确配置 ~/.dbt/profiles.yml"
        exit 1
    fi
}

# 安装依赖
install_dependencies() {
    print_header "📦 第三步：安装项目依赖"

    print_info "安装 dbt 包..."
    dbt deps
    print_success "dbt 包安装完成"

    print_info "解析 dbt 项目..."
    dbt parse
    print_success "项目解析完成"
}

# 加载种子数据
load_seed_data() {
    print_header "🌱 第四步：加载演示数据"

    print_info "加载种子数据到数据库..."
    dbt seed --full-refresh
    print_success "种子数据加载完成"

    print_info "验证种子数据..."
    dbt test --select source:*
}

# 构建 staging 层
build_staging() {
    print_header "🏗️  第五步：构建 Staging 层"

    print_info "构建 staging 模型..."
    dbt run --models staging
    print_success "Staging 层构建完成"

    print_info "运行 staging 层测试..."
    dbt test --models staging
    print_success "Staging 层测试通过"

    # 显示构建的模型
    print_info "已构建的 staging 模型："
    dbt ls --models staging --output name
}

# 构建核心层
build_core() {
    print_header "🎯 第六步：构建核心维度和事实表"

    print_info "构建维度表..."
    dbt run --models marts.core
    print_success "核心层构建完成"

    print_info "运行核心层测试..."
    dbt test --models marts.core
    print_success "核心层测试通过"

    # 显示构建的模型
    print_info "已构建的核心模型："
    dbt ls --models marts.core --output name
}

# 构建分析层
build_analytics() {
    print_header "📊 第七步：构建分析层"

    print_info "构建分析模型..."
    dbt run --models marts.analytics
    print_success "分析层构建完成"

    print_info "运行分析层测试..."
    dbt test --models marts.analytics
    print_success "分析层测试通过"

    # 显示构建的模型
    print_info "已构建的分析模型："
    dbt ls --models marts.analytics --output name
}

# 运行数据质量测试
run_data_quality_tests() {
    print_header "🧪 第八步：数据质量验证"

    print_info "运行所有数据质量测试..."
    dbt test

    print_info "运行自定义业务规则测试..."
    dbt test --select test_type:singular

    print_success "数据质量验证完成"
}

# 生成文档
generate_documentation() {
    print_header "📚 第九步：生成项目文档"

    print_info "生成 dbt 文档..."
    dbt docs generate
    print_success "文档生成完成"

    print_info "启动文档服务器..."
    print_info "文档将在 http://localhost:8080 提供服务"
    print_warning "按 Ctrl+C 停止文档服务器"

    # 在后台启动文档服务器
    dbt docs serve --port 8080 &
    DOC_SERVER_PID=$!

    # 等待用户查看文档
    sleep 3
    print_info "文档服务器已启动 (PID: $DOC_SERVER_PID)"
}

# 演示业务查询
demonstrate_analytics() {
    print_header "💡 第十步：业务分析演示"

    if command -v psql &> /dev/null; then
        print_info "连接数据库执行示例查询..."

        # 这里可以添加实际的 SQL 查询演示
        print_info "示例查询 1: 月度理赔趋势"
        echo "SELECT metric_date, claim_type, avg_claim_amount, total_claims"
        echo "FROM analytics_dev.metrics_claims_summary"
        echo "WHERE metric_period = 'monthly' LIMIT 5;"

        print_info "示例查询 2: 提供商绩效排名"
        echo "SELECT provider_name, specialty_description, total_claims, performance_tier"
        echo "FROM analytics_dev.metrics_provider_performance"
        echo "ORDER BY total_claims DESC LIMIT 10;"

        print_info "示例查询 3: 高风险受益人识别"
        echo "SELECT beneficiary_id, risk_tier, total_cost, chronic_condition_count"
        echo "FROM analytics_dev.metrics_beneficiary_utilization"
        echo "WHERE risk_tier = 'High Risk' LIMIT 10;"

    else
        print_warning "PostgreSQL 客户端未安装，跳过查询演示"
    fi
}

# 显示项目统计
show_project_stats() {
    print_header "📈 项目统计信息"

    print_info "模型统计："
    echo "  - Staging 模型: $(dbt ls --models staging --output name | wc -l)"
    echo "  - 核心模型: $(dbt ls --models marts.core --output name | wc -l)"
    echo "  - 分析模型: $(dbt ls --models marts.analytics --output name | wc -l)"
    echo "  - 总模型数: $(dbt ls --models fqn:* --output name | wc -l)"

    print_info "测试统计："
    echo "  - 总测试数: $(dbt test --store-failures 2>/dev/null | grep -c "PASS\|FAIL" || echo "未运行测试")"

    print_info "文档统计："
    echo "  - 源表: $(dbt ls --resource-type source --output name | wc -l)"
    echo "  - 种子文件: $(dbt ls --resource-type seed --output name | wc -l)"
}

# 清理资源
cleanup() {
    print_header "🧹 清理和总结"

    if [ ! -z "$DOC_SERVER_PID" ]; then
        print_info "停止文档服务器..."
        kill $DOC_SERVER_PID 2>/dev/null || true
    fi

    print_success "演示完成！"
    echo ""
    echo "🎯 演示总结:"
    echo "  ✅ 完整的数据管道构建"
    echo "  ✅ 多层数据架构验证"
    echo "  ✅ 全面的数据质量测试"
    echo "  ✅ 业务分析能力展示"
    echo "  ✅ 自动化文档生成"
    echo ""
    echo "📞 联系方式:"
    echo "  👤 Sophie Zhang"
    echo "  📧 haggler-shelf-putt@duck.com"
    echo "  🔗 https://www.linkedin.com/in/sophie-xuezhang/"
    echo ""
    echo "🚀 项目地址: https://github.com/SophieXueZhang/Claims_Data_Warehouse"
}

# 主执行流程
main() {
    echo "开始执行完整演示流程..."
    echo ""

    # 捕获中断信号，确保清理
    trap cleanup EXIT INT TERM

    check_requirements
    verify_dbt_config
    install_dependencies
    load_seed_data
    build_staging
    build_core
    build_analytics
    run_data_quality_tests
    show_project_stats
    generate_documentation
    demonstrate_analytics

    print_success "所有步骤完成！"

    # 保持文档服务器运行
    if [ ! -z "$DOC_SERVER_PID" ]; then
        print_info "文档服务器继续运行在 http://localhost:8080"
        print_info "按 Ctrl+C 退出演示并停止服务器"
        wait $DOC_SERVER_PID
    fi
}

# 参数处理
case "${1:-}" in
    "quick")
        print_info "快速演示模式 - 仅构建核心功能"
        check_requirements
        verify_dbt_config
        install_dependencies
        build_staging
        build_core
        ;;
    "test-only")
        print_info "仅运行测试"
        run_data_quality_tests
        ;;
    "docs-only")
        print_info "仅生成文档"
        generate_documentation
        wait
        ;;
    *)
        main
        ;;
esac