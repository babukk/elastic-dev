
CREATE TABLE `group_company_rel` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `company_id` varchar(32) DEFAULT NULL,
    `group_id` varchar(32) DEFAULT NULL,
      PRIMARY KEY (`id`),
      KEY `cmp_idx` (`company_id`),
      KEY `group_idx` (`group_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

CREATE TABLE `team_company_rel` (
     `id` int(11) NOT NULL AUTO_INCREMENT,
     `team_id` varchar(32) DEFAULT NULL,
     `company_id` varchar(32) DEFAULT NULL,
     PRIMARY KEY (`id`),
     KEY `company_idx` (`company_id`),
     KEY `team_idx` (`team_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

CREATE TABLE `user_team_rel` (
     `id` int(11) NOT NULL AUTO_INCREMENT,
     `user_id` varchar(32) DEFAULT NULL,
     `team_id` varchar(32) DEFAULT NULL,
     PRIMARY KEY (`id`),
     KEY `first_idx` (`team_id`),
     KEY `second_idx` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

