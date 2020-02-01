CREATE TABLE `search` (
	`id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`site_address` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`site_name` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`site_title` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`site_main_category` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`site_keywords` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`site_description` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`site_favicon_uri` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;



CREATE TABLE `add_a_link` (
	`id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`url` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`title` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`keywords` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

