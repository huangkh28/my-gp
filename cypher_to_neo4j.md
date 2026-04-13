// 创建唯一约束，防止重复节点
CREATE CONSTRAINT IF NOT EXISTS FOR (d:Document) REQUIRE d.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (c:Chapter) REQUIRE c.number IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (a:Article) REQUIRE a.number IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (ag:Agent) REQUIRE ag.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (o:Obligation) REQUIRE o.description IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (p:Purpose) REQUIRE p.description IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (pr:Principle) REQUIRE pr.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (g:Goal) REQUIRE g.description IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (au:Authority) REQUIRE au.description IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (p:Penalty) REQUIRE p.description IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (s:System) REQUIRE s.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (obj:Object) REQUIRE obj.name IS UNIQUE;


// 创建文档节点
MERGE (doc:Document {name: "广东省土地管理条例", promulgation_date: "2022年6月1日", implementation_date: "2022年8月1日", legislative_body: "广东省第十三届人民代表大会常务委员会第四十三次会议"})

// 创建第一章节点
MERGE (chapter1:Chapter {number: "第一章", title: "第一章 总则"})
MERGE (chapter1)-[:PART_OF]->(doc)

// 第一条
MERGE (art1:Article {number: "第一条", full_text: "为了加强土地管理，保护、开发土地资源，合理利用土地，落实最严格的耕地保护制度，促进社会经济的可持续发展，根据《中华人民共和国土地管理法》《中华人民共和国土地管理法实施条例》等法律、行政法规，结合本省实际，制定本条例。"})
MERGE (art1)-[:PART_OF]->(chapter1)

MERGE (purpose1:Purpose {description: "加强土地管理"})
MERGE (purpose2:Purpose {description: "保护土地资源"})
MERGE (purpose3:Purpose {description: "开发土地资源"})
MERGE (purpose4:Purpose {description: "合理利用土地"})
MERGE (purpose5:Purpose {description: "落实最严格的耕地保护制度"})
MERGE (purpose6:Purpose {description: "促进社会经济的可持续发展"})

MERGE (art1)-[:HAS_PURPOSE]->(purpose1)
MERGE (art1)-[:HAS_PURPOSE]->(purpose2)
MERGE (art1)-[:HAS_PURPOSE]->(purpose3)
MERGE (art1)-[:HAS_PURPOSE]->(purpose4)
MERGE (art1)-[:HAS_PURPOSE]->(purpose5)
MERGE (art1)-[:HAS_PURPOSE]->(purpose6)

// 引用的法律法规
MERGE (law1:Document {name: "中华人民共和国土地管理法", type: "national_law"})
MERGE (law2:Document {name: "中华人民共和国土地管理法实施条例", type: "administrative_regulation"})

MERGE (art1)-[:CITES]->(law1)
MERGE (art1)-[:CITES]->(law2)

// 第二条
MERGE (art2:Article {number: "第二条", full_text: "各级人民政府应当加强对土地管理工作的领导，坚持生态优先、绿色发展、全面规划、严格管理，优化土地资源配置，推动节约集约用地，提升用地效率，制止非法占用土地和破坏土地资源的行为。街道办事处在本辖区内办理派出它的人民政府交办的土地管理相关工作。"})
MERGE (art2)-[:PART_OF]->(chapter1)

MERGE (agent1:Agent {name: "各级人民政府", type: "government_level"})
MERGE (agent2:Agent {name: "街道办事处", type: "organization", function: "办理派出它的人民政府交办的土地管理相关工作"})

MERGE (principle1:Principle {name: "生态优先",source_article:"第二条"})
MERGE (principle2:Principle {name: "绿色发展",source_article:"第二条"})
MERGE (principle3:Principle {name: "全面规划",source_article:"第二条"})
MERGE (principle4:Principle {name: "严格管理",source_article:"第二条"})

MERGE (goal1:Goal {description: "优化土地资源配置",source_article:"第二条"})
MERGE (goal2:Goal {description: "推动节约集约用地",source_article:"第二条"})
MERGE (goal3:Goal {description: "提升用地效率",source_article:"第二条"})
MERGE (goal4:Goal {description: "制止非法占用土地",source_article:"第二条"})
MERGE (goal5:Goal {description: "制止破坏土地资源的行为",source_article:"第二条"})

// 各级人民政府的职责和遵循的原则
MERGE (agent1)-[:HAS_DUTY]->(duty1:Obligation {description: "加强对土地管理工作的领导",source_article:"第二条"})
MERGE (agent1)-[:FOLLOWS_PRINCIPLE]->(principle1)
MERGE (agent1)-[:FOLLOWS_PRINCIPLE]->(principle2)
MERGE (agent1)-[:FOLLOWS_PRINCIPLE]->(principle3)
MERGE (agent1)-[:FOLLOWS_PRINCIPLE]->(principle4)
MERGE (agent1)-[:HAS_GOAL]->(goal1)
MERGE (agent1)-[:HAS_GOAL]->(goal2)
MERGE (agent1)-[:HAS_GOAL]->(goal3)
MERGE (agent1)-[:HAS_GOAL]->(goal4)
MERGE (agent1)-[:HAS_GOAL]->(goal5)

// 街道办事处的职责
MERGE (agent2)-[:HAS_DUTY]->(duty2:Obligation {description: "在本辖区内办理派出它的人民政府交办的土地管理相关工作",source_article:"第二条"})

// 将主体与条例关联
MERGE (art2)-[:INVOLVES]->(agent1)
MERGE (art2)-[:INVOLVES]->(agent2)

// 第三条
MERGE (art3:Article {number: "第三条", full_text: "县级以上人民政府自然资源主管部门负责土地管理和监督工作。县级以上人民政府农业农村主管部门负责农村宅基地改革和管理相关工作，做好耕地质量管理相关工作；林业主管部门负责林地管理相关工作。其他有关部门按照各自职责，共同做好土地管理相关工作。"})
MERGE (art3)-[:PART_OF]->(chapter1)

// 各部门及其职责
MERGE (dept1:Agent {name: "县级以上人民政府自然资源主管部门", type: "department"})
MERGE (dept2:Agent {name: "县级以上人民政府农业农村主管部门", type: "department"})
MERGE (dept3:Agent {name: "林业主管部门", type: "department"})
MERGE (dept4:Agent {name: "其他有关部门", type: "department"})

MERGE (dept1)-[:HAS_DUTY]->(duty3:Obligation {description: "负责土地管理和监督工作",source_article:"第三条"})
MERGE (dept2)-[:HAS_DUTY]->(duty4:Obligation {description: "负责农村宅基地改革和管理相关工作",source_article:"第三条"})
MERGE (dept2)-[:HAS_DUTY]->(duty5:Obligation {description: "做好耕地质量管理相关工作",source_article:"第三条"})
MERGE (dept3)-[:HAS_DUTY]->(duty6:Obligation {description: "负责林地管理相关工作",source_article:"第三条"})
MERGE (dept4)-[:HAS_DUTY]->(duty7:Obligation {description: "按照各自职责，共同做好土地管理相关工作",source_article:"第三条"})

// 将部门与条例关联
MERGE (art3)-[:INVOLVES]->(dept1)
MERGE (art3)-[:INVOLVES]->(dept2)
MERGE (art3)-[:INVOLVES]->(dept3)
MERGE (art3)-[:INVOLVES]->(dept4)

// 第四条
MERGE (art4:Article {number: "第四条", full_text: "县级以上人民政府及自然资源主管部门应当加强土地管理信息化建设，落实经费保障，按照数字政府集约化建设要求，建立统一的国土空间基础信息平台，支撑国土空间规划、耕地保护、土地开发利用、不动产登记、土地调查、生态保护修复、执法监督等事项的信息化管理，对土地利用状况和管理情况进行动态监测。自然资源、发展改革、人力资源社会保障、住房城乡建设、交通运输、农业农村、政务服务数据管理等有关部门应当建立土地管理信息共享机制，实现土地管理数据共享和业务协同，依法公开土地管理信息。"})
MERGE (art4)-[:PART_OF]->(chapter1)

MERGE (agent3:Agent {name: "县级以上人民政府", type: "government_level"})
MERGE (agent4:Agent {name: "县级以上人民政府自然资源主管部门", type: "department"})
MERGE (agent5:Agent {name: "自然资源主管部门", type: "department"})
MERGE (agent6:Agent {name: "发展改革部门", type: "department"})
MERGE (agent7:Agent {name: "人力资源社会保障部门", type: "department"})
MERGE (agent8:Agent {name: "住房城乡建设部门", type: "department"})
MERGE (agent9:Agent {name: "交通运输部门", type: "department"})
MERGE (agent10:Agent {name: "农业农村部门", type: "department"})
MERGE (agent11:Agent {name: "政务服务数据管理部门", type: "department"})

MERGE (agent3)-[:HAS_DUTY]->(duty8:Obligation {description: "加强土地管理信息化建设",source_article:"第四条"})
MERGE (agent3)-[:HAS_DUTY]->(duty9:Obligation {description: "落实经费保障",source_article:"第四条"})
MERGE (agent4)-[:HAS_DUTY]->(duty10:Obligation {description: "建立统一的国土空间基础信息平台",source_article:"第四条"})
MERGE (agent4)-[:HAS_DUTY]->(duty11:Obligation {description: "对土地利用状况和管理情况进行动态监测",source_article:"第四条"})

MERGE (platform:Object {name: "国土空间基础信息平台", purpose: "支撑国土空间规划、耕地保护、土地开发利用、不动产登记、土地调查、生态保护修复、执法监督等事项的信息化管理",source_article:"第四条"})

MERGE (duty10)-[:USES]->(platform)

// 信息共享机制
MERGE (mechanism:Object {name: "土地管理信息共享机制", purpose: "实现土地管理数据共享和业务协同，依法公开土地管理信息"})

MERGE (agent5)-[:PARTICIPATES_IN]->(mechanism)
MERGE (agent6)-[:PARTICIPATES_IN]->(mechanism)
MERGE (agent7)-[:PARTICIPATES_IN]->(mechanism)
MERGE (agent8)-[:PARTICIPATES_IN]->(mechanism)
MERGE (agent9)-[:PARTICIPATES_IN]->(mechanism)
MERGE (agent10)-[:PARTICIPATES_IN]->(mechanism)
MERGE (agent11)-[:PARTICIPATES_IN]->(mechanism)

// 将主体与条例关联
MERGE (art4)-[:INVOLVES]->(agent3)
MERGE (art4)-[:INVOLVES]->(agent4)
MERGE (art4)-[:INVOLVES]->(agent5)
MERGE (art4)-[:INVOLVES]->(agent6)
MERGE (art4)-[:INVOLVES]->(agent7)
MERGE (art4)-[:INVOLVES]->(agent8)
MERGE (art4)-[:INVOLVES]->(agent9)
MERGE (art4)-[:INVOLVES]->(agent10)
MERGE (art4)-[:INVOLVES]->(agent11)

// 第五条
MERGE (art5:Article {number: "第五条", full_text: "任何单位和个人都有遵守土地管理法律、法规的义务，不得侵占、买卖或者以其他形式非法转让土地，不得非法占用土地。"})
MERGE (art5)-[:PART_OF]->(chapter1)

MERGE (agent12:Agent {name: "任何单位", type: "entity"})
MERGE (agent13:Agent {name: "任何个人", type: "person"})

MERGE (agent12)-[:HAS_DUTY]->(duty12:Obligation {description: "遵守土地管理法律、法规",source_article:"第五条"})
MERGE (agent13)-[:HAS_DUTY]->(duty12)

MERGE (agent12)-[:PROHIBITED_FROM]->(prohibition1:Prohibition {description: "侵占土地",source_article:"第五条"})
MERGE (agent12)-[:PROHIBITED_FROM]->(prohibition2:Prohibition {description: "买卖土地",source_article:"第五条"})
MERGE (agent12)-[:PROHIBITED_FROM]->(prohibition3:Prohibition {description: "以其他形式非法转让土地",source_article:"第五条"})
MERGE (agent12)-[:PROHIBITED_FROM]->(prohibition4:Prohibition {description: "非法占用土地",source_article:"第五条"})

MERGE (agent13)-[:PROHIBITED_FROM]->(prohibition1)
MERGE (agent13)-[:PROHIBITED_FROM]->(prohibition2)
MERGE (agent13)-[:PROHIBITED_FROM]->(prohibition3)
MERGE (agent13)-[:PROHIBITED_FROM]->(prohibition4)

// 将主体与条例关联
MERGE (art5)-[:INVOLVES]->(agent12)
MERGE (art5)-[:INVOLVES]->(agent13)























//第二章
// 创建第二章节点（确保文档节点已存在）
MATCH (doc:Document {name: "广东省土地管理条例"})
MERGE (chapter2:Chapter {number: "第二章", title: "国土空间规划"})
MERGE (chapter2)-[:PART_OF]->(doc)

// 第六条
MERGE (art6:Article {number: "第六条", full_text: "经依法批准的国土空间规划是各类开发、保护、建设活动的基本依据。不得在国土空间规划体系之外另设其他空间规划。各级人民政府应当按照国家和省有关规定组织编制国土空间规划。国土空间规划包括总体规划、详细规划和专项规划。下级国土空间规划应当服从上级国土空间规划；详细规划、专项规划应当服从总体规划；相关专项规划应当相互协同，并与详细规划做好衔接。"})
MERGE (art6)-[:PART_OF]->(chapter2)

// 规划类型
MERGE (plan_type1:Object {name: "总体规划", type: "plan_type",source_article:"第六条"})
MERGE (plan_type2:Object {name: "详细规划", type: "plan_type",source_article:"第六条"})
MERGE (plan_type3:Object {name: "专项规划", type: "plan_type",source_article:"第六条"})
MERGE (plan_type4:Object {name: "国土空间规划", type: "plan_type",source_article:"第六条"})

// 规划层级关系
MERGE (plan_type2)-[:SUBORDINATE_TO]->(plan_type1)
MERGE (plan_type3)-[:SUBORDINATE_TO]->(plan_type1)
MERGE (plan_type3)-[:COORDINATES_WITH]->(plan_type2)
MERGE (plan_type2)-[:COORDINATES_WITH]->(plan_type3)

// 规划原则
MERGE (principle1:Principle {name: "规划体系唯一性原则",source_article:"第六条"})
MERGE (principle2:Principle {name: "下级服从上级原则",source_article:"第六条"})
MERGE (principle3:Principle {name: "详细规划、专项规划服从总体规划原则",source_article:"第六条"})
MERGE (principle4:Principle {name: "专项规划协同原则",source_article:"第六条"})

MERGE (art6)-[:ESTABLISHES_PRINCIPLE]->(principle1)
MERGE (art6)-[:ESTABLISHES_PRINCIPLE]->(principle2)
MERGE (art6)-[:ESTABLISHES_PRINCIPLE]->(principle3)
MERGE (art6)-[:ESTABLISHES_PRINCIPLE]->(principle4)

// 规划编制主体
MERGE (agent1:Agent {name: "各级人民政府", type: "government_level"})
MERGE (agent1)-[:HAS_DUTY]->(duty1:Obligation {description: "按照国家和省有关规定组织编制国土空间规划",source_article:"第六条"})

// 将主体与条例关联
MERGE (art6)-[:INVOLVES]->(agent1)
MERGE (art6)-[:STIPULATE]->(plan_type4)
MERGE (plan_type4)-[:CONTAIN]->(plan_type1)
MERGE (plan_type4)-[:CONTAIN]->(plan_type2)
MERGE (plan_type4)-[:CONTAIN]->(plan_type3)

// 第七条
MERGE (art7:Article {number: "第七条", full_text: "编制国土空间规划应当细化落实国家和省发展规划提出的国土空间开发保护要求，科学有序统筹安排农业、生态、城镇等功能空间，划定落实永久基本农田、生态保护红线和城镇开发边界，优化国土空间结构和布局，提升国土空间开发保护的质量和效率。国土空间规划的编制、实施应当公开征求社会公众意见，主动接受公众监督。规划依据、内容、程序、结果、查询方式、监督方式等信息应当依法公开。"})
MERGE (art7)-[:PART_OF]->(chapter2)

// 功能空间
MERGE (space1:Object {name: "农业功能空间", type: "space",source_article:"第七条"})
MERGE (space2:Object {name: "生态功能空间", type: "space",source_article:"第七条"})
MERGE (space3:Object {name: "城镇功能空间", type: "space",source_article:"第七条"})

// 控制线
MERGE (control_line1:Object {name: "永久基本农田", type: "control_line"})
MERGE (control_line2:Object {name: "生态保护红线", type: "control_line"})
MERGE (control_line3:Object {name: "城镇开发边界", type: "control_line"})

// 规划编制内容
MERGE (duty2:Obligation {description: "细化落实国家和省发展规划提出的国土空间开发保护要求",source_article:"第七条"})
MERGE (duty3:Obligation {description: "科学有序统筹安排农业、生态、城镇等功能空间",source_article:"第七条"})
MERGE (duty4:Obligation {description: "划定落实永久基本农田、生态保护红线和城镇开发边界",source_article:"第七条"})
MERGE (duty5:Obligation {description: "优化国土空间结构和布局",source_article:"第七条"})
MERGE (duty6:Obligation {description: "提升国土空间开发保护的质量和效率",source_article:"第七条"})

// 规划公开要求
MERGE (duty7:Obligation {description: "编制、实施应当公开征求社会公众意见",source_article:"第七条"})
MERGE (duty8:Obligation {description: "主动接受公众监督",source_article:"第七条"})
MERGE (duty9:Obligation {description: "规划依据、内容、程序、结果、查询方式、监督方式等信息应当依法公开",source_article:"第七条"})

// 将义务与条例关联
MERGE (art7)-[:HAS_DUTY]->(duty2)
MERGE (art7)-[:HAS_DUTY]->(duty3)
MERGE (art7)-[:HAS_DUTY]->(duty4)
MERGE (art7)-[:HAS_DUTY]->(duty5)
MERGE (art7)-[:HAS_DUTY]->(duty6)
MERGE (art7)-[:HAS_DUTY]->(duty7)
MERGE (art7)-[:HAS_DUTY]->(duty8)
MERGE (art7)-[:HAS_DUTY]->(duty9)

// 将功能空间与义务关联
MERGE (duty3)-[:ALLOCATES_SPACE]->(space1)
MERGE (duty3)-[:ALLOCATES_SPACE]->(space2)
MERGE (duty3)-[:ALLOCATES_SPACE]->(space3)

// 将控制线与义务关联
MERGE (duty4)-[:DEFINES_CONTROL_LINE]->(control_line1)
MERGE (duty4)-[:DEFINES_CONTROL_LINE]->(control_line2)
MERGE (duty4)-[:DEFINES_CONTROL_LINE]->(control_line3)

// 第八条
MERGE (art8:Article {number: "第八条", full_text: "省国土空间总体规划由省人民政府组织编制，经省人民代表大会常务委员会审议后，报国务院批准。地级以上市国土空间总体规划由本级人民政府组织编制，经本级人民代表大会常务委员会审议后，报省人民政府批准。国家规定需报国务院批准的城市国土空间总体规划，由本级人民政府组织编制，经本级人民代表大会常务委员会审议后，由省人民政府审核并报批。县（市、区）国土空间总体规划由本级人民政府组织编制，经本级人民代表大会常务委员会审议后，按照省的规定报批。乡镇国土空间总体规划由乡镇人民政府组织编制，逐级报地级以上市人民政府批准；以多个乡镇为单元的乡镇国土空间总体规划，按照省的规定组织编制，报地级以上市人民政府批准。"})
MERGE (art8)-[:PART_OF]->(chapter2)

// 规划编制主体与审批主体
MERGE (agent2:Agent {name: "省人民政府", type: "government_level"})
MERGE (agent3:Agent {name: "省人民代表大会常务委员会", type: "legislative_body"})
MERGE (agent4:Agent {name: "国务院", type: "government_level"})
MERGE (agent5:Agent {name: "地级以上市人民政府", type: "government_level"})
MERGE (agent6:Agent {name: "地级以上市人民代表大会常务委员会", type: "legislative_body"})
MERGE (agent7:Agent {name: "县（市、区）人民政府", type: "government_level"})
MERGE (agent8:Agent {name: "乡镇人民政府", type: "government_level"})
MERGE (agent9:Agent {name: "地级以上市人民政府", type: "government_level"})
MERGE (agent10:Agent {name: "省", type: "government_level"})

// 规划类型
MERGE (plan1:Object {name: "省国土空间总体规划", type: "plan",source_article:"第八条"})
MERGE (plan2:Object {name: "地级以上市国土空间总体规划", type: "plan",source_article:"第八条"})
MERGE (plan3:Object {name: "国家规定需报国务院批准的城市国土空间总体规划", type: "plan",source_article:"第八条"})
MERGE (plan4:Object {name: "县（市、区）国土空间总体规划", type: "plan",source_article:"第八条"})
MERGE (plan5:Object {name: "乡镇国土空间总体规划", type: "plan",source_article:"第八条"})

// 审批流程
MERGE (procedure1:Procedure {name: "省国土空间总体规划审批流程", steps: "省人民政府组织编制，经省人民代表大会常务委员会审议后，报国务院批准",source_article:"第八条"})
MERGE (procedure2:Procedure {name: "地级以上市国土空间总体规划审批流程", steps: "地级以上市人民政府组织编制，经本级人民代表大会常务委员会审议后，报省人民政府批准",source_article:"第八条"})
MERGE (procedure3:Procedure {name: "需报国务院批准的城市国土空间总体规划审批流程", steps: "本级人民政府组织编制，经本级人民代表大会常务委员会审议后，由省人民政府审核并报批",source_article:"第八条"})
MERGE (procedure4:Procedure {name: "县（市、区）国土空间总体规划审批流程", steps: "县（市、区）人民政府组织编制，经本级人民代表大会常务委员会审议后，按照省的规定报批",source_article:"第八条"})
MERGE (procedure5:Procedure {name: "乡镇国土空间总体规划审批流程", steps: "乡镇人民政府组织编制，逐级报地级以上市人民政府批准；以多个乡镇为单元的，按照省的规定组织编制，报地级以上市人民政府批准",source_article:"第八条"})

// 将规划与审批流程关联
MERGE (plan1)-[:FOLLOWS_PROCEDURE]->(procedure1)
MERGE (plan2)-[:FOLLOWS_PROCEDURE]->(procedure2)
MERGE (plan3)-[:FOLLOWS_PROCEDURE]->(procedure3)
MERGE (plan4)-[:FOLLOWS_PROCEDURE]->(procedure4)
MERGE (plan5)-[:FOLLOWS_PROCEDURE]->(procedure5)

// 将主体与规划关联
MERGE (agent2)-[:ORGANIZES]->(plan1)
MERGE (agent3)-[:REVIEW]->(plan1)
MERGE (agent4)-[:HAS_AUTHORITY]->(plan1)

MERGE (agent5)-[:ORGANIZES]->(plan2)
MERGE (agent6)-[:REVIEW]->(plan2)
MERGE (agent7)-[:HAS_AUTHORITY]->(plan2)

MERGE (agent5)-[:ORGANIZES]->(plan3)
MERGE (agent6)-[:REVIEW]->(plan3)
MERGE (agent10)-[:REVIEW]->(plan3)
MERGE (agent4)-[:HAS_AUTHORITY]->(plan3)

MERGE (agent7)-[:ORGANIZES]->(plan4)
MERGE (agent7)-[:REVIEW]->(plan4)
MERGE (agent7)-[:HAS_AUTHORITY]->(plan4)

MERGE (agent8)-[:ORGANIZES]->(plan5)
MERGE (agent9)-[:HAS_AUTHORITY]->(plan5)

//将主体与条例相关联
MERGE (art8)-[:INVOLVES]->(agent2)
MERGE (art8)-[:INVOLVES]->(agent3)
MERGE (art8)-[:INVOLVES]->(agent4)
MERGE (art8)-[:INVOLVES]->(agent5)
MERGE (art8)-[:INVOLVES]->(agent6)
MERGE (art8)-[:INVOLVES]->(agent7)
MERGE (art8)-[:INVOLVES]->(agent8)
MERGE (art8)-[:INVOLVES]->(agent9)
MERGE (art8)-[:INVOLVES]->(agent10)

