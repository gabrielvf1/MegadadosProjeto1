DROP SCHEMA IF EXISTS `mydb` ;

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Usuarios`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Usuarios` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Usuarios` (
  `Login` VARCHAR(45) NOT NULL,
  `Nome` VARCHAR(45) NOT NULL,
  `Email` VARCHAR(45) NOT NULL,
  `Cidade` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Login`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Desc_passaros`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Desc_passaros` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Desc_passaros` (
  `Nome` VARCHAR(45) NOT NULL,
  `Cor` VARCHAR(45) NULL,
  `Comida` VARCHAR(45) NULL,
  `Onde_vive` VARCHAR(45) NULL,
  `Tamanho` VARCHAR(45) NULL,
  PRIMARY KEY (`Nome`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Pref_pass`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Pref_pass` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Pref_pass` (
  `loginUsuario` VARCHAR(45) NULL,
  `nomePassaro` VARCHAR(45) NULL,
  INDEX `idUsuario_idx` (`loginUsuario` ASC) VISIBLE,
  INDEX `idPassaro_idx` (`nomePassaro` ASC) VISIBLE,
  CONSTRAINT `idUsuarioPrefPass`
    FOREIGN KEY (`loginUsuario`)
    REFERENCES `mydb`.`Usuarios` (`Login`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `idPassaroPrefPass`
    FOREIGN KEY (`nomePassaro`)
    REFERENCES `mydb`.`Desc_passaros` (`Nome`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Tipo_acao`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Tipo_acao` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Tipo_acao` (
  `idTipoAcao` INT NOT NULL AUTO_INCREMENT,
  `Nome` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idTipoAcao`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Acoes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Acoes` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Acoes` (
  `loginUsuario` VARCHAR(45) NOT NULL,
  `idAcao` INT NOT NULL AUTO_INCREMENT,
  `idTipoAcao` INT NOT NULL,
  `Celular` INT NOT NULL,
  `Browser` VARCHAR(45) NULL,
  `Aparelho` VARCHAR(45) NULL,
  `IP` VARCHAR(45) NOT NULL,
  INDEX `idUsuario_idx` (`loginUsuario` ASC) VISIBLE,
  PRIMARY KEY (`idAcao`),
  INDEX `idTipoAcao_idx` (`idTipoAcao` ASC) VISIBLE,
  CONSTRAINT `idUsuarioAcoes`
    FOREIGN KEY (`loginUsuario`)
    REFERENCES `mydb`.`Usuarios` (`Login`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `idTipoAcao`
    FOREIGN KEY (`idTipoAcao`)
    REFERENCES `mydb`.`Tipo_acao` (`idTipoAcao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Posts`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Posts` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Posts` (
  `idPost` INT NOT NULL AUTO_INCREMENT,
  `Texto` VARCHAR(500) NULL,
  `Titulo` VARCHAR(45) NOT NULL,
  `loginUsuario` VARCHAR(45) NOT NULL,
  `URL_IMG` VARCHAR(45) NULL,
  `Estado` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idPost`),
  INDEX `idUsuario_idx` (`loginUsuario` ASC) VISIBLE,
  CONSTRAINT `idUsuarioPost`
    FOREIGN KEY (`loginUsuario`)
    REFERENCES `mydb`.`Usuarios` (`Login`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`User_ref`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`User_ref` ;

CREATE TABLE IF NOT EXISTS `mydb`.`User_ref` (
  `idPost` INT NOT NULL,
  `loginUsuario` VARCHAR(45) NOT NULL,
  INDEX `idPost_idx` (`idPost` ASC) VISIBLE,
  INDEX `idUsuario_idx` (`loginUsuario` ASC) VISIBLE,
  CONSTRAINT `idPostUserRef`
    FOREIGN KEY (`idPost`)
    REFERENCES `mydb`.`Posts` (`idPost`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `idUsuario`
    FOREIGN KEY (`loginUsuario`)
    REFERENCES `mydb`.`Usuarios` (`Login`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Pass_ref`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Pass_ref` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Pass_ref` (
  `nomePassaro` VARCHAR(45) NOT NULL,
  `idPost` INT NOT NULL,
  INDEX `idPassaro_idx` (`nomePassaro` ASC) VISIBLE,
  INDEX `idPost_idx` (`idPost` ASC) VISIBLE,
  CONSTRAINT `idPassaroPassRef`
    FOREIGN KEY (`nomePassaro`)
    REFERENCES `mydb`.`Desc_passaros` (`Nome`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `idPostPassRed`
    FOREIGN KEY (`idPost`)
    REFERENCES `mydb`.`Posts` (`idPost`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

DELIMITER $
CREATE TRIGGER delete_usuario BEFORE DELETE ON Usuarios
  FOR EACH ROW
  BEGIN
      UPDATE Posts SET Estado = "Inativo"
      WHERE Posts.loginUsuario = OLD.login;
END $


