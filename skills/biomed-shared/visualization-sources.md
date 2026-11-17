# Visualization sources and application limits

Consult this reference for the source rationale behind a design decision or a
source audit. Routine work uses `scientific-plotting/references/visual-design.md`
and `heatmaps.md`, or `scientific-visual-explainer/references/composition.md` in the
relevant visual workflow.

## Decisions and qualifications

| Decision | Source examples | Application |
|---|---|---|
| Task before chart | Design of data figures; Bar charts and box plots; Fujii 2026 | Choose magnitude, distribution, association, profile or matrix pattern first; a source's bar-to-dot example does not set a global chart preference |
| Scales and order | Axes, ticks and grids; Heat maps; Unentangling complex plots; Temporal data | Share scales for absolute comparisons; identify local scales for shape; retain scientific order and document alignments |
| Dense data | Managing deep data; Binning high-resolution data, Figs.1–3 | Judge usable size, choose bin statistics, retain task-relevant extrema. The latter's approximately 1-pt bins and 250/500-bin examples depend on its viewing widths, not a universal cutoff |
| Network or set task | Networks; Sets and intersections | Separate path tracing from connectivity blocks, and exclusive combinations from inclusive overlaps |
| Purpose and composition | Overview figure; Pathways; Neural circuit diagrams; The graphical abstract; Nature Reviews guide | Match summary, review, mechanism and explanation views to their reader tasks; preserve meaningful topology while simplifying context |
| Visual semantics | Intuitive design, Figs.1–4 | Distinguish intervention direction from sampling; retain identity across states. Its red/blue value judgments and spiky-cell examples are context-dependent metaphors, not fixed palettes or measured morphology |
| Grouping and labels | Gestalt principles; Negative space; Labels and callouts | Preserve meaningful distance/enclosure. Data labels follow native plotting controls; editable schematic names and arrow verbs remain part of the diagram |
| Quantitative mini-plots | PLOS graphical-abstract tutorial, Fig.3 | Distinguish method symbols from measured result panels; result panels retain quantitative decoding and the plotting workflow |
| Layout heuristics | Layout; Power of the plane | Golden ratios and approximately 45° slopes illustrate choices; use the task and final size to set aspect ratio |
| Redundancy | Neural circuit diagrams | Remove redundant decoration while preserving labels or additional cues that aid identification |
| Editorial scope | Jambor checklist 2025, p.879; Engaging figures, Fig.2 | Ordinary line plots share coordinates; evaluate the specific comparison. A cohort KM curve describes survival during observed follow-up; use a prediction model for individual prediction |
| Versions | Salience; Negative space | Salience's 2010-12-15 correction restores missing Fig.1 content. Negative space is cited as p.5 although one teaching PDF prints p.1; use DOI and figure locator |

Shared local conventions remain in [visual-standards.md](visual-standards.md).
Journal-specific 6.5/7/8-pt examples, fixed color counts and manual-editor suggestions
are source context; apply the user's current typography, palettes, native controls
and final-size inspection. Review understanding with the existing
[reader feedback](reader-feedback.md), without a separate mandatory checklist.

## Source catalogue

### Classic Points of View

