from typing import Any, List, Dict
from pydantic import BaseModel, EmailStr, HttpUrl, PrivateAttr
from enum import Enum

class IAzioneEnum(str, Enum):
    ESEGUI = "ESEGUI"
    CARICO = "CARICO"
    
class ISmistamentoEnum(str, Enum):
    CONOSCENZA = "CONOSCENZA"
    COMPETENZA = "COMPETENZA"

    
class IConfig(BaseModel):
    wsUrl: str
    wsUser: str
    wsEnte: str
    wsPassword: str
    FAKE: bool = False
    
class BaseRet(BaseModel):
    lngErrNumber: int = 0
    strErrString: str = ''

class ILoginRet(BaseRet):
    strDST: str | None
    
class IResult(BaseRet):
    lngNumPG: int = 0
    lngAnnoPG: int = 0
    strDataPG: str = ''
    lngDocID: int = 0

    
class IPersona(BaseModel):
    IndirizzoTelematico: str
    Denominazione: str | None
    Nome: str
    Cognome: str
    TitoloDitta: str | None
    CodiceFiscaleDitta: str | None
    IndirizzoTelematicoDitta: str | None
    TipoMittente: str | None
    CodiceFiscale: str
    Titolo: str

class IDocumento(BaseModel):
    id: int | None
    descrizione: str
    tipo: str
    nome: str
    content: Any
    size: int
    mimetype: str
    ext: str


class IUser(BaseModel):
    username: str
    password: str

class IAmministrazione(BaseModel):
    Denominazione: str
    CodiceAOO: str
    CodiceEnte: str
    IndirizzoTelematico: EmailStr

class IFascicolo(BaseModel):
    numero: str
    anno:str
    
class IParametro(BaseModel):
    nome: str
    valore: str

class IProtocollo(BaseModel):
    Amministrazione: IAmministrazione
    Mittente: List[IPersona]
    Flusso: str = 'E'
    Oggetto: str
    Titolario: str
    UO: str  
    Fascicolo: IFascicolo
    Principale: IDocumento
    Allegati: List[IDocumento]
    NumeroRegistrazione: str = '0'
    DataRegistrazione: str = '0'
    Applicativo: str = 'AGSPR'
    Parametri: List[IParametro]


class IMessageData(BaseModel):
    pass


