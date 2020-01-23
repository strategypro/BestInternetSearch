CREATE TABLE `search` (
	`id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`site_address` TEXT NULL COLLATE 'utf8_general_ci',
	`site_name` TEXT NULL COLLATE 'utf8_general_ci',
	`site_title` TEXT NULL COLLATE 'utf8_general_ci',
	`site_main_category` TEXT NULL COLLATE 'utf8_general_ci',
	`site_keywords` TEXT NULL COLLATE 'utf8_general_ci',
	`site_description` TEXT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=8
;

