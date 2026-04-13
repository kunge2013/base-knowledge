---
title: "快速入门 - SQLBot 文档"
source: "https://sqlbot.org/docs/v1/quick_start/"
author:
  - "[[飞致云]]"
published:
created: 2026-04-12
description: "SQLBot 是基于大模型和 RAG 的智能问数系统"
tags:
  - "clippings"
---
## 快速入门

## 1 安装 SQLBot

> [!tip] Tip
> 可以通过 1Panel 应用商店快速安装 SQLBot：
> 
> ```js
> http://目标服务器 IP 地址:8000
> 
> 用户名：admin
> 
> 默认密码：SQLBot@123456
> ```
> 
> 详细步骤参考 [**1Panel 快速安装 SQLBot**](https://sqlbot.org/docs/v1/installation/1panel_installtion/) 。
> 
> 如果是用于生产环境，推荐使用 [**离线包方式**](https://sqlbot.org/docs/v1/installation/offline_installtion/) 进行部署。

## 2 界面介绍

> [!tip] Tip
> SQLBot 主界面导航栏包含四大核心模块：【智能问数】、【数据源】、【仪表板】和【设置】。
> 
> 左侧为功能导航区域支持功能模块的快速切换，并显示当前所在的工作空间，若用户拥有多个空间权限，可在此处进行空间切换。

![导航栏](https://sqlbot.org/docs/v1/img/index/navigation_bar.png)

> [!tip] Tip
> 支持用户通过自然语言提问的方式，与 AI 模型进行对话，自动分析并返回可视化图表。
> 
> ![智能问数](https://sqlbot.org/docs/v1/img/index/smart_question.png)
> 
> 支持配置并管理数据来源，可对接 Excel/CSV、数据库等多种类型。
> 
> ![数据源](https://sqlbot.org/docs/v1/img/index/data_source.png)
> 
> 支持构建自定义可视化数据看板，将对话中的图表整合布局，进行图表展示与数据监控。
> 
> ![仪表板](https://sqlbot.org/docs/v1/img/index/dashboard.png)
> 
> 支持管理员进行成员管理、权限配置管理功能（仅管理员可见）。
> 
> ![设置](https://sqlbot.org/docs/v1/img/index/set.png)

## 3 快速上手

> [!abstract] Abstract
> SQLBot 是一款基于大语言模型的智能问数系统，用户只需配置模型和数据源，即可通过自然语言提问，快速获取可视化数据结果。下面是核心功能配置和使用。

### 3.1 配置 AI 模型

> [!abstract] Abstract
> 以 admin 用户登录后，进入【系统管理】→【AI 模型配置】，点击【添加模型】选择模型供应商，填写模型相关参数后点击【保存】。如有多个模型，可设置默认使用的模型。

![添加模型 APIkey](https://sqlbot.org/docs/v1/img/index/model_info.png)

### 3.2 创建数据源

> [!abstract] Abstract
> 切换到数据源菜单，新建一个数据源连接。
> 
> 如选择 "MySQL"数据源类型，名称为 "生产制造销售数据"，主机名 "10.123.22.252"，数据库名 "zizhaoye"，用户名 "root"，密码 "Password123@mysql" ，检验通过后点击保存即可。

![添加数据源](https://sqlbot.org/docs/v1/img/index/datasource_info.png)

### 3.3 开启智能问数

> [!abstract] Abstract
> 在数据源卡片上点击【开启问数】，或者切换到【智能问数】模块选择数据源进行对话，可选择推荐问题或手动输入问题。
> 
> 模型生成图表后，可更换图表类型、可查看明细数据和 SQL 查询语句等。支持继续提问、进行数据分析或预测。
> 
> Excel 示例文件： [**历史销售数据**](https://resource-fit2cloud-com.oss-cn-hangzhou.aliyuncs.com/sqlbot/sales_history.xlsx) 。

![开启智能问数](https://sqlbot.org/docs/v1/img/index/chat_info.png)

### 3.4 搭建仪表板

> [!abstract] Abstract
> 支持将问数对话中生成的图表整理成一个仪表板，可支持自由拖动、调整图表大小，方便集中查看。
> 
> 新建仪表板时，可添加图表、文字说明或 Tab 组件，实现信息的清晰展示和查看。

![搭建看板](https://sqlbot.org/docs/v1/img/index/cre_dashboard.png)