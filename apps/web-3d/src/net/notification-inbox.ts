import type { InboxClient, InboxItem, InboxPage } from '../types/inbox.ts';
import { apiRequest } from './api-request.ts';

const BASE = '/api/notification/v1/inbox';

export function createInboxClient(
  authorized: <T>(operation: (token: string) => Promise<T>) => Promise<T>,
): InboxClient {
  return {
    count: (signal) =>
      authorized((accessToken) =>
        apiRequest<{ count: number }>(`${BASE}/unread-count`, { accessToken, signal }),
      ),
    list: (page, signal) =>
      authorized((accessToken) =>
        apiRequest<InboxPage>(`${BASE}?page=${page}`, { accessToken, signal }),
      ),
    markRead: (id) =>
      authorized((accessToken) =>
        apiRequest<InboxItem>(`${BASE}/${encodeURIComponent(id)}/read`, {
          accessToken,
          method: 'POST',
        }),
      ),
    markAllRead: () =>
      authorized((accessToken) =>
        apiRequest<{ updated: number }>(`${BASE}/read-all`, { accessToken, method: 'POST' }),
      ),
  };
}