// 第九条
MERGE (art9:Article {number: "第九条", full_text: "详细规划应当对具体地块用途和开发建设强度等作出实施性安排，作为开展国土空间开发保护活动、实施国土空间用途管制、核发城乡建设项目规划许可、进行各项建设等的法定依据。城镇开发边界内的详细规划由地级以上市、县（市）人民政府自然资源主管部门组织编制，报本级人民政府批准。城镇开发边界外的乡村地区，由乡镇人民政府以一个或者几个行政村为单元，组织编制村庄规划作为详细规划，报上一级人民政府批准。"})
MERGE (art9)-[:PART_OF]->(chapter2)

// 详细规划类型
MERGE (detail_plan1:Object {name: "城镇开发边界内详细规划", type: "detail_plan",source_article:"第九条"})
MERGE (detail_plan2:Object {name: "城镇开发边界外村庄规划", type: "detail_plan",source_article:"第九条"})

// 详细规划功能
MERGE (duty10:Obligation {description: "对具体地块用途和开发建设强度等作出实施性安排",source_article:"第九条"})
MERGE (duty11:Obligation {description: "作为开展国土空间开发保护活动的法定依据",source_article:"第九条"})
MERGE (duty12:Obligation {description: "实施国土空间用途管制的法定依据",source_article:"第九条"})
MERGE (duty13:Obligation {description: "核发城乡建设项目规划许可的法定依据",source_article:"第九条"})
MERGE (duty14:Obligation {description: "进行各项建设的法定依据",source_article:"第九条"})

// 将义务与条例关联
MERGE (art9)-[:HAS_DUTY]->(duty10)
MERGE (art9)-[:HAS_DUTY]->(duty11)
MERGE (art9)-[:HAS_DUTY]->(duty12)
MERGE (art9)-[:HAS_DUTY]->(duty13)
MERGE (art9)-[:HAS_DUTY]->(duty14)

// 详细规划编制主体
MERGE (agent11:Agent {name: "地级以上市、县（市）人民政府自然资源主管部门", type: "department"})
MERGE (agent12:Agent {name: "乡镇人民政府", type: "government_level"})
MERGE (agent13:Agent {name: "上一级人民政府", type: "government_level"})

// 将主体与详细规划关联
MERGE (agent11)-[:ORGANIZES]->(detail_plan1)
MERGE (agent12)-[:ORGANIZES]->(detail_plan2)
MERGE (agent13)-[:HAS_AUTHORITY]->(detail_plan2)

//将主体与条例关联
MERGE (art9)-[:INVOLVES]->(agent11)
MERGE (art9)-[:INVOLVES]->(agent12)
MERGE (art9)-[:INVOLVES]->(agent13)

// 第十条
MERGE (art10:Article {number: "第十条", full_text: "专项规划应当体现特定功能，对国土空间特定区域、特定流域、特定领域的开发、保护和利用作出专门安排。不同层级、不同地区的专项规划可以结合实际选择编制的类型和精度。专项规划由县级以上人民政府自然资源主管部门或者其他相关主管部门按照职责分工组织编制。自然资源主管部门组织编制的，报本级人民政府批准；其他相关主管部门组织编制的，按照有关规定审批。"})
MERGE (art10)-[:PART_OF]->(chapter2)

// 专项规划特点
MERGE (feature1:Object {name: "体现特定功能", type: "feature"})
MERGE (feature2:Object {name: "对特定区域、特定流域、特定领域作出专门安排", type: "feature"})
MERGE (feature3:Object {name: "结合实际选择编制类型和精度", type: "feature"})

// 专项规划编制主体
MERGE (agent14:Agent {name: "县级以上人民政府自然资源主管部门", type: "department"})
MERGE (agent15:Agent {name: "其他相关主管部门", type: "department"})
MERGE (agent16:Agent {name: "本级人民政府", type: "government_level"})

// 专项规划审批流程
MERGE (procedure6:Procedure {name: "自然资源主管部门组织编制专项规划审批流程", steps: "报本级人民政府批准",source_article:"第十条"})
MERGE (procedure7:Procedure {name: "其他相关主管部门组织编制专项规划审批流程", steps: "按照有关规定审批",source_article:"第十条"})

// 将专项规划特点与条例关联
MERGE (art10)-[:DESCRIBES_FEATURE]->(feature1)
MERGE (art10)-[:DESCRIBES_FEATURE]->(feature2)
MERGE (art10)-[:DESCRIBES_FEATURE]->(feature3)

// 将编制主体与专项规划关联
MERGE (agent14)-[:ORGANIZES]->(plan_type3)
MERGE (agent15)-[:ORGANIZES]->(plan_type3)
MERGE (agent16)-[:HAS_AUTHORITY]->(plan_type3)

// 将审批流程与专项规划关联
MERGE (plan_type3)-[:FOLLOWS_PROCEDURE]->(procedure6)
MERGE (plan_type3)-[:FOLLOWS_PROCEDURE]->(procedure7)

// 将主题和条例相连
MERGE (art10)-[:INVOLVES]->(agent14)
MERGE (art10)-[:INVOLVES]->(agent15)
MERGE (art10)-[:INVOLVES]->(agent16)

// 第十一条
MERGE (art11:Article {number: "第十一条", full_text: "国土空间规划必须严格执行，不得擅自修改；确需修改的，应当经原批准机关同意后，方可按照法定程序进行修改。"})
MERGE (art11)-[:PART_OF]->(chapter2)

// 规划修改原则
MERGE (principle5:Principle {name: "规划严格执行原则",source_article:"第十一条"})
MERGE (principle6:Principle {name: "规划修改需经原批准机关同意原则",source_article:"第十一条"})

MERGE (art11)-[:ESTABLISHES_PRINCIPLE]->(principle5)
MERGE (art11)-[:ESTABLISHES_PRINCIPLE]->(principle6)

MERGE (art11)-[:STIPULATE]->(plan_type4)
MERGE (plan_type4)-[:FOLLOWS_PRINCIPLE]->(principle5)
MERGE (plan_type4)-[:FOLLOWS_PRINCIPLE]->(principle6)


// 第十二条
MERGE (art12:Article {number: "第十二条", full_text: "各级人民政府应当建立规划实施评估机制，依托国土空间基础信息平台，运用国土空间规划实施监督信息系统，开展国土空间规划动态监测评估预警，对国土空间规划实施情况进行监管和评估。"})
MERGE (art12)-[:PART_OF]->(chapter2)

// 评估机制
MERGE (mechanism1:Mechanism {name: "规划实施评估机制", purpose: "对国土空间规划实施情况进行监管和评估",source_article:"第十二条"})
MERGE (platform:Platform {name: "国土空间基础信息平台", purpose: "依托平台开展规划实施监督",source_article:"第十二条"})
MERGE (system:System {name: "国土空间规划实施监督信息系统", purpose: "运用系统开展规划动态监测评估预警",source_article:"第十二条"})

// 评估机制内容
MERGE (duty15:Obligation {description: "建立规划实施评估机制",source_article:"第十二条"})
MERGE (duty16:Obligation {description: "依托国土空间基础信息平台开展规划实施监督",source_article:"第十二条"})
MERGE (duty17:Obligation {description: "运用国土空间规划实施监督信息系统开展动态监测评估预警",source_article:"第十二条"})

// 将义务与条例关联
MERGE (art12)-[:HAS_DUTY]->(duty15)
MERGE (art12)-[:HAS_DUTY]->(duty16)
MERGE (art12)-[:HAS_DUTY]->(duty17)

// 将机制与平台、系统关联
MERGE (mechanism1)-[:USES_PLATFORM]->(platform)
MERGE (mechanism1)-[:USES_SYSTEM]->(system)
MERGE (agent1)-[:HAS_DUTY] ->(mechanism1)
MERGE (art12)-[:INVOLVES] ->(agent1)

// 第十三条
MERGE (art13:Article {number: "第十三条", full_text: "各级人民政府应当根据本级国土空间规划安排，加强土地利用的计划管理，严格按照土地利用年度计划依法批准建设用地，实行建设用地总量控制。"})
MERGE (art13)-[:PART_OF]->(chapter2)

// 土地利用计划管理
MERGE (duty18:Obligation {description: "加强土地利用的计划管理",source_article:"第十三条"})
MERGE (duty19:Obligation {description: "严格按照土地利用年度计划依法批准建设用地",source_article:"第十三条"})
MERGE (duty20:Obligation {description: "实行建设用地总量控制",source_article:"第十三条"})

// 将义务与条例关联
MERGE (art13)-[:HAS_DUTY]->(duty18)
MERGE (art13)-[:HAS_DUTY]->(duty19)
MERGE (art13)-[:HAS_DUTY]->(duty20)


























// 第三章
// 创建第三章节点（确保文档节点已存在）
MATCH (doc:Document {name: "广东省土地管理条例"})
MERGE (chapter3:Chapter {number: "第三章", title: "耕地保护"})
MERGE (chapter3)-[:PART_OF]->(doc)

// 第十四条
MERGE (art14:Article {number: "第十四条", full_text: "各级人民政府对本行政区域耕地保护负总责，其主要负责人为第一责任人。县级以上人民政府应当每年对下一级人民政府耕地保护责任目标落实情况进行考核。各级人民政府应当严格执行国土空间规划和土地利用年度计划，严格控制耕地转为非耕地，有计划地组织开发补充耕地，引导各类建设项目不占或者少占耕地，采取措施保护和提升耕地质量。耕地总量减少或者质量降低的，由上级人民政府责令在规定期限内组织开垦或者整治。新开垦和整治的耕地按照国家和省有关规定进行验收。"})
MERGE (art14)-[:PART_OF]->(chapter3)

// 责任主体
MERGE (agent1:Agent {name: "各级人民政府", type: "government_level"})
MERGE (agent2:Agent {name: "县级以上人民政府", type: "government_level"})
MERGE (agent3:Agent {name: "上级人民政府", type: "government_level"})
MERGE (agent4:Agent {name: "主要负责人", type: "position"})

// 耕地保护原则
MERGE (principle1:Principle {name: "政府负总责原则", source_article: "第十四条"})
MERGE (principle2:Principle {name: "第一责任人制度", source_article: "第十四条"})
MERGE (principle3:Principle {name: "严格控制耕地转为非耕地原则", source_article: "第十四条"})

// 耕地保护义务
MERGE (duty1:Obligation {description: "对本行政区域耕地保护负总责", source_article: "第十四条"})
MERGE (duty2:Obligation {description: "每年对下一级人民政府耕地保护责任目标落实情况进行考核", source_article: "第十四条"})
MERGE (duty3:Obligation {description: "严格执行国土空间规划和土地利用年度计划", source_article: "第十四条"})
MERGE (duty4:Obligation {description: "严格控制耕地转为非耕地", source_article: "第十四条"})
MERGE (duty5:Obligation {description: "有计划地组织开发补充耕地", source_article: "第十四条"})
MERGE (duty6:Obligation {description: "引导各类建设项目不占或者少占耕地", source_article: "第十四条"})
MERGE (duty7:Obligation {description: "采取措施保护和提升耕地质量", source_article: "第十四条"})
MERGE (duty8:Obligation {description: "在规定期限内组织开垦或者整治减少或质量降低的耕地", source_article: "第十四条"})

// 耕地补充机制
MERGE (mechanism1:Object {name: "耕地补充机制", type: "mechanism", source_article: "第十四条"})
MERGE (procedure1:Procedure {name: "新开垦和整治耕地验收程序", steps: "按照国家和省有关规定进行验收", source_article: "第十四条"})

// 关系建立
MERGE (agent1)-[:FOLLOWS_PRINCIPLE]->(principle1)
MERGE (agent1)-[:FOLLOWS_PRINCIPLE]->(principle3)
MERGE (agent4)-[:FOLLOWS_PRINCIPLE]->(principle2)

MERGE (agent1)-[:HAS_DUTY]->(duty1)
MERGE (agent1)-[:HAS_DUTY]->(duty3)
MERGE (agent1)-[:HAS_DUTY]->(duty4)
MERGE (agent1)-[:HAS_DUTY]->(duty5)
MERGE (agent1)-[:HAS_DUTY]->(duty6)
MERGE (agent1)-[:HAS_DUTY]->(duty7)

MERGE (agent2)-[:HAS_DUTY]->(duty2)
MERGE (agent3)-[:HAS_DUTY]->(duty8)

MERGE (duty5)-[:USES_MECHANISM]->(mechanism1)
MERGE (mechanism1)-[:FOLLOWS_PROCEDURE]->(procedure1)

MERGE (art14)-[:ESTABLISHES_PRINCIPLE]->(principle1)
MERGE (art14)-[:ESTABLISHES_PRINCIPLE]->(principle2)
MERGE (art14)-[:ESTABLISHES_PRINCIPLE]->(principle3)
MERGE (art14)-[:INVOLVES]->(agent1)
MERGE (art14)-[:INVOLVES]->(agent2)
MERGE (art14)-[:INVOLVES]->(agent3)
MERGE (art14)-[:INVOLVES]->(agent4)

// 第十五条
MERGE (art15:Article {number: "第十五条", full_text: "县级以上人民政府应当根据国土空间总体规划确定的永久基本农田保护任务，划定永久基本农田并落实保护责任，确保本行政区域永久基本农田数量不减少、质量不降低、布局总体稳定。地级以上市人民政府划定的永久基本农田一般应当占本行政区域耕地总面积的百分之八十以上。具体比例由省人民政府根据省国土空间总体规划和地级以上市耕地实际情况作出规定。地级以上市和县级人民政府应当将永久基本农田范围以外一定数量的优质耕地划入永久基本农田储备区，作为补划永久基本农田的后备资源。"})
MERGE (art15)-[:PART_OF]->(chapter3)

// 耕地保护概念
MERGE (concept1:Object {name: "永久基本农田"})
MERGE (concept2:Object {name: "永久基本农田储备区", type: "farmland_type"})

// 比例要求
MERGE (requirement1:Object {name: "永久基本农田比例要求", value: "百分之八十以上", source_article: "第十五条"})

// 耕地保护义务
MERGE (duty9:Obligation {description: "划定永久基本农田并落实保护责任", source_article: "第十五条"})
MERGE (duty10:Obligation {description: "确保永久基本农田数量不减少、质量不降低、布局总体稳定", source_article: "第十五条"})
MERGE (duty11:Obligation {description: "将永久基本农田范围以外一定数量的优质耕地划入永久基本农田储备区", source_article: "第十五条"})

// 关系建立
MERGE (agent2)-[:HAS_DUTY]->(duty9)
MERGE (agent2)-[:HAS_DUTY]->(duty10)

MERGE (duty9)-[:DEFINES]->(concept1)
MERGE (duty11)-[:DEFINES]->(concept2)

MERGE (concept1)-[:HAS_REQUIREMENT]->(requirement1)

MERGE (art15)-[:DEFINES_CONCEPT]->(concept1)
MERGE (art15)-[:DEFINES_CONCEPT]->(concept2)
MERGE (art15)-[:INVOLVES]->(agent2)

// 第十六条
MERGE (art16:Article {number: "第十六条", full_text: "本省依法实行占用耕地补偿制度。非农业建设经依法批准占用耕地的，由占用耕地的单位按照国家和省有关规定，负责开垦与所占用耕地的数量和质量相当的耕地；没有条件开垦或者开垦的耕地不符合要求的，应当按照国家规定缴纳耕地开垦费并用于开垦新的耕地，或者通过调剂使用补充耕地指标的方式落实耕地占补平衡。耕地开垦费、补充耕地指标调剂的相关费用，应当作为建设用地成本列入建设项目总投资，并及时足额缴纳或者兑付。地级以上市、县级人民政府应当加强补充耕地项目后期种植管护，按照规定保障后期管护费用。县级人民政府应当制定补充耕地项目后期管护实施方案，明确后期种植管护职责、措施、标准、期限等要求，落实乡镇村以及土地承包经营者的责任。"})
MERGE (art16)-[:PART_OF]->(chapter3)

// 耕地补偿制度
MERGE (system1:Object {name: "占用耕地补偿制度", type: "system", source_article: "第十六条"})
MERGE (concept3:Object {name: "耕地占补平衡", type: "concept", source_article: "第十六条"})

// 补偿方式
MERGE (method1:Object {name: "开垦相当数量和质量的耕地", type: "compensation_method", source_article: "第十六条"})
MERGE (method2:Object {name: "缴纳耕地开垦费", type: "compensation_method", source_article: "第十六条"})
MERGE (method3:Object {name: "调剂使用补充耕地指标", type: "compensation_method", source_article: "第十六条"})

// 责任主体
MERGE (agent5:Agent {name: "占用耕地的单位", type: "entity"})
MERGE (agent6:Agent {name: "地级以上市、县级人民政府", type: "government_level"})
MERGE (agent7:Agent {name: "县级人民政府", type: "government_level"})

// 管护要求
MERGE (duty12:Obligation {description: "负责开垦与所占用耕地的数量和质量相当的耕地", source_article: "第十六条"})
MERGE (duty13:Obligation {description: "缴纳耕地开垦费并用于开垦新的耕地", source_article: "第十六条"})
MERGE (duty14:Obligation {description: "将耕地开垦费作为建设用地成本列入建设项目总投资", source_article: "第十六条"})
MERGE (duty15:Obligation {description: "及时足额缴纳或者兑付相关费用", source_article: "第十六条"})
MERGE (duty16:Obligation {description: "加强补充耕地项目后期种植管护", source_article: "第十六条"})
MERGE (duty17:Obligation {description: "保障后期管护费用", source_article: "第十六条"})
MERGE (duty18:Obligation {description: "制定补充耕地项目后期管护实施方案", source_article: "第十六条"})
MERGE (duty19:Obligation {description: "明确后期种植管护职责、措施、标准、期限等要求", source_article: "第十六条"})
MERGE (duty20:Obligation {description: "落实乡镇村以及土地承包经营者的责任", source_article: "第十六条"})

// 关系建立
MERGE (art16)-[:ESTABLISHES_SYSTEM]->(system1)
MERGE (system1)-[:HAS_METHOD]->(method1)
MERGE (system1)-[:HAS_METHOD]->(method2)
MERGE (system1)-[:HAS_METHOD]->(method3)
MERGE (system1)-[:AIMS_FOR]->(concept3)

MERGE (agent5)-[:HAS_DUTY]->(duty12)
MERGE (agent5)-[:HAS_DUTY]->(duty13)
MERGE (agent5)-[:HAS_DUTY]->(duty14)
MERGE (agent5)-[:HAS_DUTY]->(duty15)

MERGE (agent6)-[:HAS_DUTY]->(duty16)
MERGE (agent6)-[:HAS_DUTY]->(duty17)

MERGE (agent7)-[:HAS_DUTY]->(duty18)
MERGE (agent7)-[:HAS_DUTY]->(duty19)
MERGE (agent7)-[:HAS_DUTY]->(duty20)

MERGE (art16)-[:INVOLVES]->(agent5)
MERGE (art16)-[:INVOLVES]->(agent6)
MERGE (art16)-[:INVOLVES]->(agent7)

// 第十七条
MERGE (art17:Article {number: "第十七条", full_text: "各级人民政府应当采取措施防止和纠正耕地非农化、非粮化和长期撂荒，加强高标准农田建设，提升耕地质量，保证其用途、质量和产能。各级人民政府应当建立耕地保护奖励机制，对耕地保护成绩显著的单位和个人予以奖励。"})
MERGE (art17)-[:PART_OF]->(chapter3)

// 耕地保护目标
MERGE (goal1:Goal {description: "防止和纠正耕地非农化", source_article: "第十七条"})
MERGE (goal2:Goal {description: "防止和纠正耕地非粮化", source_article: "第十七条"})
MERGE (goal3:Goal {description: "防止和纠正耕地长期撂荒", source_article: "第十七条"})
MERGE (goal4:Goal {description: "加强高标准农田建设", source_article: "第十七条"})
MERGE (goal5:Goal {description: "提升耕地质量，保证其用途、质量和产能", source_article: "第十七条"})

// 奖励机制
MERGE (mechanism2:Object {name: "耕地保护奖励机制", type: "mechanism", source_article: "第十七条"})

// 奖励对象
MERGE (agent8:Agent {name: "耕地保护成绩显著的单位", type: "entity"})
MERGE (agent9:Agent {name: "耕地保护成绩显著的个人", type: "person"})

// 耕地保护义务
MERGE (duty21:Obligation {description: "采取措施防止和纠正耕地非农化、非粮化和长期撂荒", source_article: "第十七条"})
MERGE (duty22:Obligation {description: "加强高标准农田建设", source_article: "第十七条"})
MERGE (duty23:Obligation {description: "提升耕地质量，保证其用途、质量和产能", source_article: "第十七条"})
MERGE (duty24:Obligation {description: "建立耕地保护奖励机制", source_article: "第十七条"})
MERGE (duty25:Obligation {description: "对耕地保护成绩显著的单位和个人予以奖励", source_article: "第十七条"})

// 关系建立
MERGE (agent1)-[:HAS_DUTY]->(duty21)
MERGE (agent1)-[:HAS_DUTY]->(duty22)
MERGE (agent1)-[:HAS_DUTY]->(duty23)
MERGE (agent1)-[:HAS_DUTY]->(duty24)
MERGE (agent1)-[:HAS_DUTY]->(duty25)

MERGE (duty21)-[:ACHIEVES_GOAL]->(goal1)
MERGE (duty21)-[:ACHIEVES_GOAL]->(goal2)
MERGE (duty21)-[:ACHIEVES_GOAL]->(goal3)
MERGE (duty22)-[:ACHIEVES_GOAL]->(goal4)
MERGE (duty23)-[:ACHIEVES_GOAL]->(goal5)

MERGE (duty24)-[:ESTABLISHES_MECHANISM]->(mechanism2)
MERGE (mechanism2)-[:REWARDS]->(agent8)
MERGE (mechanism2)-[:REWARDS]->(agent9)

MERGE (art17)-[:INVOLVES]->(agent1)
MERGE (art17)-[:INVOLVES]->(agent8)
MERGE (art17)-[:INVOLVES]->(agent9)

// 第十八条
MERGE (art18:Article {number: "第十八条", full_text: "农业生产中直接用于作物种植和畜禽水产养殖的设施农业用地，应当严格执行国家和省规定的用地范围和规模标准，按照规定备案，并将用地信息上传至设施农业用地监管系统。设施农业用地应当不占或者少占耕地。确需占用耕地的，应当采取措施防止破坏耕地耕作层；不再使用的，应当及时恢复种植条件。"})
MERGE (art18)-[:PART_OF]->(chapter3)

// 设施农业用地
MERGE (concept4:Object {name: "设施农业用地", type: "land_use_type", source_article: "第十八条"})
MERGE (concept5:Object {name: "耕作层", type: "soil_layer", source_article: "第十八条"})

// 用地原则
MERGE (principle4:Principle {name: "设施农业用地不占或少占耕地原则", source_article: "第十八条"})
MERGE (principle5:Principle {name: "保护耕作层原则", source_article: "第十八条"})

// 管理要求
MERGE (requirement2:Object {name: "用地范围和规模标准", type: "standard", source_article: "第十八条"})
MERGE (requirement3:Object {name: "备案要求", type: "requirement", source_article: "第十八条"})
MERGE (requirement4:Object {name: "信息上传要求", type: "requirement", source_article: "第十八条"})

// 系统与平台
MERGE (system2:System {name: "设施农业用地监管系统", purpose: "监管设施农业用地", source_article: "第十八条"})

// 义务主体
MERGE (agent10:Agent {name: "设施农业用地使用者", type: "entity"})

// 义务
MERGE (duty26:Obligation {description: "严格执行国家和省规定的用地范围和规模标准", source_article: "第十八条"})
MERGE (duty27:Obligation {description: "按照规定备案", source_article: "第十八条"})
MERGE (duty28:Obligation {description: "将用地信息上传至设施农业用地监管系统", source_article: "第十八条"})
MERGE (duty29:Obligation {description: "采取措施防止破坏耕地耕作层", source_article: "第十八条"})
MERGE (duty30:Obligation {description: "不再使用的设施农业用地应及时恢复种植条件", source_article: "第十八条"})

