import type { IncomingMessage, ServerResponse } from 'node:http';
import type { InboxItem } from '../src/types/inbox.ts';
import { hasFixtureAccess } from './identity-fixture.ts';

function item(index: number, title: string, read: boolean): InboxItem {
  const createdAt = new Date(Date.UTC(2026, 10, 23, index)).toISOString();
  return {
    id: `11111111-1111-4111-8111-${String(index).padStart(12, '0')}`,
    title,
    body: '<strong>Nội dung văn bản</strong>',
    createdAt,
    readAt: read ? createdAt : null,
  };
}

const items = [
  item(21, '<b>Thông báo mới nhất</b>', false),
  item(20, 'Thông báo thứ hai', false),
  ...Array.from({ length: 19 }, (_, position) =>
    item(19 - position, `Thông báo cũ ${19 - position}`, true),
  ),
];

let failList = true;

export function deliverFixtureNotice() {
  items.unshift(item(22, 'Thông báo vừa đến', false));
}

export function serveInboxFixture(request: IncomingMessage, response: ServerResponse) {
  const url = new URL(request.url ?? '/', 'http://127.0.0.1');
  const route = url.pathname.replace('/api/notification/v1/inbox', '');

  function reply(status: number, result: unknown, code = 'SUCCESS') {
    response
      .writeHead(status, { 'Content-Type': 'application/json' })
      .end(JSON.stringify({ code, result }));
  }

  if (!hasFixtureAccess(request)) {
    reply(401, null, 'COMMON.UNAUTHENTICATED');
    return;
  }
  if (request.method === 'GET' && route === '/unread-count') {
    reply(200, { count: items.filter((entry) => entry.readAt === null).length });
    return;
  }
  if (request.method === 'GET' && route === '') {
    if (failList) {
      failList = false;
      reply(503, null, 'COMMON.SERVICE_UNAVAILABLE');
      return;
    }
    const page = Number(url.searchParams.get('page') ?? 1);
    const size = 20;
    reply(200, {
      content: items.slice((page - 1) * size, page * size),
      page,
      totalPages: Math.ceil(items.length / size),
    });
    return;
  }
  if (request.method === 'POST' && route === '/read-all') {
    const unread = items.filter((entry) => entry.readAt === null);
    for (const entry of unread) entry.readAt = entry.createdAt;
    reply(200, { updated: unread.length });
    return;
  }
  if (request.method === 'POST' && route.endsWith('/read')) {
    const entry = items.find(({ id }) => route === `/${id}/read`);
    if (entry) {
      entry.readAt ??= entry.createdAt;
      reply(200, entry);
      return;
    }
  }
  reply(404, null, 'COMMON.NOT_FOUND');
}
