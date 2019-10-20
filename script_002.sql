USE `mydb` ;

-- -----------------------------------------------------
-- Alter `mydb`.`Posts`
-- -----------------------------------------------------
ALTER TABLE `mydb`.`Posts` ADD COLUMN `Data` DATETIME DEFAULT CURRENT_TIMESTAMP;

-- -----------------------------------------------------
-- Create `mydb`.`Curtidas`
-- -----------------------------------------------------

DROP TABLE IF EXISTS `mydb`.`Curtidas` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Curtidas` (
  `idPost` INT NOT NULL,
  `loginUsuario` VARCHAR(45) NOT NULL,
  `Tipo` VARCHAR(45) NOT NULL,
  INDEX `loginUsuarioCurtida_idx` (`loginUsuario` ASC) VISIBLE,
  INDEX `idPostCurtidas_idx` (`idPost` ASC) VISIBLE,
  CONSTRAINT `loginUsuarioCurtida`
    FOREIGN KEY (`loginUsuario`)
    REFERENCES `mydb`.`Usuarios` (`Login`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `idPostCurtidas`
    FOREIGN KEY (`idPost`)
    REFERENCES `mydb`.`Posts` (`idPost`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- FIX `mydb`.`Acoes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Acoes` ;
DROP TABLE IF EXISTS `mydb`.`Tipo_acao` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Tipo_acao` (
  `Nome` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Nome`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- FIX `mydb`.`Acoes`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `mydb`.`Acoes` (
  `loginUsuario` VARCHAR(45) NOT NULL,
  `idAcao` INT NOT NULL AUTO_INCREMENT,
  `Nome_acao` VARCHAR(45) NOT NULL,
  `Browser` VARCHAR(45) NULL,
  `Aparelho` VARCHAR(45) NULL,
  `IP` VARCHAR(45) NOT NULL,
  INDEX `idUsuario_idx` (`loginUsuario` ASC) VISIBLE,
  PRIMARY KEY (`idAcao`),
  CONSTRAINT `idUsuarioAcoes`
    FOREIGN KEY (`loginUsuario`)
    REFERENCES `mydb`.`Usuarios` (`Login`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Nome_acao`
    FOREIGN KEY (`Nome_acao`)
    REFERENCES `mydb`.`Tipo_acao` (`Nome`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;




