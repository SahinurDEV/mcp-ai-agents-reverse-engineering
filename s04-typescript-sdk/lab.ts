// lab.ts - Lab 4: the section 3 calculator + quotes server, ported to TypeScript.
import { McpServer, ResourceTemplate } from '@modelcontextprotocol/server';
import { StdioServerTransport } from '@modelcontextprotocol/server/stdio';
import * as z from 'zod/v4';

const QUOTES = [
  'Programs must be written for people to read. - Harold Abelson',
  'Simplicity is prerequisite for reliability. - Edsger Dijkstra',
  'Trust, but verify. - Russian proverb',
];

const server = new McpServer({ name: 'calc-quotes-ts', version: '1.0.0' });
const pair = z.object({ a: z.number(), b: z.number() });
const out = z.object({ result: z.number() });
const ok = (result: number) => ({ content: [{ type: 'text' as const, text: String(result) }], structuredContent: { result } });

server.registerTool('multiply', { description: 'Multiply two numbers.', inputSchema: pair, outputSchema: out },
  async ({ a, b }) => ok(a * b));

server.registerTool('divide', { description: 'Divide a by b. Fails clearly when b is zero.', inputSchema: pair, outputSchema: out },
  async ({ a, b }) => {
    if (b === 0) {
      return { isError: true, content: [{ type: 'text' as const, text: 'cannot divide by zero; ask the user for a non-zero divisor' }] };
    }
    return ok(a / b);
  });

server.registerResource('random-quote', 'quote://random', { description: 'A random programming quote.', mimeType: 'text/plain' },
  async uri => ({ contents: [{ uri: uri.href, text: QUOTES[Math.floor(Math.random() * QUOTES.length)] }] }));

server.registerResource('quote', new ResourceTemplate('quote://{index}', { list: undefined }),
  { description: 'Quote number index (0-based).', mimeType: 'text/plain' },
  async (uri, variables) => {
    const i = Number(variables.index);
    if (!Number.isInteger(i) || i < 0 || i >= QUOTES.length) throw new Error(`index must be 0 to ${QUOTES.length - 1}`);
    return { contents: [{ uri: uri.href, text: QUOTES[i] }] };
  });

await server.connect(new StdioServerTransport());
