export type InboxItem = {
  id: string;
  title: string;
  body: string;
  createdAt: string;
  readAt: string | null;
};

export type InboxPage = { content: InboxItem[]; page: number; totalPages: number };

export type InboxClient = {
  count: (signal: AbortSignal) => Promise<{ count: number }>;
  list: (page: number, signal: AbortSignal) => Promise<InboxPage>;
  markRead: (id: string) => Promise<InboxItem>;
  markAllRead: () => Promise<{ updated: number }>;
};
