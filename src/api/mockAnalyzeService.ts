import type { AnalyzeResponse } from '../types'

const responses: AnalyzeResponse[] = [
  {
    risk_score: 8,
    risk_level: 'LOW',
    signals: ['Known sender pattern', 'No suspicious links found'],
    urls: [],
    brands: [],
    explanation: ['The message contains no obvious pressure tactics or requests for sensitive information.', 'No unusual URL structure was detected.'],
    safe_action: 'It looks reasonable to proceed, but keep your usual account security habits in place.',
  },
  {
    risk_score: 56,
    risk_level: 'SUSPICIOUS',
    signals: ['Urgency language', 'Unfamiliar shortened URL'],
    urls: ['https://bit.ly/account-review'],
    brands: ['Parcel Service'],
    explanation: ['The message asks you to act quickly, which is a common social engineering signal.', 'The shortened link hides its final destination.'],
    safe_action: 'Do not tap the link. Visit the company website using a bookmark or a trusted search result instead.',
  },
  {
    risk_score: 91,
    risk_level: 'HIGH',
    signals: ['Credential request', 'Impersonation language', 'Mismatched domain'],
    urls: ['https://secure-paypa1.example.com/login'],
    brands: ['PayPal'],
    explanation: ['The sender appears to imitate a familiar brand while using a lookalike domain.', 'It requests login details through a message link.'],
    safe_action: 'Avoid the link and do not share any codes or passwords. Report and delete the message.',
  },
]

export const mockAnalyzeService = async (message: string): Promise<AnalyzeResponse> => {
  await new Promise((resolve) => setTimeout(resolve, 1100))
  const index = Math.abs(message.length) % responses.length
  return responses[index]
}
