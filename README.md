# PM Agent - AI 产品经理助手

基于 Anthropic 的 Product Management Plugin 转换的 KimiCode Agent。

## 核心能力

PM Agent 涵盖完整的 PM 工作流程：

### 1. Write Spec（撰写需求文档）
将想法转化为结构化的 PRD，包含：
- 问题陈述、目标、非目标
- 用户故事（按优先级排序）
- 需求分类（P0/P1/P2）
- 成功指标（领先和滞后指标）
- 待解决问题和时间线

**使用**: "帮我写 SSO 功能的 PRD"

### 2. Roadmap Update（路线图更新）
创建和更新产品路线图：
- Now/Next/Later 格式
- 季度主题
- OKR 对齐视图
- 优先级框架（RICE、MoSCoW、ICE）
- 依赖映射

**使用**: "更新下季度路线图"

### 3. Stakeholder Update（利益相关者更新）
针对不同受众定制状态更新：
- 高管层（战略、简洁）
- 工程团队（技术细节、阻塞）
- 跨职能伙伴（依赖、需求）
- 客户（收益导向）

**使用**: "写个给高管的周度更新"

### 4. Synthesize Research（综合研究）
将用户研究转化为结构化洞察：
- 主题分析
- 用户画像开发
- 机会领域识别
- 可操作的建议

**使用**: "整理这 10 份访谈笔记"

### 5. Competitive Brief（竞品分析）
创建全面的竞品分析：
- 功能对比矩阵
- 定位分析
- 优势和劣势
- 战略影响和建议

**使用**: "分析竞争对手 X 和 Y"

### 6. Metrics Review（指标审查）
分析产品指标并识别趋势：
- 指标层次结构（North Star + L1 + L2）
- 趋势分析
- 亮点和关注领域
- 可执行的建议

**使用**: "审查本月的产品指标"

### 7. Brainstorm（头脑风暴）
作为思考伙伴：
- 问题探索
- 解决方案构思
- 假设测试
- 战略探索
- 使用 HMW、JTBD、Opportunity Solution Trees 等框架

**使用**: "和我一起头脑风暴如何提高留存"

### 8. Sprint Planning（迭代规划）
规划敏捷迭代：
- 容量计算
- 待办事项优先级
- 风险识别
- 迭代目标设定

**使用**: "规划下两周的迭代"

## 安装和使用

### 1. 配置 Agent

将 `agents.md` 的内容复制到 KimiCode 的 Agent 配置中。

### 2. 使用 Agent

直接在对话中下达任务：

```
帮我写 [功能名] 的 PRD
更新产品路线图
综合这些用户访谈
分析 [竞品名]
审查本月指标
一起头脑风暴 [主题]
```

### 3. 查看产出

所有产出都保存在 `wiki/` 目录下：
- PRDs → `wiki/specs/`
- 路线图 → `wiki/roadmaps/`
- 研究综合 → `wiki/research/`
- 竞品分析 → `wiki/competitive/`
- 指标报告 → `wiki/metrics/`
- 利益相关者更新 → `wiki/updates/`
- 头脑风暴 → `wiki/ideas/`
- 迭代规划 → `wiki/sprints/`

## 目录结构

```
pm-agent/
├── agents.md              # Agent 配置文件（核心）
├── README.md              # 本文件
├── prompts/               # 详细 Prompt 模板
│   ├── write-spec.md
│   ├── roadmap-update.md
│   ├── stakeholder-update.md
│   ├── synthesize-research.md
│   ├── competitive-brief.md
│   ├── metrics-review.md
│   └── brainstorm.md
├── templates/             # 输出模板
│   ├── prd.md
│   ├── roadmap.md
│   ├── stakeholder-update.md
│   ├── research-synthesis.md
│   ├── competitive-brief.md
│   └── metrics-review.md
├── wiki/                  # 知识库（自动填充）
│   ├── index.md
│   ├── log.md
│   ├── specs/
│   ├── roadmaps/
│   ├── research/
│   ├── competitive/
│   ├── metrics/
│   ├── updates/
│   ├── ideas/
│   └── sprints/
└── raw/                   # 原始资料
```

## 工作流程示例

### 示例 1: 撰写 PRD

**你**: "帮我写 SSO 功能的 PRD"

**Agent**:
1. 询问目标用户、成功指标、约束
2. 生成结构化 PRD
3. 保存到 `wiki/specs/2024-01-15-SSO.md`
4. 更新 `wiki/index.md`

### 示例 2: 综合研究

**你**: "整理这 10 份访谈笔记"

**Agent**:
1. 读取你提供的笔记
2. 识别主题和模式
3. 生成研究综合报告
4. 保存到 `wiki/research/2024-01-15-onboarding-interviews.md`

### 示例 3: 竞品分析

**你**: "分析竞争对手 X"

**Agent**:
1. 进行研究（通过网络搜索或你提供的信息）
2. 生成功能对比和定位分析
3. 提供战略建议
4. 保存到 `wiki/competitive/2024-01-15-competitor-x.md`

## 最佳实践

1. **明确目标**: 告诉 Agent 你的决策背景
2. **提供上下文**: 分享相关文档、数据或背景信息
3. **迭代完善**: 审阅初稿并提供反馈
4. **保持更新**: 定期让 Agent 更新路线图和指标
5. **建立连接**: 在文档中使用 `[[链接]]` 建立知识关联

## 与其他工具集成

PM Agent 可以与以下工具配合使用（通过手动导入数据）：
- **项目管理**: Linear, Asana, Jira, Monday.com, ClickUp
- **分析**: Amplitude, Mixpanel, Pendo
- **用户反馈**: Intercom, Productboard
- **设计**: Figma
- **知识库**: Notion, Confluence

## 注意事项

1. **隐私**: 注意不要在输入中分享敏感信息
2. **验证**: AI 生成内容需要人工审核
3. **迭代**: 初稿是起点，需要反复打磨
4. **可追溯**: 所有产出都保存在 wiki 中便于追溯

## 自定义配置

编辑 `agents.md` 可以：
- 修改目录结构
- 调整模板内容
- 自定义标签体系
- 修改工作流程

## 故障排除

### Agent 不理解任务
- 使用更具体的语言："写 PRD" 而非 "处理这个"
- 提供背景："这是给企业客户的功能"

### 输出不符合预期
- 提供反馈："这个太详细了，需要更简洁"
- 引用示例："参考 [[之前的 PRD]] 的格式"

### 忘记保存到 wiki
- 提醒："请保存到 wiki/specs/"

## 贡献

欢迎提交 Issue 和改进建议！

## 致谢

- 基于 Anthropic 的 Product Management Plugin
- 转换为 KimiCode Agent 格式

---

**开始使用**: 配置好 Agent 后，直接说"帮我写 [功能] 的 PRD"即可开始！
