# -*- coding: utf-8 -*-
"""把 lesson-*.html 里的 <pre class="lang-flow">...</pre> 替换成 HTML 流程图。
每次运行只处理 REPLACEMENTS 字典里出现的文件。可重复运行（幂等：未匹配到原始 pre 就跳过）。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# pre 块的正则：匹配整个 <pre class="lang-flow"><code>...</code></pre>
PRE_RE = re.compile(
    r'<pre class="lang-flow"><code>.*?</code></pre>',
    re.DOTALL,
)

# 每个 lesson 的新 HTML。键是文件名，值是替换后的 HTML 片段（不含外层 pre）。
REPLACEMENTS = {}

# -------- lesson-02 --------
REPLACEMENTS["lesson-02.html"] = '''<div class="flow-diagram">
  <div class="flow-actor">
    <div class="flow-actor-label">用户（极客）</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">Claude Code CLI · 启动加载</div>
    <ul>
      <li><code>CLAUDE.md</code> — 项目记忆</li>
      <li><code>Rules</code> — 行为约束</li>
      <li><code>Auto Memory</code> — 跨会话记忆</li>
    </ul>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">推断意图</span></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">主对话 / Claude · 选择行动</div>
    <ul>
      <li><code>Command</code> — 用户显式触发</li>
      <li><code>Skill</code> — LLM 推理触发</li>
      <li><code>SubAgent</code> — 委派隔离任务</li>
      <li><code>Tool</code> — 原子操作（读 / 写 / 搜 / 执行 / 交互）</li>
    </ul>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">每个动作</span></div>
  <div class="flow-box">
    <div class="flow-box-title">Hooks</div>
    <div class="flow-box-sub">Pre / Post / Stop / SubAgentStop</div>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">外部数据</span></div>
  <div class="flow-box">
    <div class="flow-box-title">MCP Servers</div>
    <div class="flow-box-sub">stdio / HTTP / SSE</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final">
    <div class="flow-actor-label">完成 → 回到主对话</div>
  </div>
  <div class="flow-note" style="margin-top:14px">可选运行模式：交互式 <code>claude</code> · Headless <code>claude --headless</code> · Agent SDK <code>query()</code> API</div>
</div>'''

# -------- lesson-03 --------
REPLACEMENTS["lesson-03.html"] = '''<div class="flow-diagram">
  <div class="flow-actor">
    <div class="flow-actor-label">Claude Code 启动</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">加载 CLAUDE.md 四级记忆</div>
    <ul>
      <li><code>~/.claude/CLAUDE.md</code> — 用户级（低优先级，先加载）</li>
      <li><code>./CLAUDE.md</code> — 项目级（覆盖用户级同名）</li>
      <li><code>./CLAUDE.local.md</code> — 本地级（覆盖项目级同名）</li>
      <li><code>./.claude/rules/*.md</code> — 规则目录（追加到末尾，按文件名排序）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box">
    <div class="flow-box-title">合并成 system prompt 的一部分</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box">
    <div class="flow-box-title">注入到上下文窗口</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">主对话开始</div>
    <ul>
      <li>用户提问</li>
      <li>Claude 加载 Auto Memory <code>~/.claude/memories/</code></li>
      <li>推断意图 → 选择 Tool / Skill / SubAgent / Command</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final">
    <div class="flow-actor-label">执行任务</div>
  </div>

  <div class="flow-container" style="margin-top:18px">
    <div class="flow-container-title">合并优先级</div>
    <div style="font-size:13px;color:var(--fg)">用户级 &lt; 项目级 &lt; 本地级 &lt; 规则目录（单文件追加，不覆盖）</div>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">渐进式披露</div>
    <ul style="margin:4px 0;font-size:13px">
      <li>CLAUDE.md 主体（高频 20% 规则，100-300 行）</li>
      <li>引用 <code>.claude/rules/python-style.md</code>（按需加载）</li>
      <li>引用 <code>.claude/rules/db-migration.md</code>（按需加载）</li>
      <li>引用 <code>docs/api.md</code>（按需加载）</li>
    </ul>
  </div>
</div>'''

# -------- lesson-04 --------
REPLACEMENTS["lesson-04.html"] = '''<div class="flow-diagram">
  <div class="flow-actor">
    <div class="flow-actor-label">用户（主对话）</div>
    <div class="flow-actor-desc">"用 code-reviewer 审查我刚改的代码"</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">主对话 / Claude</div>
    <ul>
      <li>加载 CLAUDE.md</li>
      <li>推断用户意图</li>
      <li>匹配到 <code>code-reviewer</code></li>
    </ul>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">委派（只传任务 + 必要上下文）</span></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">SubAgent: code-reviewer</div>
    <ul>
      <li>独立 system prompt</li>
      <li>工具白名单 <code>[Read / Grep / Glob / Bash]</code></li>
      <li>独立上下文窗口</li>
      <li>独立权限边界</li>
    </ul>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">内部工作 ① git diff ② 读变更文件 ③ 输出问题清单</span></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">SubAgentStop Hook（可选）</div>
    <ul>
      <li>记录审计日志</li>
      <li>触发 Slack 通知</li>
      <li>检查输出质量</li>
    </ul>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">回传：只回 200 字摘要</span></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">主对话</div>
    <div style="font-family:'SFMono-Regular',Menlo,Consolas,monospace;font-size:12px;color:var(--fg);background:var(--code-bg);padding:8px 10px;border-radius:4px;margin-top:6px">
"code-reviewer 报告：<br>
Critical: 1<br>
Warning: 3<br>
Suggestion: 5<br>
详见子代理完整报告"
    </div>
  </div>

  <div class="flow-container" style="margin-top:18px">
    <div class="flow-container-title">三件套 vs 四特性</div>
    <ul style="margin:4px 0;font-size:13px">
      <li>三件套 = system prompt / 工具 / 上下文（定义）</li>
      <li>四特性 = 隔离 / 约束 / 复用 / 并行（效果）</li>
    </ul>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">子代理 vs 主对话</div>
    <ul style="margin:4px 0;font-size:13px">
      <li>主对话：通用、目的驱动、上下文累积、工具全集</li>
      <li>子代理：专用、任务驱动、上下文隔离、工具子集</li>
    </ul>
  </div>
</div>'''

# -------- lesson-05 --------
REPLACEMENTS["lesson-05.html"] = '''<div class="flow-diagram">
  <div class="flow-actor">
    <div class="flow-actor-label">用户执行</div>
    <div class="flow-actor-desc"><code style="background:transparent;color:#fff">git commit -m "fix: ..."</code></div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">PreToolUse Hook 触发</div>
    <ul>
      <li>匹配工具：<code>Bash</code></li>
      <li>匹配命令：<code>git commit</code></li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">执行 pre-commit-review.sh</div>
    <ul>
      <li><code>git diff --cached</code> — 拿到待提交的 diff</li>
      <li><code>claude --headless --agent code-reviewer</code> — 调起只读子代理审查</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">SubAgent: code-reviewer</div>
    <ul>
      <li>工具：<code>[Read / Grep / Glob / Bash]</code></li>
      <li>只读：无 Edit / Write</li>
      <li>system prompt：三段式</li>
    </ul>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">返回报告 Critical / Warning / Verdict</span></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">Hook 翻译 exit code</div>
    <ul>
      <li><code>REQUEST_CHANGES</code> → exit 2（阻止 commit）</li>
      <li>有 <code>Critical</code> → exit 2（阻止 commit）</li>
      <li>只有 <code>Warning</code> → exit 0（放行，提示）</li>
      <li>全 <code>APPROVE</code> → exit 0（放行）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final">
    <div class="flow-actor-label">git commit 继续 / 中止</div>
  </div>

  <div class="flow-container" style="margin-top:18px">
    <div class="flow-container-title">三段式 system prompt</div>
    <ol style="margin:4px 0;font-size:13px;padding-left:1.4em">
      <li>角色（who you are）</li>
      <li>硬约束（what you must NOT do）</li>
      <li>输出格式（how to report）</li>
    </ol>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">4 个审查场景（各自独立子代理）</div>
    <div class="flow-row flow-row-4" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">通用质量</div><div class="flow-box-sub">default</div></div>
      <div class="flow-box"><div class="flow-box-title">安全审计</div><div class="flow-box-sub">security</div></div>
      <div class="flow-box"><div class="flow-box-title">性能审查</div><div class="flow-box-sub">perf</div></div>
      <div class="flow-box"><div class="flow-box-title">测试覆盖</div><div class="flow-box-sub">coverage</div></div>
    </div>
    <div class="flow-note" style="margin-top:8px">可单独调起，或 4 个一起并行跑</div>
  </div>
</div>'''

# -------- lesson-06 --------
REPLACEMENTS["lesson-06.html"] = '''<div class="flow-diagram">
  <div class="flow-actor">
    <div class="flow-actor-label">用户（主对话）</div>
    <div class="flow-actor-desc">"用 test-runner 跑一下测试"</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">SubAgent: test-runner 启动</div>
    <ul>
      <li>tools: <code>[Bash / Read / Grep]</code></li>
      <li>permission: <code>deny / ask / allow</code></li>
    </ul>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">子代理说：跑 pytest</span></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">Claude Code 权限检查</div>
    <ul>
      <li><code>pytest*</code> → allow 列表 ✅ 放行</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box">
    <div class="flow-box-title">跑 pytest，收集输出</div>
    <div class="flow-box-sub">200 行输出，污染子代理上下文</div>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">回传 3 行摘要</span></div>
  <div class="flow-actor flow-actor-final">
    <div class="flow-actor-label">主对话</div>
    <div class="flow-actor-desc">"Passed: 47 · Failed: 3 · Coverage: 82%"</div>
  </div>

  <div class="flow-container" style="margin-top:18px;border-color:var(--warn-border)">
    <div class="flow-container-title" style="color:var(--warn-border)">如果子代理说：跑 rm -rf /tmp/test</div>
    <div class="flow-box-lg" style="margin-top:6px">
      <div class="flow-box-title" style="color:var(--warn-border)">权限检查 → ❌ 直接拒绝</div>
      <ul>
        <li><code>rm*</code> 匹配 deny 列表</li>
        <li>不询问，立即返回错误</li>
      </ul>
    </div>
    <div class="flow-note" style="margin-top:6px">子代理收到："我没有 rm 权限"</div>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">permission 优先级</div>
    <div style="font-size:13px;font-family:'SFMono-Regular',Menlo,Consolas,monospace">deny &gt; ask &gt; allow</div>
    <div class="flow-note" style="margin-top:2px">一条命令同时匹配时，deny 胜出</div>
  </div>
</div>'''

# -------- lesson-07 --------
REPLACEMENTS["lesson-07.html"] = '''<div class="flow-diagram">
  <div class="flow-actor">
    <div class="flow-actor-label">用户（主对话）</div>
    <div class="flow-actor-desc">"用 pr-drafter 帮我写个 commit message"</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">SubAgent: pr-drafter 启动</div>
    <ul>
      <li>tools: <code>[Bash / Read / Grep / Edit / Write]</code></li>
      <li>permission: ask + 路径白名单</li>
    </ul>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">① git diff --cached</span></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">生成草稿</div>
    <ul>
      <li><code>.claude/drafts/commit-msg.txt</code></li>
      <li><code>.claude/drafts/pr-desc.md</code></li>
    </ul>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">② permission 检查 file_path 匹配 allow</span></div>
  <div class="flow-box">
    <div class="flow-box-title">✅ 放行，用户无需审批</div>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">③ 写入完成</span></div>
  <div class="flow-box">
    <div class="flow-box-title">PostToolUse Hook</div>
    <div class="flow-box-sub">记录到 .claude/audit.log</div>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">④ 子代理返回</span></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">主对话</div>
    <ul>
      <li>"pr-drafter 已生成草稿"</li>
      <li><code>.claude/drafts/commit-msg.txt</code></li>
      <li>请 review 后自己 <code>git commit</code></li>
    </ul>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">用户自己跑 git commit</span></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">PreToolUse Hook 触发</div>
    <ul>
      <li>调 <code>code-reviewer</code> 再 review</li>
      <li><code>REQUEST_CHANGES</code> → exit 2</li>
      <li><code>APPROVE</code> → exit 0</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final">
    <div class="flow-actor-label">commit 成功 / 失败</div>
  </div>

  <div class="flow-container" style="margin-top:18px">
    <div class="flow-container-title">3 道防线叠加</div>
    <ol style="margin:4px 0;font-size:13px;padding-left:1.4em">
      <li>permission ask 机制（逐次审批）</li>
      <li>Audit 日志（可追溯）</li>
      <li>Git Hook（commit 前再 review）</li>
    </ol>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">4 种可写子代理模式</div>
    <div class="flow-row flow-row-2" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">pr-drafter</div><div class="flow-box-sub">写 PR 草稿</div></div>
      <div class="flow-box"><div class="flow-box-title">scaffold-generator</div><div class="flow-box-sub">写新文件，不覆盖</div></div>
      <div class="flow-box"><div class="flow-box-title">doc-writer</div><div class="flow-box-sub">只写 docs/</div></div>
      <div class="flow-box"><div class="flow-box-title">test-writer</div><div class="flow-box-sub">写测试，commit 前 review</div></div>
    </div>
  </div>
</div>'''


# -------- lesson-08 --------
REPLACEMENTS["lesson-08.html"] = '''<div class="flow-diagram">
  <div class="flow-actor">
    <div class="flow-actor-label">用户（主对话）</div>
    <div class="flow-actor-desc">"用 3 个 explorer 同时探索 auth / db / api，综合报告"</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">主对话 · 协调者</div>
    <ul>
      <li>拆任务：3 个互不依赖的探索目标</li>
      <li>派子代理：<code>explorer-auth</code> / <code>-db</code> / <code>-api</code></li>
    </ul>
  </div>
  <div class="flow-arrow-fork"></div>
  <div class="flow-row flow-row-3" style="max-width:620px;width:100%">
    <div class="flow-box">
      <div class="flow-box-title">auth explorer</div>
      <div class="flow-box-sub">01-auth.md</div>
    </div>
    <div class="flow-box">
      <div class="flow-box-title">db explorer</div>
      <div class="flow-box-sub">01-db.md</div>
    </div>
    <div class="flow-box">
      <div class="flow-box-title">api explorer</div>
      <div class="flow-box-sub">01-api.md</div>
    </div>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">各自回传</span></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">主对话 · 综合报告</div>
    <ul>
      <li>共同点（3 个子代理都同意）</li>
      <li>差异点（子代理之间矛盾）</li>
      <li>未覆盖（没有任何子代理探索到）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final">
    <div class="flow-actor-label">用户拿到总览，做决策</div>
  </div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">流水线模式（4 阶段 + 门控）</div>
    <div class="flow-steps" style="margin-top:8px">
      <div class="flow-step">
        <div class="flow-step-num">1</div>
        <div class="flow-step-body">
          <div class="flow-step-title">Explore（找位置）</div>
          <div class="flow-step-desc">输出 <code>01-explore.md</code>。门控：文件存在 + 非空</div>
        </div>
      </div>
      <div class="flow-step">
        <div class="flow-step-num">2</div>
        <div class="flow-step-body">
          <div class="flow-step-title">Reviewer（找问题）</div>
          <div class="flow-step-desc">输出 <code>02-review.md</code>。门控：文件存在 + 非空</div>
        </div>
      </div>
      <div class="flow-step">
        <div class="flow-step-num">3</div>
        <div class="flow-step-body">
          <div class="flow-step-title">Debugger（修）</div>
          <div class="flow-step-desc">输出 <code>03-debug.md</code>。门控：文件存在 + 非空</div>
        </div>
      </div>
      <div class="flow-step">
        <div class="flow-step-num">4</div>
        <div class="flow-step-body">
          <div class="flow-step-title">Test-runner（验）</div>
          <div class="flow-step-desc">输出 <code>04-test.md</code>。门控：测试全过</div>
        </div>
      </div>
    </div>
  </div>
</div>'''

# -------- lesson-09 --------
REPLACEMENTS["lesson-09.html"] = '''<div class="flow-diagram">
  <div class="flow-actor">
    <div class="flow-actor-label">用户新任务</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">选型决策树（4 步）</div>
    <ol style="margin:4px 0;padding-left:1.4em;font-size:13px">
      <li>Q1：改不改状态？</li>
      <li>Q2：输出大不大？</li>
      <li>Q3：可不可并行？</li>
      <li>Q4：要不要审批？</li>
    </ol>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box">
    <div class="flow-box-title">从 8 角色选 1 / 或决定"自定义"</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box">
    <div class="flow-box-title">使用子代理 → 输出</div>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">反馈：子代理好不好用？</span></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">问题诊断 → 调整</div>
    <ul>
      <li>漂移（实际 ≠ 预期）→ 修 system prompt</li>
      <li>太复杂 → 拆分</li>
      <li>太简单 → 合并</li>
      <li>新场景出现 → 自定义</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box">
    <div class="flow-box-title">沉淀到模板库</div>
  </div>
  <div class="flow-arrow-fork"></div>
  <div class="flow-row flow-row-3" style="max-width:520px;width:100%">
    <div class="flow-box"><div class="flow-box-title">入 git</div><div class="flow-box-sub">项目内</div></div>
    <div class="flow-box"><div class="flow-box-title">内部 NPM</div><div class="flow-box-sub">公司内</div></div>
    <div class="flow-box"><div class="flow-box-title">开源 GitHub</div><div class="flow-box-sub">跨公司</div></div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box">
    <div class="flow-box-title">持续运营</div>
    <div class="flow-box-sub">版本管理 + 质量审计 + 使用统计</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final">
    <div class="flow-actor-label">演进路径</div>
    <div class="flow-actor-desc">多模态 / Agent 协议 / MCP 集成</div>
  </div>

  <div class="flow-container" style="margin-top:18px">
    <div class="flow-container-title">8 角色速查</div>
    <ul style="margin:4px 0;font-size:13px">
      <li><strong>只读 3：</strong> code-reviewer / security-auditor / doc-explorer</li>
      <li><strong>可执行 2：</strong> test-runner / diag-runner</li>
      <li><strong>可写 3：</strong> pr-drafter / doc-writer / test-writer</li>
    </ul>
  </div>
</div>'''

# -------- lesson-10 --------
REPLACEMENTS["lesson-10.html"] = '''<div class="flow-diagram">
  <div class="flow-actor">
    <div class="flow-actor-label">Claude Code 启动</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">加载所有 SKILL.md 的 frontmatter</div>
    <div class="flow-box-sub" style="text-align:left">几十行 · 几十到几百 tokens</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box">
    <div class="flow-box-title">用户说话</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">Claude 推理：用户的话匹配哪个 Skill 的 description？</div>
    <ul>
      <li>不匹配 → 继续普通对话</li>
      <li>匹配（如 <code>sync-changelog</code> 描述里有"更新 changelog" / "release notes"）→ 进入下一步</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">加载 SKILL.md 整个正文</div>
    <div class="flow-box-sub" style="text-align:left">几百行 · 几百到几千 tokens</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">Claude 按 3 层结构执行</div>
    <ul>
      <li><strong>第 1 层：快速参考</strong> → 知道先做什么</li>
      <li><strong>第 2 层：详细步骤</strong> → 按操作手册执行</li>
      <li><strong>第 3 层：边界 case</strong> → 遇到坑时兜底</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">按需加载 references/*.md</div>
    <div class="flow-box-sub" style="text-align:left">几千行 · 只在需要时加载</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final">
    <div class="flow-actor-label">完成任务</div>
  </div>

  <div class="flow-container" style="margin-top:18px">
    <div class="flow-container-title">3 层渐进式披露 · token 经济</div>
    <div class="flow-steps" style="margin-top:6px">
      <div class="flow-step">
        <div class="flow-step-num">1</div>
        <div class="flow-step-body">
          <div class="flow-step-title">frontmatter</div>
          <div class="flow-step-desc">50 tokens · 启动时加载</div>
        </div>
      </div>
      <div class="flow-step">
        <div class="flow-step-num">2</div>
        <div class="flow-step-body">
          <div class="flow-step-title">SKILL.md 正文</div>
          <div class="flow-step-desc">500 tokens · 触发时加载</div>
        </div>
      </div>
      <div class="flow-step">
        <div class="flow-step-num">3</div>
        <div class="flow-step-body">
          <div class="flow-step-title">references/</div>
          <div class="flow-step-desc">200 tokens · 按需加载</div>
        </div>
      </div>
    </div>
    <div class="flow-note" style="margin-top:8px">总成本 750 tokens · 对比全量 5000 · 节省 85%</div>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">Skills vs SubAgent vs Commands 触发机制</div>
    <div class="flow-row flow-row-3" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">Command</div><div class="flow-box-sub">用户主动 /test</div></div>
      <div class="flow-box"><div class="flow-box-title">SubAgent</div><div class="flow-box-sub">主对话显式 @code-reviewer</div></div>
      <div class="flow-box"><div class="flow-box-title">Skill</div><div class="flow-box-sub">LLM 自动 · description 匹配</div></div>
    </div>
  </div>
</div>'''

# -------- lesson-11 --------
REPLACEMENTS["lesson-11.html"] = '''<div class="flow-diagram">
  <div class="flow-actor">
    <div class="flow-actor-label">Claude 启动</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">加载所有 Skills 的 frontmatter</div>
  </div>
  <div class="flow-arrow-fork"></div>
  <div class="flow-row flow-row-2" style="max-width:620px;width:100%">
    <div class="flow-box-lg" style="max-width:none">
      <div class="flow-box-title">普通 Skill（description 可见）</div>
      <ul>
        <li>LLM 可见 · 自动匹配</li>
        <li>例：<code>sync-changelog</code> / <code>generate-api-docs</code></li>
      </ul>
    </div>
    <div class="flow-box-lg" style="max-width:none">
      <div class="flow-box-title" style="color:var(--warn-border)">disable-model-invocation: true</div>
      <ul>
        <li>LLM 完全看不到</li>
        <li>例：<code>deploy</code> / <code>rollback</code> / <code>db-migrate</code></li>
      </ul>
    </div>
  </div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">普通 Skill 触发</div>
    <div class="flow-steps" style="margin-top:6px">
      <div class="flow-step">
        <div class="flow-step-num">1</div>
        <div class="flow-step-body"><div class="flow-step-desc">用户："帮我更新 changelog"</div></div>
      </div>
      <div class="flow-step">
        <div class="flow-step-num">2</div>
        <div class="flow-step-body"><div class="flow-step-desc">LLM 匹配到 <code>sync-changelog</code> description</div></div>
      </div>
      <div class="flow-step">
        <div class="flow-step-num">3</div>
        <div class="flow-step-body"><div class="flow-step-desc">加载 SKILL.md → 执行</div></div>
      </div>
    </div>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">disable-model-invocation Skill 触发</div>
    <div class="flow-steps" style="margin-top:6px">
      <div class="flow-step">
        <div class="flow-step-num">1</div>
        <div class="flow-step-body"><div class="flow-step-desc">用户："今天 deploy 顺利吗？"（讨论昨天的事）</div></div>
      </div>
      <div class="flow-step">
        <div class="flow-step-num">2</div>
        <div class="flow-step-body"><div class="flow-step-desc">LLM 看不到 deploy 的 description，不匹配 → 普通对话，不打搅</div></div>
      </div>
      <div class="flow-step">
        <div class="flow-step-num">3</div>
        <div class="flow-step-body"><div class="flow-step-desc">用户：<code>/deploy</code> → 加载 SKILL.md，严格按 6 步走</div></div>
      </div>
    </div>
  </div>

  <div class="flow-container" style="margin-top:14px;border-color:var(--warn-border)">
    <div class="flow-container-title" style="color:var(--warn-border)">双保险（危险操作）</div>
    <ol style="margin:4px 0;padding-left:1.4em;font-size:13px">
      <li><strong>第 1 层：</strong> <code>disable-model-invocation: true</code> → LLM 看不到，自动触发 = 0</li>
      <li><strong>第 2 层：</strong> Hook 拦截危险命令 → 即使有其他路径触发，Hook 兜底</li>
    </ol>
    <div class="flow-note" style="margin-top:4px">两层防御叠加，几乎不可能误执行</div>
  </div>
</div>'''

# -------- lesson-12 --------
REPLACEMENTS["lesson-12.html"] = '''<div class="flow-diagram">
  <div class="flow-actor">
    <div class="flow-actor-label">Claude 启动</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">加载所有 Skills 的 frontmatter（目录页）</div>
    <div class="flow-box-sub" style="text-align:left">50 tokens / Skill · 所有 Skill 全量可见</div>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">用户："分析 Q3 现金流"</span></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">Claude 推理：匹配 <code>financial-analysis</code> description？</div>
    <div class="flow-box-sub" style="text-align:left">看到"分析" / "财务" / "现金流"关键词 → 匹配</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">加载第 2 层：SKILL.md 章节</div>
    <div class="flow-box-sub" style="text-align:left">2K tokens · 200 行内</div>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">扫读：快速参考 + 详细步骤 + 边界 case</span></div>
  <div class="flow-box">
    <div class="flow-box-title">知道要读"现金流章节"</div>
    <div class="flow-box-sub">→ references/cash-flow.md</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">加载第 3 层：references/cash-flow.md</div>
    <div class="flow-box-sub" style="text-align:left">2K tokens · 深度内容</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final">
    <div class="flow-actor-label">完成分析 + 输出报告</div>
    <div class="flow-actor-desc">总成本 4.05K · 对比全量 30K · 节省 86%</div>
  </div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">3 层 vs 1 层 vs 5 层 加载路径对比</div>
    <div class="flow-row flow-row-3" style="margin-top:6px">
      <div class="flow-box-lg" style="max-width:none">
        <div class="flow-box-title">1 层全量</div>
        <ul>
          <li>加载 30K → 找 0.5K → 浪费 29.5K</li>
          <li>加载率 100% / 命中率 1.6%</li>
        </ul>
      </div>
      <div class="flow-box-lg" style="max-width:none;border-color:var(--ok-border)">
        <div class="flow-box-title" style="color:var(--ok-border)">3 层（甜区）</div>
        <ul>
          <li>目录 50 + 章节 2K + 附录 2K = 4.05K</li>
          <li>加载率 13.5% / 命中率 80%</li>
        </ul>
      </div>
      <div class="flow-box-lg" style="max-width:none">
        <div class="flow-box-title">5 层细分</div>
        <ul>
          <li>目录 + summary + main + detail + appendix</li>
          <li>加载率 ~25% / 命中率 60% / 维护成本 4+</li>
        </ul>
      </div>
    </div>
  </div>
</div>'''

# -------- lesson-13 --------
REPLACEMENTS["lesson-13.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">3 件套联动全景图</div>
  <div class="flow-actor">
    <div class="flow-actor-label">用户输入</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">Command 触发</div><div class="flow-box-sub">/review · /release</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">SubAgent 调起</div><div class="flow-box-sub">code-reviewer · deployer</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">Skill 加载</div><div class="flow-box-sub">注入（模式 1）或动态加载（模式 2）</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">Skill 执行</div><div class="flow-box-sub">读文件 · 跑测试 · 部署</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">Skill 输出</div><div class="flow-box-sub">报告 · 状态文件</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">SubAgent 综合</div><div class="flow-box-sub">整合多个 Skill 的输出</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">Command 收尾</div><div class="flow-box-sub">通知 · 写报告</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final">
    <div class="flow-actor-label">返回用户</div>
  </div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">3 种组合模式</div>
    <div class="flow-row flow-row-3" style="margin-top:8px">
      <div class="flow-box-lg" style="max-width:none">
        <div class="flow-box-title">模式 1 · Skills 喂 SubAgent</div>
        <ul>
          <li>system prompt 包含 3 个 Skill 的核心内容</li>
          <li>SubAgent 内化能力</li>
          <li>不动态加载</li>
        </ul>
      </div>
      <div class="flow-box-lg" style="max-width:none">
        <div class="flow-box-title">模式 2 · SubAgent 内部动态加载</div>
        <ul>
          <li>system prompt 小，描述"何时加载哪个 Skill"</li>
          <li>触发 description 匹配 → 加载全文 → 按工作流执行</li>
        </ul>
      </div>
      <div class="flow-box-lg" style="max-width:none">
        <div class="flow-box-title">模式 3 · 流水线组合</div>
        <ul>
          <li>Command 跑流水线 4 步</li>
          <li>各步加载 Skill A / B / C ...</li>
          <li>中间 SubAgent 综合</li>
        </ul>
      </div>
    </div>
    <div class="flow-note" style="margin-top:10px">
      <strong>代码审查专家</strong> = 模式 1（单角色 + 3 维注入）　·　<strong>部署专家</strong> = 模式 2 + 3（多阶段 + 按需 + 流水线）
    </div>
  </div>
</div>'''


# -------- lesson-14 --------
REPLACEMENTS["lesson-14.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">AI Agent 生态定位图（4 层）</div>

  <div class="flow-box-lg" style="max-width:560px">
    <div class="flow-box-title">L4 · 用户层（用对话指挥 AI）</div>
    <div class="flow-box-sub" style="text-align:left">GPTs / Actions（用户主动选功能）</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="max-width:560px;border-color:var(--link)">
    <div class="flow-box-title">L3 · AI 智能层（LLM 推理）</div>
    <ul>
      <li><strong>Claude Code Skills</strong>（LLM 语义推理触发）← 独特位置</li>
      <li>AutoGPT / Skills（任务级触发）</li>
      <li>Semantic Kernel（插件注册）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="max-width:560px">
    <div class="flow-box-title">L2 · 工程能力层（代码层控制）</div>
    <ul>
      <li>SubAgent（主对话显式调起角色）</li>
      <li>LangChain / Tools（代码层显式调用）</li>
      <li>Hook（底层拦截机制）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="max-width:560px">
    <div class="flow-box-title">L1 · 基础设施层（系统）</div>
    <ul>
      <li>Commands（用户主动命令）</li>
      <li>File System / Network / API</li>
    </ul>
  </div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">Claude Code 4 种扩展机制</div>
    <div class="flow-row flow-row-4" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">Commands</div><div class="flow-box-sub">用户层 · /&lt;name&gt;</div></div>
      <div class="flow-box"><div class="flow-box-title">SubAgent</div><div class="flow-box-sub">角色层 · @name</div></div>
      <div class="flow-box"><div class="flow-box-title">Skills</div><div class="flow-box-sub">能力层 · description 匹配</div></div>
      <div class="flow-box"><div class="flow-box-title">Hook</div><div class="flow-box-sub">机制层 · PreToolUse / PostToolUse</div></div>
    </div>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">Skills 3 大独特性</div>
    <ol style="margin:4px 0;padding-left:1.4em;font-size:13px">
      <li>LLM 语义推理触发（无代码注册，纯 description 匹配）</li>
      <li>渐进式披露（3 层加载，token 节省 91%+）</li>
      <li>Markdown 定义（纯文本，git 跟踪，无二进制）</li>
    </ol>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">设计模式四象限（频率 × 风险）</div>
    <div class="flow-quadrant" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">高频低风险</div><div class="flow-box-sub">普通 Skill · LLM 主动发现</div></div>
      <div class="flow-box"><div class="flow-box-title">高频高风险</div><div class="flow-box-sub">普通 Skill + ask 机制</div></div>
      <div class="flow-box"><div class="flow-box-title">低频低风险</div><div class="flow-box-sub">普通 Skill · description 写广</div></div>
      <div class="flow-box" style="border-color:var(--warn-border)"><div class="flow-box-title" style="color:var(--warn-border)">低频高风险</div><div class="flow-box-sub">disable + Hook 双保险</div></div>
    </div>
  </div>
</div>'''

# -------- lesson-15 --------
REPLACEMENTS["lesson-15.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">Skills 出圈时间线 · 125 天从单产品到行业标准</div>

  <div class="flow-timeline">
    <div class="flow-tl-item">
      <div class="flow-tl-date">2024-10</div>
      <div class="flow-step-body">
        <div class="flow-step-title">Anthropic 在 Claude Code 推出 SKILL.md</div>
        <div class="flow-step-desc">纯 Markdown + YAML frontmatter</div>
      </div>
    </div>
    <div class="flow-tl-item">
      <div class="flow-tl-date">2024-11</div>
      <div class="flow-step-body">
        <div class="flow-step-title">OpenAI Codex 采纳 SKILL.md</div>
        <div class="flow-step-desc">正式命名为"Agent Skills" · 第一个跨厂商信号</div>
      </div>
    </div>
    <div class="flow-tl-item">
      <div class="flow-tl-date">2024-12</div>
      <div class="flow-step-body">
        <div class="flow-step-title">Cursor 加入支持</div>
        <div class="flow-step-desc">AI IDE 领域最强扩展需求</div>
      </div>
    </div>
    <div class="flow-tl-item">
      <div class="flow-tl-date">2025-01</div>
      <div class="flow-step-body">
        <div class="flow-step-title">GitHub Copilot 采用</div>
        <div class="flow-step-desc">进入"行业基础设施"层级</div>
      </div>
    </div>
    <div class="flow-tl-item">
      <div class="flow-tl-date">2025-02</div>
      <div class="flow-step-body">
        <div class="flow-step-title">行业形成 Agent Skills 协议（跨平台规范）</div>
        <div class="flow-step-desc">5 个主流 AI Agent 工具共同确认 · 同一份 SKILL.md 5+ 平台通用</div>
      </div>
    </div>
  </div>
  <div class="flow-note" style="margin-top:6px;font-weight:600;color:var(--ok-border)">= 125 天 · 5 个节点 · 行业开放标准诞生</div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">为什么能出圈？3 个根本原因</div>
    <ol style="margin:4px 0;padding-left:1.4em;font-size:13px">
      <li><strong>足够简单：</strong>纯 Markdown · 任何工具读 Markdown + 解析 YAML 即可 · 零集成成本</li>
      <li><strong>足够强大：</strong>description 触发（LLM 智能发现）· 渐进式披露（token 节省 91%+）· Markdown + git</li>
      <li><strong>足够开放：</strong>无专利 · 无 Anthropic 专属 · 竞争对手 OpenAI 都采纳</li>
    </ol>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">未来兼容 SKILL.md 的 5 个最佳实践</div>
    <ol style="margin:4px 0;padding-left:1.4em;font-size:13px">
      <li>description 写"何时触发"不写"做什么"</li>
      <li>章节 200 行内，超过拆 references/</li>
      <li>危险操作加 disable + Hook 双保险</li>
      <li>进 git + 配 PR review</li>
      <li>用纯 Markdown，不混入 JSON / Python / C#</li>
    </ol>
  </div>
</div>'''

# -------- lesson-16 --------
REPLACEMENTS["lesson-16.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">Skills 6 讲全景 · 从"会写"到"会用"到"会选"到"会演化"</div>

  <div class="flow-steps">
    <div class="flow-step">
      <div class="flow-step-num">10</div>
      <div class="flow-step-body">
        <div class="flow-step-title">触类旁通 — 基础结构</div>
      </div>
    </div>
    <div class="flow-step">
      <div class="flow-step-num">11</div>
      <div class="flow-step-body">
        <div class="flow-step-title">令行禁止 — 任务型（disable-model-invocation）</div>
      </div>
    </div>
    <div class="flow-step">
      <div class="flow-step-num">12</div>
      <div class="flow-step-body">
        <div class="flow-step-title">循序渐进 — 渐进披露（3 层）</div>
      </div>
    </div>
    <div class="flow-step">
      <div class="flow-step-num">13</div>
      <div class="flow-step-body">
        <div class="flow-step-title">浑然天成 — 组合（Skills + SubAgent + Commands）</div>
      </div>
    </div>
    <div class="flow-step">
      <div class="flow-step-num">14</div>
      <div class="flow-step-body">
        <div class="flow-step-title">登高望远 — 设计模式四象限</div>
      </div>
    </div>
    <div class="flow-step">
      <div class="flow-step-num">15</div>
      <div class="flow-step-body">
        <div class="flow-step-title">星火燎原 — 行业影响（Agent Skills 协议）</div>
      </div>
    </div>
    <div class="flow-step">
      <div class="flow-step-num">16</div>
      <div class="flow-step-body">
        <div class="flow-step-title">Skills 专题总结（本讲）— 收官</div>
      </div>
    </div>
  </div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">4 种设计模式</div>
    <div class="flow-row flow-row-2" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">模式 1 · 自动发现</div><div class="flow-box-sub">description 匹配 + LLM 触发</div></div>
      <div class="flow-box"><div class="flow-box-title">模式 2 · 任务型</div><div class="flow-box-sub">disable + 用户主动</div></div>
      <div class="flow-box"><div class="flow-box-title">模式 3 · 渐进披露</div><div class="flow-box-sub">3 层加载 + token 经济</div></div>
      <div class="flow-box"><div class="flow-box-title">模式 4 · 组合</div><div class="flow-box-sub">Skills+SubAgent+Commands 联动</div></div>
    </div>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">Skills × Tools × SubAgents 关系</div>
    <div class="flow-row flow-row-3" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">Tools</div><div class="flow-box-sub">原子工具</div></div>
      <div class="flow-box"><div class="flow-box-title">SubAgent</div><div class="flow-box-sub">独立上下文角色</div></div>
      <div class="flow-box"><div class="flow-box-title">Skills</div><div class="flow-box-sub">自动发现能力</div></div>
    </div>
    <ul style="margin-top:8px;font-size:13px">
      <li>SubAgent 调 Tools（角色用工具）</li>
      <li>SubAgent 加载 Skills（角色获得能力）</li>
      <li>Command 触发流水线（Command 调度）</li>
      <li>Skills 喂 SubAgent（Skills 注入 system prompt）</li>
    </ul>
  </div>
</div>'''

# -------- lesson-17 --------
REPLACEMENTS["lesson-17.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">Hooks 事件驱动流程</div>

  <div class="flow-actor"><div class="flow-actor-label">Claude 启动</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">用户说话</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">Claude 推理，决定调起工具</div><div class="flow-box-sub">Bash / Read / Edit / Write 等</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--warn-border)">
    <div class="flow-box-title" style="color:var(--warn-border)">PreToolUse Hook 触发</div>
    <ul>
      <li><code>deny-pipe-exec.sh</code> 拦截 pipe 执行</li>
      <li><code>deny-extra-dangerous.sh</code> 拦截危险</li>
      <li><code>deny-edit-lockfile.sh</code> 拦 lockfile</li>
    </ul>
    <div class="flow-box-sub" style="text-align:left;margin-top:6px">退出码 0 = 放行 · 2 = 拒绝（返回原因给 Claude）</div>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">放行</span></div>
  <div class="flow-box"><div class="flow-box-title">工具实际执行</div><div class="flow-box-sub">Bash / Edit / Write</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">PostToolUse Hook 触发</div>
    <ul>
      <li><code>auto-format.sh</code> 自动格式化</li>
      <li><code>audit-log.sh</code> 记录到 .claude/audit</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">返回结果给 Claude，循环继续</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">Claude 判断任务完成</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--ok-border)">
    <div class="flow-box-title" style="color:var(--ok-border)">Stop Hook 触发</div>
    <ul>
      <li><code>check-uncommitted.sh</code> 检查未提交</li>
      <li><code>check-tests.sh</code> 检查测试通过</li>
    </ul>
    <div class="flow-box-sub" style="text-align:left;margin-top:6px">退出码 0 = 允许停止 · 2 = 强制 Claude 继续</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final"><div class="flow-actor-label">返回用户</div></div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">4 类事件触发时机</div>
    <div class="flow-row flow-row-2" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">PreToolUse</div><div class="flow-box-sub">工具前 · 可拒绝（exit 2）</div></div>
      <div class="flow-box"><div class="flow-box-title">PostToolUse</div><div class="flow-box-sub">工具后 · 可记录/修改</div></div>
      <div class="flow-box"><div class="flow-box-title">Stop</div><div class="flow-box-sub">主代理停止 · 可强制继续</div></div>
      <div class="flow-box"><div class="flow-box-title">SubAgentStop</div><div class="flow-box-sub">子代理停止</div></div>
    </div>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">安全三件套 + 质量三件套</div>
    <div class="flow-row flow-row-2" style="margin-top:6px">
      <div class="flow-box-lg" style="max-width:none;border-color:var(--warn-border)">
        <div class="flow-box-title" style="color:var(--warn-border)">安全三件套</div>
        <ul>
          <li>拦截（PreToolUse 拦危险命令）</li>
          <li>保护（Stop 检查未提交）</li>
          <li>审计（PostToolUse 记录所有）</li>
        </ul>
      </div>
      <div class="flow-box-lg" style="max-width:none;border-color:var(--ok-border)">
        <div class="flow-box-title" style="color:var(--ok-border)">质量三件套</div>
        <ul>
          <li>格式化（PostToolUse 跑 ruff format）</li>
          <li>Lint（PreToolUse 检查 lockfile）</li>
          <li>测试（Stop 检查 pytest 通过）</li>
        </ul>
      </div>
    </div>
  </div>
</div>'''

# -------- lesson-18 --------
REPLACEMENTS["lesson-18.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">Hooks 完整防御链（6 个 Hook 串成）</div>

  <div class="flow-actor"><div class="flow-actor-label">Claude 启动</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">用户说话 → Claude 推理 → 决定调起工具</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--warn-border)">
    <div class="flow-box-title" style="color:var(--warn-border)">① PreToolUse（工具前）</div>
    <ul>
      <li><code>deny-pipe-exec.sh</code> 拦 pipe 执行</li>
      <li><code>deny-extra-dangerous.sh</code> 拦危险</li>
      <li><code>deny-edit-lockfile.sh</code> 拦 lockfile</li>
    </ul>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">放行</span></div>
  <div class="flow-box"><div class="flow-box-title">工具实际执行</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">② PostToolUse（工具后）</div>
    <ul>
      <li><code>auto-format.sh</code> 自动 ruff format</li>
      <li><code>audit-log.sh</code> 记录到 audit log</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">SubAgent 调起（任务隔离）</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--link)">
    <div class="flow-box-title">③ SubAgentStop（子代理停止）</div>
    <ul>
      <li><code>subagent-accept.sh</code> 验收 + 汇总</li>
      <li>① 报告完整性（必填段）</li>
      <li>② 状态文件（必须写）</li>
      <li>③ 输出格式（## 标题）</li>
      <li>④ 汇总到 .claude/state/.../md</li>
      <li>⑤ 通知主对话</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--ok-border)">
    <div class="flow-box-title" style="color:var(--ok-border)">④ Stop（主代理停止）· 4 步质量门控</div>
    <ol style="padding-left:1.2em;font-size:13px">
      <li>未提交检查（强制 commit）</li>
      <li>测试通过（强制修复）</li>
      <li>文档同步（强制 sync）</li>
      <li>审查 checklist 完整</li>
    </ol>
    <div class="flow-box-sub" style="text-align:left;margin-top:4px">退出码 0 = 放行 · 2 = 强制继续</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final"><div class="flow-actor-label">返回用户</div></div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">三维决策框架（什么时候该配 Hook）</div>
    <div class="flow-row flow-row-3" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">性能</div><div class="flow-box-sub">&lt; 1 秒</div></div>
      <div class="flow-box"><div class="flow-box-title">必要性</div><div class="flow-box-sub">真实问题发生过</div></div>
      <div class="flow-box"><div class="flow-box-title">UX</div><div class="flow-box-sub">&lt; 5 次/天 阻断</div></div>
    </div>
    <div class="flow-note" style="margin-top:8px">3 维全通过 = 应该配 · 任 1 维失败 = 不配</div>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">5 条最佳实践</div>
    <ol style="margin:4px 0;padding-left:1.4em;font-size:13px">
      <li>Hook 脚本 &lt; 1 秒</li>
      <li>拒绝要说清原因</li>
      <li>规则要精准</li>
      <li>配置后要测试</li>
      <li>进 git + PR review</li>
    </ol>
  </div>
</div>'''

# -------- lesson-19 --------
REPLACEMENTS["lesson-19.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">MCP 工具调用全流程</div>

  <div class="flow-actor"><div class="flow-actor-label">Claude Code 启动</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">读取 MCP 配置</div>
    <ul>
      <li><code>.mcp.json</code>（项目级）</li>
      <li><code>~/.claude/.mcp.json</code>（全局）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">启动 / 连接 MCP server</div>
    <ul>
      <li>stdio：本地子进程</li>
      <li>HTTP / SSE：远程</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box">
    <div class="flow-box-title">拉所有 server 工具清单</div>
    <div class="flow-box-sub">Claude 看到 mcp__github__create_issue 等</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box">
    <div class="flow-box-title">用户说话 → Claude 推理决定调外部工具</div>
    <div class="flow-box-sub">"创建 GitHub issue: bug #123"</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--link)">
    <div class="flow-box-title">mcp client 构造 JSON-RPC 2.0 请求</div>
    <pre style="font-size:11px;margin:6px 0;padding:8px;background:var(--code-bg);border-radius:4px;color:var(--fg);overflow-x:auto">{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create_issue",
    "arguments": { "repo": "owner/repo", "title": "bug #123", "body": "..." }
  },
  "id": 1
}</pre>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">stdio / HTTP / SSE 传输</span></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">MCP Server</div>
    <ul>
      <li>解析 JSON-RPC 请求</li>
      <li>调 GitHub API（POST /repos/.../issues）</li>
      <li>收到响应，构造 JSON-RPC 响应</li>
    </ul>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">JSON-RPC 响应</span></div>
  <div class="flow-box"><div class="flow-box-title">mcp client 解析，返回给 Claude</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final">
    <div class="flow-actor-label">用户收到："已创建 issue #124"</div>
  </div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">3 种传输方式</div>
    <div class="flow-row flow-row-3" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">stdio</div><div class="flow-box-sub">本地进程 · ~5-10ms · 最快</div></div>
      <div class="flow-box"><div class="flow-box-title">HTTP</div><div class="flow-box-sub">远程 SaaS · ~50-200ms · 跨机器</div></div>
      <div class="flow-box"><div class="flow-box-title">SSE</div><div class="flow-box-sub">流式 · ~50-200ms · 实时长任务</div></div>
    </div>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">4 种扩展机制边界</div>
    <div class="flow-row flow-row-2" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">MCP · 桥梁</div><div class="flow-box-sub">连接外部 API · 标准化协议</div></div>
      <div class="flow-box"><div class="flow-box-title">Skills · 说明书</div><div class="flow-box-sub">LLM 推理触发 · 软规范</div></div>
      <div class="flow-box"><div class="flow-box-title">Hooks · 门卫</div><div class="flow-box-sub">事件驱动拦截 · 硬约束</div></div>
      <div class="flow-box"><div class="flow-box-title">SubAgent · 角色</div><div class="flow-box-sub">独立上下文 · 隔离执行</div></div>
    </div>
  </div>
</div>'''


# -------- lesson-20 --------
REPLACEMENTS["lesson-20.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">Claude Code 工具使用 · 5 类原子操作 + 涌现路径</div>

  <div class="flow-actor">
    <div class="flow-actor-label">用户说话</div>
    <div class="flow-actor-desc">精确意图</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">Claude 推理（选原子操作）</div></div>
  <div class="flow-arrow-fork"></div>
  <div class="flow-row flow-row-auto" style="max-width:680px;width:100%">
    <div class="flow-box">
      <div class="flow-box-title">读</div>
      <div class="flow-box-sub">Read / Glob</div>
    </div>
    <div class="flow-box">
      <div class="flow-box-title">写</div>
      <div class="flow-box-sub">Write / Edit</div>
    </div>
    <div class="flow-box">
      <div class="flow-box-title">搜</div>
      <div class="flow-box-sub">Grep / Glob</div>
    </div>
    <div class="flow-box">
      <div class="flow-box-title">执行</div>
      <div class="flow-box-sub">Bash</div>
    </div>
    <div class="flow-box">
      <div class="flow-box-title">交互</div>
      <div class="flow-box-sub">Ask / WebFetch / WebSearch</div>
    </div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">涌现：组合产生复杂能力</div>
    <ul>
      <li>Read + Edit = 理解 + 修改（代码审查）</li>
      <li>Bash + Grep = 查 + 改（批量重构）</li>
      <li>Write + Bash = 生成 + 执行（写脚本并跑）</li>
      <li>Grep + Read + Edit = 搜 + 读 + 改（多文件修复）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final"><div class="flow-actor-label">完成任务 → 返回用户</div></div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">4 个设计原则</div>
    <div class="flow-row flow-row-2" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">原子性</div><div class="flow-box-sub">每工具只做一件事</div></div>
      <div class="flow-box"><div class="flow-box-title">稳定性</div><div class="flow-box-sub">工具 API 不变</div></div>
      <div class="flow-box"><div class="flow-box-title">LLM 友好</div><div class="flow-box-sub">description 清晰</div></div>
      <div class="flow-box"><div class="flow-box-title">跨任务通用</div><div class="flow-box-sub">工具复用</div></div>
    </div>
    <div class="flow-note" style="margin-top:10px;font-style:normal;color:var(--link);font-weight:600">
      设计哲学：少即是多 · 约束产生创造力 · Unix 哲学的 AI Agent 应用
    </div>
  </div>
</div>'''

# -------- lesson-21 --------
REPLACEMENTS["lesson-21.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">Headless CI/CD 流水线完整流程</div>

  <div class="flow-actor"><div class="flow-actor-label">开发者 push 代码 / 提 PR</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">GitHub Actions 触发</div><div class="flow-box-sub">on: pull_request / push</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">checkout + 配置</div>
    <ul>
      <li>checkout 代码</li>
      <li>setup <code>.claude/</code>（Hook / Skills / SubAgent 配置）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box">
    <div class="flow-box-title">启动 Claude Code（Headless 模式）</div>
    <div class="flow-box-sub">沙箱：Docker 容器（隔离）</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--warn-border)">
    <div class="flow-box-title" style="color:var(--warn-border)">PreToolUse Hook（权限收窄）</div>
    <ul>
      <li><code>ci-allowlist.sh</code> 白名单命令</li>
      <li><code>deny-pipe-exec.sh</code> 拦 pipe</li>
      <li><code>deny-extra-dangerous.sh</code> 拦危险</li>
    </ul>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">白名单内</span></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">Claude 跑任务（PR Review / 自动修复）</div>
    <ul>
      <li>Tools 读 PR diff（Read / Grep / Glob）</li>
      <li>SubAgent 跑代码审查（@code-reviewer）</li>
      <li>MCP 调 GitHub API（读 repo / 写评论）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">PostToolUse Hook（记录审计）</div>
    <ul>
      <li><code>ci-audit-log.sh</code> 记录到 log</li>
      <li><code>ci-stats.sh</code> 统计拦截次数</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--ok-border)">
    <div class="flow-box-title" style="color:var(--ok-border)">Stop Hook（质量门控）</div>
    <ul>
      <li><code>ci-stop-gate.sh</code> 检查质量</li>
      <li><code>ci-tests.sh</code> 跑测试</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">Claude 输出审查结果（JSON）</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final">
    <div class="flow-actor-label">写 PR 评论 / 自动 commit + push</div>
    <div class="flow-actor-desc">workflow 结束 · 日志完整记录</div>
  </div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">5 维权限收窄</div>
    <div class="flow-row flow-row-auto" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">Hook 白名单</div></div>
      <div class="flow-box"><div class="flow-box-title">token scope 收窄</div></div>
      <div class="flow-box"><div class="flow-box-title">Docker 沙箱</div></div>
      <div class="flow-box"><div class="flow-box-title">失败 fallback</div></div>
      <div class="flow-box"><div class="flow-box-title">日志完整</div></div>
    </div>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">Headless vs 交互式</div>
    <div class="flow-row flow-row-2" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">交互式</div><div class="flow-box-sub">人在回路 · 开发用</div></div>
      <div class="flow-box"><div class="flow-box-title">Headless</div><div class="flow-box-sub">人不在 · CI 用</div></div>
    </div>
    <div class="flow-note" style="margin-top:8px">5 种扩展机制（Tools / Skills / SubAgent / Hooks / MCP）在 Headless 下仍可用，区别只在"有没有人确认"</div>
  </div>
</div>'''

# -------- lesson-22 --------
REPLACEMENTS["lesson-22.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">Rules × 5 种扩展机制完整图景（6 层工作流）</div>

  <div class="flow-actor">
    <div class="flow-actor-label">用户说话</div>
    <div class="flow-actor-desc">意图："改 src/api/users.py"</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--link)">
    <div class="flow-box-title">① Rules 层（软规范 + 硬权限）</div>
    <ul>
      <li>路径匹配 <code>src/**/*.py</code></li>
      <li>加载 <code>.claude/rules/python-style.md</code></li>
      <li><code>permissions</code> 字段：deny / ask / allow</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box">
    <div class="flow-box-title">Claude 推理（遵守软规范）</div>
    <div class="flow-box-sub">type hints / 写测试 / ruff format</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">② Tools 层（原子操作）</div>
    <ul>
      <li><code>Read</code> src/api/users.py</li>
      <li><code>Edit</code> 改代码</li>
      <li><code>Bash</code> pytest / ruff</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--warn-border)">
    <div class="flow-box-title" style="color:var(--warn-border)">③ PreToolUse Hook（硬约束拦截）</div>
    <ul>
      <li>权限检查（deny / ask / allow）</li>
      <li>白名单命令检查</li>
      <li>危险命令拦截</li>
    </ul>
  </div>
  <div class="flow-arrow"><span class="flow-arrow-label">放行</span></div>
  <div class="flow-box"><div class="flow-box-title">工具执行</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">④ PostToolUse Hook（记录审计）</div>
    <ul>
      <li>audit-log 记录命令</li>
      <li>auto-format 自动格式化</li>
      <li>触发 Skills 自动发现</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">⑤ SubAgent 调起（复杂任务隔离）</div>
    <div class="flow-box-sub" style="text-align:left">@code-reviewer 跑代码审查，独立上下文，完成报告</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">⑥ Skills 触发（软规范能力）</div>
    <div class="flow-box-sub" style="text-align:left">自动发现 commit-skill · 用 conventional commits 规范</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">⑦ MCP 调用（连接外部世界）</div>
    <div class="flow-box-sub" style="text-align:left"><code>mcp__github__create_pr</code> 自动化创建 PR</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--ok-border)">
    <div class="flow-box-title" style="color:var(--ok-border)">⑧ Stop Hook（质量门控）</div>
    <ul>
      <li>check-uncommitted</li>
      <li>check-tests</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final"><div class="flow-actor-label">返回用户</div></div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">6 种扩展机制工作层次</div>
    <div class="flow-row flow-row-3" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">Rules</div><div class="flow-box-sub">宪法层（最顶）</div></div>
      <div class="flow-box"><div class="flow-box-title">Skills</div><div class="flow-box-sub">招式层（LLM）</div></div>
      <div class="flow-box"><div class="flow-box-title">Hooks</div><div class="flow-box-sub">门卫层（事件）</div></div>
      <div class="flow-box"><div class="flow-box-title">MCP</div><div class="flow-box-sub">桥梁层（外部）</div></div>
      <div class="flow-box"><div class="flow-box-title">SubAgent</div><div class="flow-box-sub">角色层（隔离）</div></div>
      <div class="flow-box"><div class="flow-box-title">Tools</div><div class="flow-box-sub">内功层（原子）</div></div>
    </div>
    <div class="flow-note" style="margin-top:10px"><strong>Rules 软规范</strong>（<code>.claude/rules/*.md</code>） + <strong>硬权限</strong>（<code>permissions</code> 字段）= 两层防御</div>
  </div>
</div>'''

# -------- lesson-23 --------
REPLACEMENTS["lesson-23.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">Agent SDK 调用流程</div>

  <div class="flow-actor">
    <div class="flow-actor-label">应用代码</div>
    <div class="flow-actor-desc">Flask / CLI / pipeline</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">query(prompt, options)</div>
    <ul>
      <li><code>prompt</code> — 任务描述</li>
      <li><code>options</code> — ClaudeCodeOptions 11 字段</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">SDK 启动 Claude Code 子进程</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">Claude Code 加载配置</div>
    <ul>
      <li><code>.claude/settings.json</code></li>
      <li><code>.claude/skills/</code></li>
      <li><code>.claude/agents/</code></li>
      <li><code>.mcp.json</code>（MCP servers）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">Claude 推理</div>
    <ul>
      <li>收到 prompt</li>
      <li>调工具（<code>allowed_tools</code> 限制）</li>
      <li>输出消息</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--link)">
    <div class="flow-box-title">返回 stream（4 类消息）</div>
    <ul>
      <li><strong>AssistantMessage</strong> — Claude 的回复（文本/工具调用）</li>
      <li><strong>UserMessage</strong> — 工具结果</li>
      <li><strong>SystemMessage</strong> — 系统事件</li>
      <li><strong>ResultMessage</strong> — 任务结果 + 元数据（cost / turns / duration）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">应用代码处理消息</div>
    <ul>
      <li>AssistantMessage → 累积输出 / 实时打印</li>
      <li>UserMessage → 调试打印</li>
      <li>SystemMessage → 调试打印</li>
      <li>ResultMessage → 提取费用 / 轮次，上报监控</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final">
    <div class="flow-actor-label">应用返回结果</div>
    <div class="flow-actor-desc">HTTP 响应 / CLI 输出 / 数据库写入</div>
  </div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">SDK vs MCP vs Headless</div>
    <div class="flow-row flow-row-3" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">SDK</div><div class="flow-box-sub">调用者侧（query Claude）</div></div>
      <div class="flow-box"><div class="flow-box-title">MCP</div><div class="flow-box-sub">工具提供侧（server）</div></div>
      <div class="flow-box"><div class="flow-box-title">Headless</div><div class="flow-box-sub">进程级一次性 CLI</div></div>
    </div>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">11 个配置项</div>
    <div class="flow-row flow-row-auto" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-sub">allowed_tools</div></div>
      <div class="flow-box"><div class="flow-box-sub">system_prompt</div></div>
      <div class="flow-box"><div class="flow-box-sub">cwd</div></div>
      <div class="flow-box"><div class="flow-box-sub">mcp_servers</div></div>
      <div class="flow-box"><div class="flow-box-sub">max_turns</div></div>
      <div class="flow-box"><div class="flow-box-sub">permission_mode</div></div>
      <div class="flow-box"><div class="flow-box-sub">model</div></div>
      <div class="flow-box"><div class="flow-box-sub">resume</div></div>
      <div class="flow-box"><div class="flow-box-sub">extra_args</div></div>
      <div class="flow-box"><div class="flow-box-sub">settings</div></div>
      <div class="flow-box"><div class="flow-box-sub">env</div></div>
    </div>
  </div>
</div>'''

# -------- lesson-24 --------
REPLACEMENTS["lesson-24.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">Agent SDK 高级应用完整图景</div>

  <div class="flow-actor">
    <div class="flow-actor-label">应用代码</div>
    <div class="flow-actor-desc">Flask / CLI / pipeline</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--link)">
    <div class="flow-box-title">SDK 启动 · 加载 .claude/ 配置</div>
    <ul>
      <li><code>rules/</code>（软规范）</li>
      <li><code>skills/</code>（本地能力）</li>
      <li><code>agents/</code>（SubAgent）</li>
      <li><code>settings.json</code>（Hooks + permissions）</li>
      <li><code>.mcp.json</code>（MCP server）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">Claude 推理（主 Agent）</div>
    <ul>
      <li>调自定义工具（<code>@tool</code> 装饰器）：get_user / send_email / ...</li>
      <li>调 SubAgent：@code-reviewer / @test-runner / @linter</li>
      <li>调 MCP server：<code>mcp__github__create_issue</code> · in-process SDK MCP server</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">流式返回消息</div>
    <div class="flow-box-sub" style="text-align:left">Assistant · User · System · Result (cost / turns / session_id)</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--warn-border)">
    <div class="flow-box-title" style="color:var(--warn-border)">错误处理（3 层）</div>
    <ol style="padding-left:1.2em;font-size:13px">
      <li>try / except 捕获 4 种异常</li>
      <li>指数退避重试（≤ 3 次）</li>
      <li>fallback 降级（简单规则）</li>
    </ol>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">主 Agent 汇总 SubAgent 报告</div>
    <ul>
      <li>code-reviewer 报告</li>
      <li>test-runner 报告</li>
      <li>linter 报告</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final"><div class="flow-actor-label">返回应用</div></div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">自动化测试修复 Agent · 4 层权限管理</div>
    <div class="flow-steps" style="margin-top:6px">
      <div class="flow-step">
        <div class="flow-step-num">1</div>
        <div class="flow-step-body">
          <div class="flow-step-title">只读分析（plan 模式）</div>
          <div class="flow-step-desc"><code>allowed_tools = Read / Grep / Glob / Bash(pytest)</code> · 阶段 1：分析失败原因</div>
        </div>
      </div>
      <div class="flow-step">
        <div class="flow-step-num">2</div>
        <div class="flow-step-body">
          <div class="flow-step-title">编辑修复（acceptEdits 模式）</div>
          <div class="flow-step-desc">+ Edit / Write · 阶段 2：改代码 + 验证</div>
        </div>
      </div>
      <div class="flow-step">
        <div class="flow-step-num">3</div>
        <div class="flow-step-body">
          <div class="flow-step-title">Hook 拦截（PreToolUse）</div>
          <div class="flow-step-desc">deny-pipe-exec / deny-extra-dangerous · 危险命令根本跑不出来</div>
        </div>
      </div>
      <div class="flow-step">
        <div class="flow-step-num">4</div>
        <div class="flow-step-body">
          <div class="flow-step-title">审计日志（PostToolUse）</div>
          <div class="flow-step-desc">audit-log 记录所有 Edit / Write · 出事后可追溯</div>
        </div>
      </div>
    </div>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">in-process MCP vs stdio MCP</div>
    <div class="flow-row flow-row-2" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">in-process</div><div class="flow-box-sub">进程内调用 · 启动快 · 易调试</div></div>
      <div class="flow-box"><div class="flow-box-title">stdio</div><div class="flow-box-sub">跨进程 · 跨语言 · 跨机器</div></div>
    </div>
  </div>
</div>'''

# -------- lesson-25 --------
REPLACEMENTS["lesson-25.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">Plugin 完整生命周期</div>

  <div class="flow-actor"><div class="flow-actor-label">Plugin 作者</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">写 plugin（.claude-plugin/ 根 + 5 子目录）</div>
    <ul>
      <li><code>plugin.json</code> — manifest（必填）</li>
      <li><code>skills/</code> — Skill 文件</li>
      <li><code>agents/</code> — SubAgent 文件</li>
      <li><code>commands/</code> — Command 文件</li>
      <li><code>hooks/</code> — Hook 脚本</li>
      <li><code>.mcp.json</code> — MCP server 配置</li>
      <li><code>README.md</code> — 用法说明</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">本地测试</div><div class="flow-box-sub">claude plugin install .</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">配版本号（semver: 1.0.0）+ 推到 git</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box"><div class="flow-box-title">claude plugin login → publish</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--link)">
    <div class="flow-box-title">Marketplace（5 种类型）</div>
    <ul>
      <li>GitHub 仓库</li>
      <li>公司内部 registry</li>
      <li>Anthropic 官方 marketplace</li>
      <li>第三方平台</li>
      <li>本地文件</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box">
    <div class="flow-box-title">用户安装</div>
    <div class="flow-box-sub">claude plugin install code-review-suite</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">Claude Code 加载 plugin</div>
    <ul>
      <li>skills/ → .claude/skills/</li>
      <li>agents/ → .claude/agents/</li>
      <li>commands/ → .claude/commands/</li>
      <li>hooks/ → .claude/settings.json hooks</li>
      <li>.mcp.json → .mcp.json</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">团队使用</div>
    <ul>
      <li>@code-reviewer 审查代码</li>
      <li>Skill 自动发现</li>
      <li>Hook 拦截 / 记录</li>
      <li>MCP 调外部 API</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final">
    <div class="flow-actor-label">更新 / 卸载</div>
    <div class="flow-actor-desc">claude plugin update · uninstall</div>
  </div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">Plugin vs 散装配置</div>
    <div class="flow-row flow-row-2" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">Plugin</div><div class="flow-box-sub">团队通用能力（2+ 项目）</div></div>
      <div class="flow-box"><div class="flow-box-title">散装</div><div class="flow-box-sub">项目专属配置（本项目用）</div></div>
    </div>
    <div class="flow-note" style="margin-top:8px">边界：通用 → Plugin · 专属 → 散装</div>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">Plugin 之于 Claude Code，类似…</div>
    <div class="flow-row flow-row-3" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">Plugin</div><div class="flow-box-sub">之于 Claude Code</div></div>
      <div class="flow-box"><div class="flow-box-title">npm 包</div><div class="flow-box-sub">之于 Node.js</div></div>
      <div class="flow-box"><div class="flow-box-title">pip 包</div><div class="flow-box-sub">之于 Python</div></div>
    </div>
    <div class="flow-note" style="margin-top:8px">同样的"包"概念，不同生态</div>
  </div>
</div>'''


# -------- lesson-26 --------
REPLACEMENTS["lesson-26.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">Claude Code 工程化全景图</div>

  <div class="flow-actor"><div class="flow-actor-label">用户</div></div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--link)">
    <div class="flow-box-title">层 1 · 交互层</div>
    <ul>
      <li>REPL 交互式</li>
      <li>Headless（<code>claude -p</code>）</li>
      <li>Agent SDK（<code>query()</code>）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--link)">
    <div class="flow-box-title">层 2 · 能力层</div>
    <ul>
      <li>Skills（本地能力）</li>
      <li>SubAgent（隔离角色）</li>
      <li>Tools（原子操作）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--link)">
    <div class="flow-box-title">层 3 · 协控层</div>
    <ul>
      <li>Hooks（事件拦截）</li>
      <li>Rules（软规范）</li>
      <li>permissions（权限）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--link)">
    <div class="flow-box-title">层 4 · 扩展层</div>
    <ul>
      <li>MCP（外部 API）</li>
      <li>Plugins（打包分发）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final">
    <div class="flow-actor-label">企业级应用</div>
    <div class="flow-actor-desc">工具化 → 流程化 → 平台化</div>
  </div>

  <div class="flow-container" style="margin-top:22px">
    <div class="flow-container-title">学习路径（4 阶段）</div>
    <div class="flow-row flow-row-4" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">阶段 1 · 基础</div><div class="flow-box-sub">第 1-3 讲</div></div>
      <div class="flow-box"><div class="flow-box-title">阶段 2 · 扩展</div><div class="flow-box-sub">第 4-18 讲</div></div>
      <div class="flow-box"><div class="flow-box-title">阶段 3 · 集成</div><div class="flow-box-sub">第 19-24 讲</div></div>
      <div class="flow-box"><div class="flow-box-title">阶段 4 · 分发</div><div class="flow-box-sub">第 25-33 讲</div></div>
    </div>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">6 机制一句话总结</div>
    <ul style="margin:4px 0;font-size:13px">
      <li><strong>Skills</strong> = 告诉 Claude 怎么做</li>
      <li><strong>SubAgent</strong> = 隔离上下文</li>
      <li><strong>Hooks</strong> = 事件拦截</li>
      <li><strong>MCP</strong> = 外部 API 桥</li>
      <li><strong>Rules</strong> = 软规范</li>
      <li><strong>Plugins</strong> = 打包分发</li>
    </ul>
  </div>

  <div class="flow-container" style="margin-top:14px">
    <div class="flow-container-title">2 落地路径</div>
    <div class="flow-row flow-row-2" style="margin-top:6px">
      <div class="flow-box"><div class="flow-box-title">自上而下</div><div class="flow-box-sub">大企业 / 传统行业</div></div>
      <div class="flow-box"><div class="flow-box-title">自下而上</div><div class="flow-box-sub">互联网 / 技术驱动</div></div>
    </div>
    <div class="flow-note" style="margin-top:8px">推荐：自下而上起步，自上而下加速</div>
  </div>
</div>'''

# -------- lesson-27 --------
REPLACEMENTS["lesson-27.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">🔑 4 大共通设计密码</div>

  <div class="flow-steps">
    <div class="flow-step">
      <div class="flow-step-num">1</div>
      <div class="flow-step-body">
        <div class="flow-step-title">Harness 包裹一切</div>
        <div class="flow-step-desc">模型只是心脏，Harness 才是身体 → 课程第 28 讲专讲</div>
      </div>
    </div>
    <div class="flow-step">
      <div class="flow-step-num">2</div>
      <div class="flow-step-body">
        <div class="flow-step-title">Channel 抽象输入</div>
        <div class="flow-step-desc">CLI / IDE / IM / Web 都走同一接口 → 用户从哪问，Agent 都答得上来</div>
      </div>
    </div>
    <div class="flow-step">
      <div class="flow-step-num">3</div>
      <div class="flow-step-body">
        <div class="flow-step-title">Skills 按需加载</div>
        <div class="flow-step-desc">全量加载 = 烧 Token · 按 description 触发 = 渐进式披露 → 课程第 12 讲专讲</div>
      </div>
    </div>
    <div class="flow-step">
      <div class="flow-step-num">4</div>
      <div class="flow-step-body">
        <div class="flow-step-title">SubAgent 隔离上下文</div>
        <div class="flow-step-desc">大任务 = 多 Agent 协作 → 课程第 4-9 讲专讲</div>
      </div>
    </div>
  </div>

  <div class="flow-container" style="margin-top:22px;border-color:var(--ok-border)">
    <div class="flow-container-title" style="color:var(--ok-border)">总结</div>
    <div class="flow-note" style="font-style:normal;color:var(--fg);font-size:14px;margin:0">
      4 个密码 = 4 个范式 · 组合起来 = 完整的 Agent 工程实践
    </div>
  </div>
</div>'''

# -------- lesson-28 --------
REPLACEMENTS["lesson-28.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">🏗️ Harness 7 层架构</div>

  <div class="flow-box-lg" style="max-width:560px">
    <div class="flow-box-title">L7 · User Interface</div>
    <div class="flow-box-sub" style="text-align:left">CLI / TUI / Web / IDE / IM</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="max-width:560px">
    <div class="flow-box-title">L6 · Channel Adapter</div>
    <div class="flow-box-sub" style="text-align:left">把消息标准化成 Agent 能理解的格式（Telegram / Slack / WebSocket / stdio）</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="max-width:560px;border-color:var(--link)">
    <div class="flow-box-title">L5 · Orchestrator</div>
    <div class="flow-box-sub" style="text-align:left">主循环 + 子代理调度 · 决定"这一步调哪个 Agent"</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="max-width:560px">
    <div class="flow-box-title">L4 · Memory Store</div>
    <div class="flow-box-sub" style="text-align:left">短期消息历史 · CLAUDE.md / 长期记忆</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="max-width:560px">
    <div class="flow-box-title">L3 · Tool Layer</div>
    <div class="flow-box-sub" style="text-align:left">Bash / Read / Edit / Grep / MCP（含权限 + 风险等级）</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="max-width:560px;border-color:var(--warn-border)">
    <div class="flow-box-title" style="color:var(--warn-border)">L2 · Boundary & Hooks</div>
    <ul>
      <li>PreToolUse 拦截</li>
      <li>PostToolUse 审计</li>
      <li>Stop 收尾</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="max-width:560px">
    <div class="flow-box-title">L1 · Model Adapter</div>
    <div class="flow-box-sub" style="text-align:left">Opus / Sonnet / Haiku 抽象 · 流式输出 + retry + fallback</div>
  </div>

  <div class="flow-container" style="margin-top:22px;border-color:var(--ok-border)">
    <div class="flow-container-title" style="color:var(--ok-border)">总结</div>
    <div class="flow-note" style="font-style:normal;color:var(--fg);font-size:14px;margin:0">
      上面 7 层 = 一个完整的 Harness · Claude Code / OpenClaw / OpenCode 都是这样
    </div>
  </div>
</div>'''

# -------- lesson-30 --------
REPLACEMENTS["lesson-30.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">🚀 团队落地 4 阶段路线图</div>

  <div class="flow-timeline">
    <div class="flow-tl-item">
      <div class="flow-tl-date">Month 0<br>Week 1</div>
      <div class="flow-step-body">
        <div class="flow-step-title">单人探索</div>
        <ul style="margin:4px 0;padding-left:1.4em;font-size:13px">
          <li>1 个工程师跑通</li>
          <li>选 1 个真实项目做试点</li>
          <li>写 1 份种子报告</li>
        </ul>
        <div class="flow-note" style="margin-top:4px;font-style:normal;color:var(--ok-border)">退出标准：1 人能日常用 + 1 份 ROI 种子报告</div>
      </div>
    </div>
    <div class="flow-tl-item">
      <div class="flow-tl-date">Month 1<br>Week 2-4</div>
      <div class="flow-step-body">
        <div class="flow-step-title">Skills 库建设</div>
        <ul style="margin:4px 0;padding-left:1.4em;font-size:13px">
          <li>5 人小组共建团队 Skills 库</li>
          <li>团队 CLAUDE.md 模板</li>
          <li>Onboarding 5-20 人</li>
        </ul>
        <div class="flow-note" style="margin-top:4px;font-style:normal;color:var(--ok-border)">退出标准：团队 Skills 库 5+ 个 + 20+ 人能用</div>
      </div>
    </div>
    <div class="flow-tl-item">
      <div class="flow-tl-date">Month 2-3</div>
      <div class="flow-step-body">
        <div class="flow-step-title">Plugins 共享</div>
        <ul style="margin:4px 0;padding-left:1.4em;font-size:13px">
          <li>封装 Plugin 推 3 跨团队</li>
          <li>建内部 Marketplace</li>
          <li>Champion + Steward 双角色</li>
        </ul>
        <div class="flow-note" style="margin-top:4px;font-style:normal;color:var(--ok-border)">退出标准：3 跨团队 + 内部 Marketplace 上线</div>
      </div>
    </div>
    <div class="flow-tl-item">
      <div class="flow-tl-date">Month 4-6</div>
      <div class="flow-step-body">
        <div class="flow-step-title">CI/CD 集成</div>
        <ul style="margin:4px 0;padding-left:1.4em;font-size:13px">
          <li>Headless 模式集成 GitHub Actions</li>
          <li>5 维权限收窄</li>
          <li>Platform Team 3-5 人承接</li>
        </ul>
        <div class="flow-note" style="margin-top:4px;font-style:normal;color:var(--ok-border)">退出标准：80% PR 自动过审查 + 零事故</div>
      </div>
    </div>
  </div>
</div>'''

# -------- lesson-31 --------
REPLACEMENTS["lesson-31.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">🚀 性能调优剧本 · 5 步法</div>

  <div class="flow-steps">
    <div class="flow-step">
      <div class="flow-step-num">1</div>
      <div class="flow-step-body">
        <div class="flow-step-title">摸清现状</div>
        <div class="flow-step-desc">跑 <code>.claude/hooks/log-usage.sh</code> 一周 → 看到底哪些任务在烧钱</div>
      </div>
    </div>
    <div class="flow-step">
      <div class="flow-step-num">2</div>
      <div class="flow-step-body">
        <div class="flow-step-title">锁定大头</div>
        <div class="flow-step-desc">找出 Token 消耗 Top 3 的任务类型 → 通常是"长链路 refactor"和"全仓 review"</div>
      </div>
    </div>
    <div class="flow-step">
      <div class="flow-step-num">3</div>
      <div class="flow-step-body">
        <div class="flow-step-title">拆分模型</div>
        <div class="flow-step-desc">把 lint / format / 单测改用 <code>haiku</code> 子代理；架构 / 重构保留 <code>opus</code> → 预期降本 40%</div>
      </div>
    </div>
    <div class="flow-step">
      <div class="flow-step-num">4</div>
      <div class="flow-step-body">
        <div class="flow-step-title">改造上下文</div>
        <div class="flow-step-desc">长任务拆成多个短会话；中间用 CLAUDE.md 衔接；强制每 40 轮提醒 <code>/compact</code> → 预期再降本 20%</div>
      </div>
    </div>
    <div class="flow-step">
      <div class="flow-step-num">5</div>
      <div class="flow-step-body">
        <div class="flow-step-title">建立基线</div>
        <ul style="margin:4px 0;padding-left:1.4em;font-size:13px">
          <li>单任务 &gt; 50k token 必须拆分</li>
          <li>工具调用 &gt; 100 次必须分阶段</li>
          <li>同一文件 3 次未改对必须 <code>/rewind</code></li>
        </ul>
        <div class="flow-note" style="margin-top:4px">把优化沉淀为团队约定</div>
      </div>
    </div>
  </div>
</div>'''

# -------- lesson-33 --------
REPLACEMENTS["lesson-33.html"] = '''<div class="flow-diagram">
  <div class="flow-note" style="font-size:14px;font-weight:600;color:var(--link);font-style:normal;margin-bottom:10px">🏗️ PR 审查 Agent · 整体架构</div>

  <div class="flow-actor">
    <div class="flow-actor-label">⬆️ GitHub PR</div>
    <div class="flow-actor-desc">📥 webhook</div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">对接层</div>
    <ul>
      <li>GitHub MCP（读 PR / 写评论）</li>
      <li>Agent SDK（在 CI 里驱动主 Agent）</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--link)">
    <div class="flow-box-title">编排层 · 主 Agent（opus）</div>
    <ul>
      <li>读 PR diff</li>
      <li>调用 4 个子代理并行审查</li>
      <li>汇总 + 写评论</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg">
    <div class="flow-box-title">能力层 · 4 个 SubAgent 并行</div>
    <div class="flow-row flow-row-2" style="margin-top:8px">
      <div class="flow-box"><div class="flow-box-title">LintSubAgent</div><div class="flow-box-sub">haiku</div></div>
      <div class="flow-box"><div class="flow-box-title">TestSubAgent</div><div class="flow-box-sub">sonnet</div></div>
      <div class="flow-box"><div class="flow-box-title">SecuritySubAgent</div><div class="flow-box-sub">sonnet</div></div>
      <div class="flow-box"><div class="flow-box-title">StyleSubAgent</div><div class="flow-box-sub">haiku</div></div>
    </div>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-box-lg" style="border-color:var(--warn-border)">
    <div class="flow-box-title" style="color:var(--warn-border)">Hooks · 横切</div>
    <ul>
      <li>PreToolUse：PII 脱敏 + 权限检查</li>
      <li>PostToolUse：审计日志</li>
      <li>Stop：用量统计 + 告警</li>
    </ul>
  </div>
  <div class="flow-arrow"></div>
  <div class="flow-actor flow-actor-final">
    <div class="flow-actor-label">回写 PR 评论</div>
    <div class="flow-actor-desc">GitHub Comment API</div>
  </div>
</div>'''


def main():
    only = set(sys.argv[1:])  # 可选：只处理指定文件
    for name, new_html in REPLACEMENTS.items():
        if only and name not in only:
            continue
        path = ROOT / name
        if not path.exists():
            print(f"MISS {name}")
            continue
        src = path.read_text(encoding="utf-8")
        new, n = PRE_RE.subn(new_html, src, count=1)
        if n == 0:
            print(f"SKIP {name} (no <pre class='lang-flow'> block — already converted?)")
        else:
            path.write_text(new, encoding="utf-8")
            print(f"OK   {name}")


if __name__ == "__main__":
    main()
