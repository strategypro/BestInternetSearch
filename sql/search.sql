CREATE TABLE `search` (
	`id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`site_address` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`site_name` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`site_title` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`site_main_category` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`site_description` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`site_favicon_uri` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`stock_trading_symbol` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`stock_trading_exchange` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`wikipedia_page` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `site_address_indx` (`site_address`(255)) USING BTREE
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



/* POSTGRESQL */
CREATE TABLE data (
key bigserial primary key,
item text,
title text
);
CREATE INDEX data_indx ON data (title);


/* MYSQL */
CREATE TABLE `data` (
	`key` INT(11) NOT NULL AUTO_INCREMENT,
	`item` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	`title` TEXT(65535) NOT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`key`) USING BTREE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;
CREATE INDEX title_idx ON data(title(255));

