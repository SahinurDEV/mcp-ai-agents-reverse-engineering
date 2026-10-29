// type_error.ts - Zod types flow into the handler, so the compiler catches misuse.
import { McpServer } from '@modelcontextprotocol/server';
import * as z from 'zod/v4';

const server = new McpServer({ name: 'type-error', version: '1.0.0' });
server.registerTool('shout', { description: 'Upper-case a count.', inputSchema: z.object({ count: z.number() }) },
  async ({ count }) => ({ content: [{ type: 'text', text: count.toUpperCase() }] }));
