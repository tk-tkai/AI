'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'
import './globals.css' // อย่าลืม import css ของคุณ

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  // สร้าง QueryClient ไว้ใน state เพื่อให้คงอยู่ตลอดการใช้งาน
  const [queryClient] = useState(() => new QueryClient())

  return (
    <html lang="th">
      <body>
        <QueryClientProvider client={queryClient}>
          {children}
        </QueryClientProvider>
      </body>
    </html>
  )
}