// 关系建立
MERGE (agent10)-[:HAS_DUTY]->(duty26)
MERGE (agent10)-[:HAS_DUTY]->(duty27)
MERGE (agent10)-[:HAS_DUTY]->(duty28)
MERGE (agent10)-[:HAS_DUTY]->(duty29)
MERGE (agent10)-[:HAS_DUTY]->(duty30)

MERGE (duty26)-[:FOLLOWS_REQUIREMENT]->(requirement2)
MERGE (duty27)-[:FOLLOWS_REQUIREMENT]->(requirement3)
MERGE (duty28)-[:FOLLOWS_REQUIREMENT]->(requirement4)
MERGE (duty28)-[:USES_SYSTEM]->(system2)

MERGE (concept4)-[:FOLLOWS_PRINCIPLE]->(principle4)
MERGE (concept4)-[:FOLLOWS_PRINCIPLE]->(principle5)

MERGE (duty29)-[:PROTECTS]->(concept5)
MERGE (duty30)-[:RESTORES]->(concept5)

MERGE (art18)-[:DEFINES_CONCEPT]->(concept4)
MERGE (art18)-[:INVOLVES]->(agent10)
MERGE (art18)-[:USES_SYSTEM]->(system2)

// 第十九条
MERGE (art19:Article {number: "第十九条", full_text: "禁止任何单位和个人在国土空间规划确定的禁止开垦的范围内从事土地开发活动。按照国土空间规划，开发未确定土地使用权的国有荒山、荒地、荒滩从事种植业、林业、畜牧业、渔业生产的，应当向土地所在地的县级人民政府自然资源主管部门提出申请，由县级人民政府批准。开发农民集体所有荒山、荒地、荒滩的，应当符合农村土地承包管理有关规定。"})
MERGE (art19)-[:PART_OF]->(chapter3)

// 禁止行为
MERGE (prohibition1:Prohibition {description: "在禁止开垦范围内从事土地开发活动", source_article: "第十九条"})
MERGE (art19)-[:DEFINES_PROHIBITION]->(prohibition1)

// 土地类型与权属关系
MERGE (land_type_gov:Object {name: "国有荒山荒地荒滩", type: "land_type", ownership: "state", source_article: "第十九条"})
MERGE (land_type_collective:Object {name: "农民集体所有荒山荒地荒滩", type: "land_type", ownership: "collective", source_article: "第十九条"})

// 细分土地类型
MERGE (wasteland_mountain:Object {name: "荒山", type: "land_subtype", source_article: "第十九条"})
MERGE (wasteland_land:Object {name: "荒地", type: "land_subtype", source_article: "第十九条"})
MERGE (wasteland_beach:Object {name: "荒滩", type: "land_subtype", source_article: "第十九条"})

// 产业类型
MERGE (industry1:Object {name: "种植业", type: "industry", source_article: "第十九条"})
MERGE (industry2:Object {name: "林业", type: "industry", source_article: "第十九条"})
MERGE (industry3:Object {name: "畜牧业", type: "industry", source_article: "第十九条"})
MERGE (industry4:Object {name: "渔业", type: "industry", source_article: "第十九条"})

// 申请审批主体
MERGE (agent11:Agent {name: "土地开发者", type: "entity"})
MERGE (agent12:Agent {name: "县级人民政府自然资源主管部门", type: "department"})
MERGE (agent13:Agent {name: "县级人民政府", type: "government_level"})

// 法规依据
MERGE (regulation1:Object {name: "农村土地承包管理规定", type: "regulation", source_article: "第十九条"})
MERGE (regulation2:Object {name: "国土空间规划"})

// 审批流程
MERGE (procedure2:Procedure {name: "国有荒山荒地荒滩开发审批流程", steps: "向土地所在地的县级人民政府自然资源主管部门提出申请，由县级人民政府批准", source_article: "第十九条"})

// 义务
MERGE (duty31:Obligation {description: "向土地所在地的县级人民政府自然资源主管部门提出申请", source_article: "第十九条"})
MERGE (duty32:Obligation {description: "符合农村土地承包管理有关规定", source_article: "第十九条"})

// 土地开发条件
MERGE (condition1:Object {name: "未确定土地使用权", type: "condition", source_article: "第十九条"})
MERGE (condition2:Object {name: "按照国土空间规划", type: "condition", source_article: "第十九条"})

// 关系建立（增强土地类型连接）
// 土地类型与细分类型关系
MERGE (land_type_gov)-[:INCLUDES]->(wasteland_mountain)
MERGE (land_type_gov)-[:INCLUDES]->(wasteland_land)
MERGE (land_type_gov)-[:INCLUDES]->(wasteland_beach)
MERGE (land_type_collective)-[:INCLUDES]->(wasteland_mountain)
MERGE (land_type_collective)-[:INCLUDES]->(wasteland_land)
MERGE (land_type_collective)-[:INCLUDES]->(wasteland_beach)

// 土地类型与权属关系
MERGE (land_type_gov)-[:HAS_OWNERSHIP]->(regulation2)
MERGE (land_type_collective)-[:GOVERNED_BY]->(regulation1)

// 土地类型与产业类型关系
MERGE (land_type_gov)-[:SUITABLE_FOR]->(industry1)
MERGE (land_type_gov)-[:SUITABLE_FOR]->(industry2)
MERGE (land_type_gov)-[:SUITABLE_FOR]->(industry3)
MERGE (land_type_gov)-[:SUITABLE_FOR]->(industry4)
MERGE (land_type_collective)-[:SUITABLE_FOR]->(industry1)
MERGE (land_type_collective)-[:SUITABLE_FOR]->(industry2)
MERGE (land_type_collective)-[:SUITABLE_FOR]->(industry3)
MERGE (land_type_collective)-[:SUITABLE_FOR]->(industry4)

// 土地开发条件与土地类型关系
MERGE (land_type_gov)-[:REQUIRES_CONDITION]->(condition1)
MERGE (land_type_gov)-[:REQUIRES_CONDITION]->(condition2)
MERGE (land_type_collective)-[:REQUIRES_CONDITION]->(condition2)

// 申请流程与土地类型关系
MERGE (procedure2)-[:APPLIES_TO]->(land_type_gov)
MERGE (procedure2)-[:REQUIRES]->(condition1)
MERGE (procedure2)-[:REQUIRES]->(condition2)

// 主体与义务关系
MERGE (agent11)-[:PROHIBITED_FROM]->(prohibition1)
MERGE (agent11)-[:HAS_DUTY]->(duty31)
MERGE (agent11)-[:HAS_DUTY]->(duty32)

// 义务与土地类型关系
MERGE (duty31)-[:APPLIES_TO]->(land_type_gov)
MERGE (duty32)-[:APPLIES_TO]->(land_type_collective)

// 义务与审批流程关系
MERGE (duty31)-[:FOLLOWS_PROCEDURE]->(procedure2)
MERGE (duty31)-[:SUBMITS_TO]->(agent12)
MERGE (agent12)-[:FORWARDS_TO]->(agent13)
MERGE (agent13)-[:HAS_AUTHORITY]->(land_type_gov)

// 文章与主体关系
MERGE (art19)-[:INVOLVES]->(agent11)
MERGE (art19)-[:INVOLVES]->(agent12)
MERGE (art19)-[:INVOLVES]->(agent13)

// 文章与土地类型关系
MERGE (art19)-[:REGULATES]->(land_type_gov)
MERGE (art19)-[:REGULATES]->(land_type_collective)
MERGE (art19)-[:REFERENCES]->(regulation1)
MERGE (art19)-[:REFERENCES]->(regulation2)

// 文章与产业类型关系
MERGE (art19)-[:COVERS_INDUSTRY]->(industry1)
MERGE (art19)-[:COVERS_INDUSTRY]->(industry2)
MERGE (art19)-[:COVERS_INDUSTRY]->(industry3)
MERGE (art19)-[:COVERS_INDUSTRY]->(industry4)

// 第二十条
MERGE (art20:Article {number: "第二十条", full_text: "省人民政府应当根据耕地总量动态平衡目标制定开垦耕地计划，由地级以上市人民政府组织实施。"})
MERGE (art20)-[:PART_OF]->(chapter3)

// 耕地开垦计划
MERGE (plan1:Object {name: "开垦耕地计划", type: "plan", source_article: "第二十条"})
MERGE (goal6:Goal {description: "耕地总量动态平衡", source_article: "第二十条"})

// 责任主体
MERGE (agent14:Agent {name: "省人民政府", type: "government_level"})
MERGE (agent15:Agent {name: "地级以上市人民政府", type: "government_level"})

// 义务
MERGE (duty33:Obligation {description: "根据耕地总量动态平衡目标制定开垦耕地计划", source_article: "第二十条"})
MERGE (duty34:Obligation {description: "组织实施开垦耕地计划", source_article: "第二十条"})

// 关系建立
MERGE (agent14)-[:HAS_DUTY]->(duty33)
MERGE (agent15)-[:HAS_DUTY]->(duty34)

MERGE (duty33)-[:AIMS_FOR]->(goal6)
MERGE (duty33)-[:CREATES_PLAN]->(plan1)
MERGE (duty34)-[:IMPLEMENTS_PLAN]->(plan1)

MERGE (art20)-[:INVOLVES]->(agent14)
MERGE (art20)-[:INVOLVES]->(agent15)

// 第二十一条
MERGE (art21:Article {number: "第二十一条", full_text: "因挖损、塌陷、压占等造成土地破坏的，用地单位和个人应当按照国家和省有关规定负责复垦。用地单位和个人用地前应当依法编制土地复垦方案，合理安排足额的土地复垦费用。县级以上人民政府自然资源主管部门应当综合考虑土地类型、预计损毁面积及程度、复垦标准、复垦用途和完成复垦任务所需的工程量等因素，根据土地复垦有关标准和要求，对土地复垦方案安排的土地复垦费用进行审查。土地复垦费用测算不足够、不合理，或者预存和使用计划不清晰的，不予通过审查。用地单位和个人应当与损毁土地所在地县级以上人民政府自然资源主管部门、银行共同签订土地复垦费用使用监管协议，明确土地复垦费用预存和使用的时间、数额、程序、条件和违约责任等，并明确支取土地复垦费用的情形。用地单位和个人应当按照土地复垦方案开展土地复垦工作。拒不履行土地复垦义务，或者复垦验收中经整改仍不合格的，依法缴纳土地复垦费。县级以上人民政府自然资源主管部门可以委托第三方机构测算土地复垦费，测算数额按照有关规定审查确定，测算费用一并计入土地复垦费。用地单位和个人未按照审查确定的数额缴纳土地复垦费，经催告仍不缴纳的，由县级以上人民政府自然资源主管部门会同有关部门代为组织复垦。所需费用由县级以上人民政府自然资源主管部门出具支取通知书，按照土地复垦费用使用监管协议约定从预存的土地复垦费用中支取，对因分期预存等原因导致不足部分可以继续向用地单位和个人追缴。"})
MERGE (art21)-[:PART_OF]->(chapter3)

// 土地复垦概念
MERGE (concept6:Object {name: "土地复垦", type: "concept", source_article: "第二十一条"})
MERGE (concept7:Object {name: "土地复垦费", type: "fee", source_article: "第二十一条"})
MERGE (concept8:Object {name: "土地复垦费用", type: "fee", source_article: "第二十一条"})

// 责任主体
MERGE (agent16:Agent {name: "用地单位和个人", type: "entity"})
MERGE (agent17:Agent {name: "县级以上人民政府自然资源主管部门", type: "department"})
MERGE (agent18:Agent {name: "银行", type: "organization"})
MERGE (agent19:Agent {name: "第三方机构", type: "organization"})

// 复垦方案
MERGE (plan2:Object {name: "土地复垦方案", type: "plan", source_article: "第二十一条"})

// 监管协议
MERGE (agreement1:Object {name: "土地复垦费用使用监管协议", type: "agreement", source_article: "第二十一条"})

// 审查标准
MERGE (criterion1:Object {name: "土地复垦费用审查标准", factors: "土地类型、预计损毁面积及程度、复垦标准、复垦用途和完成复垦任务所需的工程量等因素", source_article: "第二十一条"})

// 义务
MERGE (duty35:Obligation {description: "负责复垦被破坏的土地", source_article: "第二十一条"})
MERGE (duty36:Obligation {description: "编制土地复垦方案", source_article: "第二十一条"})
MERGE (duty37:Obligation {description: "合理安排足额的土地复垦费用", source_article: "第二十一条"})
MERGE (duty38:Obligation {description: "签订土地复垦费用使用监管协议", source_article: "第二十一条"})
MERGE (duty39:Obligation {description: "按照土地复垦方案开展土地复垦工作", source_article: "第二十一条"})
MERGE (duty40:Obligation {description: "依法缴纳土地复垦费", source_article: "第二十一条"})

// 审查义务
MERGE (duty41:Obligation {description: "对土地复垦方案安排的土地复垦费用进行审查", source_article: "第二十一条"})
MERGE (duty42:Obligation {description: "委托第三方机构测算土地复垦费", source_article: "第二十一条"})
MERGE (duty43:Obligation {description: "代为组织复垦", source_article: "第二十一条"})

// 关系建立
MERGE (agent16)-[:HAS_DUTY]->(duty35)
MERGE (agent16)-[:HAS_DUTY]->(duty36)
MERGE (agent16)-[:HAS_DUTY]->(duty37)
MERGE (agent16)-[:HAS_DUTY]->(duty38)
MERGE (agent16)-[:HAS_DUTY]->(duty39)
MERGE (agent16)-[:HAS_DUTY]->(duty40)

MERGE (agent17)-[:HAS_DUTY]->(duty41)
MERGE (agent17)-[:HAS_DUTY]->(duty42)
MERGE (agent17)-[:HAS_DUTY]->(duty43)

MERGE (duty36)-[:CREATES_PLAN]->(plan2)
MERGE (duty41)-[:FOLLOWS_CRITERION]->(criterion1)
MERGE (duty38)-[:SIGNS_AGREEMENT]->(agreement1)

MERGE (agent16)-[:PARTICIPATES_IN]->(agreement1)
MERGE (agent17)-[:PARTICIPATES_IN]->(agreement1)
MERGE (agent18)-[:PARTICIPATES_IN]->(agreement1)

MERGE (duty40)-[:PAYS_FEE]->(concept7)
MERGE (duty37)-[:ALLOWS_FEE]->(concept8)

MERGE (art21)-[:DEFINES_CONCEPT]->(concept6)
MERGE (art21)-[:INVOLVES]->(agent16)
MERGE (art21)-[:INVOLVES]->(agent17)
MERGE (art21)-[:INVOLVES]->(agent18)
MERGE (art21)-[:INVOLVES]->(agent19)

// 第二十二条
MERGE (art22:Article {number: "第二十二条", full_text: "县级以上人民政府应当加强对耕地耕作层的保护，依法对建设所占用耕地耕作层的土壤利用作出合理安排。非农业建设占用耕地的，应当编制耕作层剥离再利用方案，按照国家有关技术规范进行耕作层剥离，并按照要求将剥离的耕作层土壤用于新开垦耕地、劣质地或者其他耕地的土壤改良等。剥离相关费用作为生产成本列入建设项目投资预算。确因受到严重破坏或者严重污染等无法剥离再利用的，经县级人民政府同意后方可不实施剥离。鼓励依托公共资源交易平台，探索剥离耕作层土壤交易。"})
MERGE (art22)-[:PART_OF]->(chapter3)

// 耕作层保护核心概念
MERGE (concept9:Object {name: "耕地耕作层", type: "soil_layer", source_article: "第二十二条"})
MERGE (concept10:Object {name: "耕作层剥离再利用", type: "concept", source_article: "第二十二条"})
MERGE (concept11:Object {name: "耕作层土壤", type: "soil_type", source_article: "第二十二条"})

// 保护主体
MERGE (agent20:Agent {name: "非农业建设单位", type: "entity"})
MERGE (agent21:Agent {name: "县级人民政府", type: "government_level"})

// 保护方案与方法
MERGE (plan3:Object {name: "耕作层剥离再利用方案", type: "plan", source_article: "第二十二条"})
MERGE (method4:Object {name: "耕作层剥离", type: "protection_method", source_article: "第二十二条"})
MERGE (method5:Object {name: "土壤改良", type: "improvement_method", source_article: "第二十二条"})

// 技术规范
MERGE (standard1:Object {name: "国家有关技术规范", type: "standard", source_article: "第二十二条"})

// 土壤利用去向
MERGE (land_use1:Object {name: "新开垦耕地", type: "land_use", source_article: "第二十二条"})
MERGE (land_use2:Object {name: "劣质地", type: "land_use", source_article: "第二十二条"})
MERGE (land_use3:Object {name: "其他耕地", type: "land_use", source_article: "第二十二条"})

// 费用管理
MERGE (cost1:Object {name: "剥离相关费用", type: "cost", source_article: "第二十二条"})
MERGE (budget1:Object {name: "建设项目投资预算", type: "budget", source_article: "第二十二条"})

// 例外情况
MERGE (exception1:Object {name: "严重破坏", type: "exception_condition", source_article: "第二十二条"})
MERGE (exception2:Object {name: "严重污染", type: "exception_condition", source_article: "第二十二条"})
MERGE (exception3:Object {name: "无法剥离再利用", type: "exception_condition", source_article: "第二十二条"})

// 交易平台
MERGE (platform1:Object {name: "公共资源交易平台", type: "platform", purpose: "耕作层土壤交易", source_article: "第二十二条"})
MERGE (transaction1:Object {name: "剥离耕作层土壤交易", type: "transaction_type", source_article: "第二十二条"})

// 保护义务
MERGE (duty44:Obligation {description: "加强对耕地耕作层的保护", source_article: "第二十二条"})
MERGE (duty45:Obligation {description: "对建设所占用耕地耕作层的土壤利用作出合理安排", source_article: "第二十二条"})
MERGE (duty46:Obligation {description: "编制耕作层剥离再利用方案", source_article: "第二十二条"})
MERGE (duty47:Obligation {description: "按照国家有关技术规范进行耕作层剥离", source_article: "第二十二条"})
MERGE (duty48:Obligation {description: "将剥离的耕作层土壤用于新开垦耕地、劣质地或者其他耕地的土壤改良等", source_article: "第二十二条"})
MERGE (duty49:Obligation {description: "将剥离相关费用作为生产成本列入建设项目投资预算", source_article: "第二十二条"})
MERGE (duty52:Obligation {description: "经县级人民政府同意后方可不实施剥离", condition: "确因受到严重破坏或者严重污染等无法剥离再利用", source_article: "第二十二条"})

// 鼓励措施
MERGE (encourage1:Object {name: "探索剥离耕作层土壤交易", type: "encouragement", source_article: "第二十二条"})

// 关系建立（全面连接各实体）
// 政府保护责任关系
MERGE (agent2)-[:HAS_DUTY]->(duty44)
MERGE (agent2)-[:HAS_DUTY]->(duty45)
MERGE (duty44)-[:PROTECTS]->(concept9)
MERGE (duty45)-[:MANAGES]->(concept11)

// 非农业建设单位义务关系
MERGE (agent20)-[:HAS_DUTY]->(duty46)
MERGE (agent20)-[:HAS_DUTY]->(duty47)
MERGE (agent20)-[:HAS_DUTY]->(duty48)
MERGE (agent20)-[:HAS_DUTY]->(duty49)
MERGE (agent20)-[:HAS_DUTY]->(duty52)

// 方案与方法关系
MERGE (duty46)-[:CREATES_PLAN]->(plan3)
MERGE (plan3)-[:USES_METHOD]->(method4)
MERGE (method4)-[:PROTECTS]->(concept9)
MERGE (duty47)-[:FOLLOWS_STANDARD]->(standard1)

// 土壤利用关系
MERGE (duty48)-[:USES_SOIL]->(concept11)
MERGE (duty48)-[:USES_METHOD]->(method5)
MERGE (concept11)-[:USED_FOR_IMPROVEMENT_OF]->(land_use1)
MERGE (concept11)-[:USED_FOR_IMPROVEMENT_OF]->(land_use2)
MERGE (concept11)-[:USED_FOR_IMPROVEMENT_OF]->(land_use3)
MERGE (method5)-[:IMPROVES]->(land_use1)
MERGE (method5)-[:IMPROVES]->(land_use2)
MERGE (method5)-[:IMPROVES]->(land_use3)

// 费用管理关系
MERGE (duty49)-[:ALLOWS_COST]->(cost1)
MERGE (cost1)-[:INCLUDED_IN]->(budget1)
MERGE (budget1)-[:BELONGS_TO]->(agent20)

// 例外情况关系
MERGE (exception1)-[:LEADS_TO]->(exception3)
MERGE (exception2)-[:LEADS_TO]->(exception3)
MERGE (exception3)-[:REQUIRES_APPROVAL_FROM]->(agent21)
MERGE (duty52)-[:TRIGGERED_BY]->(exception3)
MERGE (duty52)-[:REQUIRES_APPROVAL_FROM]->(agent21)

// 交易平台关系
MERGE (platform1)-[:SUPPORTS]->(transaction1)
MERGE (transaction1)-[:TRADES]->(concept11)
MERGE (art22)-[:ENCOURAGES]->(encourage1)
MERGE (encourage1)-[:USES_PLATFORM]->(platform1)
MERGE (encourage1)-[:PROMOTES]->(transaction1)

// 文章与主体关系
MERGE (art22)-[:INVOLVES]->(agent2)
MERGE (art22)-[:INVOLVES]->(agent20)
MERGE (art22)-[:INVOLVES]->(agent21)

// 文章与核心概念关系
MERGE (art22)-[:DEFINES_CONCEPT]->(concept9)
MERGE (art22)-[:DEFINES_CONCEPT]->(concept10)
MERGE (art22)-[:DEFINES_CONCEPT]->(concept11)

// 文章与平台关系
MERGE (art22)-[:USES_PLATFORM]->(platform1)
MERGE (art22)-[:PROMOTES_TRANSACTION]->(transaction1)

// 第二十三条
MERGE (art23:Article {number: "第二十三条", full_text: "各级人民政府应当加强对耕地质量的保护和提升，任何单位和个人不得损毁耕地种植条件。因人为因素损毁耕地种植条件需要进行技术鉴定的，行政机关、当事人或者其他利害关系人可以向具备鉴定能力的机构或者县级以上人民政府农业农村等相关主管部门申请。"})
MERGE (art23)-[:PART_OF]->(chapter3)

// 耕地质量保护
MERGE (concept13:Object {name: "耕地种植条件", type: "concept", source_article: "第二十三条"})
MERGE (concept12:Object {name: "耕地质量", type: "concept", source_article: "第二十三条"})

// 禁止行为
MERGE (prohibition2:Prohibition {description: "损毁耕地种植条件", source_article: "第二十三条"})

// 技术鉴定
MERGE (service1:Object {name: "耕地种植条件技术鉴定", type: "service", source_article: "第二十三条"})

// 申请主体
MERGE (applicant1:Agent {name: "行政机关", type: "entity"})
MERGE (applicant2:Agent {name: "当事人", type: "person"})
MERGE (applicant3:Agent {name: "利害关系人", type: "entity"})
MERGE (applicant4:Agent {name: "县级以上人民政府农业农村主管部门", type: "department"})

// 保护义务
MERGE (duty50:Obligation {description: "加强对耕地质量的保护和提升", source_article: "第二十三条"})
MERGE (duty51:Obligation {description: "不得损毁耕地种植条件", source_article: "第二十三条"})

// 申请权利
MERGE (right1:Right {description: "向具备鉴定能力的机构或者县级以上人民政府农业农村等相关主管部门申请技术鉴定", source_article: "第二十三条"})

// 关系建立
MERGE (agent1)-[:HAS_DUTY]->(duty50)
MERGE (agent1)-[:HAS_DUTY]->(duty51)
MERGE (applicant1)-[:HAS_RIGHT]->(right1)
MERGE (applicant2)-[:HAS_RIGHT]->(right1)
MERGE (applicant3)-[:HAS_RIGHT]->(right1)

MERGE (applicant1)-[:PROHIBITED_FROM]->(prohibition2)
MERGE (applicant2)-[:PROHIBITED_FROM]->(prohibition2)
MERGE (applicant3)-[:PROHIBITED_FROM]->(prohibition2)

