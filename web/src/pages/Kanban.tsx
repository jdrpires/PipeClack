import React, { useState, useEffect } from 'react'
import { useDrop, useDrag, DndProvider, useDragDropManager } from 'react-dnd'
import { HTML5Backend } from 'react-dnd-html5-backend'
import api from '../services/api'

interface Card { id:number; titulo:string }
interface Column { id:number; nome:string; cards:Card[] }
const initial: Column[] = [
  {id:1, nome:'Todo', cards:[{id:1,titulo:'Task'}]},
  {id:2, nome:'Doing', cards:[]}
]

export default function Kanban({type, backend, managerCallback}:{type:string; backend?: any; managerCallback?:(mgr:any)=>void}){
  const Backend = backend || HTML5Backend
  return (
    <DndProvider backend={Backend}>
      <Board managerCallback={managerCallback} />
    </DndProvider>
  )
}

function Board({managerCallback}:{managerCallback?:(mgr:any)=>void}){
  const manager = useDragDropManager()
  useEffect(()=>{ managerCallback?.(manager) },[manager])
  const [cols,setCols] = useState<Column[]>(initial)
  const moveCard = async (card:Card, toColumn:Column)=>{
    setCols(cols.map(c=>{
      if(c.id===toColumn.id) return {...c, cards:[...c.cards, card]}
      return {...c, cards:c.cards.filter(cc=>cc.id!==card.id)}
    }))
    await api.post(`/cards/${card.id}/move`, {to_column_id: toColumn.id, position:1000})
  }
  useEffect(()=>{
    (window as any).testMove = (cardId:number, toCol:number)=>{
      const card = cols.flatMap(c=>c.cards).find(c=>c.id===cardId)
      const column = cols.find(c=>c.id===toCol)
      if(card && column) moveCard(card, column)
    }
  },[cols])
  return (
    <div className="flex gap-4">
      {cols.map(col=> <ColumnComp key={col.id} column={col} moveCard={moveCard} />)}
    </div>
  )
}

function ColumnComp({column, moveCard}:{column:Column; moveCard:(card:Card, toColumn:Column)=>void}){
  const [, drop] = useDrop({ accept:'CARD', drop:(item:Card)=>moveCard(item,column) })
  return (
    <div ref={drop} className="w-48 min-h-[200px] border p-2" data-testid={`col-${column.id}`}>
      <h3>{column.nome}</h3>
      {column.cards.map(c=> <CardComp key={c.id} card={c} />)}
    </div>
  )
}

function CardComp({card}:{card:Card}){
  const [, drag] = useDrag({ type:'CARD', item:card })
  return <div ref={drag} className="p-2 bg-white border mt-2" data-testid={`card-${card.id}`}>{card.titulo}</div>
}
