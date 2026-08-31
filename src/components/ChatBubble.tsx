interface ChatBubbleProps { message: string }

export const ChatBubble = ({ message }: ChatBubbleProps) => (
  <div className="user-row"><div className="user-bubble">{message}</div></div>
)
