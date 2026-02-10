import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Get the pathname
  const path = request.nextUrl.pathname

  // Define protected paths
  const isProtectedPath = path.startsWith('/dashboard')

  // Check if user is authenticated (has token in localStorage - but we can't access it here)
  // So we'll rely on client-side redirect for now
  // In production, you'd use cookies or a more robust solution

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*'],
}
