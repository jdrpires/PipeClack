import { Navigate } from 'react-router-dom'
import { useAuth } from '../stores/auth'
import React from 'react'

interface Props { roles?: string[]; element: React.ReactElement }
export default function ProtectedRoute({roles, element}: Props){
  const {user} = useAuth()
  if(!user) return <Navigate to="/login" replace />
  if(roles && !roles.some(r=>user.roles.includes(r))) return <Navigate to="/403" replace />
  return element
}
