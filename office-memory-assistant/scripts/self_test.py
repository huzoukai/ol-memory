#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(args, cwd=None):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(map(str, args))}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return result.stdout


def write_fixture(data_dir: Path):
    fixtures = {
        "profile/personal-profile.md": "# 个人资料\n\n- 称呼：林夏\n- 岗位/角色：项目经理\n- 常写材料：投标材料、周报、项目总结、客户方案\n",
        "profile/company-profile.md": "# 公司资料\n\n- 公司/团队名称：澄明数字服务有限公司\n- 一句话介绍：一家为制造业和服务业提供业务数字化咨询与系统实施的测试公司。\n- 主要客户类型：区域制造企业、连锁服务企业、园区运营方\n- 服务范围：需求梳理、流程设计、数据看板、系统集成、上线陪跑\n- 资质/奖项/认证（需证据）：暂无已确认资料，生成时不得编写。\n",
        "profile/role-and-responsibilities.md": "# 岗位职责\n\n- 主要职责：需求访谈、项目推进、验收材料整理\n- 常参与项目：数据看板、流程数字化、客户方案\n- 协作对象：客户、实施、销售、上级\n",
        "profile/work-preferences.md": "# 工作偏好\n\n- 希望 AI 多问问题还是先给草稿：先给保守草稿，再列缺失信息\n- 输出保守程度：不夸大，不写无证据结论\n",
        "knowledge/project-cases.md": "# 项目案例\n\n## 园区运营看板项目\n\n- 项目名称：园区运营看板项目\n- 可公开程度：匿名\n- 背景：园区需要统一查看招商、入驻、报修和能耗数据。\n- 我的职责：需求访谈、里程碑管理、验收材料整理。\n- 结果：形成统一看板和周度运营例会机制。\n- 可复用表达：围绕业务流程和责任边界推进数字化落地。\n",
        "knowledge/capabilities.md": "# 能力库\n\n- 核心能力：需求梳理、流程设计、数据看板、系统集成、上线陪跑。\n- 交付能力：访谈、方案、原型、实施跟进、验收材料。\n- 技术/服务能力：业务流程数字化、数据指标整理、跨部门协同推进。\n- 证据来源：匿名项目案例。\n",
        "knowledge/forbidden-claims.md": "# 禁止编造和敏感边界\n\n- 禁止表达：行业领先、全链路赋能、革命性、全国第一\n- 未确认不得写：专利数量、客户数量、金额、认证、奖项。\n",
        "style/writing-style.md": "# 写作风格\n\n- 总体语气：简洁、正式、少 AI 味\n- 偏好：少用形容词，多写事实、动作和交付边界。\n",
        "style/favorite-phrases.md": "# 喜欢的表达\n\n- 具备相关项目经验\n- 围绕实际业务流程\n- 明确交付边界\n",
        "style/disliked-phrases.md": "# 不喜欢的表达\n\n- 赋能\n- 持续优化\n- 打造闭环\n- 不要写空泛的全链路价值表达\n",
        "style/audience-profiles.md": "# 受众偏好\n\n## 上级\n\n- 看重点、进展、风险和下一步。\n\n## 客户\n\n- 看问题理解、服务边界和可落地动作。\n",
        "style/leader-signals.md": "# 上级偏好\n\n## 最近关注主题\n\n- 结果\n- 责任边界\n\n## 喜欢的表达角度\n\n- 先讲业务问题，再讲方案。\n\n## 不喜欢的表达角度\n\n- 只喊口号。\n\n## 写材料时可借用的判断\n\n- 给上级看的材料优先写重点、风险、决策项和需要协调的资源。\n",
        "knowledge/leader-shared-materials.md": "# 上级转发内容\n\n## 素材 1\n\n- 日期：2026-07-01\n- 类型：文章\n- 来源或链接：内部转发\n- 上级转发时说了什么：做方案别只写系统功能。\n- 内容摘要：强调业务流程、责任人和指标追踪。\n- 关键词：流程、责任人、指标、复盘\n- 可能代表上级在意：方案要解释管理动作。\n- 可用于哪些材料：周报/月报/述职/方案\n- 是否可直接引用：否\n",
        "knowledge/leader-talking-points.md": "# 上级偏好的表达和论点\n\n这些不是公司事实，不能当资质或业绩写。\n\n## 可复用角度\n\n- 从业务问题出发，而不是从工具功能出发。\n- 结果、影响、下一步要比过程描述更靠前。\n\n## 常见关键词\n\n- 结果\n- 责任边界\n- 指标追踪\n\n## 写作提醒\n\n- 上级转发的内容通常只能作为偏好和方向，不能直接当成事实证据。\n",
        "templates/bid-capability.md": "# 投标公司能力说明模板\n\n## 草稿\n\n先写客户问题，再写能力边界、匿名案例和不能夸大的风险。\n\n## 使用资料\n\n公司资料、能力库、项目案例、禁忌边界。\n",
        "templates/weekly-report.md": "# 周报模板\n\n## 正式版\n\n本周完成事项、问题风险、下周计划。\n\n## 领导友好版\n\n优先写结果、影响、风险和需要协调的事项。\n",
        "templates/company-intro.md": "# 公司介绍模板\n\n## 150 字\n\n服务对象、核心能力、交付边界、匿名案例类型。\n",
    }
    for rel, content in fixtures.items():
        (data_dir / rel).write_text(content, encoding="utf-8")


