import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'SpyBnB - Monitor Airbnb Competitors',
  description: 'Track competitor prices and get alerts when prices drop',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
