CREATE DATABASE IF NOT EXISTS bt_adn_reports;
use bt_adn_reports;

CREATE TABLE IF NOT EXISTS bidmatic_report (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT 'report date',
    `country` VARCHAR(20) NOT NULL DEFAULT '' COMMENT 'country code',
    `ad_type` TINYINT(1) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'ad type(0: video, 1: display)',
    `domain` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'website',
    `os` VARCHAR(32) NOT NULL DEFAULT '' COMMENT 'operating system',
    `ad_requests` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'ad requests',
    `ad_opportunities` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'ad responses',
    `impressions_good` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'impressions',
    `revenue` DECIMAL(20, 6) NOT NULL DEFAULT '0' COMMENT 'revenue',
    PRIMARY KEY (`id`),
    INDEX day_country_ad_type_idx(`day`, `country`, `ad_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='bidmatic report';

CREATE TABLE IF NOT EXISTS didna_report (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT 'report date',
    `property` VARCHAR(20) NOT NULL DEFAULT '' COMMENT 'website',
    `ad_type` TINYINT(1) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'ad type(0: video, 1: display)',
    `requests` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'requests',
    `impressions` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'impressions',
    `revenue` DECIMAL(20, 6) NOT NULL DEFAULT '0' COMMENT 'revenue',
    PRIMARY KEY (`id`),
    INDEX day_ad_type_idx(`day`, `ad_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='didna report';

CREATE TABLE IF NOT EXISTS cpmstar_report (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT 'report date',
    `country` VARCHAR(20) NOT NULL DEFAULT '' COMMENT 'country code',
    `ad_type` TINYINT(1) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'ad type(0: video, 1: display)',
    `pool_id` INT(11) NOT NULL DEFAULT '0' COMMENT 'unit id',
    `pool_name` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'unit name',
    `clicks` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'clicks',
    `impressions` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'impressions',
    `revenue` DECIMAL(20, 6) NOT NULL DEFAULT '0' COMMENT 'revenue',
    `actions` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'actions',
    PRIMARY KEY (`id`),
    INDEX day_country_idx(`day`, `country`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='cpmstar report';

CREATE TABLE IF NOT EXISTS smartAdServer_report (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT 'report date',
    `country` VARCHAR(20) NOT NULL DEFAULT '' COMMENT 'country code',
    `clicks` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'clicks',
    `impressions` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'impressions',
    `auctions` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'auctions',
    `revenue` DECIMAL(20, 6) NOT NULL DEFAULT '0' COMMENT 'revenue',
    PRIMARY KEY (`id`),
    INDEX day_country_idx(`day`, `country`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='smartAdServer report';

CREATE TABLE IF NOT EXISTS freewheel_report (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT 'report date',
    `country` VARCHAR(20) NOT NULL DEFAULT '' COMMENT 'country code',
    `publisher_id` INT(11) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'publisher website id',
    `zone_id` INT(11) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'unit id',
    `requests` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'requests',
    `clicks` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'clicks',
    `impressions` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'impressions',
    `revenue` DECIMAL(20, 6) NOT NULL DEFAULT '0' COMMENT 'revenue',
    PRIMARY KEY (`id`),
    INDEX day_country_idx(`day`, `country`, `publisher_id`, `zone_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='freewheel report';

CREATE TABLE applovin_max_report (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT 'report date',
    `ad_format` VARCHAR(64)  NOT NULL DEFAULT '' COMMENT 'ad format',
    `application` VARCHAR(64)  NOT NULL DEFAULT '' COMMENT 'app name',
    `attempts`  BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'request attempts',
    `country` VARCHAR(20) NOT NULL DEFAULT '' COMMENT 'country code',
    `device_type` tinyint(1) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'device type(0: unknown, 1: phone, 2: tablet)',
    `estimated_revenue` DECIMAL(20, 6) NOT NULL DEFAULT '0' COMMENT 'revenue',
    `impressions` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'impressions',
    `max_ad_unit_name` VARCHAR(128) NOT NULL DEFAULT '' COMMENT 'applovin max ad unit name',
    `max_ad_unit_id` VARCHAR(128) NOT NULL DEFAULT '' COMMENT 'applovin max ad unit id',
    `platform` tinyint(1) UNSIGNED NOT NULL DEFAULT '1' COMMENT 'platform (0:pc, 1:android, 2:ios)',
    `responses` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'ad responses',
    `network` VARCHAR(64)  NOT NULL DEFAULT '' COMMENT 'network name',
    PRIMARY KEY (`id`),
    INDEX day_country_platform_idx(`day`, `country`, `platform`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='applovin max report';

CREATE TABLE IF NOT EXISTS xaprio_report (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT 'report date',
    `zone_id` INT(11) NOT NULL DEFAULT '0' COMMENT 'unit id',
    `zone_name` VARCHAR(128) NOT NULL DEFAULT '' COMMENT 'unit name',
    `ad_type` TINYINT(1) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'ad type(0: video, 1: display)',
    `requests` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'requests',
    `coverage` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'responses',
    `clicks` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'clicks',
    `impressions` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'impressions',
    `revenue` DECIMAL(20, 6) NOT NULL DEFAULT '0' COMMENT 'revenue',
    PRIMARY KEY (`id`),
    INDEX day_zone_id_idx(`day`, `zone_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='xaprio report';

CREATE TABLE IF NOT EXISTS adn_aggregation_revenue_report (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `adn_network` VARCHAR(128) NOT NULL DEFAULT '' COMMENT 'ADN网络名称',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT '日期',
    `country` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '国家代码(2位大写)',
    `platform` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '平台(IOS/Android/PC)',
    `app_id` tinyint(1) UNSIGNED NOT NULL DEFAULT '0' COMMENT '应用ID(0: unknown, 1: bt-android, 2: ut-android, 3: rainberrytv.com, 4: bittorrent.com, 5: utorrent.com)',
    `app_name` VARCHAR(128) NOT NULL DEFAULT '' COMMENT '应用名称(bt-android/ut-android/rainberrytv.com/bittorrent.com/utorrent.com)',
    `unit_id` VARCHAR(128) NOT NULL DEFAULT '' COMMENT '广告单元ID',
    `unit_name` VARCHAR(128) NOT NULL DEFAULT '' COMMENT '广告单元名称',
    `device_type` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '设备类型',
    `os_type` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '系统类型',
    `ad_type` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '广告类型(Video/Display)',
    `ad_size` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '广告尺寸(宽x高)',
    `revenue` DECIMAL(20, 6) NOT NULL DEFAULT '0' COMMENT '收入',
    `requests` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT '请求数',
    `responses` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT '响应数',
    `clicks` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT '点击数',
    `impressions` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT '展示数',
    PRIMARY KEY (`id`),
    INDEX adn_idx(adn_network, day, country, platform, app_id, unit_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='ADN聚合收入报告表';

CREATE TABLE IF NOT EXISTS yandex_report (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT 'report date',
    `unit_name` VARCHAR(128) NOT NULL DEFAULT '0' COMMENT 'unit name',
    `country` VARCHAR(20) NOT NULL DEFAULT '' COMMENT 'country code',
    `requests` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'requests',
    `clicks` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'clicks',
    `impressions` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'impressions',
    `revenue` DECIMAL(20, 6) NOT NULL DEFAULT '0' COMMENT 'revenue',
    PRIMARY KEY (`id`),
    INDEX day_country_unit_idx(`day`, `country`, `unit_name`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='yandex report';

CREATE TABLE IF NOT EXISTS seedtag_report (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT 'report date',
    `publisher_name` VARCHAR(128) NOT NULL DEFAULT '0' COMMENT 'app name',
    `ad_type` VARCHAR(20) NOT NULL DEFAULT '' COMMENT 'ad type',
    `clicks` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'clicks',
    `impressions` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'impressions',
    `revenue` DECIMAL(20, 6) NOT NULL DEFAULT '0' COMMENT 'revenue',
    PRIMARY KEY (`id`),
    INDEX day_publisher_adtype_idx(`day`, `publisher_name`, `ad_type`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='seedtag report';

CREATE TABLE IF NOT EXISTS firebase (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT 'report date',
    `events` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'number of events',
    `users` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'number of users',
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='firebase';


CREATE TABLE IF NOT EXISTS google_play_all_users_install (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT 'report date',
    `app` VARCHAR(20) NOT NULL DEFAULT '' COMMENT 'app',
    `users` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'number of users',
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='google play all_users_install';


CREATE TABLE IF NOT EXISTS google_play_new_users_install (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT 'report date',
    `app` VARCHAR(20) NOT NULL DEFAULT '' COMMENT 'app',
    `users` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'number of users',
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='google play new_users_install';

CREATE TABLE IF NOT EXISTS google_play_all_countries_install (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT 'report date',
    `app` VARCHAR(20) NOT NULL DEFAULT '' COMMENT 'app',
    `users` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'number of users',
    `country` VARCHAR(20) NOT NULL DEFAULT '' COMMENT 'country code',
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='google play all_countries_install';

CREATE TABLE IF NOT EXISTS paypro_report (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT 'report date',
    `order_id` INT(11) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'order id',
    `order_status_id` INT(11) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'order status id',
    `order_status_name` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'order status name',
    `payment_method_id` INT(11) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'payment method id',
    `payment_method_name` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'payment method name',
    `created_at` DATETIME NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT 'order created time',
    `billing_currency_code` VARCHAR(10) NOT NULL DEFAULT '' COMMENT 'billing currency code',
    `balance_currency_code` VARCHAR(10) NOT NULL DEFAULT '' COMMENT 'balance currency code',
    `country` VARCHAR(20) NOT NULL DEFAULT '' COMMENT 'country code',
    `billing_price` DECIMAL(20, 6) NOT NULL DEFAULT '0' COMMENT 'billing price',
    `product_id` INT(11) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'product id',
    `order_item_name` VARCHAR(256) NOT NULL DEFAULT '' COMMENT 'order item name',
    `billing_price_tax_refund` DECIMAL(20, 6) NOT NULL DEFAULT '0' COMMENT 'billing price tax refund',
    `billing_price_refund` DECIMAL(20, 6) NOT NULL DEFAULT '0' COMMENT 'billing price refund',
    `balance_vendor_amount` DECIMAL(20, 6) NOT NULL DEFAULT '0' COMMENT 'balance vendor amount',
    `balance_pay_pro_amount` DECIMAL(20, 6) NOT NULL DEFAULT '0' COMMENT 'balance PayPro amount',
    PRIMARY KEY (`id`),
    INDEX day_order_idx(`day`, `order_id`),
    INDEX day_country_idx(`day`, `country`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='PayPro payment report';

CREATE TABLE IF NOT EXISTS add_torrent (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT 'report date',
    `events` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'number of events',
    `users` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'number of users',
    PRIMARY KEY (`id`),
    INDEX day_idx(`day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='add torrent events report';

CREATE TABLE IF NOT EXISTS bittorrent_installer_report (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `day` DATE NOT NULL DEFAULT '1970-01-01' COMMENT 'report date',
    `installer_name` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'installer name',
    `geo` VARCHAR(20) NOT NULL DEFAULT '' COMMENT 'country/region code',
    `installation_started` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'installation started count',
    `installer_success_rate` DECIMAL(10, 4) DEFAULT NULL COMMENT 'installer success rate (%)',
    `installer_error_rate` DECIMAL(10, 4) DEFAULT NULL COMMENT 'installer error rate (%)',
    `installer_quit_rate` DECIMAL(10, 4) DEFAULT NULL COMMENT 'installer quit rate (%)',
    `revenue_per_started` DECIMAL(20, 6) DEFAULT NULL COMMENT 'revenue per started installation',
    `offers_made` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'offers made count',
    `offers_installs` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'offers installs count',
    `revenue` DECIMAL(20, 6) DEFAULT NULL COMMENT 'total revenue',
    `installation_completed` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'installation completed count',
    `revenue_per_completed` DECIMAL(20, 6) DEFAULT NULL COMMENT 'revenue per completed installation',
    PRIMARY KEY (`id`),
    INDEX day_installer_geo_idx(`day`, `installer_name`, `geo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='bittorrent installer report';
