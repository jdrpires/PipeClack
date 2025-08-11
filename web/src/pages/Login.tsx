import React from 'react'
import { useForm } from 'react-hook-form'
import { useAuth } from '../stores/auth'
import { useNavigate } from 'react-router-dom'

export default function Login(){
  const { register, handleSubmit } = useForm()
  const login = useAuth(s=>s.login)
  const navigate = useNavigate()
  const onSubmit = async (data:any)=>{ await login(data.email, data.password); navigate('/') }
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="p-4 flex flex-col gap-2">
      <input {...register('email')} placeholder="email" className="border p-1" />
      <input {...register('password')} type="password" placeholder="password" className="border p-1" />
      <button type="submit" className="bg-blue-500 text-white p-1">Login</button>
    </form>
  )
}
