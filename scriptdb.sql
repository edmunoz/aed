-- -----------------------------------------------------
-- Table `post`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `post` (
  `id_post` BIGINT NOT NULL AUTO_INCREMENT,
  `created_time` VARCHAR(100) NULL,
  `icon` VARCHAR(100) NULL,
  `id` VARCHAR(100) NULL,
  `link` VARCHAR(1000) NULL,
  `message` VARCHAR(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `multi_share_optimized` TINYINT(1) NULL,
  `name` VARCHAR(1000) NULL,
  `picture` VARCHAR(1000) NULL,
  PRIMARY KEY (`id_post`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `post_like`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `post_like` (
  `id_post_like` BIGINT NOT NULL AUTO_INCREMENT,
  `id_post` BIGINT NOT NULL,
  `id` VARCHAR(100) NULL,
  `name` VARCHAR(1000) NULL,
  PRIMARY KEY (`id_post_like`),
  INDEX `fk_post_like_post1_idx` (`id_post` ASC),
  CONSTRAINT `fk_post_like_post1`
    FOREIGN KEY (`id_post`)
    REFERENCES `post` (`id_post`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `post_from`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `post_from` (
  `id_post_from` BIGINT NOT NULL AUTO_INCREMENT,
  `id_post` BIGINT NOT NULL,
  `category` VARCHAR(500) NULL,
  `id` VARCHAR(100) NULL,
  `name` VARCHAR(1000) NULL,
  PRIMARY KEY (`id_post_from`),
  INDEX `fk_post_from_post_idx` (`id_post` ASC),
  CONSTRAINT `fk_post_from_post`
    FOREIGN KEY (`id_post`)
    REFERENCES `post` (`id_post`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `comment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `comment` (
  `id_comment` BIGINT NOT NULL AUTO_INCREMENT,
  `id_post` BIGINT NOT NULL,
  `can_remove` TINYINT(1) NULL,
  `created_time` VARCHAR(100) NULL,
  `id` VARCHAR(100) NULL,
  `like_count` BIGINT NULL,
  `message` VARCHAR(2000) NULL,
  `user_likes` TINYINT(1) NULL,
  PRIMARY KEY (`id_comment`),
  INDEX `fk_comment_post1_idx` (`id_post` ASC),
  CONSTRAINT `fk_comment_post1`
    FOREIGN KEY (`id_post`)
    REFERENCES `post` (`id_post`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `comment_from`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `comment_from` (
  `id_comment_from` BIGINT NOT NULL AUTO_INCREMENT,
  `id_comment` BIGINT NOT NULL,
  `id` VARCHAR(100) NULL,
  `name` VARCHAR(1000) NULL,
  PRIMARY KEY (`id_comment_from`),
  INDEX `fk_comment_from_comment1_idx` (`id_comment` ASC),
  CONSTRAINT `fk_comment_from_comment1`
    FOREIGN KEY (`id_comment`)
    REFERENCES `comment` (`id_comment`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;