MERGE (duty50)-[:PROTECTS]->(concept12)
MERGE (duty51)-[:PROTECTS]->(concept12)
MERGE (right1)-[:REQUESTS_SERVICE]->(service1)
MERGE (service1)-[:RELATED_TO]->(concept13)

MERGE (art23)-[:INVOLVES]->(agent1)
MERGE (art23)-[:INVOLVES]->(applicant1)
MERGE (art23)-[:INVOLVES]->(applicant2)
MERGE (art23)-[:INVOLVES]->(applicant3)
MERGE (art23)-[:INVOLVES]->(applicant4)





























// 第四章
// 创建第四章节点（确保文档节点已存在）
MATCH (doc:Document {name: "广东省土地管理条例"})
MERGE (chapter4:Chapter {number: "第四章", title: "农用地转用和土地征收"})
MERGE (chapter4)-[:PART_OF]->(doc)

// 第二十四条
MERGE (art24:Article {number: "第二十四条", full_text: "建设占用土地涉及农用地转为建设用地的，应当办理农用地转用审批手续；涉及征收土地的，应当同时提出征收土地申请，报有批准权的人民政府批准。农用地转用、征收土地依法由省人民政府批准或者审核上报的，应当先经地级以上市人民政府审核。"})
MERGE (art24)-[:PART_OF]->(chapter4)

// 土地类型
MERGE (land_type1:Object {name: "农用地", type: "land_type", source_article: "第二十四条"})
MERGE (land_type2:Object {name: "建设用地", type: "land_type", source_article: "第二十四条"})

// 审批主体
MERGE (agent22:Agent {name: "有批准权的人民政府", type: "government_level"})
MERGE (agent23:Agent {name: "省人民政府", type: "government_level"})
MERGE (agent24:Agent {name: "地级以上市人民政府", type: "government_level"})

// 审批程序
MERGE (procedure3:Object {name: "农用地转用审批手续", type: "procedure", source_article: "第二十四条"})
MERGE (procedure4:Object {name: "征收土地申请", type: "procedure", source_article: "第二十四条"})
MERGE (procedure5:Object {name: "审核程序", type: "procedure", source_article: "第二十四条"})

// 义务
MERGE (duty53:Obligation {description: "办理农用地转用审批手续", source_article: "第二十四条"})
MERGE (duty54:Obligation {description: "提出征收土地申请", source_article: "第二十四条"})
MERGE (duty55:Obligation {description: "先经地级以上市人民政府审核", condition: "农用地转用、征收土地依法由省人民政府批准或者审核上报", source_article: "第二十四条"})

// 关系建立
MERGE (agent22)-[:HAS_AUTHORITY]->(procedure3)
MERGE (agent22)-[:HAS_AUTHORITY]->(procedure4)
MERGE (agent23)-[:HAS_DUTY]->(duty55)
MERGE (agent24)-[:PERFORMS]->(procedure5)

MERGE (procedure3)-[:CONVERTS]->(land_type1)
MERGE (procedure3)-[:TO]->(land_type2)
MERGE (procedure4)-[:INVOLVES]->(land_type1)

MERGE (duty53)-[:FOLLOWS_PROCEDURE]->(procedure3)
MERGE (duty54)-[:FOLLOWS_PROCEDURE]->(procedure4)
MERGE (duty55)-[:FOLLOWS_PROCEDURE]->(procedure5)

MERGE (procedure5)-[:REQUIRED_BEFORE]->(procedure3)
MERGE (procedure5)-[:REQUIRED_BEFORE]->(procedure4)
MERGE (procedure5)-[:PERFORMED_BY]->(agent24)
MERGE (procedure5)-[:REQUIRED_FOR]->(agent23)

MERGE (art24)-[:REGULATES_PROCEDURE]->(procedure3)
MERGE (art24)-[:REGULATES_PROCEDURE]->(procedure4)
MERGE (art24)-[:INVOLVES]->(agent22)
MERGE (art24)-[:INVOLVES]->(agent23)
MERGE (art24)-[:INVOLVES]->(agent24)

// 第二十五条
MERGE (art25:Article {number: "第二十五条", full_text: "建设占用未利用地的，应当办理未利用地转用审批手续，由地级以上市人民政府批准；同时占用农用地和未利用地的，由农用地转用批准机关一并审批。"})
MERGE (art25)-[:PART_OF]->(chapter4)


MERGE (land_type3:Object {name: "审批占用未利用地", type: "land_type", source_article: "第二十五条"})
MERGE (land_type4:Object {name: "审批同时占用农用地和未利用地的", type: "land_type", source_article: "第二十五条"})
MERGE (agent56:Agent {name: "农用地转用批准机关", type: "government_level"})

// 审批程序
MERGE (procedure6:Object {name: "未利用地转用审批手续", type: "procedure", source_article: "第二十五条"})

// 义务
MERGE (duty56:Obligation {description: "办理未利用地转用审批手续", source_article: "第二十五条"})

// 关系建立
MERGE (agent24)-[:HAS_AUTHORITY]->(procedure6)
MERGE (agent24)-[:HAS_AUTHORITY]->(land_type3)
MERGE (duty56)-[:FOLLOWS_PROCEDURE]->(procedure6)
MERGE (procedure6)-[:CONVERTS]->(land_type3)
MERGE (procedure6)-[:TO]->(land_type2)
MERGE (agent56)-[:HAS_AUTHORITY]->(land_type4)

// 一并审批机制
MERGE (mechanism3:Object {name: "一并审批机制", type: "mechanism", source_article: "第二十五条"})
MERGE (mechanism3)-[:HANDLES]->(procedure3)
MERGE (mechanism3)-[:HANDLES]->(procedure6)
MERGE (procedure3)-[:APPROVING_AUTHORITY_HANDLES]->(mechanism3)

MERGE (art25)-[:REGULATES_PROCEDURE]->(procedure6)
MERGE (art25)-[:INVOLVES]->(agent24)
MERGE (art25)-[:INVOLVES]->(agent56)
MERGE (art25)-[:USES_MECHANISM]->(mechanism3)

// 第二十六条
MERGE (art26:Article {number: "第二十六条", full_text: "为了公共利益的需要征收土地的，县级以上人民政府应当依法完成征收土地预公告、土地现状调查及结果确认、社会稳定风险评估、征地补偿安置公告、征地补偿登记、征地补偿安置协议签订等前期工作后，方可提出征收土地申请。涉及成片开发建设需要征收土地的，应当编制土地征收成片开发方案。"})
MERGE (art26)-[:PART_OF]->(chapter4)

// 征收主体
MERGE (agent25:Agent {name: "县级以上人民政府", type: "government_level"})

// 征收前期工作
MERGE (task1:Object {name: "征收土地预公告", type: "task", source_article: "第二十六条"})
MERGE (task2:Object {name: "土地现状调查及结果确认", type: "task", source_article: "第二十六条"})
MERGE (task3:Object {name: "社会稳定风险评估", type: "task", source_article: "第二十六条"})
MERGE (task4:Object {name: "征地补偿安置公告", type: "task", source_article: "第二十六条"})
MERGE (task5:Object {name: "征地补偿登记", type: "task", source_article: "第二十六条"})
MERGE (task6:Object {name: "征地补偿安置协议签订", type: "task", source_article: "第二十六条"})

// 征收目的
MERGE (purpose1:Object {name: "公共利益需要", type: "purpose", source_article: "第二十六条"})

// 特殊征收类型
MERGE (plan4:Object {name: "土地征收成片开发方案", type: "plan", source_article: "第二十六条"})
MERGE (condition3:Object {name: "成片开发建设需要", type: "condition", source_article: "第二十六条"})

// 征收前置条件
MERGE (condition4:Object {name: "完成前期工作", type: "condition", source_article: "第二十六条"})

// 义务
MERGE (duty57:Obligation {description: "完成征收土地前期工作", source_article: "第二十六条"})
MERGE (duty58:Obligation {description: "编制土地征收成片开发方案", condition: "涉及成片开发建设需要征收土地", source_article: "第二十六条"})

// 关系建立
MERGE (agent25)-[:HAS_DUTY]->(duty57)
MERGE (agent25)-[:HAS_DUTY]->(duty58)

MERGE (duty57)-[:INCLUDES_TASK]->(task1)
MERGE (duty57)-[:INCLUDES_TASK]->(task2)
MERGE (duty57)-[:INCLUDES_TASK]->(task3)
MERGE (duty57)-[:INCLUDES_TASK]->(task4)
MERGE (duty57)-[:INCLUDES_TASK]->(task5)
MERGE (duty57)-[:INCLUDES_TASK]->(task6)

MERGE (duty57)-[:REQUIRED_BEFORE]->(procedure4)
MERGE (procedure4)-[:REQUIRES_CONDITION]->(condition4)

MERGE (task1)-[:SERVES_PURPOSE]->(purpose1)
MERGE (task2)-[:SERVES_PURPOSE]->(purpose1)
MERGE (task3)-[:SERVES_PURPOSE]->(purpose1)
MERGE (task4)-[:SERVES_PURPOSE]->(purpose1)
MERGE (task5)-[:SERVES_PURPOSE]->(purpose1)
MERGE (task6)-[:SERVES_PURPOSE]->(purpose1)

MERGE (duty58)-[:REQUIRED_WHEN]->(condition3)
MERGE (duty58)-[:CREATES_PLAN]->(plan4)
MERGE (plan4)-[:REQUIRED_FOR]->(procedure4)

MERGE (art26)-[:INVOLVES]->(agent25)
MERGE (art26)-[:REGULATES_PROCEDURE]->(procedure4)
MERGE (art26)-[:DEFINES_TASK]->(task1)
MERGE (art26)-[:DEFINES_TASK]->(task2)
MERGE (art26)-[:DEFINES_TASK]->(task3)
MERGE (art26)-[:DEFINES_TASK]->(task4)
MERGE (art26)-[:DEFINES_TASK]->(task5)
MERGE (art26)-[:DEFINES_TASK]->(task6)

// 第二十七条
MERGE (art27:Article {number: "第二十七条", full_text: "征收土地应当依法预公告，采用书面张贴、网站公开、信息推送或者上户送达等多种有利于社会公众知晓的方式，在拟征收土地所在的乡镇和村、村民小组范围内发布，预公告时间不少于十个工作日，并采取拍照、录像、公证等方式留存记录。"})
MERGE (art27)-[:PART_OF]->(chapter4)

// 公告方式
MERGE (method6:Object {name: "书面张贴", type: "announcement_method", source_article: "第二十七条"})
MERGE (method7:Object {name: "网站公开", type: "announcement_method", source_article: "第二十七条"})
MERGE (method8:Object {name: "信息推送", type: "announcement_method", source_article: "第二十七条"})
MERGE (method9:Object {name: "上户送达", type: "announcement_method", source_article: "第二十七条"})

// 公告范围
MERGE (scope1:Object {name: "乡镇和村、村民小组范围", type: "announcement_scope", source_article: "第二十七条"})

// 公告要求
MERGE (requirement5:Object {name: "预公告时间不少于十个工作日", type: "time_requirement", source_article: "第二十七条"})
MERGE (requirement6:Object {name: "采取拍照、录像、公证等方式留存记录", type: "record_requirement", source_article: "第二十七条、第三十条、第三十四条"})

// 义务
MERGE (duty59:Obligation {description: "依法进行征收土地预公告", source_article: "第二十七条"})
MERGE (duty60:Obligation {description: "采用多种有利于社会公众知晓的方式发布预公告", source_article: "第二十七条"})
MERGE (duty61:Obligation {description: "在规定范围内发布预公告", source_article: "第二十七条"})
MERGE (duty62:Obligation {description: "确保预公告时间不少于十个工作日", source_article: "第二十七条"})

// 关系建立
MERGE (agent25)-[:HAS_DUTY]->(duty59)
MERGE (agent25)-[:HAS_DUTY]->(duty60)
MERGE (agent25)-[:HAS_DUTY]->(duty61)
MERGE (agent25)-[:HAS_DUTY]->(duty62)
MERGE (agent25)-[:HAS_DUTY]->(requirement6)

MERGE (duty59)-[:INCLUDES_TASK]->(task1)
MERGE (duty60)-[:USES_METHOD]->(method6)
MERGE (duty60)-[:USES_METHOD]->(method7)
MERGE (duty60)-[:USES_METHOD]->(method8)
MERGE (duty60)-[:USES_METHOD]->(method9)

MERGE (duty61)-[:APPLIES_TO_SCOPE]->(scope1)
MERGE (duty62)-[:MEETS_REQUIREMENT]->(requirement5)

MERGE (task1)-[:USES_METHOD]->(method6)
MERGE (task1)-[:USES_METHOD]->(method7)
MERGE (task1)-[:USES_METHOD]->(method8)
MERGE (task1)-[:USES_METHOD]->(method9)
MERGE (task1)-[:APPLIES_TO_SCOPE]->(scope1)
MERGE (task1)-[:HAS_TIME_REQUIREMENT]->(requirement5)
MERGE (task1)-[:HAS_RECORD_REQUIREMENT]->(requirement6)

MERGE (art27)-[:DEFINES_TASK]->(task1)
MERGE (art27)-[:INVOLVES]->(agent25)

// 第二十八条
MERGE (art28:Article {number: "第二十八条", full_text: "土地现状调查由县级以上人民政府组织有关部门或者乡镇人民政府开展。调查结果应当由拟征收土地的所有权人、使用权人予以确认。个别土地所有权人、使用权人因客观原因无法确认或者拒不确认的，有关部门或者乡镇人民政府应当在调查结果中注明原因，对调查结果采取见证、公证等方式留存记录，并在拟征收土地所在的乡镇和村、村民小组范围内公示，时间不少于十个工作日。公示期间有异议的，应当及时核查处理。"})
MERGE (art28)-[:PART_OF]->(chapter4)

// 调查主体
MERGE (agent26:Agent {name: "有关部门", type: "department"})
MERGE (agent27:Agent {name: "乡镇人民政府", type: "government_level"})

// 调查对象
MERGE (agent28:Agent {name: "土地所有权人", type: "rights_holder"})
MERGE (agent29:Agent {name: "土地使用权人", type: "rights_holder"})

// 调查方法
MERGE (method10:Object {name: "见证", type: "record_method", source_article: "第二十八条"})
MERGE (method11:Object {name: "公证", type: "record_method", source_article: "第二十八条"})

// 公示要求
MERGE (requirement7:Object {name: "公示时间不少于十个工作日", type: "time_requirement", source_article: "第二十八条"})
MERGE (requirement8:Object {name: "及时核查处理异议", type: "handling_requirement", source_article: "第二十八条"})

// 特殊情况
MERGE (exception4:Object {name: "因客观原因无法确认", type: "exception_condition", source_article: "第二十八条"})
MERGE (exception5:Object {name: "拒不确认", type: "exception_condition", source_article: "第二十八条"})

// 义务
MERGE (duty64:Obligation {description: "组织开展土地现状调查", source_article: "第二十八条"})
MERGE (duty65:Obligation {description: "确认调查结果", source_article: "第二十八条"})
MERGE (duty66:Obligation {description: "在调查结果中注明无法确认或拒不确认的原因", condition: "个别土地所有权人、使用权人因客观原因无法确认或者拒不确认", source_article: "第二十八条"})
MERGE (duty67:Obligation {description: "对调查结果采取见证、公证等方式留存记录", condition: "个别土地所有权人、使用权人因客观原因无法确认或者拒不确认", source_article: "第二十八条"})
MERGE (duty68:Obligation {description: "在规定范围内公示调查结果", condition: "个别土地所有权人、使用权人因客观原因无法确认或者拒不确认", source_article: "第二十八条"})
MERGE (duty69:Obligation {description: "及时核查处理公示期间的异议", source_article: "第二十八条"})

// 关系建立
MERGE (agent25)-[:HAS_DUTY]->(duty64)
MERGE (agent26)-[:PARTICIPATES_IN]->(duty64)
MERGE (agent27)-[:PARTICIPATES_IN]->(duty64)

MERGE (agent28)-[:HAS_DUTY]->(duty65)
MERGE (agent29)-[:HAS_DUTY]->(duty65)

MERGE (agent26)-[:HAS_DUTY]->(duty66)
MERGE (agent27)-[:HAS_DUTY]->(duty66)
MERGE (agent26)-[:HAS_DUTY]->(duty67)
MERGE (agent27)-[:HAS_DUTY]->(duty67)
MERGE (agent26)-[:HAS_DUTY]->(duty68)
MERGE (agent27)-[:HAS_DUTY]->(duty68)
MERGE (agent26)-[:HAS_DUTY]->(duty69)
MERGE (agent27)-[:HAS_DUTY]->(duty69)

MERGE (duty64)-[:INCLUDES_TASK]->(task2)
MERGE (task2)-[:INVOLVES]->(agent28)
MERGE (task2)-[:INVOLVES]->(agent29)

MERGE (duty66)-[:TRIGGERED_BY]->(exception4)
MERGE (duty66)-[:TRIGGERED_BY]->(exception5)
MERGE (duty67)-[:TRIGGERED_BY]->(exception4)
MERGE (duty67)-[:TRIGGERED_BY]->(exception5)
MERGE (duty68)-[:TRIGGERED_BY]->(exception4)
MERGE (duty68)-[:TRIGGERED_BY]->(exception5)

MERGE (duty67)-[:USES_METHOD]->(method10)
MERGE (duty67)-[:USES_METHOD]->(method11)

MERGE (duty68)-[:APPLIES_TO_SCOPE]->(scope1)
MERGE (duty68)-[:MEETS_REQUIREMENT]->(requirement7)

MERGE (duty69)-[:MEETS_REQUIREMENT]->(requirement8)

MERGE (task2)-[:HAS_EXCEPTION]->(exception4)
MERGE (task2)-[:HAS_EXCEPTION]->(exception5)
MERGE (task2)-[:USES_METHOD]->(method10)
MERGE (task2)-[:USES_METHOD]->(method11)
MERGE (task2)-[:HAS_SCOPE]->(scope1)
MERGE (task2)-[:HAS_TIME_REQUIREMENT]->(requirement7)
MERGE (task2)-[:HAS_HANDLING_REQUIREMENT]->(requirement8)

MERGE (art28)-[:DEFINES_TASK]->(task2)
MERGE (art28)-[:INVOLVES]->(agent25)
MERGE (art28)-[:INVOLVES]->(agent26)
MERGE (art28)-[:INVOLVES]->(agent27)
MERGE (art28)-[:INVOLVES]->(agent28)
MERGE (art28)-[:INVOLVES]->(agent29)

// 第二十九条
MERGE (art29:Article {number: "第二十九条", full_text: "社会稳定风险评估由县级以上人民政府组织有关部门或者委托第三方机构开展，针对拟征收土地社会稳定风险状况进行综合研判，确定风险点，提出风险防范措施和处置预案，形成评估报告。社会稳定风险评估应当有被征地的农村集体经济组织及其成员、村民委员会和其他利害关系人参加，充分听取其意见。"})
MERGE (art29)-[:PART_OF]->(chapter4)

// 评估主体
MERGE (agent30:Agent {name: "第三方机构", type: "organization"})

// 评估参与方
MERGE (agent31:Agent {name: "被征地的农村集体经济组织", type: "organization"})
MERGE (agent32:Agent {name: "农村集体经济组织成员", type: "person"})
MERGE (agent33:Agent {name: "村民委员会", type: "organization"})
MERGE (agent34:Agent {name: "其他利害关系人", type: "person"})

// 评估内容
MERGE (content1:Object {name: "社会稳定风险状况综合研判", type: "assessment_content", source_article: "第二十九条"})
MERGE (content2:Object {name: "确定风险点", type: "assessment_content", source_article: "第二十九条"})
MERGE (content3:Object {name: "提出风险防范措施", type: "assessment_content", source_article: "第二十九条"})
MERGE (content4:Object {name: "提出处置预案", type: "assessment_content", source_article: "第二十九条"})
MERGE (content5:Object {name: "形成评估报告", type: "assessment_content", source_article: "第二十九条"})

// 评估要求
MERGE (requirement9:Object {name: "充分听取参与方意见", type: "participation_requirement", source_article: "第二十九条"})

// 义务
MERGE (duty70:Obligation {description: "组织开展社会稳定风险评估", source_article: "第二十九条"})
MERGE (duty71:Obligation {description: "委托第三方机构开展评估", option: true, source_article: "第二十九条"})
MERGE (duty72:Obligation {description: "确保相关方参与评估过程", source_article: "第二十九条"})
MERGE (duty73:Obligation {description: "充分听取参与方意见", source_article: "第二十九条"})

// 关系建立
MERGE (agent25)-[:HAS_DUTY]->(duty70)
MERGE (agent25)-[:HAS_OPTION]->(duty71)
MERGE (agent25)-[:HAS_DUTY]->(duty72)
MERGE (agent25)-[:HAS_DUTY]->(duty73)

MERGE (agent26)-[:PARTICIPATES_IN]->(duty70)
MERGE (agent30)-[:CONDUCTS]->(duty70)

MERGE (agent31)-[:PARTICIPATES_IN]->(duty72)
MERGE (agent32)-[:PARTICIPATES_IN]->(duty72)
MERGE (agent33)-[:PARTICIPATES_IN]->(duty72)
MERGE (agent34)-[:PARTICIPATES_IN]->(duty72)

MERGE (duty70)-[:INCLUDES_TASK]->(task3)
MERGE (task3)-[:INCLUDES_CONTENT]->(content1)
MERGE (task3)-[:INCLUDES_CONTENT]->(content2)
MERGE (task3)-[:INCLUDES_CONTENT]->(content3)
MERGE (task3)-[:INCLUDES_CONTENT]->(content4)
MERGE (task3)-[:INCLUDES_CONTENT]->(content5)

MERGE (duty73)-[:MEETS_REQUIREMENT]->(requirement9)
MERGE (task3)-[:HAS_REQUIREMENT]->(requirement9)

MERGE (art29)-[:DEFINES_TASK]->(task3)
MERGE (art29)-[:INVOLVES]->(agent25)
MERGE (art29)-[:INVOLVES]->(agent26)
MERGE (art29)-[:INVOLVES]->(agent30)
MERGE (art29)-[:INVOLVES]->(agent31)
MERGE (art29)-[:INVOLVES]->(agent32)
MERGE (art29)-[:INVOLVES]->(agent33)
MERGE (art29)-[:INVOLVES]->(agent34)

// 第三十条
MERGE (art30:Article {number: "第三十条", full_text: "依法拟定的征地补偿安置方案，应当在拟征收土地所在的乡镇和村、村民小组范围内进行公告，听取被征地的农村集体经济组织及其成员、村民委员会和其他利害关系人的意见。公告时间不少于三十日，并采取拍照、录像、公证等方式留存记录。公告应当载明办理补偿登记的方式和期限、不办理补偿登记的后果以及异议反馈渠道等内容。征地补偿安置公告期满，过半数被征地的农村集体经济组织成员对征地补偿安置方案有异议或者县级以上人民政府认为确有必要的，应当组织召开听证会。方案需要修改的，修改后重新公告，公告时间不少于十个工作日，并重新载明办理补偿登记期限；方案无需修改的，应当公布不修改的理由。"})
MERGE (art30)-[:PART_OF]->(chapter4)

// 公告内容
MERGE (content6:Object {name: "办理补偿登记的方式和期限", type: "announcement_content", source_article: "第三十条"})
MERGE (content7:Object {name: "不办理补偿登记的后果", type: "announcement_content", source_article: "第三十条"})
MERGE (content8:Object {name: "异议反馈渠道", type: "announcement_content", source_article: "第三十条"})

// 公告要求
MERGE (requirement10:Object {name: "公告时间不少于三十日", type: "time_requirement", source_article: "第三十条"})

// 听证条件
MERGE (condition5:Object {name: "过半数被征地的农村集体经济组织成员有异议", type: "hearing_condition", source_article: "第三十条"})
MERGE (condition6:Object {name: "县级以上人民政府认为确有必要", type: "hearing_condition", source_article: "第三十条"})

// 听证后续
MERGE (consequence1:Object {name: "方案需要修改", type: "hearing_consequence", source_article: "第三十条"})
MERGE (consequence2:Object {name: "方案无需修改", type: "hearing_consequence", source_article: "第三十条"})

