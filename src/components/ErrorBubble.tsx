import { RotateCcw } from 'lucide-react'

interface ErrorBubbleProps { onRetry: () => void }
export const ErrorBubble = ({ onRetry }: ErrorBubbleProps) => <div className="error-bubble"><div><strong>We couldn't complete that check.</strong><span>Please try again.</span></div><button onClick={onRetry}><RotateCcw size={15} /> Retry</button></div>
