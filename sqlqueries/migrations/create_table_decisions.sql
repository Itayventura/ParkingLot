CREATE TABLE `decisions` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`can_enter` TINYINT(1) NULL DEFAULT NULL,
	`file_source` VARCHAR(255) NOT NULL,
	`is_url` ENUM('Y','N') NOT NULL DEFAULT 'N',
	`created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`plate_id` INT(11) NOT NULL,
	PRIMARY KEY (`id`),
	INDEX `plate_id` (`plate_id`),
	INDEX `timestamp` (`created_at`),
	CONSTRAINT `plate_id` FOREIGN KEY (`plate_id`) REFERENCES `plates` (`id`)
)
COLLATE='latin1_swedish_ci'
ENGINE=InnoDB
AUTO_INCREMENT=93
;
