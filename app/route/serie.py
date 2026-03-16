from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.model.serie import SerieModel
from app.schema.serie import SerieSchema
 
serie = APIRouter()
 
@serie.post("/")
async def criar_serie(dados: SerieSchema, db: Session = Depends(get_db)):
    nova_serie = SerieModel(**dados.model_dump())
    db.add(nova_serie)
    db.commit()
    db.refresh(nova_serie)
    return nova_serie
 
@serie.get("/")
async def listar_serie(db: Session = Depends(get_db)):
    return db.query(SerieModel).all()
 
@serie.delete("/serie/{id}/delete")
async def deletar_serie(id: int, db: Session = Depends(get_db)):
    serie= db.query(SerieModel).filter(SerieModel.id == id).first()
   
    if not serie:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail = f"a serie com id {id} nao foi encontrada.")
   
    db.delete(serie)
    db.commit()
    
    return{"serie deletada com sucesso"}
 

@serie.put("/{id}")
async def atualizar_serie(id: int, dados: SerieSchema = Depends(), db: Session = Depends(get_db)):
    serie_encontrada = db.query(SerieModel).filter(SerieModel.id == id).first()

    if not serie_encontrada:                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"serie com {id} nao encontrada",
        )       
    # Atualiza automaticamente só o que você preencheu
    dados_atualizados = dados.model_dump(exclude_unset=True)

    for chave, valor in dados_atualizados.items():
        setattr(serie_encontrada, chave, valor)

    db.commit()
    db.refresh(serie_encontrada)
    return serie_encontrada