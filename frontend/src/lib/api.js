import { supabase } from './supabase'

export async function apiFetch(path, options = {}) {
  const { data: { session } } = await supabase.auth.getSession()
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  if (session?.access_token) {
    headers['Authorization'] = `Bearer ${session.access_token}`
  }

  const response = await fetch(path, {
    ...options,
    headers,
  })

  if (!response.ok) {
    let errorMsg = response.statusText
    try {
      const errorData = await response.json()
      errorMsg = errorData.detail || errorData.message || errorMsg
    } catch (e) {
      // Keep default statusText
    }
    throw new Error(`Error ${response.status}: ${errorMsg}`)
  }

  return response.json()
}
