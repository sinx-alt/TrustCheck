import { ArrowUp } from 'lucide-react'
import { FormEvent, useState } from 'react'

interface InputBarProps { disabled: boolean; onSubmit: (message: string) => void }

export const InputBar = ({ disabled, onSubmit }: InputBarProps) => {
  const [message, setMessage] = useState('')
  const submit = (event: FormEvent) => { event.preventDefault(); const value = message.trim(); if (!value || disabled) return; onSubmit(value); setMessage('') }
  return <form className="input-wrap" onSubmit={submit}><input value={message} onChange={(event) => setMessage(event.target.value)} placeholder="Paste a message or URL..." aria-label="Message or URL" disabled={disabled} /><button className="send-button" type="submit" disabled={disabled || !message.trim()} aria-label="Analyze message"><ArrowUp size={20} /></button></form>
}