// 修改方案要求
MERGE (requirement12:Object {name: "修改后重新公告", type: "modification_requirement", source_article: "第三十条"})
MERGE (requirement13:Object {name: "重新公告时间不少于十个工作日", type: "time_requirement", source_article: "第三十条"})
MERGE (requirement14:Object {name: "重新载明办理补偿登记期限", type: "content_requirement", source_article: "第三十条"})
MERGE (requirement15:Object {name: "公布不修改的理由", type: "disclosure_requirement", source_article: "第三十条"})

// 义务
MERGE (duty74:Obligation {description: "公告征地补偿安置方案", source_article: "第三十条"})
MERGE (duty75:Obligation {description: "在规定范围内公告方案", source_article: "第三十条"})
MERGE (duty76:Obligation {description: "确保公告时间不少于三十日", source_article: "第三十条"})
MERGE (duty78:Obligation {description: "载明公告必要内容", source_article: "第三十条"})
MERGE (duty79:Obligation {description: "组织召开听证会", condition: "征地补偿安置公告期满，过半数被征地的农村集体经济组织成员对征地补偿安置方案有异议或者县级以上人民政府认为确有必要", source_article: "第三十条"})
MERGE (duty80:Obligation {description: "修改方案并重新公告", condition: "方案需要修改", source_article: "第三十条"})
MERGE (duty81:Obligation {description: "公布不修改的理由", condition: "方案无需修改", source_article: "第三十条"})

// 关系建立
MERGE (agent25)-[:HAS_DUTY]->(duty74)
MERGE (agent25)-[:HAS_DUTY]->(duty75)
MERGE (agent25)-[:HAS_DUTY]->(duty76)
MERGE (agent25)-[:HAS_DUTY]->(requirement6)
MERGE (agent25)-[:HAS_DUTY]->(duty78)
MERGE (agent25)-[:HAS_DUTY]->(duty79)
MERGE (agent25)-[:HAS_DUTY]->(duty80)
MERGE (agent25)-[:HAS_DUTY]->(duty81)

MERGE (duty74)-[:INCLUDES_TASK]->(task4)
MERGE (duty75)-[:APPLIES_TO_SCOPE]->(scope1)
MERGE (duty76)-[:MEETS_REQUIREMENT]->(requirement10)
MERGE (requirement6)-[:MEETS_REQUIREMENT]->(requirement6)
MERGE (duty78)-[:INCLUDES_CONTENT]->(content6)
MERGE (duty78)-[:INCLUDES_CONTENT]->(content7)
MERGE (duty78)-[:INCLUDES_CONTENT]->(content8)

MERGE (task4)-[:HAS_SCOPE]->(scope1)
MERGE (task4)-[:HAS_TIME_REQUIREMENT]->(requirement10)
MERGE (task4)-[:HAS_RECORD_REQUIREMENT]->(requirement6)
MERGE (task4)-[:HAS_CONTENT]->(content6)
MERGE (task4)-[:HAS_CONTENT]->(content7)
MERGE (task4)-[:HAS_CONTENT]->(content8)

MERGE (duty79)-[:TRIGGERED_BY]->(condition5)
MERGE (duty79)-[:TRIGGERED_BY]->(condition6)
MERGE (condition5)-[:INVOLVES]->(agent32)
MERGE (condition6)-[:DECIDED_BY]->(agent25)

MERGE (duty79)-[:LEADS_TO]->(consequence1)
MERGE (duty79)-[:LEADS_TO]->(consequence2)
MERGE (consequence1)-[:TRIGGERS]->(duty80)
MERGE (consequence2)-[:TRIGGERS]->(duty81)

MERGE (duty80)-[:MEETS_REQUIREMENT]->(requirement12)
MERGE (duty80)-[:MEETS_REQUIREMENT]->(requirement13)
MERGE (duty80)-[:MEETS_REQUIREMENT]->(requirement14)

MERGE (art30)-[:DEFINES_TASK]->(task4)
MERGE (art30)-[:INVOLVES]->(agent25)
MERGE (art30)-[:INVOLVES]->(agent31)
MERGE (art30)-[:INVOLVES]->(agent32)
MERGE (art30)-[:INVOLVES]->(agent33)
MERGE (art30)-[:INVOLVES]->(agent34)

// 第三十一条
MERGE (art31:Article {number: "第三十一条", full_text: "拟征收土地的所有权人、使用权人应当在公告载明的办理补偿登记期限内，持不动产权属证明材料办理补偿登记；规定期限内未办理补偿登记的，相关情况按照经确认或者公示的土地现状调查结果确定。补偿登记办理过程，可以采用邀请公证机构现场公证等形式进行记录。"})
MERGE (art31)-[:PART_OF]->(chapter4)

// 补偿登记要求
MERGE (requirement16:Object {name: "持不动产权属证明材料", type: "document_requirement", source_article: "第三十一条"})
MERGE (requirement17:Object {name: "在公告载明的办理补偿登记期限内", type: "time_requirement", source_article: "第三十一条"})
MERGE (requirement18:Object {name: "邀请公证机构现场公证", type: "record_method", source_article: "第三十一条"})

// 补偿登记程序
MERGE (procedure11:Object {name: "补偿登记", type: "procedure", source_article: "第三十一条"})

// 未登记处理方式
MERGE (handling1:Object {name: "按照经确认或者公示的土地现状调查结果确定", type: "handling_method", source_article: "第三十一条"})

// 义务
MERGE (duty82:Obligation {description: "办理补偿登记", source_article: "第三十一条"})
MERGE (duty83:Obligation {description: "持不动产权属证明材料", source_article: "第三十一条"})
MERGE (duty84:Obligation {description: "在规定期限内办理补偿登记", source_article: "第三十一条"})

// 关系建立
MERGE (agent28)-[:HAS_DUTY]->(duty82)
MERGE (agent29)-[:HAS_DUTY]->(duty82)
MERGE (duty82)-[:REQUIRES_DOCUMENT]->(requirement16)
MERGE (duty82)-[:HAS_DEADLINE]->(requirement17)
MERGE (duty82)-[:FOLLOWS_PROCEDURE]->(procedure11)
MERGE (procedure11)-[:HAS_RECORD_METHOD]->(requirement18)
MERGE (procedure11)-[:HAS_EXCEPTION_HANDLING]->(handling1)
MERGE (handling1)-[:BASED_ON]->(task2)

MERGE (art31)-[:DEFINES_PROCEDURE]->(procedure11)
MERGE (art31)-[:INVOLVES]->(agent28)
MERGE (art31)-[:INVOLVES]->(agent29)

// 第三十二条
MERGE (art32:Article {number: "第三十二条", full_text: "县级以上人民政府根据法律、法规的规定和听证会等情况确定征地补偿安置方案后，应当组织测算并落实土地补偿费、安置补助费以及农村村民住宅、其他地上附着物和青苗等的补偿费用（以下统称征收土地补偿费用），以及被征地农民社会保障费用，由有关部门与拟征收土地的所有权人、使用权人签订征地补偿安置协议。涉及不同权利主体的，征地补偿安置协议中应当明确各权利主体利益，并附各权利主体签名或者盖章。征地补偿安置协议应当对交付土地的期限、条件、安置方式以及征收土地补偿费用支付期限等进行约定。征地补偿安置协议签订期限内，个别确实难以达成协议的，县级以上人民政府应当在申请征收土地时如实说明，并做好风险化解工作。"})
MERGE (art32)-[:PART_OF]->(chapter4)

// 补偿费用类型
MERGE (comp1:Object {name: "土地补偿费", type: "compensation_type", source_article: "第三十二条"})
MERGE (comp2:Object {name: "安置补助费", type: "compensation_type", source_article: "第三十二条"})
MERGE (comp3:Object {name: "农村村民住宅补偿", type: "compensation_type", source_article: "第三十二条"})
MERGE (comp4:Object {name: "其他地上附着物补偿", type: "compensation_type", source_article: "第三十二条"})
MERGE (comp5:Object {name: "青苗补偿", type: "compensation_type", source_article: "第三十二条"})
MERGE (comp6:Object {name: "被征地农民社会保障费用", type: "compensation_type", source_article: "第三十二条"})

// 征收土地补偿费用
MERGE (total_comp:Object {name: "征收土地补偿费用", type: "compensation_total", source_article: "第三十二条"})

// 补偿安置协议
MERGE (agreement1:Object {name: "征地补偿安置协议", type: "agreement", source_article: "第三十二条"})

// 协议内容
MERGE (content13:Object {name: "交付土地的期限", type: "agreement_content", source_article: "第三十二条"})
MERGE (content14:Object {name: "交付土地的条件", type: "agreement_content", source_article: "第三十二条"})
MERGE (content15:Object {name: "安置方式", type: "agreement_content", source_article: "第三十二条、第三十五条"})
MERGE (content16:Object {name: "征收土地补偿费用支付期限", type: "agreement_content", source_article: "第三十二条"})

// 特殊情况处理
MERGE (exception7:Object {name: "个别确实难以达成协议", type: "exception_condition", source_article: "第三十二条"})
MERGE (measure3:Object {name: "如实说明", condition: "申请征收土地时", source_article: "第三十二条"})
MERGE (measure4:Object {name: "做好风险化解工作", source_article: "第三十二条"})

// 义务
MERGE (duty85:Obligation {description: "组织测算并落实征收土地补偿费用", source_article: "第三十二条"})
MERGE (duty86:Obligation {description: "签订征地补偿安置协议", source_article: "第三十二条"})
MERGE (duty87:Obligation {description: "明确各权利主体利益", condition: "涉及不同权利主体", source_article: "第三十二条"})
MERGE (duty88:Obligation {description: "附各权利主体签名或者盖章", condition: "涉及不同权利主体", source_article: "第三十二条"})
MERGE (duty89:Obligation {description: "约定交付土地的期限、条件、安置方式以及征收土地补偿费用支付期限", source_article: "第三十二条"})
MERGE (duty90:Obligation {description: "如实说明难以达成协议的情况", condition: "征地补偿安置协议签订期限内，个别确实难以达成协议", source_article: "第三十二条"})
MERGE (duty91:Obligation {description: "做好风险化解工作", condition: "征地补偿安置协议签订期限内，个别确实难以达成协议", source_article: "第三十二条"})

// 关系建立
MERGE (agent25)-[:HAS_DUTY]->(duty85)
MERGE (agent25)-[:HAS_DUTY]->(duty86)
MERGE (agent25)-[:HAS_DUTY]->(duty90)
MERGE (agent25)-[:HAS_DUTY]->(duty91)

MERGE (total_comp)-[:INCLUDES]->(comp1)
MERGE (total_comp)-[:INCLUDES]->(comp2)
MERGE (total_comp)-[:INCLUDES]->(comp3)
MERGE (total_comp)-[:INCLUDES]->(comp4)
MERGE (total_comp)-[:INCLUDES]->(comp5)
MERGE (total_comp)-[:INCLUDES]->(comp6)

MERGE (duty85)-[:CALCULATES]->(total_comp)
MERGE (duty85)-[:CALCULATES]->(comp6)

MERGE (duty86)-[:CREATES]->(agreement1)
MERGE (agreement1)-[:INVOLVES]->(agent28)
MERGE (agreement1)-[:INVOLVES]->(agent29)

MERGE (duty87)-[:RELATED_TO]->(agreement1)
MERGE (duty88)-[:RELATED_TO]->(agreement1)
MERGE (duty89)-[:RELATED_TO]->(agreement1)

MERGE (agreement1)-[:CONTAINS]->(content13)
MERGE (agreement1)-[:CONTAINS]->(content14)
MERGE (agreement1)-[:CONTAINS]->(content15)
MERGE (agreement1)-[:CONTAINS]->(content16)

MERGE (duty90)-[:TRIGGERED_BY]->(exception7)
MERGE (duty91)-[:TRIGGERED_BY]->(exception7)
MERGE (exception7)-[:HANDLED_BY]->(measure3)
MERGE (exception7)-[:HANDLED_BY]->(measure4)

MERGE (art32)-[:DEFINES]->(total_comp)
MERGE (art32)-[:DEFINES]->(agreement1)
MERGE (art32)-[:INVOLVES]->(agent25)
MERGE (art32)-[:INVOLVES]->(agent28)
MERGE (art32)-[:INVOLVES]->(agent29)

// 第三十三条
MERGE (art33:Article {number: "第三十三条", full_text: "征收土地补偿费用、被征地农民社会保障费用实行预存制度。申请征收土地的县级以上人民政府在上报有批准权的人民政府审批前，应当将测算的征收土地补偿费用足额预存至土地补偿和安置补助费有关账户，将社会保障费用足额预存至收缴被征地农民社会保障资金过渡户，并保证专款专用。有关费用未足额预存到专门账户的，不得批准征收土地。"})
MERGE (art33)-[:PART_OF]->(chapter4)

// 预存制度
MERGE (system3:Object {name: "预存制度", type: "financial_system", source_article: "第三十三条"})

// 预存账户
MERGE (account1:Object {name: "土地补偿和安置补助费有关账户", type: "account", source_article: "第三十三条"})
MERGE (account2:Object {name: "收缴被征地农民社会保障资金过渡户", type: "account", source_article: "第三十三条"})

// 预存要求
MERGE (requirement19:Object {name: "足额预存", type: "financial_requirement", source_article: "第三十三条"})
MERGE (requirement20:Object {name: "专款专用", type: "financial_requirement", source_article: "第三十三条"})
MERGE (requirement21:Object {name: "上报审批前完成预存", type: "time_requirement", source_article: "第三十三条"})

// 审批限制
MERGE (restriction1:Object {name: "不得批准征收土地", condition: "有关费用未足额预存到专门账户", type: "approval_restriction", source_article: "第三十三条"})

// 义务
MERGE (duty92:Obligation {description: "足额预存征收土地补偿费用", source_article: "第三十三条"})
MERGE (duty93:Obligation {description: "足额预存社会保障费用", source_article: "第三十三条"})
MERGE (duty94:Obligation {description: "保证专款专用", source_article: "第三十三条"})

// 关系建立
MERGE (agent25)-[:HAS_DUTY]->(duty92)
MERGE (agent25)-[:HAS_DUTY]->(duty93)
MERGE (agent25)-[:HAS_DUTY]->(duty94)

MERGE (system3)-[:REQUIRES]->(duty92)
MERGE (system3)-[:REQUIRES]->(duty93)
MERGE (system3)-[:REQUIRES]->(duty94)

MERGE (duty92)-[:DEPOSITS_TO]->(account1)
MERGE (duty92)-[:INVOLVES]->(total_comp)
MERGE (duty93)-[:DEPOSITS_TO]->(account2)
MERGE (duty93)-[:INVOLVES]->(comp6)

MERGE (duty92)-[:MEETS_REQUIREMENT]->(requirement19)
MERGE (duty93)-[:MEETS_REQUIREMENT]->(requirement19)
MERGE (duty94)-[:MEETS_REQUIREMENT]->(requirement20)
MERGE (duty92)-[:HAS_DEADLINE]->(requirement21)
MERGE (duty93)-[:HAS_DEADLINE]->(requirement21)

MERGE (restriction1)-[:ENFORCED_BY]->(agent22)
MERGE (restriction1)-[:RELATED_TO]->(requirement19)

MERGE (art33)-[:ESTABLISHES]->(system3)
MERGE (art33)-[:INVOLVES]->(agent25)
MERGE (art33)-[:REGULATES]->(total_comp)
MERGE (art33)-[:REGULATES]->(comp6)

// 第三十四条
MERGE (art34:Article {number: "第三十四条", full_text: "征收土地申请经依法批准后，县级以上人民政府应当在收到批准文件之日起十五个工作日内，在拟征收土地所在的乡镇和村、村民小组范围内发布征收土地公告并组织实施，公告期不少于十个工作日，并采取拍照、录像、公证等方式留存记录。公告应当包括下列内容：（一）征地批准机关、文号、时间、用途和征收范围；（二）征地补偿安置方案；（三）征收土地补偿费用以及被征地农民社会保障等费用的支付方式和期限等；（四）其他需要公告的内容。"})
MERGE (art34)-[:PART_OF]->(chapter4)

// 公告要求
MERGE (requirement22:Object {name: "收到批准文件之日起十五个工作日内", type: "time_requirement", source_article: "第三十四条"})
MERGE (requirement23:Object {name: "公告期不少于十个工作日", type: "time_requirement", source_article: "第三十四条"})

// 公告内容
MERGE (content17:Object {name: "征地批准机关、文号、时间、用途和征收范围", type: "announcement_content", source_article: "第三十四条"})
MERGE (content18:Object {name: "征地补偿安置方案", type: "announcement_content", source_article: "第三十四条"})
MERGE (content19:Object {name: "征收土地补偿费用以及被征地农民社会保障等费用的支付方式和期限", type: "announcement_content", source_article: "第三十四条"})
MERGE (content20:Object {name: "其他需要公告的内容", type: "announcement_content", source_article: "第三十四条"})

// 公告范围
MERGE (scope2:Object {name: "拟征收土地所在的乡镇和村、村民小组范围", type: "announcement_scope", source_article: "第三十四条"})

// 义务
MERGE (duty95:Obligation {description: "发布征收土地公告", source_article: "第三十四条"})
MERGE (duty96:Obligation {description: "在规定时间内发布征收土地公告", source_article: "第三十四条"})
MERGE (duty97:Obligation {description: "在规定范围内发布征收土地公告", source_article: "第三十四条"})
MERGE (duty98:Obligation {description: "确保公告期不少于十个工作日", source_article: "第三十四条"})
MERGE (duty99:Obligation {description: "留存公告记录", source_article: "第三十四条"})
MERGE (duty100:Obligation {description: "组织实施征收土地", source_article: "第三十四条"})

// 关系建立
MERGE (agent25)-[:HAS_DUTY]->(duty95)
MERGE (agent25)-[:HAS_DUTY]->(duty96)
MERGE (agent25)-[:HAS_DUTY]->(duty97)
MERGE (agent25)-[:HAS_DUTY]->(duty98)
MERGE (agent25)-[:HAS_DUTY]->(duty99)
MERGE (agent25)-[:HAS_DUTY]->(duty100)

MERGE (duty95)-[:REQUIRES]->(procedure4)
MERGE (duty96)-[:MEETS_REQUIREMENT]->(requirement22)
MERGE (duty97)-[:APPLIES_TO_SCOPE]->(scope2)
MERGE (duty98)-[:MEETS_REQUIREMENT]->(requirement23)
MERGE (duty99)-[:USING_METHOD]->(requirement6)

MERGE (duty95)-[:INCLUDES_CONTENT]->(content17)
MERGE (duty95)-[:INCLUDES_CONTENT]->(content18)
MERGE (duty95)-[:INCLUDES_CONTENT]->(content19)
MERGE (duty95)-[:INCLUDES_CONTENT]->(content20)

MERGE (content17)-[:RELATED_TO]->(procedure4)
MERGE (content18)-[:RELATED_TO]->(agreement1)
MERGE (content19)-[:RELATED_TO]->(total_comp)
MERGE (content19)-[:RELATED_TO]->(comp6)

MERGE (art34)-[:DEFINES_TASK]->(task1)
MERGE (art34)-[:INVOLVES]->(agent25)
MERGE (art34)-[:REGULATES_PROCEDURE]->(procedure4)

// 第三十五条
MERGE (art35:Article {number: "第三十五条", full_text: "对个别未达成征地补偿安置协议的，由县级以上人民政府在征收土地公告期满后，依据征地补偿安置方案和补偿登记结果作出征地补偿安置决定，明确征收范围、土地现状、征收目的、补偿方式和标准、安置对象、安置方式、社会保障以及交地期限等内容，并依法组织实施。被征收土地的所有权人、使用权人未按照征地补偿安置协议交出土地，经催告后仍不履行的，或者在征地补偿安置决定规定的期限内不交出土地的，由县级以上人民政府作出责令交出土地的决定；拒不交出土地的，依法申请人民法院强制执行。"})
MERGE (art35)-[:PART_OF]->(chapter4)

// 特殊情况处理
MERGE (exception8:Object {name: "个别未达成征地补偿安置协议", type: "exception_condition", source_article: "第三十五条"})

// 补偿安置决定
MERGE (decision3:Object {name: "征地补偿安置决定", type: "administrative_decision", source_article: "第三十五条"})

// 决定内容
MERGE (content21:Object {name: "征收范围", type: "decision_content", source_article: "第三十五条"})
MERGE (content22:Object {name: "土地现状", type: "decision_content", source_article: "第三十五条"})
MERGE (content23:Object {name: "征收目的", type: "decision_content", source_article: "第三十五条"})
MERGE (content24:Object {name: "补偿方式和标准", type: "decision_content", source_article: "第三十五条"})
MERGE (content25:Object {name: "安置对象", type: "decision_content", source_article: "第三十五条"})
MERGE (content27:Object {name: "社会保障", type: "decision_content", source_article: "第三十五条"})
MERGE (content28:Object {name: "交地期限", type: "decision_content", source_article: "第三十五条"})

// 土地交出程序
MERGE (procedure12:Object {name: "责令交出土地的决定", type: "enforcement_procedure", source_article: "第三十五条"})
MERGE (procedure13:Object {name: "申请人民法院强制执行", type: "enforcement_procedure", source_article: "第三十五条"})

// 不履行情形
MERGE (violation1:Object {name: "未按照征地补偿安置协议交出土地，经催告后仍不履行", type: "violation_condition", source_article: "第三十五条"})
MERGE (violation2:Object {name: "在征地补偿安置决定规定的期限内不交出土地", type: "violation_condition", source_article: "第三十五条"})

// 义务
MERGE (duty101:Obligation {description: "作出征地补偿安置决定", condition: "个别未达成征地补偿安置协议", source_article: "第三十五条"})
MERGE (duty102:Obligation {description: "明确决定内容", source_article: "第三十五条"})
MERGE (duty103:Obligation {description: "依法组织实施征地补偿安置决定", source_article: "第三十五条"})
MERGE (duty104:Obligation {description: "作出责令交出土地的决定", condition: "未按照征地补偿安置协议交出土地，经催告后仍不履行或在征地补偿安置决定规定的期限内不交出土地", source_article: "第三十五条"})
MERGE (duty105:Obligation {description: "申请人民法院强制执行", condition: "拒不交出土地", source_article: "第三十五条"})

// 关系建立
MERGE (agent25)-[:HAS_DUTY]->(duty101)
MERGE (agent25)-[:HAS_DUTY]->(duty102)
MERGE (agent25)-[:HAS_DUTY]->(duty103)
MERGE (agent25)-[:HAS_DUTY]->(duty104)
MERGE (agent25)-[:HAS_DUTY]->(duty105)

MERGE (duty101)-[:TRIGGERED_BY]->(exception8)
MERGE (duty101)-[:BASED_ON]->(task4)
MERGE (duty101)-[:BASED_ON]->(procedure11)
MERGE (duty101)-[:CREATES]->(decision3)

MERGE (decision3)-[:CONTAINS]->(content21)
MERGE (decision3)-[:CONTAINS]->(content22)
MERGE (decision3)-[:CONTAINS]->(content23)
MERGE (decision3)-[:CONTAINS]->(content24)
MERGE (decision3)-[:CONTAINS]->(content25)
MERGE (decision3)-[:CONTAINS]->(content15)
MERGE (decision3)-[:CONTAINS]->(content27)
MERGE (decision3)-[:CONTAINS]->(content28)

MERGE (duty104)-[:TRIGGERED_BY]->(violation1)
MERGE (duty104)-[:TRIGGERED_BY]->(violation2)
MERGE (duty104)-[:FOLLOWS_PROCEDURE]->(procedure12)

MERGE (duty105)-[:TRIGGERED_BY]->(procedure12)
MERGE (duty105)-[:FOLLOWS_PROCEDURE]->(procedure13)

MERGE (violation1)-[:RELATED_TO]->(agreement1)
MERGE (violation2)-[:RELATED_TO]->(decision3)

MERGE (art35)-[:DEFINES_EXCEPTION]->(exception8)
MERGE (art35)-[:DEFINES_PROCEDURE]->(procedure12)
MERGE (art35)-[:DEFINES_PROCEDURE]->(procedure13)
MERGE (art35)-[:INVOLVES]->(agent25)
MERGE (art35)-[:INVOLVES]->(agent28)
MERGE (art35)-[:INVOLVES]->(agent29)