def main():
    tmp = Path(tempfile.mkdtemp(prefix="office-memory-self-test-"))
    try:
        data_dir = tmp / "OL-Memory"
        trae_dir = tmp / "trae-pack"

        init_out = json.loads(run(["python3", SCRIPTS / "init_workspace.py", "--data-dir", data_dir]))
        assert init_out["status"] == "ok"
        manifest = json.loads((data_dir / "manifest.json").read_text(encoding="utf-8"))
        assert manifest["profile_name"] == ""
        assert manifest["company_name"] == ""
        write_fixture(data_dir)

        validation = json.loads(run(["python3", SCRIPTS / "validate_memory.py", "--data-dir", data_dir]))
        assert validation["status"] in {"HEALTHY", "WARNING"}
        assert validation["completeness_score"] >= 90
        assert validation["next_suggestion"].count(" / ") == 1

        empty_dir = tmp / "Empty-OL-Memory"
        run(["python3", SCRIPTS / "init_workspace.py", "--data-dir", empty_dir])
        empty_validation = json.loads(run(["python3", SCRIPTS / "validate_memory.py", "--data-dir", empty_dir]))
        assert "可能还没有填写实质内容" in empty_validation["warnings"][0]
        assert "Possibly empty Markdown" in empty_validation["warnings"][0]

        intake_dir = tmp / "Intake-OL-Memory"
        intake = json.loads(run([
            "python3", SCRIPTS / "intake_profile.py",
            "--data-dir", intake_dir,
            "--name", "林夏",
            "--role", "项目经理",
            "--common-docs", "周报,述职,投标材料",
            "--company-name", "澄明数字服务有限公司",
            "--company-intro", "为制造业客户提供数字化服务",
            "--service-scope", "需求调研、方案设计、上线陪跑",
            "--project-case", "某园区运营看板项目，匿名可用",
            "--forbidden-claims", "客户名称、金额、资质、奖项未确认不能写",
            "--writing-tone", "正式、简洁、少 AI 味",
            "--disliked-phrases", "赋能,持续优化"
        ]))
        assert intake["status"] == "ok"
        assert "林夏" in (intake_dir / "profile/personal-profile.md").read_text(encoding="utf-8")
        assert "制造业客户" in (intake_dir / "profile/company-profile.md").read_text(encoding="utf-8")
        intake_validation = json.loads(run(["python3", SCRIPTS / "validate_memory.py", "--data-dir", intake_dir]))
        assert intake_validation["completeness_score"] > empty_validation["completeness_score"]

        context = json.loads(run(["python3", SCRIPTS / "compose_context.py", "--data-dir", data_dir, "--scenario", "bid-materials"]))
        for required in ["profile/company-profile.md", "knowledge/project-cases.md", "knowledge/forbidden-claims.md", "knowledge/leader-talking-points.md"]:
            assert required in context["sources"], required
        assert "行业领先" in context["context"]

        leader_learning = json.loads(run(["python3", SCRIPTS / "compose_context.py", "--data-dir", data_dir, "--scenario", "leader-learning"]))
        assert "knowledge/leader-shared-materials.md" in leader_learning["sources"]

        run([
            "python3", SCRIPTS / "add_leader_material.py",
            "--data-dir", data_dir,
            "--title", "上级转发测试素材",
            "--summary", "上级转发的内容强调结果、复盘和下一步动作。",
            "--leader-comment", "这个表达方式可以学一下",
            "--signals", "上级关注结果和行动项"
        ])
        assert "上级转发测试素材" in (data_dir / "knowledge/leader-shared-materials.md").read_text(encoding="utf-8")

        learning = json.loads(run([
            "python3", SCRIPTS / "learn_from_output.py",
            "--data-dir", data_dir,
            "--feedback", "我不喜欢“持续优化”和“赋能”，以后别这么写。",
            "--source-task", "self_test"
        ]))
        assert learning["status"] == "pending_created"
        assert learning["item"]["suggested_target_file"] == "style/disliked-phrases.md"

        accepted = json.loads(run([
            "python3", SCRIPTS / "learn_from_output.py",
            "--data-dir", data_dir,
            "--accept", learning["item"]["id"]
        ]))
        assert accepted["status"] == "accepted"
        assert "以后别这么写" in (data_dir / "style/disliked-phrases.md").read_text(encoding="utf-8")

        run(["python3", SCRIPTS / "export_trae_pack.py", "--data-dir", data_dir, "--out-dir", trae_dir])
        assert (trae_dir / "TRAE_USAGE.md").exists()
        assert "launch_ui.py" in (trae_dir / "TRAE_USAGE.md").read_text(encoding="utf-8")

        print(json.dumps({
            "status": "passed",
            "checks": [
                "init_empty_workspace",
                "write_test_fixture",
                "validate_memory",
                "validate_bilingual_warnings",
                "first_run_intake_profile",
                "compose_bid_context",
                "compose_leader_learning_context",
                "add_leader_material",
                "pending_learning",
                "accept_learning",
                "export_trae_pack"
            ],
            "temp_dir": str(tmp)
        }, ensure_ascii=False, indent=2))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