| ID | Year | Source | Application |
|---|---|---|---|
| PV01 | 2010 | [Color coding](https://www.nature.com/articles/nmeth0810-573) | 同一颜色会受背景影响；类别色需可辨，精确量值的比较优先用位置或长度。 |
| PV02 | 2010 | [Design of data figures](https://www.nature.com/articles/nmeth0910-665) | 需要比较数量时，优先让读者沿共同位置或长度刻度判断。 |
| PV03 | 2010 | [Salience](https://www.nature.com/articles/nmeth1010-773) | 需要读者立即看见的特征，使用清楚且不互相争抢的视觉差异。 |
| PV04 | 2010 | [Gestalt principles (part 1)](https://www.nature.com/articles/nmeth1110-863) | 距离、相似性、连接和包围会自动形成分组，因此布局必须对应科学关系。 |
| PV05 | 2010 | [Gestalt principles (part 2)](https://www.nature.com/articles/nmeth1210-941) | 用少量对齐线与连续路径组织内容，减少靠重复边框维持的结构。 |
| PV06 | 2011 | [Negative space](https://www.nature.com/articles/nmeth0111-5) | 留白用来分组、分层和突出重点，应把零碎空隙整理成清楚的间隔。 |
| PV07 | 2011 | [Points of review (part 1)](https://www.nature.com/articles/nmeth0211-101) | 以图的目的安排结构，并让同一对象贯穿步骤时保持身份一致。 |
| PV08 | 2011 | [Points of review (part 2)](https://www.nature.com/articles/nmeth0311-189) | 编码应让需要的比较直接出现；遮挡严重时拆分视图可比继续加颜色更有效。 |
| PV09 | 2011 | [Typography](https://www.nature.com/articles/nmeth0411-277) | 统一字体和少量字号，以段落、行距和对齐表达文字层级。 |
| PV10 | 2011 | [The overview figure](https://www.nature.com/articles/nmeth0511-365) | 用稳定对象与动作短语连接状态，并把条件比较排成可逐步对应的结构。 |
| PV11 | 2011 | [Color blindness](https://www.nature.com/articles/nmeth.1618) | 颜色辨识需考虑明度、饱和度和实际使用尺寸，关键分类可另有可读标识。 |
| PV12 | 2011 | [Avoiding color](https://www.nature.com/articles/nmeth.1642) | 当问题关乎峰形、相位或排序时，让几何形状承担比较，颜色承担更少的工作。 |
| PV13 | 2011 | [Simplify to clarify](https://www.nature.com/articles/nmeth.1660) | 删除不推进主意的信息，合并重复步骤和标签，同时保留解释必需的结构。 |
| PV14 | 2011 | [Arrows](https://www.nature.com/articles/nmeth.1676) | 把箭头作为有明确含义的关系动词，区分过程、定位和结构连接。 |
| PV15 | 2011 | [Layout](https://www.nature.com/articles/nmeth.1711) | 网格、视觉权重和空间安排应让读者知道先看什么、再理解什么。 |
| PV16 | 2011 | [Salience to relevance](https://www.nature.com/articles/nmeth.1762) | 最显眼的对象应与科学重点一致，并随观看场景分配注意力。 |
| PV17 | 2011 | [The design process](https://www.nature.com/articles/nmeth.1783) | 把图看作供读者完成一个理解任务的工具，先定目的，再选视觉语汇与构图。 |
| PV18 | 2012 | [Data exploration](https://www.nature.com/articles/nmeth.1829) | 探索阶段用低维切片与一致尺度发现未知模式，并记录浏览选择。 |
| PV19 | 2012 | [Networks](https://www.nature.com/articles/nmeth.1862) | 节点边图方便追踪路径，邻接矩阵方便看大网络的连接块。 |
| PV20 | 2012 | [Heat maps](https://www.nature.com/articles/nmeth.1902) | 热图颜色与排序共同决定可见模式，时间和剂量等自然顺序应保留。 |
| PV21 | 2012 | [Integrating data](https://www.nature.com/articles/nmeth.1944) | 按任务把实测量映射到固定生物学关系中，多状态比较宜同时可见。 |
| PV22 | 2012 | [Representing the genome](https://www.nature.com/articles/nmeth.1992) | 按基因组距离或共同锚点组织位置，并保留特征尺度和变换说明。 |
| PV23 | 2012 | [Managing deep data in genome browsers](https://www.nature.com/articles/nmeth.2049) | 区分表示压缩与统计汇总，并让概要仍可回到原始轨道。 |
| PV24 | 2012 | [Representing genomic structural variation](https://www.nature.com/articles/nmeth.2018) | 根据断点、序列方向、重排顺序或功能连接选择表示。 |
| PV25 | 2012 | [Mapping quantitative data to color](https://www.nature.com/articles/nmeth.2134) | 先定义有意义的端点和中心，再选择顺序或发散色标及范围。 |
| PV26 | 2012 | [Into the third dimension](https://www.nature.com/articles/nmeth.2151) | 三维应承担真实空间信息，并检查遮挡、透视与明暗对数值读取的影响。 |
| PV27 | 2012 | [Power of the plane](https://www.nature.com/articles/nmeth.2186) | 平行坐标支持追踪多变量样本，散点矩阵支持读变量对关系。 |
| PV28 | 2012 | [Pencil and paper](https://www.nature.com/articles/nmeth.2223) | 草图能把隐含的空间与机制假设变成可讨论的具体选择。 |
| PV29 | 2012 | [Visualizing biological data](https://www.nature.com/articles/nmeth.2258) | 可视化应由研究者实际要发现或解释的模式驱动，并与分析共同迭代。 |
| PV30 | 2013 | [Axes, ticks and grids](https://www.nature.com/articles/nmeth.2337) | 导航元素保持数量可读，其视觉权重低于数据。 |
| PV31 | 2013 | [Labels and callouts](https://www.nature.com/articles/nmeth.2405) | 标签要在布局阶段设计，锚定其对象，并以一致格式降低来回查找。 |
| PV32 | 2013 | [Elements of visual style](https://www.nature.com/articles/nmeth.2444) | 给同类科学关系一致的视觉表达，装饰与不必要的形状变化应让位于信息。 |
| PV33 | 2013 | [Plotting symbols](https://www.nature.com/articles/nmeth.2490) | 符号要在实际重叠密度下保持类别可分，并让显著性对应科学相关性。 |
| PV34 | 2013 | [Multidimensional data](https://www.nature.com/articles/nmeth.2531) | 先列变量与层级，再用生物学关系组织高维图的视觉通道。 |
| PV35 | 2013 | [Storytelling](https://www.nature.com/articles/nmeth.2571) | 让各面板依次回答问题，提供足够背景后呈现发现和生物学意义。 |
| PV36 | 2014 | [Bar charts and box plots](https://www.nature.com/articles/nmeth.2807) | 先确定总量、类别比较或分布，再选择柱图布局或分布图。 |
| PV37 | 2014 | [Sets and intersections](https://www.nature.com/articles/nmeth.3033) | 先分清互斥组合、两两交集及集合大小，再选 Euler、UpSet 或矩阵。 |
| PV38 | 2015 | [Temporal data](https://www.nature.com/articles/nmeth.3262) | 区分绝对时间与周期相位，让坐标直接支持峰位、峰高或时长比较。 |
| PV39 | 2015 | [Unentangling complex plots](https://www.nature.com/articles/nmeth.3451) | 共同尺度便于比较绝对量，局部尺度须显出缩放并保留所需全局语境。 |
| PV40 | 2016 | [Pathways](https://www.nature.com/articles/nmeth.3699) | 用区室、规则连接与模块分组使连续路径易于追踪，并让节点细节服务于科学重点。 |
| PV41 | 2016 | [Neural circuit diagrams](https://www.nature.com/articles/nmeth.3777) | 按科学问题决定哪些空间拓扑必须保留，并通过必要形态与连接类型让复杂回路可读。 |
| PV42 | 2016 | [Binning high-resolution data](https://www.nature.com/articles/nmeth.3873) | 按最终尺寸选择分箱，并用任务所需的中心、范围或极值保存高密度数据的重要特征。 |
| PV43 | 2016 | [Intuitive design](https://www.nature.com/articles/nmeth.4041) | 颜色、方向和形状会带来直觉解释，应检查这些解释与所画关系是否一致。 |

### Points of View, 2026

| ID | Year | Source | Application |
|---|---|---|---|
| PV44 | 2026 | [Color scales and the birth of viridis](https://www.nature.com/articles/s41592-026-03114-w) | 颜色映射应匹配数值顺序与阅读任务，使用可解释的明度变化。 |
| PV45 | 2026 | [Click to plot](https://www.nature.com/articles/s41592-026-03147-1) | 按科学任务选择绘图工具，并保存工具参数、变换和可编辑导出。 |
| PV46 | 2026 | [Code to plot](https://www.nature.com/articles/s41592-026-03173-z) | 让数据处理和数量编码可重运行，并核查 AI 绘图代码中的分析步骤。 |
| PV47 | 2026 | [The graphical abstract](https://www.nature.com/articles/s41592-026-03207-6) | 围绕一个中心发现组织视觉摘要，并按目录、报告或海报的观看场景调整布局。 |
| PV48 | 2026 | [Engaging figures](https://www.nature.com/articles/s41592-026-03241-4) | 以必要的个体、时间、空间和生物学后果帮助读者理解结果。 |
| PV49 | 2026 | [The companion website](https://www.nature.com/articles/s41592-026-03276-7) | 用总览与按需细节承载适合交互探索的补充材料。 |

### Supporting tutorials and editorials

| ID | Year | Source | Application |
|---|---|---|---|
| SUP01 | 2019 | [About figures](https://www.nature.com/articles/s42254-019-0094-7) | 让综述图承担有用的解释，并为内容重组与出版编辑保留真正的矢量来源。 |
| SUP02 | 2022 | [Figuring it out](https://www.nature.com/articles/s44160-022-00067-8) | 按科学主题组织面板，使图、标签、单位与图注共同引导读者理解发现。 |
| SUP03 | 2024 | [Ten simple rules for designing graphical abstracts](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011789) | 从中心消息出发，按过程、并列、嵌套或循环关系选布局，再用具体读者反馈修订。 |
| SUP04 | 2025 | [A checklist for designing and improving the visualization of scientific data](https://www.nature.com/articles/s41556-025-01684-z) | 把图型、文字、布局、颜色与读者反馈组织成可按需使用的设计检查。 |
| SUP05 | 2026 | [How to design effective scientific figures](https://www.nature.com/articles/s41562-026-02466-9) | 先确定主信息、读者时间和互动机会，再确定表达细节。 |
| SUP06 | 2026 | [Points of View, anew](https://www.nature.com/articles/s41592-026-03143-5) | 可视化也参与发现数据问题、完善设计和检查模型。 |
| SUP07 | Undated | [Nature Reviews guide to designing figures / conceptual figures](https://www.nature.com/documents/natrev-artworkguide.pdf) | 把视觉层级、细节分配和内容删减用于概念解释，保留可编辑标签与关键关系。 |