// 第三十六条
MERGE (art36:Article {number: "第三十六条", full_text: "征收土地应当给予公平、合理的补偿。征收农用地的土地补偿费、安置补助费标准由区片综合地价确定。地级以上市人民政府组织拟定区片综合地价时，一并拟定征收建设用地和未利用地的补偿标准，由省人民政府批准并公布实施。区片综合地价至少每三年调整或者重新公布一次。地级以上市人民政府应当组织拟定农村村民住宅、其他地上附着物以及青苗等补偿费用标准，由省人民政府批准并公布实施。县级以上人民政府应当将被征地农民纳入相应的养老等社会保障体系，依法安排被征地农民的社会保障费用。"})
MERGE (art36)-[:PART_OF]->(chapter4)

// 补偿原则
MERGE (principle1:Object {name: "公平、合理的补偿", type: "compensation_principle", source_article: "第三十六条"})

// 区片综合地价
MERGE (standard1:Object {name: "区片综合地价", type: "compensation_standard", source_article: "第三十六条"})
MERGE (standard2:Object {name: "征收建设用地补偿标准", type: "compensation_standard", source_article: "第三十六条"})
MERGE (standard3:Object {name: "征收未利用地补偿标准", type: "compensation_standard", source_article: "第三十六条"})
MERGE (standard4:Object {name: "农村村民住宅补偿费用标准", type: "compensation_standard", source_article: "第三十六条"})
MERGE (standard5:Object {name: "其他地上附着物补偿费用标准", type: "compensation_standard", source_article: "第三十六条"})
MERGE (standard6:Object {name: "青苗补偿费用标准", type: "compensation_standard", source_article: "第三十六条"})

// 调整要求
MERGE (requirement25:Object {name: "至少每三年调整或者重新公布一次", type: "update_requirement", source_article: "第三十六条"})

// 社会保障
MERGE (system4:Object {name: "养老等社会保障体系", type: "social_security_system", source_article: "第三十六条"})

// 义务
MERGE (duty106:Obligation {description: "给予公平、合理的补偿", source_article: "第三十六条"})
MERGE (duty107:Obligation {description: "组织拟定区片综合地价", source_article: "第三十六条"})
MERGE (duty108:Obligation {description: "一并拟定征收建设用地和未利用地的补偿标准", source_article: "第三十六条"})
MERGE (duty109:Obligation {description: "定期调整或重新公布区片综合地价", source_article: "第三十六条"})
MERGE (duty110:Obligation {description: "组织拟定农村村民住宅、其他地上附着物以及青苗等补偿费用标准", source_article: "第三十六条"})
MERGE (duty111:Obligation {description: "将被征地农民纳入相应的社会保障体系", source_article: "第三十六条"})
MERGE (duty112:Obligation {description: "依法安排被征地农民的社会保障费用", source_article: "第三十六条"})

// 关系建立
MERGE (agent25)-[:HAS_DUTY]->(duty106)
MERGE (agent24)-[:HAS_DUTY]->(duty107)
MERGE (agent24)-[:HAS_DUTY]->(duty108)
MERGE (agent24)-[:HAS_DUTY]->(duty109)
MERGE (agent24)-[:HAS_DUTY]->(duty110)
MERGE (agent25)-[:HAS_DUTY]->(duty111)
MERGE (agent25)-[:HAS_DUTY]->(duty112)

MERGE (duty106)-[:FOLLOWS_PRINCIPLE]->(principle1)
MERGE (duty107)-[:CREATES_STANDARD]->(standard1)
MERGE (duty108)-[:CREATES_STANDARD]->(standard2)
MERGE (duty108)-[:CREATES_STANDARD]->(standard3)
MERGE (duty109)-[:MEETS_REQUIREMENT]->(requirement25)
MERGE (duty110)-[:CREATES_STANDARD]->(standard4)
MERGE (duty110)-[:CREATES_STANDARD]->(standard5)
MERGE (duty110)-[:CREATES_STANDARD]->(standard6)
MERGE (duty111)-[:USES_SYSTEM]->(system4)
MERGE (duty112)-[:PAYS]->(comp6)

MERGE (standard1)-[:APPLIES_TO]->(land_type1)
MERGE (standard1)-[:DETERMINES]->(comp1)
MERGE (standard1)-[:DETERMINES]->(comp2)
MERGE (standard2)-[:APPLIES_TO]->(land_type2)
MERGE (standard3)-[:APPLIES_TO]->(land_type3)
MERGE (comp3)-[:BASED_ON_STANDARD]->(standard4)
MERGE (comp4)-[:BASED_ON_STANDARD]->(standard5)
MERGE (comp5)-[:BASED_ON_STANDARD]->(standard6)

MERGE (agent23)-[:HAS_AUTHORITY]->(standard1)
MERGE (agent23)-[:HAS_AUTHORITY]->(standard2)
MERGE (agent23)-[:HAS_AUTHORITY]->(standard3)
MERGE (agent23)-[:HAS_AUTHORITY]->(standard4)
MERGE (agent23)-[:HAS_AUTHORITY]->(standard5)
MERGE (agent23)-[:HAS_AUTHORITY]->(standard6)

MERGE (art36)-[:DEFINES_PRINCIPLE]->(principle1)
MERGE (art36)-[:DEFINES_STANDARD]->(standard1)
MERGE (art36)-[:INVOLVES]->(agent25)
MERGE (art36)-[:INVOLVES]->(agent24)
MERGE (art36)-[:INVOLVES]->(agent23)

// 第三十七条
MERGE (art37:Article {number: "第三十七条", full_text: "县级以上人民政府应当在征收土地公告期满之日起三个月内，足额支付征收土地补偿费用，并落实被征地农民社会保障费用。对个别未达成征地补偿安置协议的，支付征收土地补偿费用的期限自征地补偿安置决定作出之日起计算。征收土地补偿费用、被征地农民社会保障费用等未按照规定足额支付到位或者提存公证的，不得强行征收、占用被征收土地。禁止侵占、挪用征收土地补偿费用和其他有关费用。"})
MERGE (art37)-[:PART_OF]->(chapter4)

// 支付期限
MERGE (deadline3:Object {name: "征收土地公告期满之日起三个月内", type: "time_limit", source_article: "第三十七条"})
MERGE (deadline4:Object {name: "征地补偿安置决定作出之日起计算", condition: "个别未达成征地补偿安置协议", type: "time_limit", source_article: "第三十七条"})

// 支付要求
MERGE (requirement26:Object {name: "足额支付", type: "payment_requirement", source_article: "第三十七条"})
MERGE (requirement27:Object {name: "提存公证", alternative: true, source_article: "第三十七条"})

// 强制措施限制
MERGE (restriction2:Object {name: "不得强行征收、占用被征收土地", condition: "征收土地补偿费用、被征地农民社会保障费用等未按照规定足额支付到位或者提存公证", type: "enforcement_restriction", source_article: "第三十七条"})

// 禁止行为
MERGE (prohibition1:Object {name: "侵占征收土地补偿费用", type: "prohibited_action", source_article: "第三十七条"})
MERGE (prohibition2:Object {name: "挪用征收土地补偿费用", type: "prohibited_action", source_article: "第三十七条"})
MERGE (prohibition3:Object {name: "侵占其他有关费用", type: "prohibited_action", source_article: "第三十七条"})
MERGE (prohibition4:Object {name: "挪用其他有关费用", type: "prohibited_action", source_article: "第三十七条"})

// 义务
MERGE (duty113:Obligation {description: "足额支付征收土地补偿费用", source_article: "第三十七条"})
MERGE (duty114:Obligation {description: "落实被征地农民社会保障费用", source_article: "第三十七条"})
MERGE (duty115:Obligation {description: "在规定期限内支付征收土地补偿费用", source_article: "第三十七条"})

// 关系建立
MERGE (agent25)-[:HAS_DUTY]->(duty113)
MERGE (agent25)-[:HAS_DUTY]->(duty114)
MERGE (agent25)-[:HAS_DUTY]->(duty115)

MERGE (duty113)-[:PAYS]->(total_comp)
MERGE (duty114)-[:PAYS]->(comp6)
MERGE (duty115)-[:HAS_DEADLINE]->(deadline3)
MERGE (duty115)-[:HAS_ALTERNATIVE_DEADLINE]->(deadline4)
MERGE (duty115)-[:MEETS_REQUIREMENT]->(requirement26)

MERGE (restriction2)-[:TRIGGERED_BY]->(requirement26)
MERGE (restriction2)-[:ALTERNATIVE_TRIGGERED_BY]->(requirement27)

MERGE (prohibition1)-[:RELATED_TO]->(total_comp)
MERGE (prohibition2)-[:RELATED_TO]->(total_comp)
MERGE (prohibition3)-[:RELATED_TO]->(comp6)
MERGE (prohibition4)-[:RELATED_TO]->(comp6)

MERGE (agent25)-[:MUST_NOT]->(prohibition1)
MERGE (agent25)-[:MUST_NOT]->(prohibition2)
MERGE (agent25)-[:MUST_NOT]->(prohibition3)
MERGE (agent25)-[:MUST_NOT]->(prohibition4)

MERGE (art37)-[:REGULATES]->(total_comp)
MERGE (art37)-[:REGULATES]->(comp6)
MERGE (art37)-[:INVOLVES]->(agent25)
MERGE (art37)-[:DEFINES_RESTRICTION]->(restriction2)

// 第三十八条
MERGE (art38:Article {number: "第三十八条", full_text: "经批准收回国有农、林、牧、渔、盐场的土地，参照征收农民集体所有土地的标准给予公平、合理的补偿。法律、行政法规另有规定的，从其规定。"})
MERGE (art38)-[:PART_OF]->(chapter4)

// 特殊土地类型
MERGE (land_type5:Object {name: "经批准回收国有农、林、牧、渔、盐场的土地", type: "land_type", source_article: "第三十八条"})

// 补偿方式
MERGE (comp_method1:Object {name: "参照征收农民集体所有土地的标准", type: "compensation_method", source_article: "第三十八条"})

// 例外规定
MERGE (exception9:Object {name: "法律、行政法规另有规定", type: "legal_exception", source_article: "第三十八条"})

// 义务
MERGE (duty116:Obligation {description: "参照征收农民集体所有土地的标准进行补偿", condition: "收回国有农、林、牧、渔、盐场的土地", source_article: "第三十八条"})

// 关系建立
MERGE (agent22)-[:HAS_DUTY]->(duty116)

MERGE (duty116)-[:USES_METHOD]->(comp_method1)
MERGE (comp_method1)-[:REFERENCES]->(art36)

MERGE (exception9)-[:OVERRIDES]->(duty116)

MERGE (art38)-[:REGULATES]->(land_type5)
MERGE (art38)-[:REFERENCES]->(art36)
MERGE (art38)-[:HAS_EXCEPTION]->(exception9)

































// 第五章 建设用地供应与利用
// 创建第五章节点（确保文档节点已存在）
MATCH (doc:Document {name: "广东省土地管理条例"})
MERGE (chapter5:Chapter {number: "第五章", title: "建设用地供应与利用"})
MERGE (chapter5)-[:PART_OF]->(doc)

// 第三十九条
MERGE (art39:Article {number: "第三十九条", full_text: "地级以上市、县级人民政府自然资源主管部门应当按照规定组织编制年度建设用地供应计划，征求有关单位意见，报本级人民政府批准后，在政府网站上向社会公布，供社会公众查阅。县级以上人民政府自然资源主管部门应当加强土地市场动态监测与监管，对建设用地批准和供应后的开发情况实行全程监管。"})
MERGE (art39)-[:PART_OF]->(chapter5)

// 相关主体
MERGE (agent38:Agent {name: "地级以上市人民政府自然资源主管部门", type: "department"})
MERGE (agent39:Agent {name: "县级人民政府自然资源主管部门", type: "department"})
MERGE (agent41:Agent {name: "社会公众", type: "public"})

// 供应计划
MERGE (plan1:Object {name: "年度建设用地供应计划", type: "plan"})
MERGE (action1:Object {name: "组织编制", type: "action"})
MERGE (action2:Object {name: "征求有关单位意见", type: "action"})
MERGE (action3:Object {name: "批准", type: "action"})
MERGE (action4:Object {name: "向社会公布", type: "action"})
MERGE (platform1:Object {name: "政府网站", type: "platform"})

// 监管要求
MERGE (monitoring1:Object {name: "土地市场动态监测与监管", type: "monitoring"})
MERGE (monitoring2:Object {name: "全程监管", type: "monitoring", target: "建设用地批准和供应后的开发情况"})

// 义务
MERGE (duty118:Obligation {description: "组织编制年度建设用地供应计划", source_article: "第三十九条"})
MERGE (duty119:Obligation {description: "征求有关单位意见", source_article: "第三十九条"})
MERGE (duty120:Obligation {description: "报本级人民政府批准", source_article: "第三十九条"})
MERGE (duty121:Obligation {description: "在政府网站上向社会公布", source_article: "第三十九条"})
MERGE (duty122:Obligation {description: "加强土地市场动态监测与监管", source_article: "第三十九条"})
MERGE (duty123:Obligation {description: "对建设用地批准和供应后的开发情况实行全程监管", source_article: "第三十九条"})

// 关系建立
MERGE (agent38)-[:HAS_DUTY]->(duty118)
MERGE (agent39)-[:HAS_DUTY]->(duty118)
MERGE (agent38)-[:HAS_DUTY]->(duty119)
MERGE (agent39)-[:HAS_DUTY]->(duty119)
MERGE (agent38)-[:HAS_DUTY]->(duty120)
MERGE (agent39)-[:HAS_DUTY]->(duty120)
MERGE (agent38)-[:HAS_DUTY]->(duty121)
MERGE (agent39)-[:HAS_DUTY]->(duty121)
MERGE (agent38)-[:HAS_DUTY]->(duty122)
MERGE (agent39)-[:HAS_DUTY]->(duty122)
MERGE (agent38)-[:HAS_DUTY]->(duty123)
MERGE (agent39)-[:HAS_DUTY]->(duty123)

MERGE (duty118)-[:PRODUCES]->(plan1)
MERGE (duty119)-[:RELATES_TO]->(plan1)
MERGE (duty120)-[:APPLIES_TO]->(plan1)
MERGE (duty121)-[:PUBLISHES]->(plan1)
MERGE (duty121)-[:USES_PLATFORM]->(platform1)
MERGE (duty121)-[:TARGETS]->(agent41)

MERGE (duty122)-[:IMPLEMENTS]->(monitoring1)
MERGE (duty123)-[:IMPLEMENTS]->(monitoring2)

// 第四十条
MERGE (art40:Article {number: "第四十条", full_text: "新供应国有工业用地，地级以上市、县级人民政府可以与工业用地取得方签订项目履约监管协议，明确产业准入条件、投产时间、投资强度、产出效率、退出机制、股权变更约束、生态环境保护要求等内容。地级以上市、县（市）人民政府可以探索采取先租赁后出让的方式供应工业用地，出让年期在法定出让最高年期内合理确定。采取先租赁后出让方式供应的，应当符合国家规定的条件。"})
MERGE (art40)-[:PART_OF]->(chapter5)

// 相关主体
MERGE (agent42:Agent {name: "工业用地取得方", type: "entity"})
MERGE (agent43:Agent {name: "县（市）人民政府", type: "government"})

// 协议与内容
MERGE (agreement2:Object {name: "项目履约监管协议", type: "agreement"})
MERGE (content29:Object {name: "产业准入条件", type: "agreement_content"})
MERGE (content30:Object {name: "投产时间", type: "agreement_content"})
MERGE (content31:Object {name: "投资强度", type: "agreement_content"})
MERGE (content32:Object {name: "产出效率", type: "agreement_content"})
MERGE (content33:Object {name: "退出机制", type: "agreement_content"})
MERGE (content34:Object {name: "股权变更约束", type: "agreement_content"})
MERGE (content35:Object {name: "生态环境保护要求", type: "agreement_content"})

// 供地方式
MERGE (supply_method1:Object {name: "先租赁后出让", type: "supply_method"})
MERGE (requirement28:Object {name: "符合国家规定的条件", type: "requirement"})
MERGE (term_limit:Object {name: "法定出让最高年期", type: "term_limit"})

// 义务
MERGE (duty124:Obligation {description: "签订项目履约监管协议", condition: "新供应国有工业用地", source_article: "第四十条"})
MERGE (duty125:Obligation {description: "明确协议内容", source_article: "第四十条"})
MERGE (duty126:Obligation {description: "探索采取先租赁后出让的方式供应工业用地", source_article: "第四十条"})
MERGE (duty127:Obligation {description: "合理确定出让年期", source_article: "第四十条"})
MERGE (duty128:Obligation {description: "符合国家规定的条件", condition: "采取先租赁后出让方式供应", source_article: "第四十条"})

// 关系建立
MERGE (agent24)-[:HAS_DUTY]->(duty124)
MERGE (agent24)-[:HAS_DUTY]->(duty126)
MERGE (agent43)-[:HAS_DUTY]->(duty126)
MERGE (agent24)-[:HAS_DUTY]->(duty127)
MERGE (agent43)-[:HAS_DUTY]->(duty127)
MERGE (agent24)-[:HAS_DUTY]->(duty128)
MERGE (agent43)-[:HAS_DUTY]->(duty128)

MERGE (duty124)-[:CREATES]->(agreement2)
MERGE (duty124)-[:INVOLVES]->(agent42)
MERGE (duty125)-[:RELATED_TO]->(agreement2)
MERGE (duty125)-[:SPECIFIES]->(content29)
MERGE (duty125)-[:SPECIFIES]->(content30)
MERGE (duty125)-[:SPECIFIES]->(content31)
MERGE (duty125)-[:SPECIFIES]->(content32)
MERGE (duty125)-[:SPECIFIES]->(content33)
MERGE (duty125)-[:SPECIFIES]->(content34)
MERGE (duty125)-[:SPECIFIES]->(content35)

MERGE (duty126)-[:USES_METHOD]->(supply_method1)
MERGE (duty127)-[:BASED_ON]->(term_limit)
MERGE (duty128)-[:MEETS_REQUIREMENT]->(requirement28)

// 第四十一条
MERGE (art41:Article {number: "第四十一条", full_text: "乡镇企业、乡镇村公共设施、公益事业等乡镇村建设，需要使用农村集体所有土地的，由县级人民政府批准；其中，涉及占用农用地、未利用地的，依法办理相关审批手续。县级以上人民政府应当优先引导和推动城中村、城边村、村镇工业集聚区等可连片开发的存量集体经营性建设用地入市，推动集体所有制经济和乡村产业发展。集体经营性建设用地入市应当通过公开的交易平台进行交易，纳入公共资源交易平台体系，并按照国家和省有关规定实施。"})
MERGE (art41)-[:PART_OF]->(chapter5)

// 相关主体
MERGE (agent44:Agent {name: "县级人民政府", type: "government_level"})
MERGE (agent45:Agent {name: "乡镇企业", type: "entity"})
MERGE (agent46:Agent {name: "农村集体经济组织", type: "organization"})

// 用地类型
MERGE (land_use4:Object {name: "乡镇企业用地", type: "land_use_type"})
MERGE (land_use5:Object {name: "乡镇村公共设施用地", type: "land_use_type"})
MERGE (land_use6:Object {name: "公益事业用地", type: "land_use_type"})
MERGE (land_use7:Object {name: "集体经营性建设用地", type: "land_use_type"})

// 重点区域
MERGE (area1:Object {name: "城中村", type: "development_area"})
MERGE (area2:Object {name: "城边村", type: "development_area"})
MERGE (area3:Object {name: "村镇工业集聚区", type: "development_area"})

// 交易机制
MERGE (trading1:Object {name: "公开的交易平台", type: "trading_platform"})
MERGE (trading2:Object {name: "公共资源交易平台体系", type: "trading_system"})

// 义务
MERGE (duty129:Obligation {description: "批准乡镇村建设使用农村集体所有土地", source_article: "第四十一条"})
MERGE (duty130:Obligation {description: "办理相关审批手续", condition: "涉及占用农用地、未利用地", source_article: "第四十一条"})
MERGE (duty131:Obligation {description: "优先引导和推动存量集体经营性建设用地入市", source_article: "第四十一条"})
MERGE (duty132:Obligation {description: "通过公开的交易平台进行交易", condition: "集体经营性建设用地入市", source_article: "第四十一条"})
MERGE (duty133:Obligation {description: "按照国家和省有关规定实施", condition: "集体经营性建设用地入市", source_article: "第四十一条"})

// 关系建立
MERGE (agent44)-[:HAS_DUTY]->(duty129)
MERGE (agent45)-[:HAS_DUTY]->(duty130)
MERGE (agent25)-[:HAS_DUTY]->(duty131)
MERGE (agent46)-[:HAS_DUTY]->(duty132)
MERGE (agent46)-[:HAS_DUTY]->(duty133)

MERGE (duty129)-[:APPLIES_TO]->(land_use4)
MERGE (duty129)-[:APPLIES_TO]->(land_use5)
MERGE (duty129)-[:APPLIES_TO]->(land_use6)
MERGE (duty130)-[:REQUIRES_PROCEDURE]->(procedure4)
MERGE (duty130)-[:REQUIRES_PROCEDURE]->(procedure5)

MERGE (duty131)-[:PRIORITIZES]->(area1)
MERGE (duty131)-[:PRIORITIZES]->(area2)
MERGE (duty131)-[:PRIORITIZES]->(area3)
MERGE (duty131)-[:PROMOTES]->(land_use7)
MERGE (duty131)-[:PROMOTES]->(agent31)
MERGE (duty131)-[:PROMOTES]->(agent46)

MERGE (duty132)-[:USES_PLATFORM]->(trading1)
MERGE (trading1)-[:PART_OF]->(trading2)
MERGE (land_use7)-[:TRADED_ON]->(trading1)

// 第四十二条
MERGE (art42:Article {number: "第四十二条", full_text: "县级以上人民政府应当按照国家和省有关规定落实建设用地指标，合理保障本行政区域农村村民宅基地需求。农村村民一户只能拥有一处宅基地，新批准宅基地的面积按照以下标准执行：平原地区和城市郊区每户不得超过八十平方米，丘陵地区每户不得超过一百二十平方米，山区每户不得超过一百五十平方米。农村村民应当严格按照批准面积和建房标准建设住宅，禁止未批先建、超面积占用宅基地。鼓励通过集体建房、合建住房等方式，保障农村村民户有所居。"})
MERGE (art42)-[:PART_OF]->(chapter5)

// 相关主体
MERGE (agent47:Agent {name: "农村村民", type: "individual"})
MERGE (agent48:Agent {name: "本行政区域", type: "administrative_area"})

// 宅基地管理
MERGE (land_use8:Object {name: "宅基地", type: "land_use_type",source_article: "第四十二条"})
MERGE (indicator1:Object {name: "建设用地指标", type: "land_indicator",source_article: "第四十二条"})
MERGE (standard7:Object {name: "宅基地面积标准", type: "standard",source_article: "第四十二条"})
MERGE (condition1:Object {name: "一户只能拥有一处宅基地", type: "condition",source_article: "第四十二条"})
MERGE (limit3:Object {name: "平原地区和城市郊区每户不超过八十平方米", type: "area_limit",source_article: "第四十二条"})
MERGE (limit4:Object {name: "丘陵地区每户不超过一百二十平方米", type: "area_limit",source_article: "第四十二条"})
MERGE (limit5:Object {name: "山区每户不超过一百五十平方米", type: "area_limit",source_article: "第四十二条"})

// 住宅建设
MERGE (construction1:Object {name: "严格按照批准面积和建房标准建设住宅", type: "construction_requirement"})
MERGE (prohibition5:Object {name: "未批先建", type: "prohibited_action"})
MERGE (prohibition6:Object {name: "超面积占用宅基地", type: "prohibited_action"})

// 保障方式
MERGE (housing1:Object {name: "集体建房", type: "housing_method"})
MERGE (housing2:Object {name: "合建住房", type: "housing_method"})
MERGE (goal3:Object {name: "保障农村村民户有所居", type: "policy_goal"})

