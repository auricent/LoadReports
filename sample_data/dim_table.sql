CREATE TABLE IF NOT EXISTS dim_network_mapping (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    `source_adn_name` VARCHAR(64) NOT NULL COMMENT '原始渠道名称（来自源表或接口）',
    `target_adn_name` VARCHAR(64) NOT NULL COMMENT '标准渠道名称（用于展示和聚合）',
    `is_active` TINYINT(1) DEFAULT '1' COMMENT '是否启用',
    `remark` VARCHAR(255) DEFAULT NULL COMMENT '备注',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_source_name` (`source_adn_name`) -- 确保原始名称唯一，防止重复定义
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='ADN渠道名称标准映射表';

INSERT INTO dim_network_mapping (source_adn_name, target_adn_name, remark) VALUES
('applovin_custom', 'Applovin', 'Applovin Custom Integration'),
('applovin_exchange', 'Applovin', 'Applovin Exchange'),
('applovin_network', 'Applovin', 'Applovin Network'),
('bidmachine_via_max', 'BidMachine', 'BidMachine via Applovin MAX'),
('chartboost_via_max', 'Chartboost', 'Chartboost via Applovin MAX'),
('fyber_via_max', 'Fyber', 'Fyber (Digital Turbine) via MAX'),
('imobi_via_max', 'InMobi', 'InMobi via MAX'),
('ironsource_via_max', 'ironSource', 'ironSource via MAX'),
('mintegral_via_max', 'Mintegral', 'Mintegral via MAX'),
('moloco_via_max', 'Moloco', 'Moloco via MAX'),
('tiktok_via_max', 'Pangle', 'TikTok (Pangle) via MAX'),
('unity_via_max', 'Unity', 'Unity via MAX'),
('verve_via_max', 'Verve', 'Verve via MAX'),
('vungle_via_max', 'Vungle', 'Liftoff (Vungle) via MAX'),
('bidmatic', 'Bidmatic', 'Bidmatic'),
('BIGO_BIDDING', 'Bigo', 'Bigo Bidding'),
('cpmstar', 'Cpmstar', 'Cpmstar'),
('didna', 'DiDNA', 'DiDNA'),
('IRONSOURCE_NETWORK', 'ironSource', 'ironSource Direct'),
('seedtag', 'Seedtag', 'Seedtag'),
('smartAdServer', 'smartAdServer', 'Smart AdServer / Equativ'),
('xaprio', 'Xaprio', 'Xaprio'),
('yandex', 'Yandex', 'Yandex'),
('amazon_aps', 'Amazon', 'Amazon Publisher Services'); -- 预留示例


CREATE TABLE IF NOT EXISTS dim_ad_unit_mapping (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    -- 源端维度
    `source_adn_name` VARCHAR(64) NOT NULL COMMENT '原始渠道名称(如 applovin_max)',
    `source_unit_id` VARCHAR(128) NOT NULL COMMENT '原始广告单元ID',
    `source_ad_type` VARCHAR(64) DEFAULT NULL COMMENT '原始广告类型(如 0, 1, 或 "inter")',

    -- 目标标准化维度
    `target_unit_id` VARCHAR(128) NOT NULL COMMENT '标准化后的统一单元ID',
    `target_unit_name` VARCHAR(128) DEFAULT NULL COMMENT '标准化的单元名称(如 "Home_Bottom_Banner")',
    `target_ad_type` VARCHAR(64) NOT NULL COMMENT '标准广告类型',

    `is_active` TINYINT(1) DEFAULT '1' COMMENT '是否启用',
    PRIMARY KEY (`id`),
    -- 唯一索引：确保同一个渠道下的同一个原始 ID 只有一条映射规则
    UNIQUE KEY `uk_source_unit` (`source_adn_name`, `source_unit_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='广告单元与类型标准化映射表';


CREATE TABLE IF NOT EXISTS dim_app_mapping (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    -- 源端维度：标识数据从哪来，原始叫什么
    `source_adn_name` VARCHAR(64) NOT NULL COMMENT '原始渠道名称(如 applovin, bidmatic)',
    `source_app_identifier` VARCHAR(128) NOT NULL COMMENT '原始应用标识(可能是包名、App ID或原始名称)',

    -- 目标标准化维度：内部标准的ID和名称
    `target_app_id` INT(11) UNSIGNED NOT NULL COMMENT '标准内部应用ID(1:BT-Android, 2:UT-Android等)',
    `target_app_name` VARCHAR(128) NOT NULL COMMENT '标准化应用名称',
    `platform` VARCHAR(64) NOT NULL DEFAULT 'Android' COMMENT '标准平台',
    `is_active` TINYINT(1) DEFAULT '1' COMMENT '是否启用',
    PRIMARY KEY (`id`),
    -- 唯一索引：确保同一个渠道下的同一个原始标识只对应一个标准APP
    UNIQUE KEY `uk_source_app` (`source_adn_name`, `source_app_identifier`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='应用维度标准化映射表';

INSERT INTO dim_app_mapping (source_adn_name, source_app_identifier, target_app_id, target_app_name, platform) VALUES
('applovin_custom', 'bt-android', 1, 'bt-android', 'android'),
('applovin_custom', 'ut-android', 2, 'ut-android', 'android'),
('applovin_exchange', 'bt-android', 1, 'bt-android', 'android'),
('applovin_exchange', 'ut-android', 2, 'ut-android', 'android'),
('applovin_network', 'bt-android', 1, 'bt-android', 'android'),
('applovin_network', 'ut-android', 2, 'ut-android', 'android'),
('bidmachine_via_max', 'bt-android', 1, 'bt-android', 'android'),
('bidmachine_via_max', 'ut-android', 2, 'ut-android', 'android'),
('chartboost_via_max', 'bt-android', 1, 'bt-android', 'android'),
('chartboost_via_max', 'ut-android', 2, 'ut-android', 'android'),
('fyber_via_max', 'bt-android', 1, 'bt-android', 'android'),
('fyber_via_max', 'ut-android', 2, 'ut-android', 'android'),
('imobi_via_max', 'bt-android', 1, 'bt-android', 'android'),
('imobi_via_max', 'ut-android', 2, 'ut-android', 'android'),
('ironsource_via_max', 'bt-android', 1, 'bt-android', 'android'),
('ironsource_via_max', 'ut-android', 2, 'ut-android', 'android'),
('mintegral_via_max', 'bt-android', 1, 'bt-android', 'android'),
('mintegral_via_max', 'ut-android', 2, 'ut-android', 'android'),
('moloco_via_max', 'bt-android', 1, 'bt-android', 'android'),
('moloco_via_max', 'ut-android', 2, 'ut-android', 'android'),
('tiktok_via_max', 'bt-android', 1, 'bt-android', 'android'),
('tiktok_via_max', 'ut-android', 2, 'ut-android', 'android'),
('unity_via_max', 'bt-android', 1, 'bt-android', 'android'),
('unity_via_max', 'ut-android', 2, 'ut-android', 'android'),
('verve_via_max', 'bt-android', 1, 'bt-android', 'android'),
('verve_via_max', 'ut-android', 2, 'ut-android', 'android'),
('vungle_via_max', 'bt-android', 1, 'bt-android', 'android'),
('vungle_via_max', 'ut-android', 2, 'ut-android', 'android'),
('bidmatic', 'rainberrytv.com', 3, 'rainberrytv.com', 'pc'),
('BIGO_BIDDING', 'bt-android', 1, 'bt-android', 'android'),
('BIGO_BIDDING', 'ut-android', 2, 'ut-android', 'android'),
('cpmstar', 'rainberrytv.com', 3, 'rainberrytv.com', 'pc'),
('didna', 'rainberrytv.com', 3, 'rainberrytv.com', 'pc'),
('IRONSOURCE_NETWORK', 'bt-android', 1, 'bt-android', 'android'),
('IRONSOURCE_NETWORK', 'ut-android', 2, 'ut-android', 'android'),
('seedtag', 'rainberrytv.com', 3, 'rainberrytv.com', 'pc'),
('smartAdServer', 'rainberrytv.com', 3, 'rainberrytv.com', 'pc'),
('xaprio', 'rainberrytv.com', 3, 'rainberrytv.com', 'pc');