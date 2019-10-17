USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Posts`
-- -----------------------------------------------------
ALTER TABLE `mydb`.`Posts` ADD COLUMN `Data` `datetime` DEFAULT(getdate());

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