// 义务
MERGE (duty134:Obligation {description: "落实建设用地指标", source_article: "第四十二条"})
MERGE (duty135:Obligation {description: "合理保障农村村民宅基地需求", source_article: "第四十二条"})
MERGE (duty136:Obligation {description: "遵守一户一宅规定", source_article: "第四十二条"})
MERGE (duty137:Obligation {description: "严格按照批准面积和建房标准建设住宅", source_article: "第四十二条"})
MERGE (duty138:Obligation {description: "不得未批先建、超面积占用宅基地", source_article: "第四十二条"})

// 鼓励措施
MERGE (encourage1:Object {name: "通过集体建房、合建住房等方式保障农村村民户有所居", type: "encouraged_practice", source_article: "第四十二条"})

// 关系建立
MERGE (agent25)-[:HAS_DUTY]->(duty134)
MERGE (agent25)-[:HAS_DUTY]->(duty135)
MERGE (agent47)-[:HAS_DUTY]->(duty136)
MERGE (agent47)-[:HAS_DUTY]->(duty137)
MERGE (agent47)-[:MUST_NOT]->(prohibition5)
MERGE (agent47)-[:MUST_NOT]->(prohibition6)

MERGE (duty134)-[:RELATED_TO]->(indicator1)
MERGE (duty135)-[:TARGETS]->(land_use8)
MERGE (duty135)-[:TARGETS]->(agent47)
MERGE (duty136)-[:FOLLOWS_CONDITION]->(condition1)
MERGE (duty136)-[:FOLLOWS_STANDARD]->(standard7)
MERGE (standard7)-[:INCLUDES_LIMIT]->(limit3)
MERGE (standard7)-[:INCLUDES_LIMIT]->(limit4)
MERGE (standard7)-[:INCLUDES_LIMIT]->(limit5)

MERGE (duty137)-[:FOLLOWS_REQUIREMENT]->(construction1)
MERGE (construction1)-[:RELATED_TO]->(land_use8)

MERGE (encourage1)-[:USES_METHOD]->(housing1)
MERGE (encourage1)-[:USES_METHOD]->(housing2)
MERGE (encourage1)-[:SERVES_GOAL]->(goal3)
MERGE (art42)-[:ENCOURAGES]->(encourage1)

// 第四十三条
MERGE (art43:Article {number: "第四十三条", full_text: "对进城落户的农村村民，可以通过多种方式鼓励其依法自愿有偿退出宅基地。退出的宅基地，应当优先用于保障本农村集体经济组织成员的宅基地需求。在符合国土空间规划、用途管制和农村村民自愿的前提下，鼓励利用闲置的宅基地用于乡镇村公共设施、公益事业和集体经营性建设用地等用途，或者复垦为农用地。"})
MERGE (art43)-[:PART_OF]->(chapter5)

// 相关主体
MERGE (agent49:Agent {name: "进城落户的农村村民", type: "individual"})
MERGE (agent50:Agent {name: "本农村集体经济组织成员", type: "individual"})

// 退出机制
MERGE (exit_mechanism:Object {name: "依法自愿有偿退出宅基地", type: "exit_mechanism"})
MERGE (priority_use:Object {name: "优先用于保障本农村集体经济组织成员的宅基地需求", type: "priority_use"})

// 闲置宅基地利用
MERGE (idle_land_use1:Object {name: "乡镇村公共设施", type: "land_use_type", source_article: "第四十三条"})
MERGE (idle_land_use2:Object {name: "公益事业", type: "land_use_type"})
MERGE (idle_land_use4:Object {name: "复垦为农用地", type: "land_use_type", source_article: "第四十三条"})
MERGE (condition2:Object {name: "符合国土空间规划", type: "condition", source_article: "第四十三条、第五十二条"})
MERGE (condition3:Object {name: "符合用途管制", type: "condition", source_article: "第四十三条"})
MERGE (condition4:Object {name: "农村村民自愿", type: "condition", source_article: "第四十三条"})

// 义务与鼓励措施
MERGE (encourage2:Object {name: "鼓励依法自愿有偿退出宅基地", type: "encouraged_practice", source_article: "第四十三条"})
MERGE (encourage3:Object {name: "优先用于保障宅基地需求", type: "encouraged_practice", source_article: "第四十三条"})
MERGE (encourage4:Object {name: "鼓励利用闲置宅基地", type: "encouraged_practice", source_article: "第四十三条"})

// 关系建立
MERGE (agent25)-[:ENCOURAGES]->(encourage2)
MERGE (agent25)-[:ENCOURAGES]->(encourage3)
MERGE (agent25)-[:ENCOURAGES]->(encourage4)

MERGE (encourage2)-[:TARGETS]->(agent49)
MERGE (encourage2)-[:RELATED_TO]->(exit_mechanism)
MERGE (encourage3)-[:RELATED_TO]->(priority_use)
MERGE (encourage3)-[:TARGETS]->(agent50)
MERGE (encourage4)-[:REQUIRES_CONDITION]->(condition2)
MERGE (encourage4)-[:REQUIRES_CONDITION]->(condition3)
MERGE (encourage4)-[:REQUIRES_CONDITION]->(condition4)
MERGE (encourage4)-[:USES_FOR]->(idle_land_use1)
MERGE (encourage4)-[:USES_FOR]->(idle_land_use2)
MERGE (encourage4)-[:USES_FOR]->(land_use7)
MERGE (encourage4)-[:USES_FOR]->(idle_land_use4)

// 第四十四条
MERGE (art44:Article {number: "第四十四条", full_text: "县级以上人民政府应当引导各项建设优先开发利用空闲、废弃、闲置和低效利用的土地，稳妥有序推进旧城镇、旧厂房、旧村庄改造。旧城镇、旧厂房、旧村庄改造应当坚持生态优先、绿色发展，提高节约集约用地水平，依法保护历史文化名城、名镇、名村（传统村落）、街区和不可移动文物、历史建筑、历史地段、非物质文化遗产、红色资源、自然景观、古树名木等，保障权利人合法权益。旧城镇、旧厂房、旧村庄改造具体管理办法由省人民政府制定。"})
MERGE (art44)-[:PART_OF]->(chapter5)

// 土地类型
MERGE (land_status1:Object {name: "空闲土地", type: "land_status"})
MERGE (land_status2:Object {name: "废弃土地", type: "land_status"})
MERGE (land_status3:Object {name: "闲置土地", type: "land_status"})
MERGE (land_status4:Object {name: "低效利用土地", type: "land_status"})

// 三旧改造
MERGE (renovation1:Object {name: "旧城镇改造", type: "renovation_type"})
MERGE (renovation2:Object {name: "旧厂房改造", type: "renovation_type"})
MERGE (renovation3:Object {name: "旧村庄改造", type: "renovation_type"})

// 改造原则
MERGE (principle2:Object {name: "生态优先", type: "principle"})
MERGE (principle3:Object {name: "绿色发展", type: "principle"})
MERGE (principle4:Object {name: "节约集约用地", type: "principle"})

// 保护对象
MERGE (protection1:Object {name: "历史文化名城", type: "protection_object"})
MERGE (protection2:Object {name: "名镇", type: "protection_object"})
MERGE (protection3:Object {name: "名村（传统村落）", type: "protection_object"})
MERGE (protection4:Object {name: "街区", type: "protection_object"})
MERGE (protection5:Object {name: "不可移动文物", type: "protection_object"})
MERGE (protection6:Object {name: "历史建筑", type: "protection_object"})
MERGE (protection7:Object {name: "历史地段", type: "protection_object"})
MERGE (protection8:Object {name: "非物质文化遗产", type: "protection_object"})
MERGE (protection9:Object {name: "红色资源", type: "protection_object"})
MERGE (protection10:Object {name: "自然景观", type: "protection_object"})
MERGE (protection11:Object {name: "古树名木", type: "protection_object"})

// 管理办法
MERGE (management1:Object {name: "旧城镇、旧厂房、旧村庄改造具体管理办法", type: "management_measure"})

// 义务
MERGE (duty139:Obligation {description: "引导优先开发利用空闲、废弃、闲置和低效利用的土地", source_article: "第四十四条"})
MERGE (duty140:Obligation {description: "稳妥有序推进旧城镇、旧厂房、旧村庄改造", source_article: "第四十四条"})
MERGE (duty141:Obligation {description: "坚持生态优先、绿色发展", condition: "三旧改造", source_article: "第四十四条"})
MERGE (duty142:Obligation {description: "提高节约集约用地水平", condition: "三旧改造", source_article: "第四十四条"})
MERGE (duty143:Obligation {description: "依法保护文化遗产和自然资源", condition: "三旧改造", source_article: "第四十四条"})
MERGE (duty144:Obligation {description: "保障权利人合法权益", condition: "三旧改造", source_article: "第四十四条"})
MERGE (duty145:Obligation {description: "制定三旧改造具体管理办法", source_article: "第四十四条"})

// 关系建立
MERGE (agent25)-[:HAS_DUTY]->(duty139)
MERGE (agent25)-[:HAS_DUTY]->(duty140)
MERGE (agent25)-[:HAS_DUTY]->(duty141)
MERGE (agent25)-[:HAS_DUTY]->(duty142)
MERGE (agent25)-[:HAS_DUTY]->(duty143)
MERGE (agent25)-[:HAS_DUTY]->(duty144)
MERGE (agent23)-[:HAS_DUTY]->(duty145)

MERGE (duty139)-[:PROMOTES_USE_OF]->(land_status1)
MERGE (duty139)-[:PROMOTES_USE_OF]->(land_status2)
MERGE (duty139)-[:PROMOTES_USE_OF]->(land_status3)
MERGE (duty139)-[:PROMOTES_USE_OF]->(land_status4)

MERGE (duty140)-[:PROMOTES]->(renovation1)
MERGE (duty140)-[:PROMOTES]->(renovation2)
MERGE (duty140)-[:PROMOTES]->(renovation3)

MERGE (duty141)-[:FOLLOWS_PRINCIPLE]->(principle2)
MERGE (duty141)-[:FOLLOWS_PRINCIPLE]->(principle3)
MERGE (duty142)-[:FOLLOWS_PRINCIPLE]->(principle4)

MERGE (duty143)-[:PROTECTS]->(protection1)
MERGE (duty143)-[:PROTECTS]->(protection2)
MERGE (duty143)-[:PROTECTS]->(protection3)
MERGE (duty143)-[:PROTECTS]->(protection4)
MERGE (duty143)-[:PROTECTS]->(protection5)
MERGE (duty143)-[:PROTECTS]->(protection6)
MERGE (duty143)-[:PROTECTS]->(protection7)
MERGE (duty143)-[:PROTECTS]->(protection8)
MERGE (duty143)-[:PROTECTS]->(protection9)
MERGE (duty143)-[:PROTECTS]->(protection10)
MERGE (duty143)-[:PROTECTS]->(protection11)

MERGE (duty145)-[:PRODUCES]->(management1)
MERGE (management1)-[:REGULATES]->(renovation1)
MERGE (management1)-[:REGULATES]->(renovation2)
MERGE (management1)-[:REGULATES]->(renovation3)

// 第四十五条
MERGE (art45:Article {number: "第四十五条", full_text: "县级以上人民政府设立的土地储备机构，负责土地储备的具体实施工作。土地储备机构按照国家规定实行名录制管理，未纳入国家名录的，不得承担土地储备相关工作。鼓励土地储备机构指导农村集体经济组织开展集体经营性建设用地的前期开发、管护等工作。"})
MERGE (art45)-[:PART_OF]->(chapter5)

// 相关主体
MERGE (agent51:Agent {name: "土地储备机构", type: "organization"})
MERGE (agent52:Agent {name: "国家名录", type: "registry"})

// 土地储备
MERGE (land_reserve:Object {name: "土地储备", type: "land_management"})
MERGE (management2:Object {name: "名录制管理", type: "management_method"})
MERGE (prohibition7:Object {name: "未纳入国家名录不得承担土地储备相关工作", type: "prohibition"})

// 鼓励措施
MERGE (encourage5:Object {name: "指导农村集体经济组织开展集体经营性建设用地的前期开发、管护等工作", type: "encouraged_practice", source_article: "第四十五条"})
MERGE (development_work:Object {name: "前期开发", type: "development_work"})
MERGE (maintenance_work:Object {name: "管护", type: "maintenance_work"})

// 义务
MERGE (duty146:Obligation {description: "负责土地储备的具体实施工作", source_article: "第四十五条"})
MERGE (duty147:Obligation {description: "按照国家规定实行名录制管理", source_article: "第四十五条"})
MERGE (duty148:Obligation {description: "不得承担土地储备相关工作", condition: "未纳入国家名录", source_article: "第四十五条"})

// 关系建立
MERGE (agent51)-[:HAS_DUTY]->(duty146)
MERGE (agent25)-[:HAS_DUTY]->(duty147)
MERGE (agent51)-[:MUST_NOT]->(prohibition7)

MERGE (duty146)-[:IMPLEMENTING]->(land_reserve)
MERGE (duty147)-[:USES_METHOD]->(management2)
MERGE (duty147)-[:MANAGES]->(agent52)

MERGE (prohibition7)-[:CONDITIONED_BY]->(agent52)
MERGE (agent51)-[:ENCOURAGED_TO]->(encourage5)
MERGE (encourage5)-[:TARGETS]->(agent31)
MERGE (encourage5)-[:INVOLVES_WORK]->(development_work)
MERGE (encourage5)-[:INVOLVES_WORK]->(maintenance_work)
MERGE (development_work)-[:RELATED_TO]->(land_use7)
MERGE (maintenance_work)-[:RELATED_TO]->(land_use7)

// 第四十六条
MERGE (art46:Article {number: "第四十六条", full_text: "建设项目施工、地质勘查需要临时使用土地的，由县级以上人民政府自然资源主管部门批准。使用国有土地的，应当与有关自然资源主管部门签订临时使用土地合同；使用农民集体所有土地的，应当与土地所属的农村集体经济组织或者村民委员会签订临时使用土地合同。对原土地使用权人或者土地承包经营权人造成损失的，由签订合同的自然资源主管部门或者农村集体经济组织、村民委员会依法给予补偿，相关补偿费用纳入临时使用土地补偿费。"})
MERGE (art46)-[:PART_OF]->(chapter5)

// 相关主体
MERGE (agent53:Agent {name: "建设项目施工单位", type: "entity"})
MERGE (agent54:Agent {name: "地质勘查单位", type: "entity"})
MERGE (agent55:Agent {name: "村民委员会", type: "organization"})

// 临时用地
MERGE (temp_land_use:Object {name: "临时使用土地", type: "land_use_type"})
MERGE (temp_contract:Object {name: "临时使用土地合同", type: "contract_type"})
MERGE (approval2:Object {name: "临时使用土地批准", type: "approval"})
MERGE (compensation3:Object {name: "临时使用土地补偿费", type: "compensation_type"})

// 合同签订主体
MERGE (contract_party1:Object {name: "自然资源主管部门（国有土地）", type: "contract_party"})
MERGE (contract_party2:Object {name: "农村集体经济组织或村民委员会（集体土地）", type: "contract_party"})

// 义务
MERGE (duty149:Obligation {description: "批准临时使用土地", source_article: "第四十六条"})
MERGE (duty150:Obligation {description: "（国有）签订临时使用土地合同", condition: "使用国有土地", source_article: "第四十六条"})
MERGE (duty151:Obligation {description: "（农民集体）签订临时使用土地合同", condition: "使用农民集体所有土地", source_article: "第四十六条"})
MERGE (duty152:Obligation {description: "依法给予补偿", condition: "对原土地使用权人或者土地承包经营权人造成损失", source_article: "第四十六条"})

// 关系建立
MERGE (agent38)-[:HAS_DUTY]->(duty149)
MERGE (agent39)-[:HAS_DUTY]->(duty149)
MERGE (agent53)-[:HAS_DUTY]->(duty150)
MERGE (agent54)-[:HAS_DUTY]->(duty150)
MERGE (agent53)-[:HAS_DUTY]->(duty151)
MERGE (agent54)-[:HAS_DUTY]->(duty151)
MERGE (agent38)-[:HAS_DUTY]->(duty152)
MERGE (agent39)-[:HAS_DUTY]->(duty152)
MERGE (agent31)-[:HAS_DUTY]->(duty152)
MERGE (agent55)-[:HAS_DUTY]->(duty152)

MERGE (duty149)-[:HAS_AUTHORITY]->(temp_land_use)
MERGE (duty149)-[:GRANTS_APPROVAL]->(approval2)

MERGE (duty150)-[:SIGNS_CONTRACT_WITH]->(contract_party1)
MERGE (duty150)-[:SIGNS_CONTRACT]->(temp_contract)
MERGE (duty151)-[:SIGNS_CONTRACT_WITH]->(contract_party2)
MERGE (duty151)-[:SIGNS_CONTRACT]->(temp_contract)

MERGE (duty152)-[:PAYS_COMPENSATION]->(compensation3)
MERGE (compensation3)-[:RELATED_TO]->(temp_contract)
MERGE (compensation3)-[:COMPENSATES]->(agent28)
MERGE (compensation3)-[:COMPENSATES]->(agent29)









































// 第六章 监督检查
// 创建第六章节点（确保文档节点已存在）
MATCH (doc:Document {name: "广东省土地管理条例"})
MERGE (chapter6:Chapter {number: "第六章", title: "监督检查"})
MERGE (chapter6)-[:PART_OF]->(doc)

// 第四十七条
MERGE (art47:Article {number: "第四十七条", full_text: "省人民政府建立土地督察制度，对地级以上市人民政府土地利用和土地管理情况进行督察。省人民政府授权的机构进行督察时，有权向有关单位和个人了解督察事项有关情况。有关单位和个人应当支持、协助，如实反映情况，并提供有关资料。被督察的人民政府违反土地管理法律、法规、规章，或者落实国家和省有关土地管理决策不力的，省人民政府授权的机构可以向被督察的人民政府下达督察意见书，被督察的人民政府应当认真组织整改，及时报告整改情况。省人民政府授权的机构可以约谈被督察的人民政府有关负责人，并可以依法向监察机关、任免机关等有关机关提出追究相关责任人责任的建议。"})
MERGE (art47)-[:PART_OF]->(chapter6)

// 主体
MERGE (prov_gov:Agent {name: "省人民政府", type: "government_level"})
MERGE (authorized_institution:Agent {name: "省人民政府授权的机构", type: "institution"})
MERGE (municipal_gov:Agent {name: "地级以上市人民政府", type: "government_level"})
MERGE (relevant_units:Agent {name: "有关单位", type: "entity"})
MERGE (relevant_individuals:Agent {name: "个人", type: "individual"})
MERGE (supervision_target_gov:Agent {name: "被督察的人民政府", type: "government_level"})
MERGE (supervision_target_resp_person:Agent {name: "被督察的人民政府有关负责人", type: "individual"})
MERGE (supervisory_organs:Agent {name: "监察机关、任免机关等有关机关", type: "organization"})

// 制度
MERGE (land_supervision_system:System {name: "土地督察制度", type: "supervision_system", source_article: "第四十七条"})

// 义务
MERGE (duty47_1:Obligation {description: "建立土地督察制度", source_article: "第四十七条"})
MERGE (duty47_2:Obligation {description: "支持、协助督察工作，如实反映情况，并提供有关资料", source_article: "第四十七条"})
MERGE (duty47_3:Obligation {description: "认真组织整改，及时报告整改情况", source_article: "第四十七条"})

// 权限
MERGE (authority47_1:Authority {description: "向有关单位和个人了解督察事项有关情况", source_article: "第四十七条"})
MERGE (authority47_2:Authority {description: "向被督察的人民政府下达督察意见书", source_article: "第四十七条"})
MERGE (authority47_3:Authority {description: "约谈被督察的人民政府有关负责人", source_article: "第四十七条"})
MERGE (authority47_4:Authority {description: "向监察机关、任免机关等有关机关提出追究相关责任人责任的建议", source_article: "第四十七条"})

// 关系建立 - 第四十七条
MERGE (prov_gov)-[:HAS_DUTY]->(duty47_1)
MERGE (prov_gov)-[:ESTABLISHES]->(land_supervision_system)
MERGE (land_supervision_system)-[:SUPERVISES]->(municipal_gov)
MERGE (authorized_institution)-[:HAS_AUTHORITY]->(authority47_1)
MERGE (authorized_institution)-[:HAS_AUTHORITY]->(authority47_2)
MERGE (authorized_institution)-[:HAS_AUTHORITY]->(authority47_3)
MERGE (authorized_institution)-[:HAS_AUTHORITY]->(authority47_4)
MERGE (relevant_units)-[:HAS_DUTY]->(duty47_2)
MERGE (relevant_individuals)-[:HAS_DUTY]->(duty47_2)
MERGE (supervision_target_gov)-[:HAS_DUTY]->(duty47_3)
MERGE (authority47_2)-[:ISSUES_TO]->(supervision_target_gov)
MERGE (authority47_3)-[:INTERVIEWS]->(supervision_target_resp_person)
MERGE (authority47_4)-[:PROPOSES_TO]->(supervisory_organs)

// 将主体与条款关联
MERGE (art47)-[:INVOLVES]->(prov_gov)
MERGE (art47)-[:INVOLVES]->(authorized_institution)
MERGE (art47)-[:INVOLVES]->(municipal_gov)
MERGE (art47)-[:INVOLVES]->(relevant_units)
MERGE (art47)-[:INVOLVES]->(relevant_individuals)
MERGE (art47)-[:INVOLVES]->(supervision_target_gov)
MERGE (art47)-[:INVOLVES]->(supervision_target_resp_person)
MERGE (art47)-[:INVOLVES]->(supervisory_organs)

// 第四十八条
MERGE (art48:Article {number: "第四十八条", full_text: "县级以上人民政府自然资源、农业农村主管部门以及乡镇人民政府应当按照各自职责建立土地巡查制度，运用卫星遥感、无人机航摄、视频监控等手段加强土地违法行测，及时发现并依法制止土地违法行为。各级人民政府应当科学合理配备负责日常土地管理监督检查的工作人员。"})
MERGE (art48)-[:PART_OF]->(chapter6)

// 主体
MERGE (county_above_gov:Agent {name: "县级以上人民政府", type: "government_level"})
MERGE (natural_resources_dept:Agent {name: "自然资源主管部门", type: "department"})
MERGE (agriculture_rural_dept:Agent {name: "农业农村主管部门", type: "department"})
MERGE (township_gov:Agent {name: "乡镇人民政府", type: "government_level"})
MERGE (all_level_gov:Agent {name: "各级人民政府", type: "government_level"})

// 制度与工具
MERGE (land_patrol_system:System {name: "土地巡查制度", type: "supervision_system", source_article: "第四十八条"})
MERGE (satellite_remote_sensing:Object {name: "卫星遥感", type: "monitoring_tool", source_article: "第四十八条"})
MERGE (drone_aerial_photography:Object {name: "无人机航摄", type: "monitoring_tool", source_article: "第四十八条"})
MERGE (video_monitoring:Object {name: "视频监控", type: "monitoring_tool", source_article: "第四十八条"})

// 义务
MERGE (duty48_1:Obligation {description: "按照各自职责建立土地巡查制度", source_article: "第四十八条"})
MERGE (duty48_2:Obligation {description: "运用卫星遥感、无人机航摄、视频监控等手段加强土地违法行为监测", source_article: "第四十八条"})
MERGE (duty48_3:Obligation {description: "及时发现并依法制止土地违法行为", source_article: "第四十八条"})
MERGE (duty48_4:Obligation {description: "科学合理配备负责日常土地管理监督检查的工作人员", source_article: "第四十八条"})

// 关系建立 - 第四十八条
MERGE (natural_resources_dept)-[:HAS_DUTY]->(duty48_1)
MERGE (agriculture_rural_dept)-[:HAS_DUTY]->(duty48_1)
MERGE (township_gov)-[:HAS_DUTY]->(duty48_1)
MERGE (duty48_1)-[:ESTABLISHES]->(land_patrol_system)

