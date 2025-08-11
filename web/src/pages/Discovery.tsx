import React, { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import api from '../services/api'

export default function Discovery(){
  const [template,setTemplate] = useState<any>()
  const { register, handleSubmit } = useForm()
  useEffect(()=>{ api.get('/projects/discovery/template').then(r=>setTemplate(r.data)) },[])
  const onSubmit = async (data:any)=>{
    if(!template) return
    await api.post('/projects/1/discovery', {template_id:template.id, respostas_json:data})
  }
  if(!template) return <div>Loading...</div>
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {template.sections.map((sec:any)=>{
        if(sec.type==='textarea' || sec.type==='text') return <div key={sec.key}><label>{sec.label}</label><input className="border" {...register(sec.key)} /></div>
        return null
      })}
      <button type="submit">Salvar</button>
    </form>
  )
}
