-- 插入教师数据
INSERT INTO teacher (job_number, name, sex, job_title) VALUES
('T0001', '张三', 1, 1),
('T0002', '李四', 2, 2),
('T0003', '王五', 1, 3),
('T0004', '赵六', 2, 4),
('T0005', '孙七', 1, 5);

-- 插入课程数据
INSERT INTO course (course_number, course_name, hours, course_nature) VALUES
('C0001', '数据库原理', 48, 1),
('C0002', '操作系统', 48, 1),
('C0003', '人工智能', 48, 2),
('C0004', '数据结构', 48, 1),
('C0005', '计算机网络', 48, 2);

-- 插入项目数据
INSERT INTO project (project_number, project_name, project_source, project_type, total_budget, start_year, end_year) VALUES
('P0001', '国家自然科学基金', '国家自然科学基金委员会', 1, 500000.0, '2022-01-01', '2025-12-31'),
('P0002', '省部级重点项目', '教育部', 2, 300000.0, '2021-07-01', '2024-06-30'),
('P0003', '市厅级科技项目', '上海市科技委员会', 3, 200000.0, '2023-03-01', '2026-02-28'),
('P0004', '企业合作项目', '华为', 4, 1000000.0, '2020-05-01', '2023-04-30'),
('P0005', '其它类型项目', '某公司', 5, 150000.0, '2021-09-01', '2024-08-31');

-- 插入论文数据
INSERT INTO paper (serial_number, paper_name, publish_source, publish_year, type, level) VALUES
(1, '基于机器学习的图像识别研究', 'IEEE', '2022-06-15', 1, 1),
(2, '大数据处理技术综述', 'Springer', '2021-11-20', 2, 2),
(3, '一种新型的区块链共识算法', 'ACM', '2023-03-10', 3, 3),
(4, '物联网安全研究', 'Elsevier', '2020-09-25', 4, 4),
(5, '深度学习在自然语言处理中的应用', 'CCF Transactions', '2021-05-18', 1, 5);

-- 插入负责项目数据
INSERT INTO charge_project (job_number, project_number, ranking, own_money) VALUES
('T0001', 'P0001', 1, 100000.0),
('T0002', 'P0002', 2, 50000.0),
('T0003', 'P0003', 3, 30000.0),
('T0004', 'P0004', 4, 250000.0),
('T0005', 'P0005', 5, 20000.0);

-- 插入主讲课程数据
INSERT INTO teach_course (job_number, course_number, year, term, class_hour) VALUES
('T0001', 'C0001', 2022, 1, 48),
('T0002', 'C0002', 2022, 2, 48),
('T0003', 'C0003', 2023, 1, 48),
('T0004', 'C0004', 2023, 3, 48),
('T0005', 'C0005', 2021, 1, 48);

-- 插入发表论文数据
INSERT INTO publish_paper (job_number, serial_number, ranking, corresponding_author) VALUES
('T0001', 1, 1, true),
('T0002', 2, 2, false),
('T0003', 3, 3, false),
('T0004', 4, 4, false),
('T0005', 5, 1, true);