MERGE (natural_resources_dept)-[:HAS_DUTY]->(duty48_2)
MERGE (agriculture_rural_dept)-[:HAS_DUTY]->(duty48_2)
MERGE (township_gov)-[:HAS_DUTY]->(duty48_2)
MERGE (duty48_2)-[:USES_TOOL]->(satellite_remote_sensing)
MERGE (duty48_2)-[:USES_TOOL]->(drone_aerial_photography)
MERGE (duty48_2)-[:USES_TOOL]->(video_monitoring)

MERGE (natural_resources_dept)-[:HAS_DUTY]->(duty48_3)
MERGE (agriculture_rural_dept)-[:HAS_DUTY]->(duty48_3)
MERGE (township_gov)-[:HAS_DUTY]->(duty48_3)

MERGE (all_level_gov)-[:HAS_DUTY]->(duty48_4)

// 将主体与条款关联
MERGE (art48)-[:INVOLVES]->(natural_resources_dept)
MERGE (art48)-[:INVOLVES]->(agriculture_rural_dept)
MERGE (art48)-[:INVOLVES]->(township_gov)
MERGE (art48)-[:INVOLVES]->(all_level_gov)

// 第四十九条
MERGE (art49:Article {number: "第四十九条", full_text: "省人民政府自然资源主管部门应当建立重大土地违法案件督办制度。地级以上市人民政府自然资源主管部门未按照要求和时限办理督办案件的，省人民政府自然资源主管部门可以责令其限期整改；省人民政府自然资源主管部门经省人民政府同意，可以在整改期间暂停或者责令暂停违法案件所在地有关农用地转用、征收土地的审批。"})
MERGE (art49)-[:PART_OF]->(chapter6)

// 主体
MERGE (prov_natural_resources_dept:Agent {name: "省人民政府自然资源主管部门", type: "department"})

// 制度
MERGE (major_violation_case_supervision_system:System {name: "重大土地违法案件督办制度", type: "supervision_system", source_article: "第四十九条"})

// 义务与权限
MERGE (duty49_1:Obligation {description: "建立重大土地违法案件督办制度", source_article: "第四十九条"})
MERGE (authority49_1:Authority {description: "责令限期整改", source_article: "第四十九条"})
MERGE (authority49_2:Authority {description: "暂停或者责令暂停违法案件所在地有关农用地转用、征收土地的审批", source_article: "第四十九条"})

// 相关手续
MERGE (farmland_conversion_approval:Object {name: "农用地转用审批", type: "approval", source_article: "第四十九条"})
MERGE (land_expropriation_approval:Object {name: "征收土地审批", type: "approval", source_article: "第四十九条"})

// 适用条件
MERGE (condition49_1:Object {name: "未按照要求和时限办理督办案件", type: "condition", source_article: "第四十九条"})
MERGE (condition49_2:Object {name: "整改期间，经省人民政府同意", type: "condition", source_article: "第四十九条"})

// 关系建立 - 第四十九条
MERGE (prov_natural_resources_dept)-[:HAS_DUTY]->(duty49_1)
MERGE (duty49_1)-[:ESTABLISHES]->(major_violation_case_supervision_system)
MERGE (prov_natural_resources_dept)-[:HAS_AUTHORITY]->(authority49_1)
MERGE (prov_natural_resources_dept)-[:HAS_AUTHORITY]->(authority49_2)
MERGE (authority49_1)-[:APPLIES_WHEN]->(condition49_1)
MERGE (authority49_2)-[:APPLIES_WHEN]->(condition49_2)
MERGE (authority49_2)-[:SUSPENDS]->(farmland_conversion_approval)
MERGE (authority49_2)-[:SUSPENDS]->(land_expropriation_approval)

// 将主体与条款关联
MERGE (art49)-[:INVOLVES]->(prov_natural_resources_dept)

// 第五十条
MERGE (art50:Article {number: "第五十条", full_text: "县级以上人民政府自然资源主管部门在调查处理土地违法案件期间，有权暂停或者责令暂停办理与该违法案件相关的土地审批、登记等手续。县级以上人民政府可以根保护、土地利用计划执行、土地节约集约利用、土地利用秩序等情况，按照规定相应奖励或者扣减下级人民政府土地利用年度计划指标。"})
MERGE (art50)-[:PART_OF]->(chapter6)

// 主体
MERGE (county_above_natural_resources_dept:Agent {name: "县级以上人民政府自然资源主管部门", type: "department"})
MERGE (lower_gov:Agent {name: "下级人民政府", type: "government_level"})

// 权限
MERGE (authority50_1:Authority {description: "暂停或者责令暂停办理与违法案件相关的土地审批、登记等手续", source_article: "第五十条"})
MERGE (authority50_2:Authority {description: "奖励或者扣减下级人民政府土地利用年度计划指标", source_article: "第五十条"})

// 相关手续
MERGE (land_approval:Object {name: "土地审批", type: "procedure", source_article: "第五十条"})
MERGE (land_registration:Object {name: "土地登记", type: "procedure", source_article: "第五十条"})
MERGE (land_use_annual_plan:Object {name: "土地利用年度计划指标", type: "land_use_plan", source_article: "第五十条"})

// 适用条件
MERGE (condition50_1:Object {name: "调查处理土地违法案件期间", type: "condition", source_article: "第五十条"})
MERGE (condition50_2:Object {name: "耕地保护、土地利用计划执行、土地节约集约利用、土地利用秩序等情况", type: "condition", source_article: "第五十条"})

// 关系建立 - 第五十条
MERGE (county_above_natural_resources_dept)-[:HAS_AUTHORITY]->(authority50_1)
MERGE (authority50_1)-[:SUSPENDS]->(land_approval)
MERGE (authority50_1)-[:SUSPENDS]->(land_registration)
MERGE (authority50_1)-[:APPLIES_WHEN]->(condition50_1)

MERGE (county_above_gov)-[:HAS_AUTHORITY]->(authority50_2)
MERGE (authority50_2)-[:ADJUSTS]->(land_use_annual_plan)
MERGE (authority50_2)-[:APPLIES_TO]->(lower_gov)
MERGE (authority50_2)-[:BASED_ON]->(condition50_2)

// 将主体与条款关联
MERGE (art50)-[:INVOLVES]->(county_above_natural_resources_dept)
MERGE (art50)-[:INVOLVES]->(county_above_gov)
MERGE (art50)-[:INVOLVES]->(lower_gov)

// 第五十一条
MERGE (art51:Article {number: "第五十一条", full_text: "县级以上人民政府应当将国土空间规划、土地利用年度计划、耕地保护责任制等执行情况列为国民经济和社会发展计划执行情况、国有自然资源管理情况的内容，依法向本级人民代表大会或者其常务委员会报告。"})
MERGE (art51)-[:PART_OF]->(chapter6)

// 主体
MERGE (people_congress:Agent {name: "本级人民代表大会", type: "government_level"})
MERGE (standing_committee:Agent {name: "常务委员会", type: "government_level"})

// 报告内容
MERGE (spatial_planning_execution:Object {name: "国土空间规划执行情况", type: "report_content", source_article: "第五十一条"})
MERGE (land_use_plan_execution:Object {name: "土地利用年度计划执行情况", type: "report_content", source_article: "第五十一条"})
MERGE (farmland_protection_resp_sys:Object {name: "耕地保护责任制执行情况", type: "report_content", source_article: "第五十一条"})
MERGE (economic_social_development:Object {name: "国民经济和社会发展计划执行情况", type: "report_content", source_article: "第五十一条"})
MERGE (state_natural_resources_mgmt:Object {name: "国有自然资源管理情况", type: "report_content", source_article: "第五十一条"})

// 义务
MERGE (duty51_1:Obligation {description: "将国土空间规划、土地利用年度计划、耕地保护责任制等执行情况列为国民经济和社会发展计划执行情况、国有自然资源管理情况的内容，依法向本级人民代表大会或者其常务委员会报告", source_article: "第五十一条"})

// 关系建立 - 第五十一条
MERGE (county_above_gov)-[:HAS_DUTY]->(duty51_1)
MERGE (duty51_1)-[:INCLUDES_REPORT_CONTENT]->(spatial_planning_execution)
MERGE (duty51_1)-[:INCLUDES_REPORT_CONTENT]->(land_use_plan_execution)
MERGE (duty51_1)-[:INCLUDES_REPORT_CONTENT]->(farmland_protection_resp_sys)
MERGE (duty51_1)-[:REPORTS_TO]->(people_congress)
MERGE (duty51_1)-[:REPORTS_TO]->(standing_committee)

// 将主体与条款关联
MERGE (art51)-[:INVOLVES]->(county_above_gov)
MERGE (art51)-[:INVOLVES]->(people_congress)
MERGE (art51)-[:INVOLVES]->(standing_committee)
























// 创建文档节点（如果尚未创建）
// 创建第七章节点
MATCH (doc:Document {name: "广东省土地管理条例"})
MERGE (chapter7:Chapter {number: "第七章", title: "法律责任"})
MERGE (chapter7)-[:PART_OF]->(doc)


// 第五十二条
MERGE (art52:Article {number: "第五十二条", full_text: "未经批准或者采取欺骗手段骗取批准，非法占用土地的，由县级以上人民政府自然资源主管部门责令退还非法占用的土地，对违反国土空间规划擅自占用建设用地、未利用地的，限期拆除在非法占用的土地上新建的建筑物和其他设施，恢复土地原状，对符合国土空间规划的，没收在非法占用的土地上新建的建筑物和其他设施，可以并处非法占用土地每平方米一百元以上一千元以下的罚款；对非法占用土地单位的直接负责的主管人员和其他直接责任人员，依法给予处分；构成犯罪的，依法追究刑事责任。"})
MERGE (art52)-[:PART_OF]->(chapter7)

// 主体
MERGE (county_above_natural_resources_dept:Agent {name: "县级以上人民政府自然资源主管部门", type: "department"})
MERGE (illegal_land_occupier:Agent {name: "非法占用土地单位", type: "entity"})
MERGE (directly_responsible_personnel:Agent {name: "直接负责的主管人员和其他直接责任人员", type: "individual"})

// 义务与禁止
MERGE (prohibition52_1:Prohibition {description: "未经批准非法占用土地", source_article: "第五十二条"})
MERGE (prohibition52_2:Prohibition {description: "采取欺骗手段骗取批准占用土地", source_article: "第五十二条"})

// 处罚
MERGE (penalty52_1:Penalty {description: "责令退还非法占用的土地", source_article: "第五十二条"})
MERGE (penalty52_2:Penalty {description: "限期拆除在非法占用的土地上新建的建筑物和其他设施，恢复土地原状", condition: "违反国土空间规划擅自占用建设用地、未利用地", source_article: "第五十二条"})
MERGE (penalty52_3:Penalty {description: "没收在非法占用的土地上新建的建筑物和其他设施", condition: "符合国土空间规划", source_article: "第五十二条"})
MERGE (penalty52_4:Penalty {description: "处以非法占用土地每平方米一百元以上一千元以下的罚款", source_article: "第五十二条"})
MERGE (penalty52_5:Penalty {description: "依法给予处分", target: "直接负责的主管人员和其他直接责任人员", source_article: "第五十四条"})
MERGE (penalty52_6:Penalty {description: "依法追究刑事责任", condition: "构成犯罪", source_article: "第五十二条、第五十四条"})

// 条件
MERGE (condition52_1:Object {name: "违反国土空间规划擅自占用建设用地、未利用地", type: "condition", source_article: "第五十二条"})
MERGE (condition52_2:Object {name: "符合国土空间规划"})
SET condition52_2.type = "condition", condition52_2.source_article = "第四十三条、第五十二条"
MERGE (condition52_3:Object {name: "构成犯罪", type: "condition", source_article: "第五十二条"})

// 关系建立 - 第五十二条
MERGE (county_above_natural_resources_dept)-[:HAS_AUTHORITY]->(authority52_1:Authority {description: "责令退还非法占用的土地", source_article: "第五十二条"})
MERGE (county_above_natural_resources_dept)-[:HAS_AUTHORITY]->(authority52_2:Authority {description: "限期拆除在非法占用的土地上新建的建筑物和其他设施，恢复土地原状", source_article: "第五十二条", condition: "违反国土空间规划擅自占用建设用地、未利用地"})
MERGE (county_above_natural_resources_dept)-[:HAS_AUTHORITY]->(authority52_3:Authority {description: "没收在非法占用的土地上新建的建筑物和其他设施", source_article: "第五十二条", condition: "符合国土空间规划"})
MERGE (county_above_natural_resources_dept)-[:HAS_AUTHORITY]->(authority52_4:Authority {description: "处以非法占用土地每平方米一百元以上一千元以下的罚款", source_article: "第五十二条"})

MERGE (authority52_2)-[:APPLIES_WHEN]->(condition52_1)
MERGE (authority52_3)-[:APPLIES_WHEN]->(condition52_2)
MERGE (authority52_4)-[:HAS_PENALTY]->(penalty52_4)

MERGE (illegal_land_occupier)-[:SUBJECT_TO]->(penalty52_1)
MERGE (illegal_land_occupier)-[:SUBJECT_TO]->(penalty52_2)
MERGE (illegal_land_occupier)-[:SUBJECT_TO]->(penalty52_3)
MERGE (illegal_land_occupier)-[:SUBJECT_TO]->(penalty52_4)
MERGE (directly_responsible_personnel)-[:SUBJECT_TO]->(penalty52_5)
MERGE (directly_responsible_personnel)-[:SUBJECT_TO]->(penalty52_6)

MERGE (penalty52_2)-[:APPLIES_WHEN]->(condition52_1)
MERGE (penalty52_3)-[:APPLIES_WHEN]->(condition52_2)
MERGE (penalty52_6)-[:APPLIES_WHEN]->(condition52_3)

// 将主体与条款关联
MERGE (art52)-[:INVOLVES]->(county_above_natural_resources_dept)
MERGE (art52)-[:INVOLVES]->(illegal_land_occupier)
MERGE (art52)-[:INVOLVES]->(directly_responsible_personnel)

// 第五十三条
MERGE (art53:Article {number: "第五十三条", full_text: "用地单位和个人未按照规定足额预存土地复垦费用的，由县级以上人民政府自然资源主管部门责令限期改正；逾期不改正的，处十万元以上五十万元以下的罚款。"})
MERGE (art53)-[:PART_OF]->(chapter7)

// 主体
MERGE (land_user_unit:Agent {name: "用地单位", type: "entity"})
MERGE (land_user_individual:Agent {name: "个人", type: "individual"})

// 义务
MERGE (duty53_1:Obligation {description: "按照规定足额预存土地复垦费用", source_article: "第五十三条"})

// 处罚
MERGE (penalty53_1:Penalty {description: "责令限期改正", source_article: "第五十三条"})
MERGE (penalty53_2:Penalty {description: "处十万元以上五十万元以下的罚款", condition: "逾期不改正", source_article: "第五十三条"})

// 条件
MERGE (condition53_1:Object {name: "逾期不改正", type: "condition", source_article: "第五十三条"})

// 关系建立 - 第五十三条
MERGE (county_above_natural_resources_dept)-[:HAS_AUTHORITY]->(authority53_1:Authority {description: "责令限期改正", source_article: "第五十三条"})
MERGE (county_above_natural_resources_dept)-[:HAS_AUTHORITY]->(authority53_2:Authority {description: "处十万元以上五十万元以下的罚款", source_article: "第五十三条", condition: "逾期不改正"})

MERGE (authority53_2)-[:APPLIES_WHEN]->(condition53_1)

MERGE (land_user_unit)-[:HAS_DUTY]->(duty53_1)
MERGE (land_user_individual)-[:HAS_DUTY]->(duty53_1)
MERGE (land_user_unit)-[:SUBJECT_TO]->(penalty53_1)
MERGE (land_user_individual)-[:SUBJECT_TO]->(penalty53_1)
MERGE (land_user_unit)-[:SUBJECT_TO]->(penalty53_2)
MERGE (land_user_individual)-[:SUBJECT_TO]->(penalty53_2)

// 将主体与条款关联
MERGE (art53)-[:INVOLVES]->(county_above_natural_resources_dept)
MERGE (art53)-[:INVOLVES]->(land_user_unit)
MERGE (art53)-[:INVOLVES]->(land_user_individual)

// 第五十四条
MERGE (art54:Article {number: "第五十四条", full_text: "各级人民政府及自然资源、农业农村等有关部门有下列情形之一，依照法律、法规和国家规定追究责任，对直接负责的主管人员和其他直接责任人员依法给予处分；构成犯罪的，依法追究刑事责任： （一）违反法定权限、程序擅自批准或者修改国土空间规划的； （二）违反法定权限、程序或者不按照国土空间规划确定的土地用途批准使用土地的； （三）违反法定权限、程序进行土地征收的； （四）侵占、挪用征收土地补偿费用和其他有关费用的； （五）未依法依规履行土地监督检查职责的； （六）拒绝、阻碍土地督察机构依法执行职务的； （七）其他玩忽职守、滥用职权、徇私舞弊的情形。"})
MERGE (art54)-[:PART_OF]->(chapter7)

// 主体
MERGE (all_level_gov:Agent {name: "各级人民政府", type: "government_level"})
MERGE (natural_resources_dept:Agent {name: "自然资源主管部门", type: "department"})
MERGE (agriculture_rural_dept:Agent {name: "农业农村主管部门", type: "department"})
MERGE (directly_resp_personnel:Agent {name: "直接负责的主管人员和其他直接责任人员", type: "individual"})
MERGE (land_supervision_org:Agent {name: "土地督察机构", type: "institution"})

// 禁止行为
MERGE (prohibition54_1:Prohibition {description: "违反法定权限、程序擅自批准或者修改国土空间规划", source_article: "第五十四条"})
MERGE (prohibition54_2:Prohibition {description: "违反法定权限、程序或者不按照国土空间规划确定的土地用途批准使用土地", source_article: "第五十四条"})
MERGE (prohibition54_3:Prohibition {description: "违反法定权限、程序进行土地征收", source_article: "第五十四条"})
MERGE (prohibition54_4:Prohibition {description: "侵占、挪用征收土地补偿费用和其他有关费用", source_article: "第五十四条"})
MERGE (prohibition54_5:Prohibition {description: "未依法依规履行土地监督检查职责", source_article: "第五十四条"})
MERGE (prohibition54_6:Prohibition {description: "拒绝、阻碍土地督察机构依法执行职务", source_article: "第五十四条"})
MERGE (prohibition54_7:Prohibition {description: "玩忽职守、滥用职权、徇私舞弊", source_article: "第五十四条"})

// 处罚
MERGE (penalty54_1:Penalty {description: "依照法律、法规和国家规定追究责任", source_article: "第五十四条"})

// 关系建立 - 第五十四条
MERGE (all_level_gov)-[:PROHIBITED_FROM]->(prohibition54_1)
MERGE (all_level_gov)-[:PROHIBITED_FROM]->(prohibition54_2)
MERGE (all_level_gov)-[:PROHIBITED_FROM]->(prohibition54_3)
MERGE (all_level_gov)-[:PROHIBITED_FROM]->(prohibition54_4)
MERGE (all_level_gov)-[:PROHIBITED_FROM]->(prohibition54_5)
MERGE (all_level_gov)-[:PROHIBITED_FROM]->(prohibition54_6)

MERGE (natural_resources_dept)-[:PROHIBITED_FROM]->(prohibition54_1)
MERGE (natural_resources_dept)-[:PROHIBITED_FROM]->(prohibition54_2)
MERGE (natural_resources_dept)-[:PROHIBITED_FROM]->(prohibition54_3)
MERGE (natural_resources_dept)-[:PROHIBITED_FROM]->(prohibition54_4)
MERGE (natural_resources_dept)-[:PROHIBITED_FROM]->(prohibition54_5)
MERGE (natural_resources_dept)-[:PROHIBITED_FROM]->(prohibition54_6)

MERGE (agriculture_rural_dept)-[:PROHIBITED_FROM]->(prohibition54_5)
MERGE (directly_resp_personnel)-[:SUBJECT_TO]->(penalty54_1)
MERGE (directly_resp_personnel)-[:SUBJECT_TO]->(penalty52_5)
MERGE (directly_resp_personnel)-[:SUBJECT_TO]->(penalty52_6)

// 将主体与条款关联
MERGE (art54)-[:INVOLVES]->(all_level_gov)
MERGE (art54)-[:INVOLVES]->(natural_resources_dept)
MERGE (art54)-[:INVOLVES]->(agriculture_rural_dept)
MERGE (art54)-[:INVOLVES]->(directly_resp_personnel)
MERGE (art54)-[:INVOLVES]->(land_supervision_org)










// 创建第八章节点
MERGE (chapter8:Chapter {number: "第八章", title: "附则"})
MERGE (chapter8)-[:PART_OF]->(doc)

// 第五十五条
MERGE (art55:Article {number: "第五十五条", full_text: "本条例自 2022年 8月 1日起施行，《广东省实施〈中华人民共和国土地管理法〉办法》同时废止。"})
MERGE (art55)-[:PART_OF]->(chapter8)

// 实施日期
MERGE (implementation_date:Object {name: "实施日期", value: "2022年8月1日", source_article: "第五十五条"})

// 废止法规
MERGE (repealed_regulation:Object {name: "广东省实施《中华人民共和国土地管理法》办法", type: "regulation", status: "废止", source_article: "第五十五条"})

// 关系建立 - 第五十五条
MERGE (doc)-[:HAS_IMPLEMENTATION_DATE]->(implementation_date)
MERGE (doc)-[:REPEALS]->(repealed_regulation)

// 将主体与条款关联
MERGE (art55)-[:INVOLVES]->(doc)




// 模糊化处理
CREATE FULLTEXT INDEX authorityDescription FOR (n:Authority) ON EACH [n.description];


//索引案例
// 利用索引进行模糊匹配
CALL db.index.fulltext.queryNodes("authorityDescription", "农用地 AND 转为建设用地 AND 审批") YIELD node, score
MATCH (agent:Agent)-[:HAS_AUTHORITY]->(node)
RETURN agent.name, node.description, score
ORDER BY score DESC
LIMIT 10














// 1. 创建顶层概念节点
MERGE (c_gov:Concept {name: "政府机关", description: "各级人民政府及其派出机关"})
MERGE (c_dept:Concept {name: "主管部门", description: "负责具体专项行政管理事务的政府职能部门"})
MERGE (c_leg:Concept {name: "立法机关", description: "各级人民代表大会及其常务委员会"});

// 2. 将具体“政府机关”映射到概念
MATCH (a:Agent)
WHERE a.name IN [
    '各级人民政府', '县级以上人民政府', '上级人民政府', '上一级人民政府', '被督察的人民政府',
    '国务院', '省人民政府', '地级以上市人民政府', '县（市、区）人民政府', '县级人民政府', 
    '乡镇人民政府', '街道办事处'
]
MATCH (c_gov:Concept {name: "政府机关"})
MERGE (a)-[:BELONGS_TO_CONCEPT]->(c_gov);

// 3. 将具体“主管部门”映射到概念
MATCH (a:Agent)
WHERE a.name CONTAINS '自然资源' 
   OR a.name CONTAINS '农业农村' 
   OR a.name IN [
    '林业主管部门', '发展改革部门', '人力资源社会保障部门', '住房城乡建设部门', 
    '交通运输部门', '政务服务数据管理部门', '有关部门', '其他相关主管部门'
]
MATCH (c_dept:Concept {name: "主管部门"})
MERGE (a)-[:BELONGS_TO_CONCEPT]->(c_dept);

// 4. 将具体“立法机关”映射到概念
MATCH (a:Agent)
WHERE a.name CONTAINS '人民代表大会' OR a.name = '常务委员会'
MATCH (c_leg:Concept {name: "立法机关"})
MERGE (a)-[:BELONGS_TO_CONCEPT]->(c_leg);


MATCH (all:Agent {name: "各级人民政府"})
MATCH (above_county:Agent {name: "县级以上人民政府"})
MATCH (county:Agent {name: "县级人民政府"})
MATCH (city:Agent {name: "地级以上市人民政府"})

// 建立层级包含关系
MERGE (all)-[:INCLUDES_LEVEL]->(above_county)
MERGE (all)-[:INCLUDES_LEVEL]->(county)
MERGE (all)-[:INCLUDES_LEVEL]->(city)
MERGE (above_county)-[:INCLUDES_LEVEL]->(county)
MERGE (above_county)-[:INCLUDES_LEVEL]->(city)