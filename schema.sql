-- On Sight AI - script corrigido
-- Correções em relação ao script original do Workbench:
--   1. Nomes de FK únicos no schema (antes id_campeonato e id_vencedor se repetiam)
--   2. Chave primária composta em participantes (id_campeonato, id_time)
--   3. Removida a palavra VISIBLE dos índices (é o padrão do MySQL 8 e assim o script
--      também roda no MariaDB, que não aceita essa palavra)

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8mb3;
USE `mydb`;

-- -----------------------------------------------------
-- Table `mydb`.`campeonato`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`campeonato` (
  `id` INT NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  `localizacao` VARCHAR(250) NOT NULL,
  `premiacao_total` INT NOT NULL,
  `fase` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;

-- -----------------------------------------------------
-- Table `mydb`.`time`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`time` (
  `id` INT NOT NULL,
  `ranking` INT NULL DEFAULT NULL,
  `nome` VARCHAR(45) NOT NULL,
  `titulos` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;

-- -----------------------------------------------------
-- Table `mydb`.`jogador`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`jogador` (
  `id` INT NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  `idade` INT NOT NULL,
  `nick` VARCHAR(45) NOT NULL,
  `ganhos` INT NOT NULL,
  `rating` FLOAT NOT NULL,
  `time_id` INT NULL DEFAULT NULL,
  `premiacoes` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_jogador_time_idx` (`time_id` ASC),
  CONSTRAINT `fk_jogador_time`
    FOREIGN KEY (`time_id`)
    REFERENCES `mydb`.`time` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;

-- -----------------------------------------------------
-- Table `mydb`.`config`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`config` (
  `id_jogador` INT NOT NULL,
  `dpi` INT NULL DEFAULT NULL,
  `sensibilidade` FLOAT NULL DEFAULT NULL,
  `resolucao` VARCHAR(9) NULL DEFAULT NULL,
  `cod_mira` VARCHAR(34) NULL DEFAULT NULL,
  PRIMARY KEY (`id_jogador`),
  CONSTRAINT `fk_config_jogador`
    FOREIGN KEY (`id_jogador`)
    REFERENCES `mydb`.`jogador` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;

-- -----------------------------------------------------
-- Table `mydb`.`participantes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`participantes` (
  `id_campeonato` INT NOT NULL,
  `id_time` INT NOT NULL,
  `classificacao` INT NOT NULL,
  `premiacao` INT NOT NULL,
  PRIMARY KEY (`id_campeonato`, `id_time`),
  INDEX `fk_participantes_time_idx` (`id_time` ASC),
  CONSTRAINT `fk_participantes_campeonato`
    FOREIGN KEY (`id_campeonato`)
    REFERENCES `mydb`.`campeonato` (`id`),
  CONSTRAINT `fk_participantes_time`
    FOREIGN KEY (`id_time`)
    REFERENCES `mydb`.`time` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;

-- -----------------------------------------------------
-- Table `mydb`.`serie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`serie` (
  `id` INT NOT NULL,
  `id_campeonato` INT NULL,
  `id_time1` INT NOT NULL,
  `id_time2` INT NOT NULL,
  `id_vencedor` INT NULL,
  `status` VARCHAR(20) NOT NULL,
  `formato` CHAR(3) NULL,
  `fase` VARCHAR(20) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_serie_campeonato_idx` (`id_campeonato` ASC),
  INDEX `fk_serie_time1_idx` (`id_time1` ASC),
  INDEX `fk_serie_time2_idx` (`id_time2` ASC),
  INDEX `fk_serie_vencedor_idx` (`id_vencedor` ASC),
  CONSTRAINT `fk_serie_campeonato`
    FOREIGN KEY (`id_campeonato`)
    REFERENCES `mydb`.`campeonato` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_serie_time1`
    FOREIGN KEY (`id_time1`)
    REFERENCES `mydb`.`time` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_serie_time2`
    FOREIGN KEY (`id_time2`)
    REFERENCES `mydb`.`time` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_serie_vencedor`
    FOREIGN KEY (`id_vencedor`)
    REFERENCES `mydb`.`time` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;

-- -----------------------------------------------------
-- Table `mydb`.`partida`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`partida` (
  `id` INT NOT NULL,
  `id_serie` INT NOT NULL,
  `id_vencedor` INT NULL,
  `id_perdedor` INT NULL,
  `mapa` VARCHAR(45) NULL,
  `placar` CHAR(5) NULL,
  `ordem` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_partida_serie_idx` (`id_serie` ASC),
  INDEX `fk_partida_vencedor_idx` (`id_vencedor` ASC),
  INDEX `fk_partida_perdedor_idx` (`id_perdedor` ASC),
  CONSTRAINT `fk_partida_serie`
    FOREIGN KEY (`id_serie`)
    REFERENCES `mydb`.`serie` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_partida_vencedor`
    FOREIGN KEY (`id_vencedor`)
    REFERENCES `mydb`.`time` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_partida_perdedor`
    FOREIGN KEY (`id_perdedor`)
    REFERENCES `mydb`.`time` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
