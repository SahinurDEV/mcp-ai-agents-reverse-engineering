// bad_output.ts - a deliberate bug: structuredContent does not match outputSchema.
import { McpServer } from '@modelcontextprotocol/server';
import { StdioServerTransport } from '@modelcontextprotocol/server/stdio';
import * as z from 'zod/v4';

const server = new McpServer({ name: 'bad-output', version: '1.0.0' });
server.registerTool('add',
  { description: 'Add two integers.', inputSchema: z.object({ a: z.number(), b: z.number() }), outputSchema: z.object({ result: z.number() }) },
  async ({ a, b }) => ({ content: [{ type: 'text', text: `${a + b}` }], structuredContent: { result: `${a + b}` } as any }));
await server.connect(new StdioServerTransport());
